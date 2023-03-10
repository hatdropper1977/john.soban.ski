Title: Use s3stat To Troubleshoot Your Migration from Wordpress To S3
Date: 2018-01-17 20:56
Author: john-sobanski
Category: HOWTO
Tags: AWS
Slug: use-s3stat-to-troubleshoot-your-migration-from-wordpress-to-s3
Status: published

### Introduction

Last month, I followed the example of [Full Stack Python](https://www.fullstackpython.com/pelican.html) and migrated this blog from [Wordpress](https://wordpress.com/) to Amazon Web Services (AWS) [Simple Storage Service (S3)](https://aws.amazon.com/s3).  The S3 hosting approach gives me the following features:

  -  Global caching via [Cloudfront's](https://aws.amazon.com/cloudfront/) [Content Delivery Network (CDN)](https://en.wikipedia.org/wiki/Content_delivery_network)
  -  [Secure Hypertext Transport Protocol](https://en.wikipedia.org/wiki/HTTPS) via AWS' [certificate manager](https://aws.amazon.com/certificate-manager/)
  -  Configuration management and a public record of website updates and edits via [Git](https://github.com/hatdropper1977/john.sobanski.io)
  -  Quick and easy code highlighting and hyperlinks via [Markdown](https://en.wikipedia.org/wiki/Markdown)
  -  Detailed logs and usage statistics via [Cloudwatch](https://aws.amazon.com/cloudwatch/)
  -  Insanely cheap hosting costs
     -  I accommodate about one hundred and forty (140) hits a day with CDN, DNS, hosting and logging for about three dollars ($3) a month

I configured Cloudwatch to dump the logs to a separate, dedicated log bucket.  Cloudwatch dumps the logs in a raw format, so I need a separate Architecture to parse and analyze the logs.


### Trade
In general, I need a service to ingest the logs, a service to parse/ transform the logs (i.e., create actionable key/value pairs), a service to store the key/value pairs and finally a Graphical User Interface (GUI) to view the logs.

Amazon does not provide a turnkey solution for this user story, so I faced two high level approaches:  

  -  Roll your own
     -  Approach
        -  Deploy and Integrate separate services for ingest, transformation and analysis
     -  Technology
        -  The [Elasticsearch, Logstash and Kibana (ELK)]({filename}/part-1-connect-ec2-to-the-amazon-elasticsearch-service.md) stack, which Elastic renamed to '[Elastic Stack](https://www.elastic.co/webinars/introduction-elk-stack)'
     -  Deployment
        -  You can either deploy the __Elastic stack__ via a combination of [Elastic Compute Cloud (EC2)](https://aws.amazon.com/ec2/) and the Amazon provided [Elasticsearch service](https://aws.amazon.com/elasticsearch-service/) or the Elastic provided [Elastic cloud](https://www.elastic.co/cloud)
     -  Cost
        -  The Amazon approach costs ~$15/month and the cheapest Elastic cloud approach costs [$45/month](https://www.elastic.co/cloud/as-a-service/subscriptions)
     -  Effort
        -  The Amazon approach requires a significant amount of [integration and troubleshooting](https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-aws-integrations.html#es-aws-integrations-s3-lambda-es) whereas the Elastic cloud approach just requires the deployment of a few Logstash filters
  -  Turn key
     -  Approach
        -  Use a __push button__ online service to ingest, parse and analyze the logs
     -  Technology
        -  [Loggly](https://www.loggly.com/docs/s3-ingestion-auto/), [Sumo Logic](https://www.sumologic.com/lp/aws/002/) and [s3stat](https://www.s3stat.com/)
     -  Deployment
        -  All services provide a simple 'push button' deployment (_note:  deployment may require minimal [Identity and Acess Management](https://aws.amazon.com/iam/) configurations_)
     -  Cost
        -  [Sumo Logic](https://www.sumologic.com/pricing/), [s3stat](https://www.s3stat.com/Pricing.aspx) and [Loggly](https://www.loggly.com/plans-and-pricing/) all provide free options
          -  Sumo Logic and Loggly limit retention to seven days for their free tier
          -  [s3stat](https://www.s3stat.com/web-stats/cheap-bastard-plan) offers a very creative pricing model for their free teir, which I discuss below
     -  Effort
          -  All three options require very little effort
         
> __NOTE__:  If you represent any of these companies and would like to update the bullets above, feel free to fork, [edit](https://github.com/hatdropper1977/john.sobanski.io/blob/master/content/use-s3stat-to-troubleshoot-your-migration-from-wordpress-to-s3.md) and create a pull request for this blog post.

### S3STAT
I decided to try s3stat because their [cheap bastard plan](https://www.s3stat.com/web-stats/cheap-bastard-plan) amuses me.  From their website:

> How It Works
>
> 1.  [Sign up for a Free Trial](https://www.s3stat.com/setup/register.aspx) and try out the product (making sure you actually want to use it)
>
> 2.  __Blog about S3STAT__, explaining to the world how awesome the product is, and how generous we are being to give it to a deadbeat like yourself for free.
>
> 3.  Send us an email showing us where to find that blog post.
>
> 4.  Get Hooked Up with a free, unlimited license for S3STAT.

### Test Drive
It took about thirty seconds to connect s3stat to my Cloudfront S3 logs bucket.  s3stat provides both a wizard and web app to help you get started.  Once I logged in, I saw widgets for Daily Traffic, Top Files, Total Traffic, Daily Average and Daily Unique.  s3stat also provides the costs to your AWS account.

![Splash Page]({filename}/images/Use_S3stat_To_Troubleshoot_Your_Migration_From_Wordpress_To_S3/01_Login_Screen.png)


### Troubleshooting
I clicked the other menu items and noticed that my new S3 hosted website threw a lot of error codes.

![Error Codes]({filename}/images/Use_S3stat_To_Troubleshoot_Your_Migration_From_Wordpress_To_S3/02_Error_Codes.png)

I noticed that people still clicked links from my old web page.  I could tell because when I migrated from Wordpress to S3, I took the dates out of the URL.  If a user bookmarked the Wordpress style link (which includes date), they would receive a 404 when they attempted to retrieve it.  I highlighted the stale URLs in red below.  

![Error Pages]({filename}/images/Use_S3stat_To_Troubleshoot_Your_Migration_From_Wordpress_To_S3/03_Error_Pages.png)

When I moved from Wordpress to S3, I submitted a [URL map](https://help.disqus.com/customer/en/portal/articles/912757-url-mapper) to their [migration tool](https://www.disqus.com/admin/discussions/migrate/) to migrate my comments to fit with my site's new URL approach.

I present a snippet of my URL map below.  This map removes the date from the URL and sets the protocol to HTTPS.

```csv
http://freshlex.com/2017/03/13/pass-bootstrap-html-attributes-to-flask-wtforms/, https://www.freshlex.com/pass-bootstrap-html-attributes-to-flask-wtforms.html
http://freshlex.com/2017/04/06/add-timestamp-to-your-python-elasticsearch-dsl-model/, https://www.freshlex.com/add-timestamp-to-your-python-elasticsearch-dsl-model.html
http://freshlex.com/2017/04/29/connect_aws_lambda_to_elasticsearch/, https://www.freshlex.com/connect_aws_lambda_to_elasticsearch.html
http://freshlex.com/2017/05/27/install-rabbitmq-and-minimal-erlang-on-amazon-linux/, https://www.freshlex.com/install-rabbitmq-and-minimal-erlang-on-amazon-linux.html
```

I fix the dead link issue by uploading a copy of the current web page to a file location on S3 that matches the old Wordpress style.  I wrote a script that performs this.  I simply concatenate the contents of my __URL map__ into the script, and the script creates the necessary directory structure to ensure the old Wordpress style links work (for those who bookmarked my old URL).

```bash
#!/bin/bash
cat url_map.csv | while read OLD NEW
do
  DIR=`echo $OLD | cut -f4-7 -d'/'`
  FILE=`echo $NEW | cut -f4 -d'/'`
  mkdir -p $DIR
  cd $DIR
  ln -s ../../../../$FILE index.html
  cd ../../../../
done
```

I upload the new files and directories to S3 and the old URLs now work.  I want to encourage, however, users to use the new links, so I update [robots.txt ](http://www.robotstxt.org/) to exclude any of the old style URLs.  Search engines, therefore, will ignore the old Wordpress style links.

```text
User-agent: *
Disallow: /2016/
Disallow: /2017/
Sitemap: https://www.freshlex.com/freshlex_sitemap.xml
```

I use __s3stat__ to sanity check the error pages and notice that one error returns a weird URL.

![Error Pages]({filename}/images/Use_S3stat_To_Troubleshoot_Your_Migration_From_Wordpress_To_S3/04_Trashed.png)

I attempt to click a stale link (that follows the Wordpress aproach) and of course get a hideous error.

![Bad Link]({filename}/images/Use_S3stat_To_Troubleshoot_Your_Migration_From_Wordpress_To_S3/05_Bad_Link.png)

After some investigation, I notice that I did not include this weird URL in my __URL map__.  It turns out, a user that goes to my site with the new links will see an 'also on Freshlex' callbox from Disqus that points to the old URL.

![Bad Link]({filename}/images/Use_S3stat_To_Troubleshoot_Your_Migration_From_Wordpress_To_S3/06_Also_On_Freshlex.png)

Thanks to s3stat, I identified the root cause of the issue.  I quickly go back to Disqus, and add the weird URL to the migration tool.

![Bad Link]({filename}/images/Use_S3stat_To_Troubleshoot_Your_Migration_From_Wordpress_To_S3/07_Submit_Migration.png)

After the migration tool works its magic, the 'also on' box now points to the correct, new URL.

![Bad Link]({filename}/images/Use_S3stat_To_Troubleshoot_Your_Migration_From_Wordpress_To_S3/08_Works.png)
   
### Conclusion
Thanks again to s3stat for providing an excellent product, as well as hooking me up with a free lifetime subscription thanks to the [cheap bastard plan](https://www.s3stat.com/web-stats/cheap-bastard-plan)!
