Title: S3 HTTPS Sites w/ Naked Domain & Protocol Redirects (Part 1)
Date: 2018-05-12 10:26
Author: john-sobanski
Category: HOWTO
Tags: AWS, HOWTO, IAM, S3, Certificate Manager
Slug: how-to-configure-s3-websites-to-use-https-part-1
Status: published

This [HOWTO]({category}howto) demonstrates how to secure your [Simple Storage Service (S3)](https://aws.amazon.com/s3/) hosted website via  [Hypertext Transfer Protocol Secure (HTTPS)](https://en.wikipedia.org/wiki/HTTPS).  While the S3 [Representational State Transfer (REST)](https://en.wikipedia.org/wiki/Representational_state_transfer) enpoint supports native HTTPS, an S3 bucket configured to serve web pages [does not](https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteEndpoints.html#WebsiteRestEndpointDiff).  In addition to demonstrating [how to]({category}howto) enable HTTPS, this blog demonstrates how to configure both [protocol](https://moz.com/community/q/best-practice-to-redirect-http-to-https) and [***naked*** domain](https://en.wikipedia.org/wiki/URL_normalization) redirection.  Protocol redirection ensures security, and ***naked*** domain redirection (e.g. ***yoursite.com*** to ***www.yoursite.com***) improves [Search Engine Optimization](https://www.solidstratagems.com/www-vs-non-www-url/).

## Why use HTTPS?
Starting July 2018, Google will mark all vanilla HTTP sites as "[not secure](https://security.googleblog.com/2018/02/a-secure-web-is-here-to-stay.html)."  If you do not enable HTTPS, visitors will see a garish "Not Secure" to the left of your website name.  That scarlet letter could possibly cause potential readers or customers to immediately close their tab (***bounce***).

![Not Secure]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/00_Not_Secure.png)

In addition, most sites rely on Google to drive traffic.  Google [includes the presence of HTTPS](https://security.googleblog.com/2014/08/https-as-ranking-signal_6.html) in their secret algorithm that calculates your site's page rank.  In other words, enabling HTTPS will boost your score, and as a result will drive more readers and customers to your site.

## Outline

In part one (this post) of this tutorial, we will execute the following:

  1. Configure DNS (Route 53)
  2. Create Log, WWW and Naked Domain S3 Buckets
  3. Configure S3 Bucket Naked Domain and Protocol Redirection
  4. Request a Certificate

In [part two of this tutorial]({filename}/how-to-configure-s3-websites-to-use-https-part-2.md), we will:

  5.  Upload a web page
  6.  Create CloudFront distribution
  7.  Point DNS (Route 53) to CloudFront distribution

To show the process in action, I demonstrate how to set up HTTPS with Redirection on S3 using a real world site, [***www.siliconebeltway.com***](https://www.siliconebeltway.com).  In this demonstration, you would simply replace ***siliconebeltway*** with your website's domain name.
  
At the end of this demonstration, your architecture will look like the following diagram:
 
![Route 53 Cloudfront S3]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/000_Route_53_Cloudfront_S3.png)

As shown in the diagram above, you will create a CloudFront distribution and S3 bucket pair for both your ***naked*** domain (e.g. [siliconebeltway.com](https://www.siliconebeltway.com)) and your ***www*** domain (e.g. [www.siliconebeltway.com](https://www.siliconebeltway.com)).  Route 53 will point users to either the ***naked*** or ***www*** CloudFront distribution depending on which one they request.  The ***naked*** CloudFront distribution sends the session to the ***naked*** S3 bucket, which immediately redirects the session to the authoritative ***www*** bucket.  If the client uses the HTTP protocol, the ***naked*** S3 bucket redirects them to use the HTTPS protocol.  Alternatively, if the user attempts to go to [http://www.siliconebeltway.com](http://www.siliconebeltway.com) (e.g. including ***www***) via HTTP, the protocol redirection occurs at the ***www*** CloudFront distribution.  It's a little confusing, but if you follow the green arrows on the diagram, you'll see all requests are redirected to ***www.siliconebeltway.com*** using ***HTTPS***.

## Configure DNS
In order to use HTTPS, you must have a [Secure Socket Layer (SSL)/ Transport Layer Security (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security) certificate installed on your website.  In order for Chrome (and all browsers, for that matter) to trust your certificate, it must be signed by a trusted [Certificate Authority](https://en.wikipedia.org/wiki/Certificate_authority).  Normally, this process is very tedious and frustrating.  If, however, you configure AWS to be the [Start of Authority (SOA)](https://en.wikipedia.org/wiki/SOA_record) (e.g. they manage DNS) for your website's domain name, life becomes very, very easy.  If [Route 53](https://aws.amazon.com/route53/) manages your domain name, then you can use [Certificate Manager](https://aws.amazon.com/certificate-manager/) to generate a certificate and install it on your website.  I strongly recommend, therefore, that you use Route 53 to provide DNS for your website.

If you already use Route 53 for your domain name, you can skip this section.  I registered [siliconebeltway.com](https://www.siliconebeltway.com) with [GoDaddy](https://www.godaddy.com/), so I will now show you how to point GoDaddy to use Route 53.

First, find and select the Route 53 Console.

![Find Route 53 Console]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/02_Find_Route_53_Console.png)

Click through the splash page and click "Hosted Zones." 

![Click Hosted Zones]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/03_Click_Hosted_Zones.png)

Click "Create Hosted Zone."

![Click Create Hosted Zone]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/04_Click_Create_Hosted_Zone.png)

On the right hand box, enter your site's Domain Name and an optional comment.  I entered "siliconebeltway.com" as the Domain Name.  Be sure to select "Public Hosted Zone"

![Create A Hosted Zone]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/05_Create_A_Hosted_Zone.png)

Find the AWS name servers associated with your domain.  I outlined mine in green.  Write down these name servers, since you will need to enter them in GoDaddy.  My name servers may be different than yours.

![Find The Name Servers]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/06_Find_The_Name_Servers.png)

Now, log into GoDaddy, and select the DNS button for your domain.  If you use a different registrar, then the process may be a little different.  The idea is to point your domain to the AWS name servers you copied down in the step above.

![Point Go Daddy To Amazon]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/07_Point_Go_Daddy_To_Amazon.png)

