#!/usr/bin/env python
"""Step 4: combine counts + etymologies into the data file the blog visuals load.

Output: content/js/Star_Wars/sw_data.js   (window.SW_DATA = {...})
        work/summary.json                  (numbers quoted in the article)

The data file is plain JavaScript rather than JSON so the blog can load it with a
<script src="{static}/js/Star_Wars/sw_data.js"> tag. Pelican copies any file an
article links with {static}, and a script tag avoids fetch() and CORS entirely.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from extract_words import tokenize, lemma_of, IN_UNIVERSE  # noqa: E402

WORK = HERE / "work"
OUT_JS = HERE.parent.parent / "content" / "js" / "Star_Wars" / "sw_data.js"
LANGS = json.load(open(HERE / "languages.json", encoding="utf-8"))
LANGS.pop("_comment", None)

FILM_META = {"IV": {"title": "A New Hope", "year": 1977},
             "V": {"title": "The Empire Strikes Back", "year": 1980},
             "VI": {"title": "Return of the Jedi", "year": 1983}}

QUOTES = [
    ("HAN", "IV", "What good's a reward if you ain't around to use it? Besides, attacking that battle station ain't my idea of courage. It's more like suicide."),
    ("BEN", "IV", "Remember, the Force will be with you... always."),
    ("HAN", "IV", "Hey, Luke... may the Force be with you!"),
    ("HAN", "IV", "Hokey religions and ancient weapons are no match for a good blaster at your side, kid."),
    ("VADER", "IV", "I find your lack of faith disturbing."),
    ("LEIA", "IV", "Help me, Obi-Wan Kenobi. You're my only hope."),
    ("THREEPIO", "IV", "Did you hear that? They've shut down the main reactor. We'll be destroyed for sure. This is madness!"),
    ("HAN", "V", "Never tell me the odds!"),
    ("YODA", "V", "No! Try not. Do. Or do not. There is no try."),
    ("VADER", "V", "You have failed me for the last time, Admiral."),
]

# Starting set for the knowledge graph: enough to show every layer of English without
# turning into a hairball. Readers add more words with the search box or by tapping a language.
HERO_WORDS = [
    "suicide", "admiral", "galaxy", "droid", "lightsaber", "robot", "laser", "jedi", "force",
    "empire", "rebel", "hope", "father", "ship", "sky", "planet", "princess", "senate", "captain",
    "pilot", "system", "asteroid", "blaster", "hyperdrive", "destroy", "courage", "reward", "idea",
    "reactor", "faith", "odd", "alliance", "bounty", "scoundrel", "energy", "shield", "friend",
    "they", "the", "you", "good", "bad",
]


def main():
    counts = json.load(open(WORK / "word_counts.json", encoding="utf-8"))
    etym = json.load(open(WORK / "etymologies.json", encoding="utf-8"))

    words, unknown, used_langs = [], [], set()
    for w, c in counts.items():
        if c["proper"]:
            continue
        e = etym.get(w)
        if not e or (not e["chain"] and not e["parts"] and not e["coined"] and not e.get("date")):
            unknown.append({"w": w, "n": c["n"], "speakers": dict(list(c["speakers"].items())[:3])})
            continue
        chain = [{"lang": h["lang"], "term": h["term"]} for h in e["chain"]]
        for h in chain:
            used_langs.add(h["lang"])
        if e.get("root"):
            used_langs.add(e["root"]["lang"])
        d = e.get("date") or {}
        ex = c["example"] or {}
        line = re.sub(r"\s+", " ", ex.get("line", "")).replace("ain'tmy", "ain't my")
        if len(line) > 150:
            line = line[:147].rsplit(" ", 1)[0] + "..."
        rec = {
            "w": w, "n": c["n"], "films": {k: v for k, v in c["films"].items() if v},
            "speakers": dict(list(c["speakers"].items())[:3]),
            "example": {"film": ex.get("film"), "speaker": ex.get("speaker"), "line": line},
            "chain": chain, "parts": e.get("parts") or [],
            "year": d.get("year"), "kind": d.get("kind"),
            "donor": e.get("donor"), "origin": e.get("origin"), "family": e.get("origin_family"),
        }
        # optional fields only when they carry information, to keep the file small
        if e.get("root") and not (chain and chain[-1]["lang"] == e["root"]["lang"]):
            rec["root"] = e["root"]
        if e.get("coined"):
            rec["coined"] = True
            if e.get("coiner"):
                rec["coiner"] = e["coiner"]
        if d.get("kind") != "inferred" and d.get("note"):
            rec["note"] = d["note"]
        if (e.get("title") or w) != w:
            rec["wikt"] = e["title"]
        words.append(rec)
    words.sort(key=lambda x: -x["n"])
    unknown.sort(key=lambda x: -x["n"])

    languages = {}
    for code in used_langs | {"en"}:
        L = LANGS.get(code)
        languages[code] = {"name": L["name"], "family": L["family"], "lat": L["lat"], "lon": L["lon"],
                           "era": L["era"], "proto": bool(L.get("proto"))} if L else \
                          {"name": code, "family": "Other", "lat": None, "lon": None, "era": None, "proto": code.endswith("-pro")}

    # quotes tokenised with the same pipeline so lemma lookups line up
    known = {x["w"] for x in words}
    quotes = []
    for speaker, film, text in QUOTES:
        toks = []
        for m in re.finditer(r"[A-Za-z]+(?:['’][A-Za-z]+)*(?:-[A-Za-z]+)*|[^A-Za-z\s]+|\s+", text):
            piece = m.group(0)
            if not re.match(r"[A-Za-z]", piece):
                toks.append({"t": piece, "w": None})
                continue
            lems = [lemma_of(t) for t, _ in tokenize(piece)]
            lem = next((l for l in lems if l in known), None)
            toks.append({"t": piece, "w": lem})
        quotes.append({"speaker": speaker, "film": film, "text": text, "tokens": toks})

    # --------------------------------------------------------------- summary numbers
    tokens_total = sum(x["n"] for x in words) + sum(x["n"] for x in unknown)
    by_layer_tok, by_layer_lem = Counter(), Counter()
    by_family_tok, by_family_lem = Counter(), Counter()
    by_donor_lem, by_origin_lem = Counter(), Counter()
    def layer_of(y):
        if y is None:
            return "Unknown"
        return ("Old English" if y < 1150 else "Middle English" if y < 1500 else "Early Modern English" if y < 1700
                else "Modern English" if y < 1900 else "20th century")

    for x in words:
        by_layer_tok[layer_of(x["year"])] += x["n"]
        by_layer_lem[layer_of(x["year"])] += 1
        by_family_tok[x["family"]] += x["n"]
        by_family_lem[x["family"]] += 1
        if x["donor"]:
            by_donor_lem[languages[x["donor"]]["name"]] += 1
        if x["origin"]:
            by_origin_lem[languages[x["origin"]]["name"]] += 1

    def share_by(year, film=None):
        lem_all = lem_ok = tok_all = tok_ok = 0
        for x in words:
            n = x["films"].get(film, 0) if film else x["n"]
            if not n:
                continue
            lem_all += 1
            tok_all += n
            if x["year"] is not None and x["year"] <= year:
                lem_ok += 1
                tok_ok += n
        return {"lemmas": round(100 * lem_ok / lem_all, 1), "tokens": round(100 * tok_ok / tok_all, 1)}

    speaker_lines = Counter()
    speaker_family = defaultdict(Counter)
    for x in words:
        for sp, n in counts[x["w"]]["speakers"].items():
            speaker_lines[sp] += n
            speaker_family[sp][x["family"]] += n
    top_speakers = [s for s, _ in speaker_lines.most_common(12)]
    latinate = {}
    for sp in top_speakers:
        tot = sum(speaker_family[sp].values())
        lat = sum(v for k, v in speaker_family[sp].items() if k in ("Latin", "French", "Greek", "Romance"))
        latinate[sp] = {"tokens": tot, "latinate_pct": round(100 * lat / tot, 1),
                        "english_pct": round(100 * speaker_family[sp]["English"] / tot, 1)}

    def lst(fam_or_origin, key="origin"):
        return [x["w"] for x in words if (languages.get(x[key], {}).get("name") == fam_or_origin if key == "origin" else x["family"] == fam_or_origin)][:60]

    summary = {
        "generated": date.today().isoformat(),
        "films": {f: {"title": m["title"], "year": m["year"],
                      "tokens": sum(counts[w]["films"].get(f, 0) for w in counts),
                      "lemmas": sum(1 for w in counts if counts[w]["films"].get(f) and not counts[w]["proper"])}
                  for f, m in FILM_META.items()},
        "tokens": tokens_total, "lemmas_with_etymology": len(words), "lemmas_unknown": len(unknown),
        "names_excluded": sum(1 for c in counts.values() if c["proper"]),
        "explicit_dates": sum(1 for x in words if x["kind"] in ("attested", "coined")),
        "by_layer_tokens_pct": {k: round(100 * v / tokens_total, 1) for k, v in by_layer_tok.most_common()},
        "by_layer_lemmas": dict(by_layer_lem.most_common()),
        "by_family_tokens_pct": {k: round(100 * v / tokens_total, 1) for k, v in by_family_tok.most_common()},
        "by_family_lemmas": dict(by_family_lem.most_common()),
        "by_donor_lemmas": dict(by_donor_lem.most_common(15)),
        "by_origin_lemmas": dict(by_origin_lem.most_common(25)),
        "existed_by": {y: share_by(y) for y in (1100, 1200, 1400, 1500, 1700, 1900, 1950, 1976)},
        "anh_existed_by": {y: share_by(y, "IV") for y in (1100, 1200, 1400, 1500, 1700, 1900, 1950, 1976)},
        "speakers": latinate,
        "arabic_origin": lst("Arabic"), "norse_origin": lst("Old Norse"), "greek_origin": lst("Ancient Greek"),
        "coined": [x["w"] for x in words if x.get("coined")][:60],
        "twentieth_century": [x["w"] for x in words if x["year"] and x["year"] >= 1900][:80],
        "unknown_top": [u["w"] for u in unknown[:60]],
        "hero_missing": [h for h in HERO_WORDS if h not in known],
    }
    json.dump(summary, open(WORK / "summary.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    data = {
        "meta": {"generated": summary["generated"], "films": summary["films"], "tokens": tokens_total,
                 "lemmas": len(words), "unknown": len(unknown), "source": "Wiktionary (CC BY-SA 4.0) via the MediaWiki API"},
        "languages": languages,
        "words": words,
        "unknown": unknown[:120],
        "quotes": quotes,
        "hero": [h for h in HERO_WORDS if h in known],
        "speakers": top_speakers[:10],
    }
    OUT_JS.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    OUT_JS.write_text("// Generated by tools/star_wars_etymology/build_dataset.py on " + summary["generated"] +
                      "\n// Etymologies: Wiktionary, CC BY-SA 4.0. Dialogue counts: original trilogy transcripts.\n"
                      "window.SW_DATA = " + payload + ";\n", encoding="utf-8")
    print(f"wrote {OUT_JS} ({OUT_JS.stat().st_size // 1024} KB): {len(words)} words, {len(unknown)} unknown, "
          f"{len(languages)} languages")
    print(json.dumps({k: summary[k] for k in ("by_layer_tokens_pct", "by_family_tokens_pct", "by_donor_lemmas",
                                              "anh_existed_by", "speakers", "hero_missing")}, indent=1)[:3000])


if __name__ == "__main__":
    main()
