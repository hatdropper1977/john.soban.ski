#!/usr/bin/env python
"""Step 1: turn the three original-trilogy dialogue files into word counts.

Input : SW_EpisodeIV.txt, SW_EpisodeV.txt, SW_EpisodeVI.txt
        (the widely shared dialogue-only transcripts, one spoken line per row:
         "1" "THREEPIO" "Did you hear that?...")
Output: work/word_counts.json
        { lemma: { "n": total, "films": {"IV": n, ...}, "speakers": {"HAN": n, ...},
                   "cap_ratio": share of non-sentence-initial uses that were capitalised,
                   "proper": True when the word is a character, place or ship name,
                   "example": {"film": "IV", "speaker": "HAN", "line": "..."} } }

Usage: python extract_words.py <folder holding the three txt files>
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import simplemma

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
WORK.mkdir(exist_ok=True)

FILMS = {"IV": "SW_EpisodeIV.txt", "V": "SW_EpisodeV.txt", "VI": "SW_EpisodeVI.txt"}

# Contractions are expanded before tokenising so "don't" counts as do + not.
CONTRACTIONS = [
    (re.compile(r"\b([Cc])an't\b"), r"\1an not"),
    (re.compile(r"\b([Ww])on't\b"), r"\1ill not"),
    (re.compile(r"\b([Ss])han't\b"), r"\1hall not"),
    (re.compile(r"\b([Aa])in't\b"), r"\1int"),          # keep ain't as one token
    (re.compile(r"n't\b"), " not"),
    (re.compile(r"'re\b"), " are"),
    (re.compile(r"'ve\b"), " have"),
    (re.compile(r"'ll\b"), " will"),
    (re.compile(r"'d\b"), " would"),
    (re.compile(r"'m\b"), " am"),
    (re.compile(r"'em\b"), " them"),
    (re.compile(r"'s\b"), ""),                           # possessive or "is": drop
]
TOKEN = re.compile(r"[A-Za-z]+(?:-[A-Za-z]+)*")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")

# Closed-class words whose inflected forms carry their own history. Left alone.
KEEP_SURFACE = {
    "i", "me", "my", "mine", "you", "your", "yours", "he", "him", "his", "she", "her",
    "hers", "we", "us", "our", "ours", "they", "them", "their", "theirs", "it", "its",
    "am", "is", "are", "was", "were", "be", "been", "being", "this", "that", "these",
    "those", "better", "best", "worse", "worst", "more", "most", "less", "least",
}

# In-universe names: characters, planets, ships, species. Wiktionary has no real-world
# history for them, and they would otherwise dominate the frequency table.
# Every speaker name in the transcripts is added to this list automatically.
IN_UNIVERSE = {
    "luke", "han", "leia", "chewie", "chewbacca", "artoo", "artoo-detoo", "threepio",
    "see-threepio", "vader", "darth", "obi-wan", "kenobi", "ben", "yoda", "lando",
    "calrissian", "skywalker", "solo", "organa", "jabba", "hutt", "boba", "fett",
    "owen", "beru", "biggs", "wedge", "porkins", "dack", "wormie", "greedo", "tarkin",
    "motti", "tagge", "dodonna", "ozzel", "piett", "veers", "needa", "ackbar", "nien",
    "nunb", "anakin", "palpatine", "jerjerrod", "bib", "fortuna", "oola", "wicket",
    "tatooine", "alderaan", "dagobah", "hoth", "endor", "yavin", "bespin", "dantooine",
    "anchorhead", "anoat", "kessel", "eisley", "mos", "tydirium", "sullust", "kashyyyk",
    "coruscant", "toshi", "tosche", "kuat", "bocce", "sarlacc", "jawas", "jawa", "sandpeople", "chuba",
    "tusken", "bantha", "dewback", "wampa", "tauntaun", "rancor",
    "aa-twenty-three", "ninety-four", "thx-one-one-three-eight",
}
# Speaker labels that are ordinary words (OFFICER, CAPTAIN, RED LEADER) stay words.
ROLE_WORDS = {
    "officer", "captain", "pilot", "trooper", "commander", "general", "admiral", "voice",
    "man", "controller", "deck", "leader", "red", "gold", "gray", "green", "wingman",
    "rebel", "imperial", "emperor", "creature", "bartender", "aide", "woman", "gunner",
    "technician", "chief", "ship", "guard", "medical", "droid", "tech", "first", "second",
    "third", "fourth", "operator", "announcer", "stormtrooper", "intercom", "women", "the",
    "and", "boy",
}


def expand(line):
    line = line.replace("’", "'").replace("‘", "'")
    for pat, rep in CONTRACTIONS:
        line = pat.sub(rep, line)
    return line


def tokenize(line):
    """Yield (surface_token, sentence_initial)."""
    for sentence in SENTENCE_SPLIT.split(expand(line)):
        first = True
        for m in TOKEN.finditer(sentence):
            tok = m.group(0)
            # "human-cyborg", "scruffy-looking": split ad-hoc hyphenations the
            # lemmatiser does not know, but keep real hyphenated words together
            pieces = [tok]
            if "-" in tok and tok.lower() not in IN_UNIVERSE and not simplemma.is_known(tok.lower(), lang="en"):
                pieces = tok.split("-")
            for piece in pieces:
                if len(piece) == 1 and piece.lower() not in ("i", "a"):
                    continue                  # R2, D2, X-wing fragments
                yield piece, first
                first = False


def lemma_of(tok):
    low = tok.lower()
    if low == "i":
        return "I"
    if low == "aint":
        return "ain't"
    if low in KEEP_SURFACE or low in IN_UNIVERSE or not simplemma.is_known(low, lang="en"):
        return low
    lem = (simplemma.lemmatize(low, lang="en") or low).lower()
    return "I" if lem == "i" else lem


def main(script_dir):
    script_dir = Path(script_dir)
    stats = defaultdict(lambda: {"n": 0, "films": Counter(), "speakers": Counter(),
                                 "cap": 0, "noninit": 0, "example": None})
    speakers_seen = set()
    n_lines = 0
    for film, fname in FILMS.items():
        with open(script_dir / fname, encoding="utf-8", errors="replace") as fh:
            reader = csv.reader(fh, delimiter=" ", quotechar='"', skipinitialspace=True)
            next(reader)  # header row
            for row in reader:
                if len(row) < 3:
                    continue
                speaker, line = row[1].strip(), row[2].strip()
                speakers_seen.add(speaker)
                n_lines += 1
                for tok, initial in tokenize(line):
                    lem = lemma_of(tok)
                    s = stats[lem]
                    s["n"] += 1
                    s["films"][film] += 1
                    s["speakers"][speaker] += 1
                    if not initial:
                        s["noninit"] += 1
                        s["cap"] += tok[:1].isupper()
                    # prefer a Han Solo example line when one exists
                    if s["example"] is None or (speaker == "HAN" and s["example"]["speaker"] != "HAN"):
                        s["example"] = {"film": film, "speaker": speaker, "line": line}

    # Speaker labels such as "AUNT BERU" or "DEATH STAR CONTROL" mix names with ordinary
    # words, so only the parts the lemmatiser has never heard of are treated as names.
    names = set(IN_UNIVERSE)
    for sp in speakers_seen:
        for part in re.split(r"[\s/-]+", sp.lower()):
            if len(part) > 2 and part not in ROLE_WORDS and not simplemma.is_known(part, lang="en"):
                names.add(part)

    out = {}
    for lem, s in stats.items():
        out[lem] = {
            "n": s["n"],
            "films": dict(s["films"]),
            "speakers": dict(s["speakers"].most_common()),
            "cap_ratio": round(s["cap"] / s["noninit"], 2) if s["noninit"] else None,
            "proper": lem in names,
            "example": s["example"],
        }
    with open(WORK / "word_counts.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    tokens = sum(v["n"] for v in out.values())
    proper = sum(1 for v in out.values() if v["proper"])
    print(f"{n_lines} lines, {tokens} tokens, {len(out)} distinct lemmas "
          f"({proper} in-universe names) -> {WORK / 'word_counts.json'}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else HERE / "scripts")
