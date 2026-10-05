#!/usr/bin/env python
"""Step 3: turn cached Wiktionary wikitext into a structured etymology per word.

For every lemma the parser reads the first Etymology section under ==English==
and pulls out an ordered chain of {lang, term} hops. Two template styles exist
on Wiktionary today and both are handled:

  classic  From {{inh|en|enm|admiral}}, from {{der|en|fro|admiral}}, from {{der|en|ar|أمير}}
  etymon   {{etymon|en|:inh|enm:fader<id:father>|tree=1}}   (only the first hop is
           written on the English page; the rest lives on the Middle English page)

When a chain stops in an intermediate language (Middle English, Old French,
Medieval Latin, Old Norse ...) the parser fetches that page and keeps going, so
"father" becomes  enm fader -> ang fæder -> gmw-pro *fader -> gem-pro *fadēr -> ine-pro *ph₂tḗr.

Per word the output records:
  chain, root, parts, coined/coiner, unknown,
  date    {"year", "kind", "note"}; kind = attested | coined | inferred
  layer   Old English | Middle English | Early Modern English | Modern English | 20th century
  donor   language English took the word from (ang for native words)
  origin  deepest attested (non-reconstructed) language in the chain
  deepest deepest language of all, proto-languages included

Input : work/word_counts.json, work/wikitext.json, languages.json, overrides.json
Output: work/etymologies.json   (plus work/wikitext_follow.json as a fetch cache)
"""
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fetch_wiktionary import fetch_titles, BATCH, PAUSE  # noqa: E402

WORK = HERE / "work"
LANGS = json.load(open(HERE / "languages.json", encoding="utf-8"))
LANGS.pop("_comment", None)

ENGLISH_CODES = {"en", "enm", "enm-nor", "ang", "sco"}
CODE_ALIASES = {"en-ear": "en", "ang-ang": "ang", "grc-dor": "grc", "fa-cls": "fa", "nds-nl": "nds",
                "nds-de": "nds", "egx-dem": "egy", "ira-old": "ira", "enm-esc": "enm", "gmw-msc": "gmw",
                "la-ren": "la-new", "grc-koi": "grc", "grc-att": "grc", "grc-ion": "grc", "fro-pic": "fro-nor",
                "gem-pro-nor": "gem-pro", "la-lat-med": "la-med", "zlw-ocs": "cs", "nrf": "xno", "roa-opt": "pt",
                "roa-oan": "xno", "oc-pro": "pro", "itc-ala": "la"}
# languages whose pages are worth following to extend a chain (intermediate carriers)
FOLLOW = {"enm", "enm-nor", "ang", "sco", "xno", "fro", "fro-nor", "frm", "fr", "pro",
          "la-med", "la-lat", "la-vul", "la-eme", "la-ecc", "la-new", "la", "non", "gmq-oda", "dum", "gml",
          "frk", "goh", "gmh", "osx", "odt", "nl", "de", "it", "roa-oit", "es", "osp", "pt", "gkm", "grc",
          "ar", "fa", "tr", "ota", "he", "arc", "sa", "hi", "ru", "cs", "pl", "cy", "ga", "sga"}
# Wiktionary section headings for the codes above
SECTION_NAME = {"enm": "Middle English", "enm-nor": "Middle English", "ang": "Old English", "sco": "Scots",
                "xno": "Anglo-Norman", "fro": "Old French", "fro-nor": "Old French", "frm": "Middle French",
                "fr": "French", "pro": "Old Occitan", "la": "Latin", "la-med": "Latin", "la-lat": "Latin",
                "la-vul": "Latin", "la-eme": "Latin", "la-ecc": "Latin", "la-new": "Latin", "non": "Old Norse",
                "gmq-oda": "Old Danish", "dum": "Middle Dutch", "gml": "Middle Low German", "frk": "Frankish",
                "goh": "Old High German", "gmh": "Middle High German", "osx": "Old Saxon", "odt": "Old Dutch",
                "nl": "Dutch", "de": "German", "it": "Italian", "roa-oit": "Italian", "es": "Spanish",
                "osp": "Old Spanish", "pt": "Portuguese", "gkm": "Greek", "grc": "Ancient Greek", "ar": "Arabic",
                "fa": "Persian", "tr": "Turkish", "ota": "Ottoman Turkish", "he": "Hebrew", "arc": "Aramaic",
                "sa": "Sanskrit", "hi": "Hindi", "ru": "Russian", "cs": "Czech", "pl": "Polish", "cy": "Welsh",
                "ga": "Irish", "sga": "Old Irish"}
