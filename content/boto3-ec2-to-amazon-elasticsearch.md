Title: Connect Ubuntu EC2 to Amazon Elasticsearch Service w/ Boto3
Date: 2020-05-31 02:48
Author: john-sobanski
Category: HOWTO
Tags: AWS, Elasticsearch, HOWTO, IAM, Python
Slug: boto3-ec2-to-amazon-elasticsearch
Status: published

In this [HOWTO]({category}howto), I will describe the process to connect an Ubuntu [EC2](https://aws.amazon.com/ec2/) instance to the Amazon Web Services (AWS) provided [Elasticsearch Service](https://aws.amazon.com/elasticsearch-service/) via the [boto3](https://aws.amazon.com/sdk-for-python/) Python library. This blog updates my incredibly popular original post on this topic which describes the process using [boto2]({filename}/part-1-connect-ec2-to-the-amazon-elasticsearch-service.md).  In the spirit of my original post, I once more capture and present the easiest and most direct method to connect an EC2 instance to the AWS ES service. 

![Howto]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/howot1.png)

As before, I present a caveat before we begin. You must trust me that the [Identity and Access Management (IAM)](https://aws.amazon.com/iam/) based security approach that I present below will make your life easy. This approach yields greater flexibility, greater security, greater automation (vs. an IP whitelist approach) and AWS labels it a **best practice**.  The IAM security approach provides a quick, **pull off the band-aid** method that will save you a ton of heartache and debugging down the road.

When I first played with AWS, I found that the IAM role method appeared both **boring** and **complicated** so my mind invented many reasons to avoid diving in.  You may or may not have the same gut reaction when you read this blog post.  I just ask twenty seconds of courage, to read my IAM instructions (which I spent hours simplifying), copy and paste some JSON and then soldier on! 

You may be tempted to avoid the IAM role approach for access and instead (1) Copy and Paste your AWS credentials or (2) Use an IP Whitelisti.  These approaches, however, do not provide the same level of security or flexibility.  The IP whitelist approach, for example may appear to be simple, but outside of toy integrations it becomes furiously difficult to track and you will waste time.

In summary, you will:  

  1. Discover your account ID
  2. Deploy the AWS Elasticsearch Service 
  3. Create an IAM Role, IAM Policy and configure a Trust Relationship  
  4. Connect an EC2 Instance via Boto3

> Note: Please ensure that you know how to [SSH into an EC2 instance.](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstances.html)

##1.  Find your Amazon Account ID
You will use your Account ID to configure security on the Elasticsearch Service.  To find your account ID, simply click **Support** in the AWS console and then write down your Account ID, or copy and paste into a text document.

![Account ID]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/00_Account_ID.png)


##2. Deploy an AWS Elasticsearch Instance

Amazon makes Elasticsearch deployment a breeze.  Type **Elasticsearch** into the AWS console search bar and then click it:

![Find Elasticsearch]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/01_Find_Elasticsearch.png)

Then click **Create a new domain**.

![Create New Domain]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/02_Create_New_Domain.png)

Select the desired deployment type and Elasticsearch version.

![Select Deployment Type]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/03_Select_Deployment_Type.png)

Name your domain something super-creative, like **test-domain** and select your instance type.  I select the cheapest option here, so I can save my money and invest in WATA graded NES games.

![Name your Elasticsearch Service]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/04_Name_Your_Elasticsearch_Service.png)

Click Next until you arrive at **Step 3:  Configure access and security**.

You can choose, if you prefer, to deploy your service into a [Virtual Private Cloud (VPC)](https://aws.amazon.com/vpc/).  Since we will require all access to use **signed, encrypted** requests, the public Internet will suffice.  Bots and bad actors can hit our API, but they will not be able to proceed without the proper crpytographic credentials.  If you plan to operationalize this service, then you may want to consider using a VPC.  A VPC shuts down all external paths to your service.  For now, we will rely on the security of enforcing signed requests.

![Network Config]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/05_Network_Config.png)

Scroll down to **Domain access policy** and select **Custom access policy**.

Do you remember your **Account ID**?  Paste it into the middle box as shown.  In the first box, select **IAM ARN**, in the second box, paste in your **Account ID** and then in the third box select **Allow**.  Be sure to select **Encryption**.

![Domain Access Policy]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/06_Domain_Access_Policy.png)

Click next until you see the prompt to deploy the service and then deploy the service.

After about ten minutes you will see the Elasticsearch endpoint, ready for use.