Under the Nameservers box for your domain, you will see a button labeled "Change."  Click that button.

![DNS Splash ]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/08_DNS_Splash.png)

Now enter the four name servers you copied from AWS.

![Add AWS Name Servers]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/09_Add_AWS_Name_Servers.png)

Oops!  GoDaddy does not like the trailing "dot."  Delete the Dots and click save.

![Fix Error ]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/10_Fix_Error.png)

It may take GoDaddy (or your provider) a few minutes to update your domain's name server.

## Create Log, WWW and Naked Domain S3 Buckets

### Create the Logs Bucket
Find and select the S3 console.

![Find S3 Console]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/11_Find_S3_Console.png)

Click "+ Create Bucket"

![Click Create Bucket]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/12_Click_Create_Bucket.png)

We first create the ***logs*** bucket.  With a logs bucket, you will be able to track who hits your website, to include their location, IP address, etc.  I name my logs bucket "siliconebeltway-logs."

![Create Bucket ]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/13_Create_Bucket.png)

Click next to skip the "Versioning/ Tags/ Server access logging" screen.

![Create Bucket Click Next]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/14_Create_Bucket_Click_Next.png)

Since this is your logs bucket, you will give S3 permission to use it.

![Allow Log Delivery Access]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/15_Allow_Log_Delivery_Access.png)

Review and click "Create Bucket."

![Click Create Bucket]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/16_Click_Create_Bucket.png)

### Create the WWW bucket
Go back to the S3 console and click "+ Create" bucket once more.  On the first screen, enter your domain name as the bucket name.  Be sure to include ***www***.  I name my bucket ***www.siliconebeltway.com***.  Click "Next."

![Create WWW Bucket]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/17_Create_WWW_Bucket.png)

On the second screen, click "Server Access Logging."

![Configure Log Target For WWW Bucket  ]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/18_Configure_Log_Target_For_WWW_Bucket.png)

Click "Enable Logging" and enter the name of the ***logs*** bucket you just created.  I named my ***logs*** bucket "siliconebeltway-logs."  Save and move to step three.

![Enable Logging WWW]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/19_Enable_Logging_WWW.png)

Grant public read access to this bucket (since it is for a public website).

![Grant Public Access]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/20_Grant_Public_Access.png)

Click through to the Review tab and then create the bucket.

### Create Naked Domain Bucket.
On the S3 console, click "+ Create Bucket" once more.

Enter the name of your ***naked*** domain (without the ***www***).  I name my bucket "siliconebeltway.com."  Click next.

![Name Naked Domain Bucket]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/21_Name_Naked_Domain_Bucket.png)

On step two, click "Server Access Logging," enable logging, and then enter the name of your log bucket.  Save and move to step 3.

![Enable Logging For Naked Domain Logging ]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/22_Enable_Logging_For_Naked_Domain_Logging.png)

Grant the public read access to the bucket.

![Grant Public Access For Naked Domain Bucket ]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/23_Grant_Public_Access_For_Naked_Domain_Bucket.png)