STRIP_MACRONS = {"la", "la-med", "la-lat", "la-vul", "la-eme", "la-ecc", "la-new", "ang", "grc", "gkm", "enm",
                 "sa", "ar", "he", "arc", "goh", "osx", "odt", "gmh", "dum"}
MAX_DEPTH = 6

CHAIN_TEMPLATES = {"inh", "inh+", "inh-lite", "inherited", "der", "der+", "derived", "bor", "bor+",
                   "borrowed", "uder", "ubor", "lbor", "slbor", "obor", "cal", "calque", "psm", "der-lite",
                   "bor-lite"}
PART_TEMPLATES = {"af", "affix", "suffix", "suf", "prefix", "pre", "compound", "com", "con", "confix",
                  "blend", "univerbation", "univ", "clipping", "clip", "back-form", "back-formation",
                  "surf", "surface analysis", "contraction", "deverbal", "abbrev", "abbreviation"}
ETYMON_CHAIN_RELS = {"inh", "der", "bor", "lbor", "slbor", "ubor", "uder", "obor", "cal", "calque", "psm", "inh-lite"}
ETYMON_PART_RELS = {"af", "afeq", "suf", "sufeq", "pre", "preeq", "com", "blend", "univ", "clip", "back-form", "abbrev",
                    "deverbal", "contraction", "affix", "compound", "suffix", "prefix"}
ETYMON_ANNOTATION_KEYS = {"ety", "alt", "pos", "id", "t", "tr", "ts", "g", "lit", "q", "qq", "text", "tree", "gloss"}
COIN_TEMPLATES = {"coin", "coined", "coinage"}
UNKNOWN_TEMPLATES = {"unc", "unk", "unknown", "uncertain"}
FORM_OF = re.compile(
    r"\{\{(?:plural of|comparative of|superlative of|alternative form of|alt form|alt sp|"
    r"alternative spelling of|misspelling of|obsolete spelling of|obsolete form of|past participle of|"
    r"present participle of|nonstandard spelling of|eye dialect of|pronunciation spelling of|"
    r"contraction of|informal form of|colloquial form of|short for|clipping of|abbreviation of|"
    r"initialism of|standard spelling of|stand sp|dated form of|archaic form of|synonym of|inflection of|"
    r"alt case|alternative case form of|gerund of|verbal noun of|agent noun of)"
    r"\|en\|([^|}]+)")
FORM_OF_EN = re.compile(r"\{\{en-(?:comparative|superlative|third-person singular|past|ing form|simple past|"
                        r"third person singular|past participle|archaic second-person singular|"
                        r"archaic third-person singular) of\|([^|}]+)")

YEAR = r"(1[0-9]{3}|20[0-2][0-9]|[5-9][0-9]{2})"
DATE_PATTERNS = [
    ("attested", re.compile(r"[Ff]irst (?:attested|recorded|used|appear\w*|cited|documented)[^.\n]{0,80}?\b" + YEAR + r"s?\b")),
    ("attested", re.compile(r"[Aa]ttested (?:since|from|in|by|before|around|c\.|circa|as early as)?[^.\n]{0,40}?\b" + YEAR + r"s?\b")),
    ("attested", re.compile(r"[Rr]ecorded (?:since|from|in|by|before|around)?[^.\n]{0,40}?\b" + YEAR + r"s?\b")),
    ("attested", re.compile(r"\{\{etydate\|(?:[a-z]+\|)?" + YEAR)),
    ("attested", re.compile(r"[Ff]irst (?:attested|recorded|used|appear\w*)[^.\n]{0,60}?(early |mid-|mid |late )?(\d{1,2})(?:st|nd|rd|th)[ -]century")),
    ("attested", re.compile(r"(?:sense|meaning)[^.\n]{0,80}?first appears (?:c\. |circa |around |in )?" + YEAR)),
]


