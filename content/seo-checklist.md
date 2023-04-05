Title: An Actionable, Focused, SEO Checklist for Your Website
Date: 2023-03-25 06:26
Author: john-sobanski
Category: howto
Tags: SEO, S3, Brave
og_image: images/Seo_Checklist/14_Black_Train.png
twitter_image: images/Seo_Checklist/13_Spider_Engine.png
Slug: seo-checklist
Status: published

In this blog post I present an actionable, focused checklist for the bare minimum, required SEO.

Search engines provide links to useful pages based on user queries.  You want search engines to return links to **YOUR** web page.  To improve your chances of high page ranks you need to follow basic SEO website hygiene.

![Search Engine Spider]({static}/images/Seo_Checklist/13_Spider_Engine.png)

I write my blog posts in [Markdown](https://github.com/hatdropper1977/john.soban.ski) and then use Pelican to generate static web pages.  I [use S3 and Cloudfront to serve my site over HTTPS]({filename}/how-to-configure-s3-websites-to-use-https-part-1.md).  For over seven (7) years I took a **set it and forget it** approach to website hosting.  

I did not consider Search Engine Optimization (SEO) until my Google impressions dropped in January.

Since then I learned that even static websites require housekeeping.  

## Tools Used
I discovered free tools that help identify SEO issues.

Google and Bing provide tools for their search engines.

Ahrefs also provides Software as a Service (SaaS) that audits your site.

### Google Search Tools
I do not recommend Google search tools.  They give vague diagnostic advice.

I clicked "Validate fix" back in February and still have not received any updates from the tool.

![Google Pending Alert]({static}/images/Seo_Checklist/01_Google_Pending.png)

### Bing Search Tools
I like the Bing tools.  They give concrete, actionable advice.

Microsoft gives you credits for a site scan.  I recommend running these once a week.

![Bing Site Scan]({static}/images/Seo_Checklist/02_Bing_Scan.png)

### AHREFS
I recommend [AHREFS](https://app.ahrefs.com/user/login) (Non-affiliate link!).

They run a site audit on schedule once a week.

![AHREFS Splash]({static}/images/Seo_Checklist/03_Ahrefs_Splash.png)

AHREFS gives the most actionable info.  If your site links to broken external pages, for example, you can sort by either the external links or your pages that link to those broken links.

## Step One:  A Deliberate Sitemap
Search engines use crawlers to discover web pages.  Once the crawler compiles a collection of pages, the Search engine indexes (a subset of) those discovered pages.

The indexer then grades the quality of each page.  The search engine promotes high-quality pages to high-ranking positions in search results.  The search engine demotes or ignores low-quality pages.

Low-quality pages drive a **bad apple spoils the bunch** effect on your site: Low-quality pages will tank the rank of the high-quality pages on your site.

You need to pay extra attention to the quality of the pages you include in your **sitemap.xml**.  Including low-quality pages in your sitemap demonstrates sloppiness and carelessness.  If you include low-quality pages in your sitemap, the search engine will question the reputation of your site and penalize your rank.

![No junk in sitemap]({static}/images/Seo_Checklist/04_Clean_Sitemap.png)

Low-quality pages include rambling text, grammatical errors, jargon-heavy prose, spelling errors, plagiarism, SPAM links, or technical errors (broken links, broken JavaScript, slow load times).

## Step Two:  Correct Canonicals
The Canonical of Each page in your Sitemap must point to its URL.  

I had several **canonical-related** issues with my site and did not know this fact until January.

The Jinja templates of my Pelican theme generated two canonicals per site.

```html
  <meta name="HandheldFriendly" content="True" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="referrer" content="origin" />
  <meta name="generator" content="Pelican" />
  <link href="https://john.soban.ski/" rel="canonical" />

  <!-- Feed -->
        <link href="https://john.soban.ski/feeds/all.atom.xml" type="application/atom+xml" rel="alternate" title="John Sobanski Full Atom Feed" />
          <link href="https://john.soban.ski/feeds/data-science.atom.xml" type="application/atom+xml" rel="alternate" title="John Sobanski Categories Atom Feed" />

  <link href="https://john.soban.ski/theme/css/style.css" type="text/css" rel="stylesheet" />

  <!-- Code highlight color scheme -->
      <link href="https://john.soban.ski/theme/css/code_blocks/monokai.css" rel="stylesheet">



  <link href="https://john.soban.ski/thoreau-vs-unabomber.html" rel="canonical" />
```

The Jinja template hardcodes the **canonical** tag into [base.html](https://github.com/arulrajnet/attila/blob/1e0a56e0d86c0573c584fd56cd26c43cd093b396/templates/base.html#L24).

```jinja2
<!DOCTYPE html>
<html lang="{{ DEFAULT_LANG }}">

<head>
  {% block head %}
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />

  <meta name="HandheldFriendly" content="True" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="referrer" content="origin" />
  <meta name="generator" content="Pelican" />
  <link href="{{ SITEURL }}/" rel="canonical" />
```

The [article.html](https://github.com/arulrajnet/attila/blob/1e0a56e0d86c0573c584fd56cd26c43cd093b396/templates/article.html#L32) template extendes [base.html](https://github.com/arulrajnet/attila/blob/1e0a56e0d86c0573c584fd56cd26c43cd093b396/templates/base.html#L24) and included another **canonical** line.

```jinja2
{% extends "base.html" %}
{% block title %}{{ article.title }}{% endblock %}

...

{% block head %}
  {{ super() }}

  <link href="{{ SITEURL }}/{{ article.url }}" rel="canonical" />
```

I updated my version of Attila and this fixed the issue.

The newer version of my Pelican theme includes a bug that generates the wrong canonical.

The Jinja template, for example, incorrectly hard codes the canonical for **authors.html**.

The template sets the canonical to **authors**, and not **authors.html** which results in a 404.

The search engine penalized my site for setting a canonical to a dead (404) page.

```jinja2
{% block canonical_url %}<link href="{{ SITEURL }}/authors" rel="canonical" />{% endblock canonical_url %}
```

I fixed this issue myself and created a Pull Request (PR).  

Arulrajnet merged the [fix into the code](https://github.com/arulrajnet/attila/commit/871b9bcd3ac16c990a7017d503c55a59af219e28).

The new version uses  **AUTHORS_SAVE_AS** for the canonical address.

```jinja2
{% block canonical_url %}<link href="{{ SITEURL }}/{{ AUTHORS_SAVE_AS }}" rel="canonical" />{% endblock canonical_url %}
```

In summary, look at each page and verify that each page points to the correct canonical.

If you use Jinja2 templates to generate your static pages, verify the logic of each template.

## Step Three:  Remove Redirects
On January 15th, 2023 I received a **Page indexing issue detected** alert from the Google Search Console Team.

![Google Sitemap Page Indexing Issue Detected]({static}/images/Seo_Checklist/05_Page_Indexing.png)

I use the [Pelican](https://getpelican.com/) static site generator with the [Attila](https://github.com/arulrajnet/attila) theme.

This tech stack creates a page for each of my site's [categories]({category}data-science) and [tags]({tag}howto).

I kept the configuration from the [default pelicanconf.py](https://github.com/arulrajnet/attila-demo/blob/78dd45d7189adf611d6248d8f440db5b244a211d/pelicanconf.py#L64), which sets the URL for each category to the following:

```jinja2
CATEGORY_URL = 'category/{slug}'
```

The Jinja2 template uses **CATEGORY_URL** to set the canonical.  The canonical, therefore, leaves off the trailing slash since **CATEGORY_URL** leaves off the trailing slash.

I, for example, have categories **coins**, **howto**, **ietf** and **data-science**.

My template renders the following pages:

```bash
https://example.com/category/coins
https://example.com/category/howto
https://example.com/category/ietf
https://example.com/category/data-science
```

Each one of these canonical references redirects to a URL **with** a trailing slash.

For example:

```bash
https://example.com/category/coins
```

Redirects to:

```bash
https://example.com/category/coins/
```

I host my site on S3.  

S3 returns a **302** redirect and not a **301** for these **no-trailing-slash** to **trailing-slash** redirects.

A **302** describes a **temporary** move, so the search engine will not update its index.  Each time the search engine indexes my site, it will see a **302**, and penalize my site.

To fix this issue, I moved my categories to new locations:

```bash
https://john.soban.ski/cat/coins.html
https://john.soban.ski/cat/howto.html
https://john.soban.ski/cat/ietf.html
https://john.soban.ski/cat/data-science
```

I then configured S3 to redirect (with 301) to these pages with the following logic:

```json

[
    {
        "Condition": {
            "KeyPrefixEquals": "category/data-science"
        },
        "Redirect": {
            "HostName": "john.soban.ski",
            "Protocol": "https",
            "ReplaceKeyWith": "cat/data-science.html"
        }
    },
    {
        "Condition": {
            "KeyPrefixEquals": "category/coins"
        },
        "Redirect": {
            "HostName": "john.soban.ski",
            "Protocol": "https",
            "ReplaceKeyWith": "cat/coins.html"
        }
    },
    {
        "Condition": {
            "KeyPrefixEquals": "category/ietf"
        },
        "Redirect": {
            "HostName": "john.soban.ski",
            "Protocol": "https",
            "ReplaceKeyWith": "cat/ietf.html"
        }
    },
    {
        "Condition": {
            "KeyPrefixEquals": "category/howto"
        },
        "Redirect": {
            "HostName": "john.soban.ski",
            "Protocol": "https",
            "ReplaceKeyWith": "cat/howto.html"
        }
    }
]
```

In summary, do not point **canonicals** to any page that will redirect, this includes pages with/ without trailing slashes.

Also, replace any **302** redirects with **301** redirects, which instruct the search engine of a permanent move.

## Step Four:  No Boken Content
Do not link to any dead pages or pictures in your blog posts.

AHREFS identified three cases where I linked to dead internal content.

![Bad internal links]({static}/images/Seo_Checklist/06_Bad_Internal.png)

I had incorrect markdown that generated faulty links.

![Dead internal links]({static}/images/Seo_Checklist/07_Dead_Internal.png)

I [fixed the Markdown errors](https://github.com/hatdropper1977/john.soban.ski/commit/ba039fb3fd5cfdabec94f25cec30b12e673d099e) and published my site.

## Step Five:  Link Love
The search engine audits surprised me.  I did not realize that linking to dead external sites lowers my site quality.

![Bad external Links]({static}/images/Seo_Checklist/08_Bad_External.png)

In addition, the search engines will penalize my site if I link to external pages with redirects.

The Opendaylight homepage decided to kill a few pages, which lowered my score.

They removed (useful) links to On-Demand Service Delivery, Network Function Virtualization, Network Resource Optimization, and others.

Oracle decided to remove my Ravello blog, which captured a Software Defined Networking (SDN) project I executed in 2015.

I decided to link these dead sites to [archive.org](https://archive.org/).

In terms of redirects, I have pages from 2016 on my site that pre-date the mandatory **https** requirement.  I needed to update links to open-source projects that used vanilla **http** in 2016.

## Step Six:  Multimedia Diet
S3 and Cloudfront provide a fat pipe to the Internet.

Despite this, the AHREF and Bing audits encourage me to reduce multimedia files (pictures) to under 100KB each.

I obliged, and this increased the quality of my site in the eyes of the search engines.

![Pic Reduction]({static}/images/Seo_Checklist/09_Pic_Reduce.png)

## Step Seven:  To The Point
AHREF and Bing suggest that I reduce each title to under 60 characters.

![Title too long]({static}/images/Seo_Checklist/10_Long_Title.png)

I appreciate the minimalist and focused communication approach.

I [reduced the title lengths](https://github.com/hatdropper1977/john.soban.ski/commit/1c4d915be85b3be055af5c7a6a7d7f9382773102) of my blog posts.

For example:

```html
Discrete Event Simulation (DES) of an Adaptive Forward Error Correction (AFEC) scheme for the Ka band
```

Becomes:

```html
Adaptive Forward Error Correction (AFEC) for the Ka band
```

## Step Eight:  Fix Your Script
I did not pay attention to the JavaScript that Pelican generates.

I had broken JavaScript that prevented Disqus from loading.

![Dead JavaScript]({static}/images/Seo_Checklist/11_Bad_Java.png)

I opened an [issue on the broken JavaScript](https://github.com/arulrajnet/attila/issues/81) with my template developer.

I managed to fix the issue with a link to [Highlight.js](https://highlightjs.org/).

```html
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
```

Arulrajnet accepted my pull request.

## Step Nine:  Remove Refs
Google suggests that the webmaster indicate which outgoing link [includes a referral](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links).

```html
<a rel="sponsored" href="https://cheese.example.com/Appenzeller_cheese">Appenzeller</a>
```

I decided to remove all of my referral link since I did not have too many.

## Step Ten:  Happy H2
AHREF and Bing both suggest that I remove multiple H1 tags.

My Pelican Template renders each title with an H1.

I needed to go to each of my pages and replace single hashmarks with double hash marks in each of my [raw markdown](https://github.com/hatdropper1977/john.soban.ski/commit/6717c0f2ae4d8cbdec721dc093c79fa9b363d552).

I missed one or two by hand, and the next site audit/ scan alerted me to my error.

## Step Eleven:  Noindex Thin Content
Most Pelican templates render different navigation pages for Categories and Tags.

![Example Tags Page]({static}/images/Seo_Checklist/12_Tags_Page.png)

This approach obviates the need for a Database and obviates the need for a web application.

Webmasters emulate a database approach with Static content.

These pages, however, yield **Thin Content**.  Each tag page, for example, does not provide any new or useful information.

I have dozens of tags, and the auto-generated tag pages bring my site quality down.

To combat this, I added a **noindex** to each of my auto-generated tags.

I edited the Pelican template to add this meta-tag.

```jinja2
{% block canonical_url %}
    {% if NOINDEX_THIN_CONTENT %}
  <meta name="robots" content="noindex">
    {% else %}
  <link href="{{ SITEURL }}/archives.html" rel="canonical" />
    {% endif %}
{% endblock canonical_url %}
``` 

This tag instructs the search engine to ignore the page.

## Conclusion
I recommend that you use AHREFS or Bing Search Tools to audit your site.

Even static sites require annual housekeeping to keep the search engines happy.

Please use the following checklist to audit your site.

1.  A Deliberate Sitemap
2.  Correct Canonicals
3.  Remove Redirects
4.  No Boken Content
5.  Link Love
6.  Multimedia Diet
7.  To The Point
8.  Fix Your Script
9.  Remove Refs
10.  Happy H2
11.  Noindex Thin Content
