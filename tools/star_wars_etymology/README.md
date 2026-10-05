# Star Wars etymology pipeline

Data pipeline behind the post *Han Solo Said Suicide: The Real-World History Hidden in
Star Wars Dialogue* (`content/star-wars.md`). It turns the original-trilogy dialogue
transcripts into a JavaScript data file that three interactive figures (Leaflet map,
D3 timeline, Cytoscape graph) load from `content/js/Star_Wars/`.

## Setup

```bash
python -m venv .venv
.venv/Scripts/pip install "setuptools<81" simplemma        # Windows
# .venv/bin/pip install "setuptools<81" simplemma           # macOS / Linux
```

Only `simplemma` (lemmatiser) is needed. Everything else is the standard library.

## Input

The three dialogue-only transcripts that circulate in NLP tutorials, one spoken line
per row:

```
"character" "dialogue"
"1" "THREEPIO" "Did you hear that?  They've shut down the main reactor. ..."
```

Save them as `SW_EpisodeIV.txt`, `SW_EpisodeV.txt` and `SW_EpisodeVI.txt` in a folder
of your choice. They are not committed to this repository.

## Run

```bash
python tools/star_wars_etymology/extract_words.py  <folder with the three txt files>
python tools/star_wars_etymology/fetch_wiktionary.py
python tools/star_wars_etymology/parse_etymology.py
python tools/star_wars_etymology/build_dataset.py
```

| Step | Script | Reads | Writes |
|------|--------|-------|--------|
| 1 | `extract_words.py` | transcripts | `work/word_counts.json` |
| 2 | `fetch_wiktionary.py` | word counts | `work/wikitext.json` (raw wikitext per word) |
| 3 | `parse_etymology.py` | wikitext, `languages.json`, `overrides.json` | `work/etymologies.json`, `work/wikitext_follow.json` |
| 4 | `build_dataset.py` | counts, etymologies | `content/js/Star_Wars/sw_data.js`, `work/summary.json` |

Step 2 talks to the Wiktionary API (about 110 requests, 20 titles each). Step 3
fetches the pages of intermediate languages (Middle English, Old French ...) when a
chain stops there, about 1,000 more pages the first time. Both cache to `work/`, which
is git-ignored, so re-runs are fast and offline.

## Hand-checked data

* `languages.json` maps Wiktionary language codes to a display name, a colour family,
  an approximate homeland and an era. Coordinates are deliberately rough.
* `overrides.json` holds first-attestation dates and corrected chains for the words
  the article leans on. Dates follow the decade conventions of the Online Etymology
  Dictionary. Add a word there when Wiktionary's automatic parse is wrong or thin.

## Output

`sw_data.js` sets `window.SW_DATA` with the word list (counts, speakers, example line,
etymology chain, origin, date and how that date was arrived at), the language table,
the tokenised quotes for the timeline and a hero list for the graph. The article loads
it with a plain `<script>` tag, so no fetch and no backend are involved.

Etymologies come from Wiktionary and are CC BY-SA 4.0.