# --------------------------------------------------------------------------- wikitext helpers
def language_section(text, name):
    m = re.search(r"^==" + re.escape(name) + r"==\s*\n(.*?)(?=^==[^=]|\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def etymology_section(section):
    """Body of the first ===Etymology=== / ===Etymology 1=== section."""
    m = re.search(r"^={3,4}Etymology(?: 1)?={3,4}\s*\n(.*?)(?=^={3,5}[^=]|\Z)", section, re.S | re.M)
    return m.group(1) if m else ""


def iter_templates(text):
    """Yield (name, positional_params, named_params, start, end) for every template, outermost first."""
    i, n = 0, len(text)
    while i < n:
        s = text.find("{{", i)
        if s < 0:
            return
        depth, j = 0, s
        while j < n:
            if text.startswith("{{", j):
                depth += 1; j += 2
            elif text.startswith("}}", j):
                depth -= 1; j += 2
                if depth == 0:
                    break
            else:
                j += 1
        body = text[s + 2:j - 2]
        name, pos, named = _split_template(body)
        yield (name, pos, named, s, j)
        if "{{" in body:
            for t in iter_templates(body):
                yield (t[0], t[1], t[2], s + 2 + t[3], s + 2 + t[4])
        i = j


def _split_template(body):
    parts, depth, cur, k = [], 0, [], 0
    while k < len(body):
        two = body[k:k + 2]
        if two in ("{{", "[["):
            depth += 1; cur.append(two); k += 2; continue
        if two in ("}}", "]]"):
            depth -= 1; cur.append(two); k += 2; continue
        if body[k] == "|" and depth == 0:
            parts.append("".join(cur)); cur = []
        else:
            cur.append(body[k])
        k += 1
    parts.append("".join(cur))
    name = parts[0].strip()
    pos, named = [], {}
    for p in parts[1:]:
        if re.match(r"^\s*[a-zA-Z0-9_]+\s*=", p):
            key, _, val = p.partition("=")
            named[key.strip()] = val.strip()
        else:
            pos.append(p.strip())
    return name, pos, named


def clean_term(term):
    term = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", term or "")
    term = re.sub(r"<[^>]+>", "", term)
    return term.strip()


def plain(text):
    """Strip templates, links and quotes from a snippet for human-readable notes."""
    out, depth, k = [], 0, 0
    while k < len(text):
        if text.startswith("{{", k):
            depth += 1; k += 2; continue
        if text.startswith("}}", k):
            depth = max(0, depth - 1); k += 2; continue
        if depth == 0:
            out.append(text[k])
        k += 1
    s = "".join(out)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s).replace("''", "")
    return re.sub(r"\s+", " ", s).strip()


def norm_code(code):
    code = code.strip().split(",")[0]
    code = CODE_ALIASES.get(code, code)
    if code in LANGS:
        return code
    base = code.split("-")[0]
    if base in LANGS and not code.endswith("-pro"):
        return base
    return code


def page_title(lang, term):
    term = clean_term(term).split(",")[0].strip()
    if not term or term.startswith("*"):
        return None
    if lang in STRIP_MACRONS:
        decomposed = unicodedata.normalize("NFD", term)
        term = unicodedata.normalize("NFC", "".join(ch for ch in decomposed if ch not in "̄̆"))
    return term


