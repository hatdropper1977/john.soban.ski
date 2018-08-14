Title: Part 1: Connect EC2 to the Amazon Elasticsearch Service
Date: 2016-02-20 02:48
Author: john-sobanski
Category: HOWTO
Tags: AWS, Elasticsearch, HOWTO, IAM, Python
Slug: part-1-connect-ec2-to-the-amazon-elasticsearch-service
Status: published

Step one of our journey connects [EC2](https://aws.amazon.com/ec2/) to ES using the Amazon [boto](https://aws.amazon.com/sdk-for-python/) Python library. I spent more than a few hours pouring through the AWS help docs and pounding at my keyboard on my instances to figure out the easiest and most direct method to accomplish this. As of writing this blog, I found no decent HOWTO online on how to connect EC2 to the [AWS provided ES](https://aws.amazon.com/elasticsearch-service/) so I put my chin up and started swinging. If you find that this article helps you to quickly get your job done, then please write a comment below (Even if it's just "thanks dude!") .

![Howto]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/howot1.png)

One more caveat before we begin. You need to trust me that the [IAM](https://aws.amazon.com/iam/) role approach below will make your life easy. It's a quick, "pull of the bandaid" method that will save you a ton of headaches and troubleshooting. Unfortunately, the IAM role method has two downsides (1) It appears boring and complicated so your mind come up with reasons to skip it in order to [comfort your precious ego](https://en.wikipedia.org/wiki/Defence_mechanisms) (No offense, my mind pulls the same crap and I am not nearly as smart as you) and (2) It uses JSON, which to the uninitiated also appears boring and complicated. All I ask of you is twenty seconds of courage, to read my IAM instructions (which I spent hours simplifying), copy and paste and move on! Your alternatives (1) Copy and Paste your AWS credentials or (2) Use the old "Allow by IP" hack appear to be much simpler, but after the most basic integrations become maddeningly difficult and time wasting, if not impossible.

In this blog post you will:  
  1. Deploy an AWS Elasticsearch Instance  
  2. Create an IAM Role, Policy and Trust Relationship  
  3. Connect an EC2 Instance

Note:  This blog post assumes you know how to [SSH into an EC2 instance.](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstances.html)

**1. Deploy an AWS Elasticsearch Instance**

Amazon makes Elasticsearch deployment a snap.  Just click the Elasticsearch Service icon on your management screen:

![Console]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/AWS-Management-Console-300x222.png)

Then click "New Domain."

![Console]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/Amazon-Elasticsearch-Service-Management-Console-1024x440.png)

Name your domain "test-domain" (Or whatever).

![Service MGMT]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/Amazon-Elasticsearch-Service-Management-Console-2-1024x590.png)

Keep the defaults on the next screen "Step 2: Configure Cluster."  Just click "next."   On the next screen, select: "Allow or deny access to one or more AWS accounts or IAM users".  (Resist the temptation to "Allow by IP" ).

![Set up access]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/set_up_access-1024x569.png)

Amazon makes security easy as well.  On the next menu they list your ARN.  Just copy and paste it into the text field and hit "next."

![User Access]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/User-Access-1024x623.png)

AWS generates the JSON for your Elasticsearch service:

![ES JSON]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/es_json-1024x374.png)

Click "Next" and then "confirm and create."

**2. Create an IAM Role, Policy and Trust Relationship**

**2.1 Create an IAM Role**

OK, deep breath.  Just follow me and you will confront your IAM fears.

First, select "Identity and Access Management" from the AWS access console.

![IAM Menu]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/iam_menu-300x190.png)

On the Dashboard, click "roles."

![Roles]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/roles-139x300.png)

Next, click "create new role."  I like to name the roles something obvious.  Since we want to grant an EC2 instance (i.e. a Linux server) access to Amazon services, I picked the name "EC2\_Can\_Use\_Services."

![Name the service role]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/name_the_role-1024x314.png)

On the next screen, Amazon asks you to select from popular roles.  Click on the first one "Allow EC2 instances to call AWS services on your behalf."

![Select role type]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/select_role_type-1024x529.png)

You're almost done!  Just click through the next menu "Attach Policy." 

We will worry about that in the next section.  Just click "Next Step" and then "Create Role."

**2.2 Create an IAM Policy**

Now at the IAM Management dashboard, select "Policies."

![Select Policy]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/select_policy-116x300.png)

Then, select "create policy" and then "create your own policy."

![Create Policy]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/select_create_policy-1024x596.png)

Name your policy "Can\_CRUD\_Elasticsearch," add a description and then copy and paste the following JSON into the "Policy Document:"  

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

If you click "Validate Policy," you will receive a message that it works.  If you see "the policy is valid," click "create policy."

![Validate]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/reveiw_policy-1024x532.png)

**2.3 Attach your Policy**

Go back to the Role you created, "EC2\_Can\_Use\_Services," and click "attach policy."

![Attach]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/attach_policy-1024x552.png)

Now, in the search bar, type "CRUD" and you will see the Policy you just created, "Can\_CRUD\_Elasticsearch."  Click this policy and then click "Attach Policy."

![Attach]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/attach_policy2-1024x459.png)

**2.4 Trust Elasticsearch**

Now it's time for your victory lap! After you click "attach policy," AWS takes you back to the IAM Role dashboard.  From here, click the "Trust Relationship" tab and click "Edit Trust Relationships."

