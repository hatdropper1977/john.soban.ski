Title: How to enable HTTPS with Naked Domain and Protocol Redirects on your S3 Website (Part Two)
Date: 2018-06-23 10:26
Author: john-sobanski
Category: HOWTO
Tags: AWS, HOWTO, IAM, S3, Certificate Manager, CloudFront
Slug: how-to-configure-s3-websites-to-use-https-part-2
Status: published

Part Two of this [HOWTO]({category}howto) demonstrates how to secure your [S3](https://aws.amazon.com/s3/) hosted website with  [HTTPS](https://en.wikipedia.org/wiki/HTTPS).  If you haven't completed [part one]({filename}/how-to-configure-s3-websites-to-use-https-part-1.md) yet, be sure to click [here]({filename}/how-to-configure-s3-websites-to-use-https-part-1.md).

Once you complete this HOWTO, you will have a secure website, that Google approves, as seen in the screengrab below:

![Qualys Results]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/000_qualys.png)

HTTPS and Naked Domain redirection will increase your security, reduce customer bounce rate and increase SEO.

## Outline

In [part one]({filename}/how-to-configure-s3-websites-to-use-https-part-1.md) of this tutorial, we executed the following:

  1. Configure DNS (Route 53)
  2. Create Log, WWW and Naked Domain S3 Buckets
  3. Configure S3 Bucket Naked Domain and Protocol Redirection
  4. Request a Certificate

In part two of this tutorial (this post), we will:

  5.  Upload a web page
  6.  Create CloudFront distribution
  7.  Point DNS (Route 53) to CloudFront distribution

As a reminder, to show the process in action, I demonstrate how to set up HTTPS with Redirection on S3 using a real world site, [***www.siliconebeltway.com***](https://www.siliconebeltway.com).  In this demonstration, you would simply replace ***siliconebeltway*** with your website's domain name.
  
As described in [part one]({filename}/how-to-configure-s3-websites-to-use-https-part-1.md), the following diagram depicts our desired Architecture:

![Route 53 Cloudfront S3]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/000_Route_53_Cloudfront_S3.png)

## Upload a web page
I will use a simple ***hello world*** web page to make sure everything works.  At this point, you could upload an existing static website.  In this example, I assume your site uses ***index.html*** for the main page's name.

First, go to the S3 console:
 
![Find Route 53 Console]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/02_Find_Route_53_Console.png)

Then, select the bucket that will serve the web pages, the bucket that starts with ***www***.  I select ***www.siliconebeltway.com***:


![Select S3 Bucket]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/45_Select_S3_Bucket.png)

On the "Overview" tab, selct "+ Upload:"

![Select Web Page]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/46_Select_Web_Page.png)

Click the "Add Files" box.  I created a document on my Desktop named ***index.html***.  I entered the text "Coming Soon!" into the file and saved it.  I will upload this ***index.html*** file to test the website (once we're finished configuring it).

![Select Add Files]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/47_Select_Add_Files.png)

Click next.  Again, for purposes of this demo, ensure that you named the main page ***index.html***.

![Select Next]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/48_Select_Next.png)

Again, on the 'Upload' screen, ensure that you ***grant public access***.

![Grant Public Access]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/49_Grant_Public_Access.png)

Now that you have a test file uploaded, see if AWS completed your certificate validation.

## Create CloudFront distribution
S3 does not natively support HTTPS for websites, so we will use CloudFront.  We requested a certificate from ACM to install into CloudFront.  Check to see if ACM completed issuing the certificate.  It takes about a half of an hour to complete.  Go to the Certificate Manager console, click your website, and wait until you see the following success page.  Ensure that both the ***naked*** and ***www*** domain completed.

![Certificate Validation Complete]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/50_Certificate_Validation_Complete.png)

If it completed, open the CloudFront console from the main AWS console.

![Open Cloudfront Console]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/51_Open_Cloudfront_Console.png)

Select "Create Distribution."

![Select Create Distribution]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/52_Select_Create_Distribution.png)

Select "Get Started" under "Web Delivery."

![Select HTTP Delivery]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/53_Select_HTTP_Delivery.png)

We will first create the ***www*** CloudFront distribution.  If you look at the architecture diagram at the start at this blog post, you see we enable protocol (HTTP to HTTPS) redirection for the ***www*** bucket at the CloudFront distribution.  Under "Origin Domain Name," type in the URL for your S3 bucket ***website***.  You will see an auto-complete option for the S3 bucket URL, but not the S3 bucket ***website*** URL.  I, for example, see an auto-complete option for ***www.siliconebeltway.com.s3.amazonaws.com***, but I do not want this.  Instead, I type in ***www.siliconebeltway.com.s3-website-us-east-1.amazonaws.com***.  Notice, the correct "Origin Domain Name" includes ***s3-website-us-east-1***.  Ensure you type in the correct URL for the ***website*** and not the bucket, in that this allows CloudFront to load the default page without needing to set a default object.  The console will auto-populate the "Orgin-ID" bucket with ***S3-Website-www.siliconebeltway.com.s3-website-us-east-1.amazonaws.com
*** (contrast this the bucket URL of ***S3-www.siliconebeltway.com***).  Once you double check the field, be sure to enable HTTP to HTTPS redirection by selecting that radio button.  I highlight the appropriate fields in green below.

