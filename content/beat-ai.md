Title: Beat Artificial Intelligence (AI) with Active, Present Voice
Date: 2023-10-28 01:23
Author: john-sobanski
Category: Data Science
Tags: NLP, Machine Learning
og_image: images/Beat_Ai/03_Chat_Avatar.png
twitter_image: images/Beat_Ai/03_Chat_Avatar.png
Slug: beat-ai
Status: published

When I ask ChatGPT to write detailed technical content, I find that it outputs hollow, bombastic, and meandering prose. 

Such output places a high cognitive load on my mind:  My subconscious must fill in the holes of the passive, cliche-ridden, and obtuse narratives.  I long for clear communication.

![Shocked Robot]({static}/images/Beat_Ai/01_Shocked_Robot.png)

In this blog post, I collect some ChatGPT **tells**, discuss the issues with these **tells** and then recommend how to fight the AI leviathan.

## ChatGPT
In December 2015 Elon Musk, Greg Brockman, Ilya Sutskever, and Sam Altman invested over $1B (USD) to found OpenAI.  Last year, the OpenAI foundation launched ChatGPT, a user-friendly Large Language Model (LLM) built upon the Generative Pre-trained Transformer (GPT) Four (GPT-4).  Traditional data services **retrieve** content, and ChatGPT **generates** content (notice the subtle difference).

LLM allows users to create non-existent data.  Generative AI, for example, can create an answer to the question "Name Socrates Favorite 90s Sitcom."

## ChatGPT Output
ChatGPT output appears impressive at first read.  The initial glow, however, fades in seconds.  The prose then injects the reader with a mild sense of discomfort.

Consider the following output from ChatGPT

> In the intricate world of digital communication the ability to label and prioritize data is paramount, especially when it comes to real-time data.

At first, I read this and thought:

> Wow!  Tell me more.

Then, I felt unease and thought: 

> Wait, that statement says nothing.

The ChatGPT-constructed sentence values showy cadence over communication.  

Take the phrase:

> the intricate world of digital communication

It sounds impressive but conveys nothing.  **Intricate** lacks precision, **intricate world** lacks authority.

I believe ChatGPT wants to convey the importance of **labeled/ prioritized** data, and I fail to see how the adjective **intricate** strengthens that argument.

The sentence continues with:

> the ability to label and prioritize data is paramount

I ask, **Paramount to Who?**.  I also need to take a step back and remember the definition of **Paramount**: 

> Paramount: Chief in importance or impact

ChatGPT hallucinates here.  I consider the ability to label and prioritize real-time data a useful feature of digital communications, but I do not consider it **chief in importance or impact.**  I consider the ability to transmit packets from source to sink **chief in importance** for digital communications.

Consider another ChatGPT-authored example:

> Phishing detection is of paramount importance in today's digital landscape as cybercriminals continuously refine their deceptive tactics to trick individuals and organizations into divulging sensitive information. 

I have experience with computer security and know that most security breaches result from Phishing attacks.  In that light, I would consider Phishing Detection **chief in importance or impact** to computer security.  While correct, ChatGPT makes this claim without any evidence.  

ChatGPT then uses the phrase **today's digital landscape**.  That poetic phrase sounds impressive but lacks meaning or at the very least lacks any weight in the context of this sentence.