# --------------------------------------------------------------------------- etymon template syntax
def parse_etymon_item(item):
    """'enm:admiral<id:naval commander><ety:der<fro:admiral>>' -> (lang, term, [nested hops])"""
    head, annos, depth, k, start = None, [], 0, 0, None
    for k, ch in enumerate(item):
        if ch == "<":
            if depth == 0:
                if head is None:
                    head = item[:k]
                start = k + 1
            depth += 1
        elif ch == ">":
            depth -= 1
            if depth == 0:
                annos.append(item[start:k])
    if head is None:
        head = item
    lang, term = None, head.strip()
    m = re.match(r"^([a-z]{2,3}(?:-[a-z]{2,4})*):(.+)$", head.strip())
    # 'alt:boren' or 'pos:adjective' are annotations written without angle brackets
    if m and m.group(1) not in ETYMON_ANNOTATION_KEYS:
        lang, term = m.group(1), m.group(2).strip()
    elif m:
        return None, "", []
    nested = []
    for a in annos:
        if a.startswith("ety:"):
            rel_and_items = a[4:]
            mm = re.match(r"^([a-z\-]+)(.*)$", rel_and_items, re.S)
            if mm and mm.group(1) in ETYMON_CHAIN_RELS:
                for sub in re.findall(r"<((?:[^<>]|<[^<>]*>)*)>", mm.group(2)):
                    nested.append(parse_etymon_item(sub))
    return lang, term, nested


def parse_etymon(pos, section_lang):
    """Return (chain_hops, parts) from an {{etymon}} / {{ety}} positional list."""
    hops, parts, rel = [], [], None
    for p in pos[1:]:
        if p.startswith(":"):
            rel = p[1:].split("<")[0]          # ':lbor<ref:...>' carries an annotation
            continue
        lang, term, nested = parse_etymon_item(p)
        if not rel:                           # '{{ety|en|shoot<id:launch>}}': plain English base word
            if lang:
                hops.append({"lang": norm_code(lang), "term": clean_term(term), "via": "der"})
            elif clean_term(term):
                parts.append(clean_term(term))
            continue
        if rel in ETYMON_CHAIN_RELS and lang:
            hops.append({"lang": norm_code(lang), "term": clean_term(term), "via": rel})
            stack = list(nested)
            while stack:
                l2, t2, n2 = stack.pop(0)
                if l2:
                    hops.append({"lang": norm_code(l2), "term": clean_term(t2), "via": "etymon"})
                stack = n2 + stack
        elif rel in ETYMON_PART_RELS or (rel in ETYMON_CHAIN_RELS and not lang):
            t = clean_term(term)
            if t and t not in parts:
                parts.append(t)
    return hops, parts


# --------------------------------------------------------------------------- one etymology section
ASIDE = re.compile(r"(?:^|(?<=[.;]))\s*(?:\{\{(?:ncog|noncog|cog|doublet|dbt|displaced)\||"
                   r"(?:Displaced|Displacing|Superseded|Replaced|Cognate|Cognates|Compare|Related to|Distantly related|"
                   r"More at|See also|Doublet of|Not related|Unrelated to|Perhaps related|Possibly related))", re.M)