![Configure WWW Distribution And Protocol Redirection ]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/54_Configure_WWW_Distribution_And_Protocol_Redirection.png)

In order to point Route 53 to your cloudfront distribution, you must enter a ***CNAME*** under 'Distribution Settings.'  Enter ***www.siliconebeltway.com***.  You also must select the ACM generated SSL/TLS certificate for your website.  Click 'Custom SSL Certificate' and then select the certificate for your domain.

![Set CNAME and TLS Certificate]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/55_Set_CNAME_and_TLS_Certificate.png)

Now enable logging.  Turn on logs and select the log bucket you created.  These logs will show you who visited your site and their location.  I show you one method to [view S3 logs]({filename}/use-s3stat-to-troubleshoot-your-migration-from-wordpress-to-s3.md) in [this blog post]({filename}/use-s3stat-to-troubleshoot-your-migration-from-wordpress-to-s3.md).

![Enable Logging]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/56_Enable_Logging.png)

Once you click through all the confirmation menues, you will get back to the CloudFront console.  You will see the progress of the ***www*** CloudFront distribution deployment.  Now, create a distribution for the ***naked*** domain.  Click "Create Domain."

![View Progress And Create Naked Domain Distribution]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/57_View_Progress_And_Create_Naked_Domain_Distribution.png)

Again, select the ***naked*** S3 bucket under 'Origin Domain Name.'  Once more, ignore the auto-complete option of the S3 bucket URL  (In my case, ***siliconebeltway.com.s3.amazonaws.com***) and instead type in the S3 bucket ***website*** URL.  I, for example, type in ***siliconebeltway.com.s3-website-us-east-1.amazonaws.com
***.  CloudFront will pre-populate "Origin-ID" with ***S3-Website-siliconebeltway.com.s3-website-us-east-1.amazonaws.com
*** (if it does not, type it in by hand).  Under 'Default Cache Behavior Setting --> Viewer Protocol Policy' select 'HTTP and HTTPS.'  If you look at the Architecture diagram at the beginning of this post, you will see we execute HTTP to HTTPS protocol redirection at the ***naked*** S3 bucket.  For that reason, we do not need to redirect here, since that would result in an unecessary redirection.

![Select Bucket And Allow HTTP And HTTPS]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/58_Select_Bucket_And_Allow_HTTP_And_HTTPS.png)

Once more, set the CNAME (i.e. ***siliconebeltway.com***) and select the SSL/TLS certificate for your ***naked*** domain name.

![Set CNAME And TLS Certificate]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/59_Set_CNAME_And_TLS_Certificate.png)

Now enable logging, and point to your log bucket.

![Enable Logging]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/60_Enable_Logging.png)

Click through all the 'Save' menus and you will be taken back to the main CloudFront console.  Wait until the deployment completes.  Once it does, you will see the following success screen.

![Deployment Complete]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/61_Deployment_Complete.png)

## Point DNS (Route 53) to CloudFront distribution
From the main AWS console, open Route 53.

![Find Route 53 Console]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/02_Find_Route_53_Console.png)

Click on your hosted zone and then click "Create Record Set."

For "Name" enter ***www***.  Select "A - IPv4" address under Type.  Select "Yes" for Alias, and then select your ***www*** CloudFront distribution.  I select ***www.siliconebeltway.com***.  

![Point DNS To WWW Distribution  ]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/62_Point_DNS_To_WWW_Distribution.png)

Route 53 may bark.  If you waited for the distribution deployment to complete, then you can ignore the warning and click save.

![Review Alias]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/63_Review_Alias.png)

Be sure to repeat the process and create a record for your ***naked*** domain (just leave the 'Name' field blank) and be sure to point the Alias to your ***naked*** CloudFront distribution.  

Once Route 53 finishes the updates (five minutes or so), you can go to your website.  If you go to any combination of ***naked*** or ***www*** domain with or without HTTPS the system will redirect to the ***www*** domain with HTTPS.

If you click the secure icon (which goes away in July 2018), you will see that Google trusts the site!

![Success]({filename}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_2/64_Success.png)

Please leave a comment below, and check out some of my other [AWS tips and tricks]({tag}aws).  You may also want to [view the access logs of your website]({filename}/use-s3stat-to-troubleshoot-your-migration-from-wordpress-to-s3.md).
