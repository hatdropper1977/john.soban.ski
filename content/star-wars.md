Title: Ancient Rome in Corellia:  The Hidden History in Star Wars' Language
Date: 2026-09-26 09:00
Author: john-sobanski
Category: Data Science
Tags: Data Science, Python, JavaScript, Star Wars, Etymology, D3, Leaflet, Cytoscape
og_image: images/Star_Wars/00_Luke_Jump.jpg
twitter_image: images/Star_Wars/00_Luke_Jump.jpg
Slug: star-wars
Status: published
Summary: The words spoken in Star Wars hint at a hidden history, including Ancient Rome, Arabic civilizations, and Medieval France.  Today we look at charts that explore this history.  In addition, we see that the villains tend to use a higher proportion of Latin words, and the heroes use Anglo-Saxon words.

In college a friend told me how a physicist analyzed the structural integrity of AT-ST walkers.  Since the Ewoks crushed an AT-ST with two logs dropped on rope, the physicist surmised, they could also throw a spear through the armor.  The physicist proved this through equations of force.

This exercise in high brain power and creativity focused on a ridiculous and unimportant scenario tickled me.  Now, three decades later, I get to contribute to this silly canon.  Today, I will investigate the vocabulary used in the original trilogy and its implications for Star Wars history and geography.

## Quick Examples
In **A New Hope**, Han Solo refuses to join the attack on the Death Star:

> What good's a reward if you ain't around to use it? Besides, attacking that battle station ain't my idea of courage. It's more like suicide.