def parse_section(etym, section_lang):
    # "Displaced native Middle English elne, from Old English ellen" is an aside about the word
    # that was replaced, not part of this word's lineage, so the text is cut at the first aside.
    m = ASIDE.search(etym)
    if m and m.start() > 40:
        etym = etym[:m.start()]
    chain, parts, root = [], [], None
    coined, coiner, coin_year, unknown = False, None, None, False
    seen = set()

    def add(lang, term, via):
        lang = norm_code(lang)
        key = (lang, term)
        if lang and key not in seen and lang != section_lang:
            seen.add(key)
            chain.append({"lang": lang, "term": term, "via": via})

    for name, pos, named, s, e in iter_templates(etym):
        if not pos or pos[0] != section_lang:
            continue
        if name in CHAIN_TEMPLATES and len(pos) > 1:
            term = clean_term(pos[2]) if len(pos) > 2 else ""
            add(pos[1], "" if term == "-" else term, name.rstrip("+"))
        elif name in ("etymon", "ety"):
            hops, eparts = parse_etymon(pos, section_lang)
            for h in hops:
                add(h["lang"], h["term"], h["via"])
            for p in eparts:
                if p not in parts:
                    parts.append(p)
        elif name == "root" and len(pos) > 2:
            root = {"lang": norm_code(pos[1]), "term": clean_term(pos[2])}
        elif name in PART_TEMPLATES:
            for p in pos[1:]:
                p = clean_term(p)
                if p and p not in parts:
                    parts.append(p)
        elif name in COIN_TEMPLATES:
            coined = True
            cand = [p for p in pos[1:] if p and not re.match(r"^Q\d+$", p)]
            coiner = named.get("by") or (cand[-1] if cand else None)
            if named.get("in") and re.search(r"\d{4}", named["in"]):
                coin_year = int(re.search(r"\d{4}", named["in"]).group(0))
            else:
                tail = re.sub(r"\(born \d{4}\)", "", etym[e:e + 260])
                m = re.search(r"\b" + YEAR + r"\b", tail)
                if m:
                    coin_year = int(m.group(1))
        elif name in UNKNOWN_TEMPLATES:
            unknown = True
    # prose "Coined by X in 1957" only counts when the sentence starts that way; a passing
    # "Aristotle coined the Greek word" inside a longer history does not make the English word a coinage
    if re.search(r"(?:^|\n|\.\s+)(?:First |Originally )?[Cc]oined\b", etym):
        coined = True
        if coin_year is None:
            m = re.search(r"[Cc]oined[^.\n]{0,160}?\b" + YEAR + r"\b", etym)
            if m:
                coin_year = int(m.group(1))
    # prose fallback: "From {{m|enm|...}}" with no inh/der template
    if not chain:
        for m in re.finditer(r"[Ff]rom (?:the )?(?:[A-Z][A-Za-z\- ]+ )?\{\{m\|([a-z\-]+)\|([^|}]*)", etym):
            if m.group(1) != section_lang:
                add(m.group(1), clean_term(m.group(2)), "prose")
    # English-internal derivations: "respelling of {{l|en|OK}}", "From {{m|en|mean}}", "see [[be]] + [[-ing]]"
    if not chain and not parts:
        for m in re.finditer(r"(?:[Ff]rom|of|[Ss]ee|[Ff]ormerly|form of|variant of|[Rr]espelling of|[Pp]ast participle of)\s+"
                             r"(?:'{2,3}|\[\[)?\{\{[ml]\|" + re.escape(section_lang) + r"\|([^|}]+)", etym):
            t = clean_term(m.group(1))
            if t and t not in parts:
                parts.append(t)
        for m in re.finditer(r"(?:[Ff]rom|[Ss]ee|of)\s+''?\[\[([A-Za-z' -]{2,})\]\]''?(?:\s*\+\s*''?\[\[([A-Za-z' -]{1,})\]\])?", etym):
            for t in m.groups():
                if t and t not in parts:
                    parts.append(t)
    if not chain and not parts and re.search(r"\b(unknown|uncertain|unclear|obscure) (origin|etymology)", etym, re.I):
        unknown = True
    return chain, root, parts, coined, coiner, coin_year, unknown


def explicit_date(etym, coined, coin_year, chain=()):
    """Earliest year Wiktionary states for the word. Later sense-dates ("the slang sense is
    from 1930") lose to the earliest mention, and a coinage date is ignored for a word whose
    chain already reaches Old or Middle English (only a sub-sense was coined)."""
    medieval = any(h["lang"] in ("ang", "enm", "enm-nor") for h in chain)
    found = []
    for kind, pat in DATE_PATTERNS:
        for m in pat.finditer(etym):
            groups = [g for g in m.groups() if g]
            if "century" in pat.pattern:
                cent = int(groups[-1])
                qual = (groups[0] if len(groups) > 1 else "").strip("- ")
                year = (cent - 1) * 100 + {"early": 15, "mid": 50, "late": 85}.get(qual, 50)
                found.append({"year": year, "kind": kind, "note": f"first attested {qual + ' ' if qual else ''}{cent}th century"})
            else:
                year = int(groups[-1])
                if 500 <= year <= 2025:
                    found.append({"year": year, "kind": kind, "note": plain(m.group(0))[:140]})
    if coined and coin_year and 1500 <= coin_year <= 2025 and not medieval:
        found.append({"year": coin_year, "kind": "coined", "note": "coined " + str(coin_year)})
    found = [f for f in found if not (f["kind"] == "coined" and medieval)]
    if not found:
        return None
    return min(found, key=lambda f: f["year"])


