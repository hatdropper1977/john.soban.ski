Title: Did Thoreau inspire the Unabomber? We use AI to Find Out!
Date: 2021-05-30 03:19
Author: john-sobanski
Category: Data Science
Tags: GCP, NLP, Machine Learning, Data Science
Slug: thoreau-vs-unabomber
Status: published


## **Good Vs. Evil** - Two Opposing paths Taken by a Similar Genius
This blog post provides a comparison between Henry David Thoreau's **Walden** and Ted Kaczynski's **Unabomber Manifesto.** 

![Walden Book]({static}/images/Thoreau_Vs_Unabomber/01_Walden_Thoreau.png)

To compare these two works, I use both a modern Natural Language Processing (NLP) Artificial Intelligence (AI) tool and traditional literary analysis.

![Unabomber Sketch]({static}/images/Thoreau_Vs_Unabomber/02_Unabomber_Sketch.png)

The Google Cloud Natural Language Application Programming Interface (API) quantifies the authors' sentiment (positive or negative) and intensity of emotion while traditional Literary Analysis compares and contrasts themes.  

## Google Cloud Natural Language Analysis
The [Google Cloud Natural API](https://cloud.google.com/natural-language/docs) allows developers to use Google's advanced, massive and validated language model to infer sentiment, extract entities and classify documents.  I will use the API to infer sentiment from the two texts, and then compare the results.  Sentiment analysis provides quantifiable metrics (hard numbers) which drive mathematical comparisons.

### Process Text
I use the Google API to infer sentiment (score) and intensity (magnitude).

The [Google Cloud Natural Language API documentation](https://cloud.google.com/natural-language/docs/basics#interpreting_sentiment_analysis_values) defines **score** and **magnitude**:

  *  Score
     *  Indicates the overall emotion of a document
  *  Magnitude
     *  Indicates how much emotional content is present within the document, and this value is often proportional to the length of the document

I use the following script to split each text into individual paragraphs, send each paragraph to the API, and then record the results.

```python
#!/usr/bin/env python
import pandas as pd
from google.cloud import language_v1

# Configure book name here 
#FILENAME = 'walden.txt'
FILENAME = 'unabomber.txt'

sentiment_dict = []

# Instantiates a client
client = language_v1.LanguageServiceClient()

with open(FILENAME, encoding='utf-8') as f:
    for line in f:
        if line.strip():
            try:
                document = language_v1.Document(content=line.strip(), type_=language_v1.Document.Type.PLAIN_TEXT)
                sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
                sentiment_dict.append( { \
                    'score' : sentiment.score, \
                    'magnitude' : sentiment.magnitude, \
                    'text' : line.strip() } )
            except:
                sentiment_dict.append( { \
                    'score' : 0.0, \
                    'magnitude' : 0.0, \
                    'text' : 'ERROR: {}'.format(line.strip()) } )

sentiment_df = pd.DataFrame(sentiment_dict)

sentiment_df.to_csv('{}_sentiment.csv'.format(FILENAME.split('.')[0]),
                    index= False)
```

I use the Google Cloud Natural API Domain Specific Language (DSL), although [requests](https://docs.python-requests.org/) also works.  **Walden** includes some latin, which **breaks** the service.  To mitigate against the **erorr** I use **try/ except** logic.  The **strip()** methods remove blank lines from the analysis.

Since both texts include a wide variety of characters, I store the results in a [Pandas](https://pandas.pydata.org/) dataframe.  The **to_csv()** method will escape all of the characters that disturb the Comma Separated Values (CSV) encoded output.

The script outputs files named **unabomber_sentiment.csv** and **walden_sentiment.csv** and each row includes a score, magnitude and the appropriate paragraph text.

The following snippit records several lines of the **Walden** output:

```csv
score,magnitude,text
0.20000000298023224,0.699999988079071,"When I wrote the following pages, or rather the bulk of them, I lived alone, in the woods, a mile from any neighbor, in a house which I had built myself, on the shore of Walden Pond, in Concord, Massachusetts, and earned my living by the labor of my hands only. I lived there two years and two months. At present I am a sojourner in civilized life again."
-0.10000000149011612,4.900000095367432,"I should not obtrude my affairs so much on the notice of my readers if very particular inquiries had not been made by my townsmen concerning my mode of life, which some would call impertinent, though they do not appear to me at all impertinent, but, considering the circumstances, very natural and pertinent. Some have asked what I got to eat; if I did not feel lonesome; if I was not afraid; and the like. Others have been curious to learn what portion of my income I devoted to charitable purposes; and some, who have large families, how many poor children I maintained. I will therefore ask those of my readers who feel no particular interest in me to pardon me if I undertake to answer some of these questions in this book. In most books, the I, or first person, is omitted; in this it will be retained; that, in respect to egotism, is the main difference. We commonly do not remember that it is, after all, always the first person that is speaking. I should not talk so much about myself if there were anybody else whom I knew as well. Unfortunately, I am confined to this theme by the narrowness of my experience. Moreover, I, on my side, require of every writer, first or last, a simple and sincere account of his own life, and not merely what he has heard of other men’s lives; some such account as he would send to his kindred from a distant land; for if he has lived sincerely, it must have been in a distant land to me. Perhaps these pages are more particularly addressed to poor students. As for the rest of my readers, they will accept such portions as apply to them. I trust that none will stretch the seams in putting on the coat, for it may do good service to him whom it fits."
0.0,2.0,"I would fain say something, not so much concerning the Chinese and Sandwich Islanders as you who read these pages, who are said to live in New England; something about your condition, especially your outward condition or circumstances in this world, in this town, what it is, whether it is necessary that it be as bad as it is, whether it cannot be improved as well as not. I have travelled a good deal in Concord; and everywhere, in shops, and offices, and fields, the inhabitants have appeared to me to be doing penance in a thousand remarkable ways. What I have heard of Brahmins sitting exposed to four fires and looking in the face of the sun; or hanging suspended, with their heads downward, over flames; or looking at the heavens over their shoulders “until it becomes impossible for them to resume their natural position, while from the twist of the neck nothing but liquids can pass into the stomach;” or dwelling, chained for life, at the foot of a tree; or measuring with their bodies, like caterpillars, the breadth of vast empires; or standing on one leg on the tops of pillars,—even these forms of conscious penance are hardly more incredible and astonishing than the scenes which I daily witness. The twelve labors of Hercules were trifling in comparison with those which my neighbors have undertaken; for they were only twelve, and had an end; but I could never see that these men slew or captured any monster or finished any labor. They have no friend Iolas to burn with a hot iron the root of the hydra’s head, but as soon as one head is crushed, two spring up."
-0.30000001192092896,3.200000047683716,"I see young men, my townsmen, whose misfortune it is to have inherited farms, houses, barns, cattle, and farming tools; for these are more easily acquired than got rid of. Better if they had been born in the open pasture and suckled by a wolf, that they might have seen with clearer eyes what field they were called to labor in. Who made them serfs of the soil? Why should they eat their sixty acres, when man is condemned to eat only his peck of dirt? Why should they begin digging their graves as soon as they are born? They have got to live a man’s life, pushing all these things before them, and get on as well as they can. How many a poor immortal soul have I met well nigh crushed and smothered under its load, creeping down the road of life, pushing before it a barn seventy-five feet by forty, its Augean stables never cleansed, and one hundred acres of land, tillage, mowing, pasture, and wood-lot! The portionless, who struggle with no such unnecessary inherited encumbrances, find it labor enough to subdue and cultivate a few cubic feet of flesh."
-0.5,2.9000000953674316,"But men labor under a mistake. The better part of the man is soon plowed into the soil for compost. By a seeming fate, commonly called necessity, they are employed, as it says in an old book, laying up treasures which moth and rust will corrupt and thieves break through and steal. It is a fool’s life, as they will find when they get to the end of it, if not before. It is said that Deucalion and Pyrrha created men by throwing stones over their heads behind them:—"
0.0,0.0,"Inde genus durum sumus, experiensque laborum,"
0.10000000149011612,0.10000000149011612,Et documenta damus quâ simus origine nati.
-0.10000000149011612,0.10000000149011612,"Or, as Raleigh rhymes it in his sonorous way,—"
0.6000000238418579,0.6000000238418579,"“From thence our kind hard-hearted is, enduring pain and care,"
0.10000000149011612,0.10000000149011612,Approving that our bodies of a stony nature are.”
-0.699999988079071,0.699999988079071,"So much for a blind obedience to a blundering oracle, throwing the stones over their heads behind them, and not seeing where they fell."
-0.4000000059604645,5.400000095367432,"Most men, even in this comparatively free country, through mere ignorance and mistake, are so occupied with the factitious cares and superfluously coarse labors of life that its finer fruits cannot be plucked by them. Their fingers, from excessive toil, are too clumsy and tremble too much for that. Actually, the laboring man has not leisure for a true integrity day by day; he cannot afford to sustain the manliest relations to men; his labor would be depreciated in the market. He has no time to be anything but a machine. How can he remember well his ignorance—which his growth requires—who has so often to use his knowledge? We should feed and clothe him gratuitously sometimes, and recruit him with our cordials, before we judge of him. The finest qualities of our nature, like the bloom on fruits, can be preserved only by the most delicate handling. Yet we do not treat ourselves nor one another thus tenderly."
-0.6000000238418579,2.0,"Some of you, we all know, are poor, find it hard to live, are sometimes, as it were, gasping for breath. I have no doubt that some of you who read this book are unable to pay for all the dinners which you have actually eaten, or for the coats and shoes which are fast wearing or are already worn out, and have come to this page to spend borrowed or stolen time, robbing your creditors of an hour. It is very evident what mean and sneaking lives many of you live, for my sight has been whetted by experience; always on the limits, trying to get into business and trying to get out of debt, a very ancient slough, called by the Latins æs alienum, another’s brass, for some of their coins were made of brass; still living, and dying, and buried by this other’s brass; always promising to pay, promising to pay, tomorrow, and dying today, insolvent; seeking to curry favor, to get custom, by how many modes, only not state-prison offences; lying, flattering, voting, contracting yourselves into a nutshell of civility or dilating into an atmosphere of thin and vaporous generosity, that you may persuade your neighbor to let you make his shoes, or his hat, or his coat, or his carriage, or import his groceries for him; making yourselves sick, that you may lay up something against a sick day, something to be tucked away in an old chest, or in a stocking behind the plastering, or, more safely, in the brick bank; no matter where, no matter how much or how little."
```

### Numerical Analysis
The output includes **score**, **magnitude** and **text**.

I input each CSV into Pandas for analysis, for example:

```python
una_df = pd.read_csv('unabomber_sentiment.csv')
```

I did a quick sanity check, and used [numpy](https://numpy.org/) to identify the most negative text from each author.

```python
una_df[ una_df.score == una_df.score.min()]
```

The first line of the [Chapman](https://en.wikipedia.org/wiki/Caesar_and_Pompey) quote clocks in at the most negative (-0.9) Thoreau sentiment:

> The false society of men—

> for earthly greatness

> All heavenly comforts rarefies to air. [Thoreau 141]

Kaczynski includes three paragraphs tied for most negative (-0.6), so I selected the paragraph with the highest magnitude (8.7):

> Oversocialization can lead to low self-esteem, a sense of powerlessness, defeatism, guilt, etc. One of the most important means by which our society socializes children is by making them feel ashamed of behavior or speech that is contrary to society's expectations. If this is overdone, or if a particular child is especially susceptible to such feelings, he ends by feeling ashamed of HIMSELF... In many oversocialized people this results in a sense of constraint and powerlessness that can be a severe hardship. We suggest that oversocialization is among the more serious cruelties that human being inflict on one another. [Kaczynski 26]

This quick analysis demonstrates that the Google NLP Model appears to correctly identify sentiment.

### Graphical Analysis
Since each work includes hundreds of paragraphs, I use Data Visualization (Data Viz) in the form of a Histogram to summarize the output data.

The following Histogram records the sentiment of "The Unabomber Manifesto."  Note that the paragraphs skew negative.  

Zero indicates a **neutral** sentiment.

![Unabomber Score Histogram]({static}/images/Thoreau_Vs_Unabomber/03_Unabomber_Hist.png)

Compare Kaczynski’s Data Viz to Thoreau’s.  Thoreau's paragraphs provide a symmetrical Histogram, and most of the paragraphs land in the **neutral** zone.

![Thoreau Score Histogram]({static}/images/Thoreau_Vs_Unabomber/04_Walden_Hist.png)

Remember that the Google API returns both **score** and **magnitude**.  We need to include the **magnitude** data into the analysis, to get a feel for the overall intensity of emotion.

I use a bivarate density plot, which looks like a smooth sheet placed on top of a blocky, two dimensional histogram.  I use Kernel Density Estimation (KDE) to represent the frequency of the datum in each **bucket** in a continuous way (vs. the discrete **count** found in histograms).  I follow the [SciPy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html) to make the chart.  

The colors represent the **density**.  The darker the color, the more instances of a particular **score/magnitude** pair.  The black dots represent the actual data points.

Note that I multiply the Score by ten in order to make the Data Viz more readable.

![Walden Bivariate Density Plot]({static}/images/Thoreau_Vs_Unabomber/05_Walden_Density.png)

Again, we see that Thoreau's text concentrates around Neutral tone, with the Magnitude higher around scores of zero.

Contrast Thoreau’s Data Viz to Kaczynski.

![Unabomber Bivariate Density Plot]({static}/images/Thoreau_Vs_Unabomber/06_Unabomber_Density.png)

The near forty-five degree angle of the contour map (the blue, green and yellow oval) indicates strong correlation between sentiment and magnitude.  The more negative Kaczynski writes, the stronger his emotions.  

Overall, however, most of his text lands in the **medium-negative** sentiment range.

## Literary Analysis
Ted Kaczynski and Henry David Thoreau (despite the separation of a century) live lives of uncanny similarity. Both tackle their field of expertise in unorthodox, pioneering and peerless manners, and both graduated from Harvard. These individuals tried their hand at teaching, but eventually withdrew from the profession and instead became **hermits** living in the wilderness in modest shanties. During their seclusion from society they produced their most influential works: [Walden](https://www.gutenberg.org/files/205/205-h/205-h.htm) and [The Manifesto](http://www.self.gutenberg.org/articles/unabomber_manifesto).

### Common View of Technology and Over-Socialization
The effect of technology and over-socialization negatively reducing the human experience represents the first (and most prevalent) issue found in both works. The Unabomber opens his tirade with:

> The Industrial Revolution and its consequences have been disastrous for the human race... [it has] reduce(d) human beings and many other living organisms to engineered products and mere cogs in the social machine [Kaczynski 1]

Thoreau did not live long enough to experience the far reaching effects of our industrial infancy, but he still provides insights into finding the pitfalls of devoting one’s life to **unnecessary** industrial labor. He writes:

> The laboring man has no leisure for a true integrity day by day; he cannot afford to sustain the manliest relations to men; his labor would be depreciated in the market. He has no time to be anything but a machine [Thoreau1 491]

Thoreau’s lambaste against **model farms** in **Chapter IX: The Ponds** criticizes technology’s tendency to reduce men and animals to cogs in a machine. He writes:

> A model farm! where the house stands like a fungus in a muck-heap, chambers for men, horses, oxen and swine, cleansed and uncleansed, all contiguous to one another! Stocked with men! A great grease spot, redolent of manures and buttermilk! under a high state of cultivation, being manured with the hearts and brains of men! As if you were to raise your potatoes in the churchyard! Such is a model farm! [Thoreau1 593]

Kaczynski expresses the opinion that technology’s minimizing effect on an individual's importance in society imparts a sense of worthlessness over the general populace by taking away their autonomy and power (which he groups together as the definition for **The Power Process**, his own term). He writes:

> When an individual does not have opportunity to go throughout the power-process the consequences are boredom, demoralization, low self-esteem, inferiority feelings [sic], defeatism, depression, anxiety, guilt, frustration ...[etc.] [Kaczynski 44]

Thoreau gets the point of human demoralization across in his work more elegantly and without the use of
invented psychological jargon when he writes:

> The mass of men lead lives of quiet desperation... A stereotyped but unconscious despair is concealed even under what are called games and amusements of mankind. There is no play in them, for this comes after work [Thoreau 1492].

Thoreau later reveals that an individual should remove herself from the influence of technology and becoming one with nature in order to escape depression. In **Chapter V: Solitude**, he writes:

> There can be no very black melancholy to him who lives in the midst of nature and has his senses still... Nothing can rightly compel a simple and brave man to a vulgar sadness. While I enjoy the friendship of the seasons I trust that nothing can make a burden to me [Thoreau 1559]

The Unabomber shares the same sentiment that modern man should go back to nature to escape ennui. Unlike Thoreau, however, he gives a scientific reason to explain our difficulty in achieving contenment when removed from nature.  He writes:

> We attribute the social and psychological problems of modern society to the fact that society requires people to live under conditions radically different from those under which the human race has evolved and to behave in ways that conflict with the patterns of behavior that the human race developed while living under the earlier conditions [Kaczynski 46]

### Common View of Workaholic/ Novelty Culture
Thoreau and Kaczynski both focus on the detrimental effects of our workaholic/ consumer culture, where workers work long hours to pay for disposable, novelty items and engage in meaningless activities for distraction. Kaczynski writes:

> ...even if they have a great deal of money, [modern workers] cannot satisfy their constant craving for the shiny new toys that the marketing industry dangles before their eyes.  So, they always feel hard pressed financially, even if their income is large, and their cravings are frustrated [Kaczynski 80]

Thoreau also attacks the consumer mentality on numerous occasions, stressing that a simple life trumps a life spent accumulating junk and requires much less effort. For example:

> ...if one would live simply and eat only the crop he raised , and raise no more than he ate, and not exchange it for an unsufficient quantity of more luxurious and expensive things ... he could do all his farm work with his left hand at odd hours of the summer [Thoreau1 518]

>  ...if working were not my trade, I could get all the meat I should want by hunting... I could get all I should want for one week in one day [Thoreau 1566]

He concludes on this theme with a powerful and succinct statement:

> Superfluous wealth can buy superfluities only. Money is not required to buy one necessary of the soul [Thoreau 1660].

The Unabomber manifesto brings up an interesting aspect of human nature, which he labels the theory of **surrogate activities**.  He writes that because technological society takes care of our basic needs, we humans have to invent artificial needs in order to feel satisfied with our lives: 

> A surrogate activity is an activity that is directed toward an artificial goal that the individual pursues for the sake of the "fulfillment" that he gets from pursuing the goal, not because he needs to attain the goal itself. For instance there is no practical motive for building enormous muscles, hitting a little ball in a hole or acquiring a complete series of postage stamps. Yet many people in our society devote themselves with passion to bodybuilding, golf, or stamp collecting [Kaczynski 84]

Thoreau criticizes this same notion of devoting one’s life to the pursuit of **nonsense**, and not concentrating on what’s really important in life:

> ...It is easier to sail many thousand miles through cold and storm and cannibals ... than it is to explore the private sea, the Atlantic and the Pacific ocean of one’s being alone... It is not worth the while to go round the world to count the cats in Zanzibar. Yet do this even till you can do better, and you may perhaps find some “Symmes’ Hole” by which to get at the inside at last... if you would learn to speak all tongue and conform to the customs of all nations, if you would travel farther than all travelers...and cause the Sphinx to dash her head against the stone [Thoreau 1657] 

I predict that the Unabomber would label the surrogate activities that Thoreau just mentioned **travel-oriented surrogate activities**.  In addition to these travel-oriented activities, Thoreau criticizes other **surrogate activities** in Walden. For example, he considers the hobby of reading junk novels a useless pasttime:

> Most men are satisfied if they read or hear read, and perchance have been [convinced] by the wisdom of one good book, the Bible, and for the rest of their lives vegetate and dissipate their faculties in what is called easy reading... the result is dullness of sight, a stagnation of the vital circulations, and a general [sinking] and sloughing off of all the intellectual faculties [Thoreau 1545]

The Unabomber lists the acquisition of useless junk a surrogate activity, writing:

> ...many people put into their work far more effort than is necessary to earn whatever... they desire and this extra effort constitutes a surrogate activity [Kaczynski 84]

Thoreau also lambastes the **collecting surrogate activity**. He writes:

> ...as I preferred some things to others I especially valued my freedom ... I did not wish to spend my time in earning rich carpets... delicate cookery, or a house in the Grecian or the Gothic style just yet [Thoreau 1526]

Thoreau suggests that nonspiritual, superficial pastimes do not substitute for the higher principles of Self, God nor freedom.  The Unabomber wraps a similar sentiment in psychological jargon. 

### Common View of Rage Against the Machine
Kaczynski and Thoreau both desire to eliminate **the Machine** or what they label the ugly and evil influence of technology from the world.

![Earth Crisis Destroy the Machines Album Art]({static}/images/Thoreau_Vs_Unabomber/07_Earth_Crisis.png)

Kaczynski writes:

> it is necessary to develop and propagate an ideology that opposes technology and the industrial society... the factories should be destroyed, technical books burned, etc. [Kaczynski 165]

Thoreau considers the railroad (arguably the springboard for America’s industrial revolution) **the machine**.  Thoreau spares no feelings of mercy or clemency for the railroad.  He perceives the railroad a threat to nature, the same way the Unabomber perceives 20th century industrial society a threat to nature:

> That devilish Iron Horse, whose ear-rending neigh is heard throughout town, has muddied the Boiling Spring with his foot, and he it is that has browsed off all the woods on Walden shore, that Trojan horse, with a thousand men in his belly, introduced by mercenary Greeks! Where is the country s champion, the [dragon slayer] to meet him at the Deep Cut and thrust an avenging lance between the ribs of the bloated pest? [Thoreau 1591]

Thoreau wants mankind to preserve, if not so much return to the Natural habitat that he shares the Earth with. The Unabomber shares this sentiment. He writes:

> An ideology, in order to gain enthusiastic support... must be FOR something, as well as AGAINST something. The positive ideal [I] propose [in my manifesto] is Nature. That is, WILD nature: those aspects of the earth functioning of the Earth and its living things that are independent of human management and free of human interference and control [Kaczynski 183]

The two works provide more parallels that pertain to important social issues. The Unabomber, for example, writes: 

> Instead of removing the conditions that make people depressed, modern society gives them antidepressant drugs. [Kaczynski 145]

His statment provides an uncanny response to Thoreau’s rhetorical question:

> What is the pill which will keep us well, serene, contented? [Thoreau 1563]

### Differences
The two works have their differences in addition to their similarities. First of all, the writing styles of the two authors clash quite severely. Thoreau uses a flowery, poetic style and injects a sense of humor into the text (see the “Cenobites” pun).  Kaczynski’s uses a staccato, scientific and analytic voice and his work contains not a single iota of brevity.

In addition, **Walden** includes an overall tone of optimism, whereas Kandinsky focuses on dire pessimism. Finally, Thoreau’s “tangents” mainly describe nature, his possessions, how he built his house,  etc., which all deal with his environment. Kaczynski's tangents on the other focus on political themes.

Thoreau's work speaks for itself, and society recognizes the value of **Walden** solely by his writing talents.  Thoreau did not need to partake in any extraneous activities to bring attention to it. Thoreau did not need to use violence to set himself apart from his contemporaries. 

Contrast this with Kaczynski, who clearly states :

> In order to get our message before the public with some chance of making a lasting impression, we've had to kill people [Kaczynski 96]

Kaczynski did in fact resort to violence, and killed people.  We must not forget his cowardly actions.

## Conclusion
Based on literary analysis, Thoreau and Kaczynski see eye to eye in relation to their works’ major themes. Both authors appear to be steadfast in their pro-nature (and all the good that comes from it) / anti-technology (and all the ills that are a result of it) convictions. 

AI inference provides hard numbers that indicate Kaczynski communicates in a strong, negative tone and Thoreau uses a neutral tone in terms of both emotion and intensity.
