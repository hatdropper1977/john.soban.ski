#!/usr/bin/env python
"""Step 2: pull the raw wikitext of every word's Wiktionary page.

Wiktionary's etymology sections are written with structured templates such as
{{inh|en|enm|admiral}} ("inherited from Middle English admiral") and
{{der|en|ar|أمير}} ("derived from Arabic amir"), so the raw wikitext is far
more useful than the rendered HTML. This step only downloads and caches. The
parsing happens in parse_etymology.py so it can be re-run without touching the
network again.

Input : work/word_counts.json   (from extract_words.py)
Output: work/wikitext.json      { lemma: {"title": page title used, "wikitext": "..."} or None }

Wiktionary asks for a descriptive User-Agent and a gentle request rate. Titles
are requested 20 at a time with a short pause, which finishes in a few minutes.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
API = "https://en.wiktionary.org/w/api.php"
UA = "john.soban.ski etymology post (https://github.com/hatdropper1977/john.soban.ski)"
BATCH = 20
PAUSE = 0.6


def api(params):
    params = dict(params, format="json", formatversion="2", maxlag="5")
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.load(resp)
            if "error" in data and data["error"].get("code") == "maxlag":
                time.sleep(5)
                continue
            return data
        except Exception as exc:  # network hiccup: back off and retry
            time.sleep(2 * (attempt + 1))
            last = exc
    raise RuntimeError(f"Wiktionary API failed: {last}")


def fetch_titles(titles):
    """Return {requested_title: wikitext or None}, following redirects and continuations."""
    out = {t: None for t in titles}
    params = {"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
              "redirects": 1, "titles": "|".join(titles)}
    # map normalised / redirected titles back to what we asked for
    back = {t: t for t in titles}
    while True:
        data = api(params)
        q = data.get("query", {})
        for n in q.get("normalized", []):
            back[n["to"]] = back.get(n["from"], n["from"])
        for r in q.get("redirects", []):
            back[r["to"]] = back.get(r["from"], r["from"])
        for page in q.get("pages", []):
            if page.get("missing"):
                continue
            revs = page.get("revisions")
            if not revs:
                continue
            asked = back.get(page["title"], page["title"])
            out[asked] = revs[0]["slots"]["main"]["content"]
        if "continue" not in data:
            break
        params.update(data["continue"])
    return out


def main():
    counts = json.load(open(WORK / "word_counts.json", encoding="utf-8"))
    cache_path = WORK / "wikitext.json"
    cache = json.load(open(cache_path, encoding="utf-8")) if cache_path.exists() else {}

    lemmas = [w for w, v in counts.items() if not v["proper"] and w not in cache]
    print(f"{len(lemmas)} lemmas to fetch ({len(cache)} already cached)")

    def run(pass_name, wanted, title_of):
        todo = [(w, title_of(w)) for w in wanted]
        todo = [(w, t) for w, t in todo if t]
        for i in range(0, len(todo), BATCH):
            chunk = todo[i:i + BATCH]
            got = fetch_titles([t for _, t in chunk])
            for w, t in chunk:
                text = got.get(t)
                if text and "==English==" in text:
                    cache[w] = {"title": t, "wikitext": text}
            json.dump(cache, open(cache_path, "w", encoding="utf-8"), ensure_ascii=False)
            done = min(i + BATCH, len(todo))
            print(f"  {pass_name}: {done}/{len(todo)}", end="\r", flush=True)
            time.sleep(PAUSE)
        print()

    # pass 1: the lemma itself
    run("lemma", lemmas, lambda w: w)
    # pass 2: coined proper-ish words (Jedi, Wookiee) and simple plurals the lemmatiser missed
    missing = [w for w in lemmas if w not in cache]
    run("capitalised", missing, lambda w: w[:1].upper() + w[1:])
    missing = [w for w in lemmas if w not in cache]
    run("singular", missing, lambda w: w[:-1] if w.endswith("s") and len(w) > 3 else None)
    missing = [w for w in lemmas if w not in cache]
    run("unhyphenated", missing, lambda w: w.replace("-", "") if "-" in w else None)

    missing = [w for w in lemmas if w not in cache]
    for w in missing:
        cache[w] = None
    json.dump(cache, open(cache_path, "w", encoding="utf-8"), ensure_ascii=False)
    found = sum(1 for w in counts if not counts[w]["proper"] and cache.get(w))
    print(f"English entries found for {found} of {sum(1 for v in counts.values() if not v['proper'])} lemmas")
    print("no entry:", sorted(missing, key=lambda w: -counts[w]["n"])[:80])


if __name__ == "__main__":
    main()