![Elasticsearch Endpoint]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/07_Elasticsearch_Endpoint.png)

If you click the endpoint, you will receive the following error:

```bash
{"Message":"User: anonymous is not authorized to perform: es:ESHttpGet"}
```

If you want to use the service, you must sign and encrypt the **GET** request.  I present the easiest and most direct way to do that below.

##3. Create an IAM Role, Policy and Trust Relationship

###3.1 Create an IAM Policy

Type "IAM" into the AWS console search bar and then click it.

![IAM Menu]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/08_Find_IAM.png)

Select "Policies."

![Select Policy]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/09_Create_Policy.png)

Select **JSON** and paste in the following JSON:

```JSON
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "es:ESHttpDelete",
                "es:ESHttpGet",
                "es:ESHttpHead",
                "es:ESHttpPost",
                "es:ESHttpPut"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```

![Create Policy]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/10_JSON_Policy.png)

Click **Review policy**, name your policy **Can\_CRUD\_Elasticsearch** and then click **Create policy**

![Validate]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/11_Save_Policy.png)

###3.2 Create an IAM Role with attached Policy
On the Dashboard, click "Roles."

![Roles]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/12_Click_Roles.png)

Under **Create Role** select **AWS service** for your trusted entity and then **EC2** under common use case.

![Roles]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/13_Role_One.png)

On the second page of **Create Role** attach the policy you created above.  Simply type **Can\_CRUD\_Elasticsearch** into the search bar and then check the box next to its name.

![Roles]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/14_Attach_Policy.png)

Skip the **Tags** and go to page four.  Since this role grants EC2 instances (e.g. Ubuntu servers) access to Amazon services, I named it **EC2\_Can\_Use\_Services**.

![Name the service role]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/15_Name_Role.png)

Click **Create role**.

###3.3 Trust Elasticsearch
After you click **Create role**,  AWS returns you to the IAM Role dashboard. If not, enter **EC2\_Can\_Use\_Services** into the **find** bar and click your new **EC2\_Can\_Use\_Services** role.  From here, click the **Trust Relationship** tab and click **Edit Trust Relationships**.

![Edit Trust]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/edit_trust_relationships-1024x460.png)

Copy and paste the following JSON into the "Policy Document" field.

```JSON
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com",
        "Service": "es.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

After you click **update trust relationship**, the IAM dashboard reads as follows:

![IAM Role Done]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/iam_role_done-1024x584.png)

##4. Connect to the Elasticsearch Service
###4.1 Launch an EC2 instance with the IAM role

From the AWS Management Console, click **Launch a Virtual Machine** or type **EC2** into the search bar and then click **Launch Instance**.

![Launch an EC2]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/16_Launch_EC2.png)

In **Step 1: Choose an AMI Instance,** select **Ubuntu Server 18.04 LTS**.

In **Step 2: Choose an Instance Type** select **t2.micro** or your preferred instance type.

In **Step 3:  Configure Instance Details** select **EC2\_Can\_Use\_Services** under **IAM role**.

![Apply IAM Role]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/17_Apply_IAM.png)

Now click "Review and Launch" and then launch.  AWS will take a few minutes to launch the instance.

###4.2 Configure the instance.
For security reasons, you should update your server's Operating System (OS).

```bash
ubuntu@ip-172-31-52-51:~$ sudo apt-get -y update
ubuntu@ip-172-31-52-51:~$ sudo apt-get -y dist-upgrade 
```

Since we now live in 2020, and the Python foundation End of Life'd (EOL) **Python 2**, I assume that you will use **Python 3**.

Ensure that you have **Python 3** installed:

```bash
ubuntu@ip-172-31-52-51:~$ python3 --version
Python 3.6.9
```

###4.3 Create a Virtual Environment
A virtual environment allows you to install python packages like a maniac without permanently hosing your server. You create an environment, install packages to that environment, activate the environment, use the environment, and then deactivate the environment (at which point you can re-activate it at a later date).  Virtual environments allow you to have several different versions of Python packages on the same server without any confusion or clobbering.

```bash
ubuntu@ip-172-31-52-51:~$ sudo apt-get install python3-venv
```

Create the virtual environment and then activate the environment with **source**.

```bash
ubuntu@ip-172-31-52-51:~$ python3 -m venv connect_to_es
ubuntu@ip-172-31-52-51:~$ source ./connect_to_es/bin/activate
(connect_to_es) ubuntu@ip-172-31-52-51:~$ cd connect_to_es/
(connect_to_es) ubuntu@ip-172-31-52-51:~/connect_to_es$
```

The shell prefixes the prompt with the name of your virtual environment **(connect\_to\_es)**.

This indicates that you activated your virtual environment.

Install the following packages into your environment:

- boto3
- elasticsearch
- requests
- requests-aws4auth

Note that you need to install the proper version of the **Elasticsearch** client.  In this **HOWTO** I installed Elasticsearch version **7.4**, so I need to install **version seven** of the **Elasticsearch** client.  See the [Elasticsearch Docs](https://elasticsearch-py.readthedocs.io/en/master) for simple instructions.

In the case of **7.4** I simply type:

```bash
$ pip install 'elasticsearch>=7.0.0,<7.14'
```

Install all of the required packages into your virtual environment:

```bash
(connect_to_es) ubuntu@ip-172-31-52-51:~/connect_to_es$ pip install boto3 requests requests-aws4auth 'elasticsearch>=7.0.0,<7.14'
```

A **pip freeze** writes the installed packages to the screen:

```bash
(connect_to_es) ubuntu@ip-172-31-52-51:~/connect_to_es$ pip freeze
boto3==1.13.21
botocore==1.16.21
certifi==2020.4.5.1
chardet==3.0.4
docutils==0.15.2
elasticsearch==7.7.1
idna==2.9
jmespath==0.10.0
pkg-resources==0.0.0
python-dateutil==2.8.1
requests==2.23.0
requests-aws4auth==0.9
s3transfer==0.3.3
six==1.15.0
urllib3==1.25.9
```

###4.4 Write a Python Script
In the **AWS management console**, click the **Elasticsearch service** and copy the address for your endpoint.

![Elasticsearch Endpoint]({filename}/images/Boto3_Ec2_To_Amazon_Elasticsearch/07_Elasticsearch_Endpoint.png)

In my example, I have the following **URI** for my Elasticsearch endpoint:

https://search-testdomain-wpk2kadnkwzoqzid2msl4es2km.us-east-1.es.amazonaws.com/

Remove the **https://** and trailing slash from the **URI** and enter it into the following script under the parameter **host**.

```python
#!/usr/bin/env python3
# connect_to_es.py
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import json