# --------------------------------------------------------------------------- following chains
def follow_chains(records, follow_cache):
    """Extend each chain by reading the page of its last intermediate hop."""
    for depth in range(MAX_DEPTH):
        wanted = {}
        for w, rec in records.items():
            if not rec["chain"] or rec.get("_stop"):
                continue
            last = rec["chain"][-1]
            lang = last["lang"]
            if lang not in FOLLOW or lang not in SECTION_NAME:
                rec["_stop"] = True
                continue
            title = page_title(lang, last["term"])
            if not title:
                rec["_stop"] = True
                continue
            wanted.setdefault(title, []).append(w)
        todo = [t for t in wanted if t not in follow_cache]
        if todo:
            print(f"  depth {depth}: following {len(wanted)} pages ({len(todo)} to fetch)")
            for i in range(0, len(todo), BATCH):
                chunk = todo[i:i + BATCH]
                got = fetch_titles(chunk)
                for t in chunk:
                    follow_cache[t] = got.get(t)
                json.dump(follow_cache, open(WORK / "wikitext_follow.json", "w", encoding="utf-8"), ensure_ascii=False)
                print(f"    {min(i + BATCH, len(todo))}/{len(todo)}", end="\r", flush=True)
                time.sleep(PAUSE)
            print()
        progressed = False
        for title, words in wanted.items():
            text = follow_cache.get(title)
            for w in words:
                rec = records[w]
                last = rec["chain"][-1]
                section = language_section(text, SECTION_NAME[last["lang"]]) if text else ""
                etym = etymology_section(section)
                if not etym.strip():
                    rec["_stop"] = True
                    continue
                hops, root, _, _, _, _, _ = parse_section(etym, last["lang"].split("-")[0] if last["lang"].startswith("la-") else last["lang"])
                # Latin sub-varieties share the ==Latin== section whose templates say |la|
                if not hops and last["lang"].startswith("la-"):
                    hops, root, *_ = parse_section(etym, "la")
                if rec["root"] is None and root:
                    rec["root"] = root
                have = {(h["lang"], h["term"]) for h in rec["chain"]}
                new = [h for h in hops if (h["lang"], h["term"]) not in have and h["lang"] != "en"]
                # never let a followed page point back at a language already in the chain
                langs_in = [h["lang"] for h in rec["chain"]]
                new = [h for h in new if h["lang"] not in langs_in or h["lang"].endswith("-pro")]
                if new:
                    for h in new:
                        h["via"] = "followed:" + title
                    rec["chain"].extend(new)
                    progressed = True
                else:
                    rec["_stop"] = True
        if not progressed:
            break
    for rec in records.values():
        rec.pop("_stop", None)


# --------------------------------------------------------------------------- dating
def fam(code):
    return LANGS.get(code, {}).get("family", "Other")


def is_proto(code):
    return code.endswith("-pro") or bool(LANGS.get(code, {}).get("proto"))


def layer_for_year(y):
    if y is None:
        return None
    if y < 1150:
        return "Old English"
    if y < 1500:
        return "Middle English"
    if y < 1700:
        return "Early Modern English"
    if y < 1900:
        return "Modern English"
    return "20th century"