Click through to step four and create the bucket.

## Configure S3 Bucket Naked Domain and Protocol Redirection

### Configure your WWW bucket to host a website
At the S3 console, select your ***www*** bucket.

![Select WWW Bucket]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/24_Select_WWW_Bucket.png)

Click the "Properties" tab, and then "Static website hosting."

![Select Static Hosting]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/25_Select_Static_Hosting.png)

The "Static website hosting" box expands.  Click "Use this bucket to host a website" and then enter the name of your website's home page.  If you are unsure, just enter ***index.html*** for now.  Click "Save."

![Enable Website Hosting]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/26_Enable_Website_Hosting.png)

Now click the "Permissions" tab.  You will see the bucket policy editor.

![Open Policy Editor]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/27_Open_Policy_Editor.png)

Enter the following policy into the editor.  Be sure to change ***www.siliconebeltway.com*** to the name of your website.  Include the ***www***!

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::www.siliconebeltway.com/*"
        }
    ]
}
```

Click "Save."

![Edit Policy]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/28_Edit_Policy.png)

S3 barks.  You can ignore it.  You want the public to ***GetObject***, i.e. see your website.

![Confirm Edit]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/29_Confirm_Edit.png)

Save your changes.

### Configure your ***naked*** domain bucket to redirect
At the S3 console, select your ***naked*** domain bucket, the one without the ***www***.

![Select Naked Domain Bucket]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/30_Select_Naked_Domain_Bucket.png)

Click "Properties" and then "Static website hosting."

![Select Configure Static Website Hosting]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/31_Select_Configure_Static_Website_Hosting.png)

This bucket exists for two reasons:  (1) redirect ***naked*** domain requests to the ***www*** bucket and (2) redirect HTTP to HTTPS.  This bucket will not host any web pages.  Click "Redirect requests" and enter the target bucket (***www.siliconebeltway.com***) and under protocol, type ***https***.

![Configure Naked Redirection]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/32_Configure_Naked_Redirection.png)

Save all of your changes.

##  Request a Certificate
At the main AWS console screen, search for and select "Certificate Manager."

![Open Certificate Manager]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/33_Open_Certificate_Manager.png)

Click through the splash screen and select "Request a Certificate."

![Click Request Certificate]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/34_Click_Request_Certificate.png)

Select "Request Public Certificate" and click "Request a certificate" once more.

![Select Public Certificate]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/35_Select_Public_Certificate.png)

In ***step one*** you must enter both the ***naked*** and ***www*** domain names.  This ensures that both CloudFront distributions (which you will set up in [part two of this tutorial]({filename}/how-to-configure-s3-websites-to-use-https-part-2.md)) can use the certificate.  

![Add WWW And Naked Domain Names]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/36_Add_WWW_And_Naked_Domain_Names.png)

***Step 2***, select "DNS validation" and then "Review."

![Select DNS Validation]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/37_Select_DNS_Validation.png)

Confirm that the "Domain name" section includes both the ***naked*** and ***www*** names, and that you will validate using DNS.  Click confirm and request.

![Review Config]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/38_Review_Config.png)

The screen reads "pending validation" but nothing will happen unless you perform the next few steps.  First, click "Continue."

![Select Continue]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/39_Select_Continue.png)

Now, expand the triangle for your domain name.

![Expand Triangle]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/40_Expand_Triangle.png)

For each of the domain names (***naked*** and ***www***) you must click "Create record in Route 53."  This proves to the AWS Certificate Manager that you do, in fact, own the domain name and are therefore entitled to a certificate for that domain name.

![Create Record In Route 53]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/41_Create_Record_In_Route_53.png)

You will see a DNS record to prove that you own your site name.  It will look like a bunch of gibberish.  Click create.

![View Validation Record]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/42_View_Validation_Record.png)

ACM will show a green "Success" box.  Once you see this, repeat the process for the ***naked*** domain (expand the triangle right under the success box).  It will take at least thirty (30) minutes to complete.  Now would be a good time to teak a break.

![Success Splash]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/43_Success_Splash.png)

If you're curious, you can look at Route 53, where you will see the two validation records that ACM configured.

![Validation Records In Route 53]({static}/images/How_To_Configure_S3_Websites_To_Use_Https_Part_1/44_Validation_Records_In_Route_53.png)

Again, you will need to wait at least a half of an hour before you can use your certificates.  In the meantime, head over to [part two of this tutorial]({filename}/how-to-configure-s3-websites-to-use-https-part-2.md), where we will:

  1.  Upload a web page
  2.  Create CloudFront distribution
  3.  Point DNS (Route 53) to CloudFront distribution