I use my [Kagi Search Engine](https://kagi.com/) (Non-affiliate link) to retrieve a definition of **Digital Landscape**.  It returns dozens of different definitions, including one for advertising, one for online games, and one for communications infrastructure policy.  

I consider **Digital Landscape** a marketing buzzword, an empty vessel for **content creators** to fill in a way that serves their narrative.

ChatGPT should define **digital landscape** to remove ambiguity.

## ChatGPT Tells
I ask ChatGPT to create two-sentence summaries for a variety of topics.  I then highlight any turns of phrase that lead to sensations of discomfort.

I organize them here in the hopes that a pattern will emerge.

I name the first Category **Empty Phrases That Almost Sound Smart**.  ChatGPT peppers these phrases in introductory paragraphs, without justification or evidence.

For example:

- In today's **digital landscape**
- In the **intricate world** of
- In **this era** of
- **Unlocking new horizons**
- A **strategic imperative**
- Recognizing the **inherent challenges in this domain**
- and the **unique challenges they face**
- an increasingly important part of **our global economy**

I call the next category **Unsubstantiated Grandiosity**:

- Infrastructure as Code (IaC) is a **paradigm-shifting** approach
- Businesses can achieve **unprecedented** agility
- These models provide valuable insights...making them **indispensable** for decision-making
- Graphics Processing Units (GPUs) have **transcended** their original role in rendering graphics to become **indispensable accelerators**
- Digital advertising holds **immense significance**
- Blockchain... brings **unprecedented efficiency**

Next up, **Empty Cliches in Passive Voice**

- Phishing detection **is of paramount importance**
- Regression models **are powerful tools**
- ...making robust security frameworks **a paramount concern**
- Embracing and diligently implementing security frameworks **is not just** a regulatory necessity but a strategic imperative
- Cleaning data **is the essential first step**

**Adverbs** speak for themselves:

- to share and decipher data **seamlessly** is paramount
- **specifically** designed for Banks and the unique challenges they face
- an **increasingly** important part of our global economy
- Embracing and **diligently** implementing security frameworks

![Kevin and Dustin in Outbreak]({static}/images/Beat_Ai/02_Outbreak_Quote.png)

> KEVIN SPACEY (as Casey Schuler in Outbreak): It’s an adverb, Sam. It’s a lazy tool of a weak mind.

I call the next group **Cringe Words**, words that actual humans never use in normal conversation unless they want to appear smart while high on Meth.  

- Indeed
- Alas
- Especially

I maintain that the word **Indeed** signals ChatGPT text more than any other **tell**, so I wrote a bash script to detect ChatGPT prose:

```bash
str=`grep -i indeed prose.txt`
if [ "$str" ]
   then echo 'ChatGPT wrote this'
fi
```

I call the next group **Midwit Words**, words that people use to appear smart.

- Leverage (Instead of use)
- Ensure (Instead of an appropriate verb)
- Utilize (Instead of use)
- Penultimate (Instead of Ultimate)
	

## My Recommendation
ChatGPT produces wordy, loose text, light on meaning or evidence, and peppered with bombastic flourishes and empty cliches.  Authors must tighten their prose to separate their work from ChatGPT output.

![ChatGPT Avatar]({static}/images/Beat_Ai/03_Chat_Avatar.png)

I recommend an active, present voice that follows the [Subject-Verb-Object (SVO)](https://en.wikipedia.org/wiki/Subject%E2%80%93verb%E2%80%93object_word_order) template.  I advise against adverbs, you should instead choose a precise verb.  Do not use adjectives without proper context.  Never write a cliche.

Take the original ChatGPT sentence:

> In the intricate world of digital communication the ability to label and prioritize data is paramount, especially when it comes to real-time data.

Rewrite it to:

> Digital Communications systems label and prioritize Real-Time Data to prevent jitter and buffering

I encourage you to investigate [E-Prime](https://en.wikipedia.org/wiki/E-Prime), an upgrade to the English language that prioritizes clarity, precision and respect for the listener.

D. David Bourland Jr studied under General Semantics founder [Alfred Korzybski](https://en.wikipedia.org/wiki/Alfred_Korzybski) and developed E-Prime.  

E-Prime removes all forms of the verb **to be**.  This includes (along with negative contractions and contractions):

- am
- is
- are
- was
- were

The verb **to be** short circuits the [Subject-Verb-Object (SVO)](https://en.wikipedia.org/wiki/Subject%E2%80%93verb%E2%80%93object_word_order) word order.  It allows lazy, imprecise writing.  **To be** verbs drive passive voice:

Consider

> OpenAI was founded in 2015

Versus

>  Elon Musk, Greg Brockman, Ilya Sutskever and Sam Altman founded OpenAI in 2015

Consider this lazy, loose sentence:

> OpenDaylight is a Software Defined Network (SDN) Controller.

I must work harder to construct a sentence without the verb **to be**.  I need to select subjects, and verbs and provide evidence.  The additional information benefits the reader:

> Internet Service Providers (ISP), Cloud Service Providers (CSP), Data Center Engineers, and Academics use the OpenDaylight (ODL) platform to tailor and automate computer networks. 

Kellog and Bouland write:

> [misuse of the verb **to be** creates] a deity mode of speech [and allows] even the most ignorant to transform their opinions magically into god-like pronouncements on the nature of things - Kellogg, E. W.; Bourland Jr., D. David (1990). "Working with E-Prime: Some Practical Notes" (PDF). Et Cetera. 47 (4): 376–392.

I use E-Prime exclusively on my blog.  I encourage you to read my other posts and notice how I avoid the verb **to be** and write with a clear, active, SVO voice.

## Conclusion
ChatGPT provides a useful service.  It generates prose in seconds, based on little user input.

ChatGPT excels in some use cases:

- You need bullets for advertising copy
- You need an invite for an event or meetup
- You need a quick outline
- You have writer's block and need a nudge
- You need to produce rote/ box-checking paperwork 
- You need copious "good enough" content to increase your web presence
- Your company values **looking busy** over **productivity**

If you need to communicate a clear message to your user, I recommend you craft your narrative by hand and use SVO, deliberate adjectives, and E-Prime.