def infer_layer(chain, coined, parts, part_dates, unknown=False):
    codes = [c["lang"] for c in chain]
    if not codes and not parts and not coined and unknown:
        return "Early Modern English", 1600, "origin unknown; first appears in Modern English", None
    donor = next((c for c in codes if c not in ENGLISH_CODES), None)
    if "ang" in codes:
        return "Old English", 800, "inherited from Old English", "ang"
    if codes and codes[0] in ("enm", "enm-nor"):
        if donor is None:
            return "Middle English", 1300, "first seen in Middle English", "enm"
        if donor.startswith(("non", "gmq")):
            return "Middle English", 1200, "Norse loan into Middle English", donor
        return "Middle English", 1350, "borrowed into Middle English", donor
    if codes and codes[0] == "sco":
        return "Early Modern English", 1600, "from Scots", "sco"
    if donor:
        return "Early Modern English", 1600, "borrowed into Modern English", donor
    if coined:
        return "20th century", 1950, "coined", None
    if parts:
        years = [part_dates[p.strip("-")] for p in parts if p.strip("-") in part_dates]
        if years:
            y = max(years)
            return layer_for_year(y), y, "built from English parts: " + " + ".join(parts), None
        return "Modern English", 1750, "built from English parts: " + " + ".join(parts), None
    return None, None, None, None


def finish(rec, part_dates):
    layer, year, note, donor = infer_layer(rec["chain"], rec["coined"], rec["parts"], part_dates, rec.get("unknown", False))
    d = rec.get("date")
    if d and d.get("kind") != "inferred":
        rec["layer"] = layer_for_year(d["year"])
    elif year:
        rec["date"] = {"year": year, "kind": "inferred", "note": note}
        rec["layer"] = layer
    else:
        rec["date"], rec["layer"] = None, None
    codes = [c["lang"] for c in rec["chain"]]
    # The lineage runs from English down to the first reconstructed proto-language. Hops written
    # after that point are asides ("reinforced by Old Norse ...") and must not steal the origin.
    lineage = []
    for c in codes:
        if is_proto(c):
            break
        lineage.append(c)
    if not lineage:
        lineage = [c for c in codes if not is_proto(c)]
    rec["donor"] = donor or next((c for c in lineage if c not in ENGLISH_CODES), "ang" if "ang" in codes else None)
    rec["origin"] = lineage[-1] if lineage else (codes[-1] if codes else None)
    rec["deepest"] = rec["root"]["lang"] if rec.get("root") else (codes[-1] if codes else None)
    if rec["origin"]:
        rec["origin_family"] = fam(rec["origin"])
    elif rec["coined"]:
        rec["origin_family"] = "Coined"
    elif rec["parts"]:
        rec["origin_family"] = "English"
    else:
        rec["origin_family"] = "Unknown"