# Remove the https:// and trailing slash from your ES endpoint
# https://search-testdomain-wpk2kadnkwzoqzid2msl4es2km.us-east-1.es.amazonaws.com/

host = 'search-testdomain-wpk2kadnkwzoqzid2msl4es2km.us-east-1.es.amazonaws.com'
region = 'us-east-1'

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

print(json.dumps(es.info(), indent=4, sort_keys=True))
```

> Our Python script uses the **Boto3** library to access the credentials of the **IAM Role** assigned to our **EC2 Instance**.  This allows us to sign and encrypt requests to the **Elasticsearch Service** without having to install **ACCESS KEYS** into our home directory.

Now, from your active virtual environment, execute the script with the following command.

```bash
(connect_to_es) ubuntu@ip-172-31-52-51:~/connect_to_es$ python3 connect_to_es.py
```

The script returns the following output, which indicates that the script succesfully signed and encrypted the request, using the **IAM policy**.

```JSON
{
    "cluster_name": "138226304273:testdomain",
    "cluster_uuid": "Ef-k0ho8TZqTvuGttbhw9g",
    "name": "0fb4e11ccfafe89e61c8c037fa0bea4c",
    "tagline": "You Know, for Search",
    "version": {
        "build_date": "2020-05-05T04:47:22.951128Z",
        "build_flavor": "oss",
        "build_hash": "unknown",
        "build_snapshot": false,
        "build_type": "tar",
        "lucene_version": "8.2.0",
        "minimum_index_compatibility_version": "6.0.0-beta1",
        "minimum_wire_compatibility_version": "6.8.0",
        "number": "7.4.2"
    }
}
```

Congratulations! You connected an Ubuntu server in the cloud to the Elasticsearch service without compromising your security posture.  You did not need to install your **AWS\_ACCESS\_KEY** or **AWS\_SECRET\_KEY** into your server. You did not need to figure out the Public IP address of your EC2 instance in order to update the security policy of the Elasticsearch service. You can now spin up more servers and have them connect to Elasticsearch.  Just (1) Ensure they have the same Account ID (by default they will) and (2) Ensure that you attach the proper IAM role to your server creation time.

You can also take things a step further and use this process to connect [Lambda to the Elasticsearch service]({filename}/connect_aws_lambda_to_elasticsearch.md).