The word **Suicide** sounds like ancient Latin.  Since Han uses that word, can we assume that Corellia had an ancient Rome?  (FWIW Thomas Browne first recorded that word in 1643's **Religio Medici**).  **Courage** also includes Latin origins. 

The name **Admiral Ackbar** includes a word of Arabic origins (أمير).  Darth Vader speaks the word **Admiral** on multiple occasions.  Can we infer that the Rebel Alliance and the Empire both include worlds with Arabic heritage?

I cataloged all words spoken in the original trilogy and then traced them through (our) real-world English history.  This helps illustrate the hidden history of the Star Wars universe.  

## Where?  A Map of the Vocabulary
The first figure puts every word on the map based on their geographic origin.  Circle size shows the frequency of words spoken in the original trilogy.  Color depicts the date of entry to the English language.  You can switch the color to language family instead.

Borrowed words follow a geographic path through time.  **Galaxy**, for example, originated in Athens, moved to France and then landed in English.  You can select the **Origin Depth** menu to investigate nodes on this path.

Dashed lines trace the routes of the forty most frequent **traveling** words.  Type a word into the box to draw its route.  Try **admiral**.  This shows **Baghdad to Bologna to Paris to Rouen to England**.

<div id="sw-map-app" class="sw-viz"><p>This figure needs JavaScript.</p></div>

A quick glance at the map indicates the importance of each region/time on the English language, with England most important, Rome next (Latin words) followed by Athens (for science and politics).  We even see that Norway supplies a significant number of words to our everyday speech.

## When?  A Timeline With a Slider

The second figure shows the **birth dates** of **Star Wars** words.  The bars count the words that entered English in each fifty-year window, colored by origin and drawn on a square-root scale for visibility.  The colored strip above the chart shows the presence of each language in each period.

The slider moves through time, to show the words of each epoch.  The presets jump to the Norman conquest, Chaucer, Shakespeare and the release of **A New Hope**.

You can pick famous lines in the quote box, to see which words each character's line owes to each era.

<div id="sw-timeline-app" class="sw-viz"><p>This figure needs JavaScript.</p></div>

This table shows the growth of **A New Hope** vocabulary over time, in terms of distinct words vs. total corpus.

| Year | Distinct words | Every word spoken |
|------|---------------:|------------------:|
| 1100 | 41% | 79% |
| 1200 | 44% | 82% |
| 1400 | 80% | 95% |
| 1700 | 95% | 98% |
| 1900 | 99% | 99.6% |

60% of the distinct words in the film postdate the Norman conquest and 40% of the distinct words pre-date it.

## How?  An Etymology Knowledge Graph

The third figure depicts the word network.  Words connect to the forms they passed through, the forms connect to their languages and the six most talkative characters connect to the words they say.  Chains start at the deepest attested form and end at the reconstructed root, so **suicide** runs from Han Solo through **suīcīdium** and **suī** plus **caedere** to Latin.

You can select a language or a character to walk the knowledge graph. You can also use the search box to add any word not already displayed.

<div id="sw-graph-app" class="sw-viz"><p>This figure needs JavaScript.</p></div>

## Findings

**Native English accounts for most of the dialogue (1,003 words, 81% of everything spoken).**  This includes pronouns, articles, prepositions and the verbs **be**, **have**, **do**, **go**, **come**, **know**, **see** and **make**.  English also drives the emotional core: **father**, **friend**, **hope**, **fear**, **love**, **hate**, **dark**, **light**, **death**, **life**.

**Old Norse provides 65 words.**  The Vikings gave English its third-person plural pronouns: **they**, **them**, **their**.  Norse provides **get**, **take**, **give**, **want**, **die**, **hit**, **wrong**, **bad**, **big**, **weak**, **both**, **sky** and **skin**.  Do you know the Han meme **Never tell me the odds**? Norse provided us with **odds**.

**French provides nearly 700 words.**  Old French, Anglo-Norman and Middle French together handed English more distinct words than any source (barring Old English), but most derive from Latin.  This vocabulary stresses power and organization: **empire**, **emperor**, **imperial**, **rebel**, **rebellion**, **alliance**, **senate**, **governor**, **princess**, **captain**, **general**, **station**, **destroy**, **courage**, **reward**, **battle**, **faith**, **religion**.  The Galactic Empire administers its world in the language of Norman aristocracy.

**Direct Latin (not derived from French) provides 144 words.**  These include: **suicide**, **transmission**, **data**, **tractor**, **vector**.  Who knew **data** stems from Ancient Rome?

**Ancient Greek provides 72 words.**  These words focus on science and the cosmos: **galaxy**, **planet**, **asteroid**, **meteor**, **system**, **energy**, **ion**, **proton**, **thermal**, **technology**, **strategy**, **logic**, **academy**, **pilot** and, via **android**, **droid**.

**Arabic - just Admiral - 12x.**  Arabic **amīr**, commander, via **amīr al-baḥr**, commander of the sea, passed through Norman Sicily into Medieval Latin to French and into English around 1200.  Every time Vader says "Admiral Piett" he uses a word the Caliphate gave to the Mediterranean.

**Japanese - only Jedi - 43x.**  George Lucas connected **Jedi** to **jidaigeki**, the Japanese period dramas that shaped the films.  

**The 20th century contributes 20 words.**  **Robot** arrived in 1923 from Karel Čapek's play **R.U.R.**, built on Czech **robota**, forced labor.  Mari Wolf coined **droid** in 1952.  **Laser** represents an acronym from 1957.  Lucas coined **lightsaber**, **Wookiee** and **nerf** for the films.

When I score each character by the share of their words with Latin, French or Greek ancestry, the ranking sorts the galaxy by class.  The Empire speaks the most Latin, with Grand Moff Tarkin the most Latinate.  About a fifth of his words stem from Latin origins.  Darth Vader follows with 17% and the protocol droid C-3PO lands at 15%.  Luke Skywalker, the farm boy, has the lowest Latinate proportion (8%), with Han Solo next.  I find it interesting that the bureaucratic villains use mostly Latin derived words, and the humble heroes use mostly Old-English derived words.

## The Method
My analysis uses words, etymologies and dates.

### Words
I collect the words via dialogue-only transcripts of Episodes IV, V and VI.  Each row holds a speaker and a line:

```bash
$ head -3 SW_EpisodeIV.txt
"character" "dialogue"
"1" "THREEPIO" "Did you hear that?  They've shut down the main reactor.  We'll be destroyed for sure.  This is madness!"
"2" "THREEPIO" "We're doomed!"
```

A Python script tokenizes the lines and lemmatizes the tokens.  It expands contractions so that **don't** becomes **do** plus **not**.  I use the pure-Python [simplemma](https://github.com/adbar/simplemma) to collapse **ships**, **destroyed** and **feelings** into **ship**, **destroy** and **feeling**.  I do not process pronouns or irregular forms, since **me**, **were** and **better** each carry their own history.

```python
CONTRACTIONS = [
    (re.compile(r"\b([Cc])an't\b"), r"\1an not"),
    (re.compile(r"\b([Ww])on't\b"), r"\1ill not"),
    (re.compile(r"\b([Aa])in't\b"), r"\1int"),   # keep ain't as one token
    (re.compile(r"n't\b"), " not"),
    (re.compile(r"'re\b"), " are"),
    (re.compile(r"'ve\b"), " have"),
    (re.compile(r"'ll\b"), " will"),
    (re.compile(r"'d\b"), " would"),
    (re.compile(r"'m\b"), " am"),
    (re.compile(r"'s\b"), ""),                    # possessive or "is": drop
]

def lemma_of(tok):
    low = tok.lower()
    if low in KEEP_SURFACE or not simplemma.is_known(low, lang="en"):
        return low
    return simplemma.lemmatize(low, lang="en").lower()
```

I place character, planet and ship names on an exclusion list.  **Luke**, **Tatooine** and **Chewbacca**, for example, have no real-world history to trace and they would otherwise dominate the frequency table.

The three films give us 2,523 lines, 26,094 spoken words and 2,152 distinct lemmas after processing.

### The Etymologies
I use [Wiktionary](https://en.wiktionary.org) for the history of each word.  The rendered pages read like prose, and behind them lie structured wikitext.  The structured etymologies include templates that name the relationship, source language and source word:

```
From {{inh|en|enm|admiral}}, from {{der|en|xno|-}} and {{der|en|fro|admiral}},
from {{der|en|la-med|admiralis}}, ... from {{der|en|ar|أَمِير||commander}}
```

The example above shows that **admiral** stems from Middle English, which derived it from Anglo-Norman and Old French, which derived it from Medieval Latin, which derived it from the Arabic **amīr** (commander).  The MediaWiki API loads raw text twenty pages at a time:

```python
API = "https://en.wiktionary.org/w/api.php"

def fetch_titles(titles):
    params = {"action": "query", "prop": "revisions", "rvprop": "content",
              "rvslots": "main", "redirects": 1, "titles": "|".join(titles),
              "format": "json", "formatversion": "2"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)
```

The parser walks the first Etymology section under the **English** heading and collects every hop.  It accommodates a Wiktionary API gotcha.  Newer entries only list the first hop, so the script follows the chain into the Middle English and Old French pages.

I assign a display name, a color family and an approximate homeland to each source language.  Latin sits at Rome, Old Norse in Norway, Anglo-Norman at Rouen, Arabic at Baghdad and Proto-Indo-European on the Pontic steppe.  

### The Dates

I use plenty of **engineer's margin** to assign dates.  Wiktionary does not provide dates for all words, so I augment the data set with dates from the Online Etymology Dictionary.  For undated words, I impute the dates from their epoch.  Old English words become 800, Middle English French becomes 1350 and so on.  I color these roughly-imputed words with a paler shade to indicate them on the timeline.


<div class="sw-assets">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<link rel="stylesheet" href="{static}/js/Star_Wars/star_wars.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.30.4/cytoscape.min.js" defer></script>
<script src="{static}/js/Star_Wars/sw_data.js" defer></script>
<script src="{static}/js/Star_Wars/star_wars.js" defer></script>
</div>

## Limits
- **Date Estimation.**  Wiktionary states a date for 102 words and I hand-checked about fifty more.  The remaining 1,900 sit at the midpoint of the era their chain implies.
- **Wiktionary.**  Wiktionary could have issues, since the public can edit it.
- **One etymology per word.**  When **Wiktionary** provides multiple etymologies for a word, I pick the first.
- **Lemmatization.**  Some words do not match the Python lemmatization logic and I drop them.

## Conclusion
The words spoken in Star Wars hint at a hidden history, including Ancient Rome, Arabic civilizations, and Medieval France.  Today we looked at charts that explore this history.  In addition, we see that the villains tend to use a higher proportion of Latin words, and the heroes use Anglo-Saxon words.  I also feel proud to contribute to the beloved institution of silly deep dives into science fiction lore.

![Luke Jump]({static}/images/Star_Wars/00_Luke_Jump.jpg)