# --------------------------------------------------------------------------- main
def main():
    counts = json.load(open(WORK / "word_counts.json", encoding="utf-8"))
    cache = json.load(open(WORK / "wikitext.json", encoding="utf-8"))
    follow_path = WORK / "wikitext_follow.json"
    follow_cache = json.load(open(follow_path, encoding="utf-8")) if follow_path.exists() else {}
    overrides_path = HERE / "overrides.json"
    overrides = json.load(open(overrides_path, encoding="utf-8")) if overrides_path.exists() else {}
    overrides.pop("_comment", None)

    parsed, alias, unresolved = {}, {}, []
    for w, entry in cache.items():
        if not entry or w in overrides and overrides[w].get("replace"):
            continue
        eng = language_section(entry["wikitext"], "English")
        etym = etymology_section(eng)
        if not etym.strip():
            m = FORM_OF.search(eng) or FORM_OF_EN.search(eng)
            if m:
                alias[w] = clean_term(m.group(1)).lower()
            else:
                unresolved.append(w)
            continue
        chain, root, parts, coined, coiner, coin_year, unknown = parse_section(etym, "en")
        parsed[w] = {"title": entry["title"], "chain": chain, "root": root, "parts": parts,
                     "coined": coined, "coiner": coiner, "unknown": unknown,
                     "date": explicit_date(etym, coined, coin_year, chain), "excerpt": plain(etym)[:300]}

    print(f"parsed {len(parsed)} English etymology sections; following intermediate languages ...")
    follow_chains(parsed, follow_cache)

    # form-of aliases (bigger -> big, droids -> droid) and crude suffix stripping for the rest
    for w, base in alias.items():
        if base in parsed:
            parsed[w] = dict(parsed[base], alias_of=base)
        else:
            unresolved.append(w)
    still = []
    for w in unresolved:
        cands = [w[:-1], w[:-2], w[:-3], w[:-3] + "e", w[:-2] + "e", w[:-4], w[:-4] + "e", w[:-3] + "y"]
        base = next((c for c in cands if len(c) > 2 and c in parsed), None)
        if base:
            parsed[w] = dict(parsed[base], alias_of=base)
        else:
            still.append(w)
    unresolved = still

    for rec in parsed.values():
        finish(rec, {})
    part_dates = {w: rec["date"]["year"] for w, rec in parsed.items() if rec["date"]}
    for rec in parsed.values():
        if rec["parts"] and not rec["chain"] and (not rec["date"] or rec["date"]["kind"] == "inferred"):
            rec["date"] = None
            finish(rec, part_dates)

    # hand-checked overrides win over everything above
    for w, o in overrides.items():
        base = parsed.get(w) if not o.get("replace") else None
        base = base or {"title": w, "chain": [], "root": None, "parts": [], "coined": False, "coiner": None,
                        "unknown": False, "date": None, "excerpt": ""}
        base.update({k: v for k, v in o.items() if k != "replace"})
        base["override"] = True
        finish(base, part_dates)
        if "date" in o:                       # a hand-checked date always wins
            base["date"] = o["date"]
            base["layer"] = o.get("layer") or layer_for_year(o["date"]["year"])
        parsed[w] = base

    # plurals of overridden words (wookiees -> wookiee) can only be resolved now
    still = []
    for w in unresolved:
        base = next((c for c in (w[:-1], w[:-2], w[:-3] + "e") if len(c) > 2 and c in parsed), None)
        if base:
            parsed[w] = dict(parsed[base], alias_of=base)
        else:
            still.append(w)
    unresolved = still

    json.dump(parsed, open(WORK / "etymologies.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # report
    lemmas = [w for w, v in counts.items() if not v["proper"]]
    have = [w for w in lemmas if w in parsed]
    with_chain = [w for w in have if parsed[w]["chain"]]
    dated = [w for w in have if parsed[w]["date"]]
    explicit = [w for w in dated if parsed[w]["date"]["kind"] != "inferred"]
    print(f"lemmas {len(lemmas)} | parsed {len(have)} | with chain {len(with_chain)} | dated {len(dated)} "
          f"(explicit {len(explicit)}) | aliases {len(alias)} | unresolved {len(unresolved)}")
    codes = {}
    for w in have:
        for c in parsed[w]["chain"]:
            codes[c["lang"]] = codes.get(c["lang"], 0) + 1
    print("codes missing from languages.json:", sorted(((c, n) for c, n in codes.items() if c not in LANGS), key=lambda x: -x[1])[:40])
    unresolved = [w for w in unresolved if w in counts]
    print("unresolved:", sorted(unresolved, key=lambda w: -counts[w]["n"])[:60])
    for w in ["suicide", "admiral", "galaxy", "droid", "lightsaber", "the", "sky", "force", "empire", "father",
              "ship", "blaster", "hyperdrive", "jedi", "wookiee", "robot", "computer", "asteroid", "tractor", "you"]:
        r = parsed.get(w)
        if r:
            print(f"  {w:11s} {[(c['lang'], c['term']) for c in r['chain']][:7]} root={(r['root'] or {}).get('term')} "
                  f"parts={r['parts']} coined={r['coined']} date={r['date']} origin={r['origin']}")
        else:
            print(f"  {w:11s} -- not parsed")


if __name__ == "__main__":
    main()