![Edit Trust]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/edit_trust_relationships-1024x460.png)

<!-- HTML generated using hilite.me -->Now edit the JSON to reflect the JSON below.  You can copy and paste the JSON into the "Policy Document" field.

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

After you click "update trust relationship," your IAM Role Dashboard will read as follows:

![IAM Role Done]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/iam_role_done-1024x584.png)

Congrats!  You made it through the hardest part!!!

**3. Connect an EC2 instance**  
**3.1 Launch an EC2 instance with the IAM role**

You can only attach an IAM role at instance creation.  So, we will need to launch a brand new EC2 instance (no biggie).  From the AWS Management Console, click EC2 and then "Launch Instance."

![Launch an EC2]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/Launch_an_EC2-300x264.png)

In "Step 1: Choose an AMI Instance," select "Ubuntu Server 14.04 LTS (HVM), SSD Volume Type."

In "Step 2: Choose an Instance Type" select t2.micro.

Now, this part is very important, in Step 3, be sure to pick your IAM role.

![Apply IAM Role]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/apply_IAM_role-1024x569.png)

Now click "Review and Launch" and then launch.  AWS will take a few minutes to launch the instance.

**3.2 Configure the instance.**

First up, you want to add your hostname to /etc/hosts, to remove any sudo warnings:

```bash
ubuntu@ip-172-31-35-80:~$ sudo vim /etc/hosts
```

Then, update your server.

```bash
ubuntu@ip-172-31-35-80:~$ sudo apt-get -y update
ubuntu@ip-172-31-35-80:~$ sudo apt-get -y dist-upgrade 
```

Now install Python VirtualEnv. VirtualEnv allows you to make sense of any Python button mashing. You point VirtualEnv to a directory, type "activate" and then install packages to your hearts content without screwing with the rest of the server. Once you're done, you click "deactivate" and you're back to a clean distro. You can always go back to where you left off with the "activate"
command.

```bash
ubuntu@ip-172-31-35-80:~$ sudo apt-get install -y python-virtualenv
```

You can activate an environment with a "." or "source" (or El Duderino if you're not into the whole brevity thing).

```bash
ubuntu@ip-172-31-35-80:~$ mkdir connect_to_es
ubuntu@ip-172-31-35-80:~$ virtualenv connect_to_es/
New python executable in connect_to_es/bin/python
Installing setuptools, pip...done.
ubuntu@ip-172-31-35-80:~$ . connect_to_es/bin/activate
(connect_to_es)ubuntu@ip-172-31-35-80:~$ cd connect_to_es/
(connect_to_es)ubuntu@ip-172-31-35-80:~/connect_to_es$ 
```

Notice that the shell prompt lists the name of your virtual environment (connect\_to\_es).  Since you're in a virtual sandbox, you can pip install (or easy\_install) to your heart's content.


```bash
(connect_to_es)ubuntu@ip-172-31-35-80:~/connect_to_es$ easy_install boto
```

Go back to the AWS Management console, click the Elasticsearch service and copy the address for your endpoint.

![ES Endpoint]({filename}/images/Part_1_Connect_EC2_to_the_Amazon_Elasticsearch_Service/es_endpoint-1024x562.png)

Now, edit the following Python script with your Endpoint address for "host."  

```python
# connect_test.py
from boto.connection import AWSAuthConnection

class ESConnection(AWSAuthConnection):

    def __init__(self, region, **kwargs):
        super(ESConnection, self).__init__(**kwargs)
        self._set_auth_region_name(region)
        self._set_auth_service_name("es")

    def _required_auth_capability(self):
        return ['hmac-v4']

if __name__ == "__main__":
    client = ESConnection(
            region='us-east-1',
            # Be sure to put the URL for your Elasticsearch endpoint below!
            host='search-test-domain-ircp547akjoolsbp4ehu2a56u4.us-east-1.es.amazonaws.com',
            is_secure=False)

    resp = client.make_request(method='GET',path='/')
    print resp.read()
```

Then (from your Virtual Environment), execute the script.  

```bash
(connect_to_es)ubuntu@ip-172-31-35-80:~/connect_to_es$ python connect_test.py 
```

And you will get your result...  

```JSON
{
  "status" : 200,
  "name" : "Chemistro",
  "cluster_name" : "XXXXXXXXXXXX:test-domain",
  "version" : {
    "number" : "1.5.2",
    "build_hash" : "62ff9868b4c8a0c45860bebb259e21980778ab1c",
    "build_timestamp" : "2015-04-27T09:21:06Z",
    "build_snapshot" : false,
    "lucene_version" : "4.10.4"
  },
  "tagline" : "You Know, for Search"
}
```

Think about what you just did.  You connected to an AWS provided Elasticsearch service without any need to copy in paste your AWS\_ACCESS\_KEY or AWS\_SECRET\_KEY.  You did not need to figure out the Public IP address of your EC2 instance in order to update the security policy of the Elasticsearch service.  Given these two points, you can easily spin up spot instances and have them connect to
Elasticsearch by simply (1) Ensuring they have the same ARN (by default they will) and (2) Ensuring you point to the proper IAM role at creation time.  This process will come in handy when you connect ElasticBeanstalk to the Elasticsearch service, which we will do in [part 2]({filename}/part-2-let-internet-facing-forms-update-elasticsearch-via-flask.md) of this HOWTO!
