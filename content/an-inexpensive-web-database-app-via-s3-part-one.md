Title: A Web Database App via S3 - Part One:  A Flask Approach
Date: 2019-03-30 10:26
Author: john-sobanski
Category: HOWTO
Tags:  AWS, Chalice, HOWTO, IAM, Lambda, Python, S3
Slug: an-inexpensive-web-database-app-via-s3-part-one
Status: published
Publisher: freshlex

I deployed my first web database application back in 2002 thanks to the seminal O'Reilly book [Web Database Applications with PHP and Mysql](https://www.oreilly.com/library/view/web-database-applications/0596000413/) by David Lane and Hugh E. Williams.  In the past sixteen years, the industry developed tons of frameworks and ecosystems to help deploy web database applications, but the core concept generally remains the same.  In summary, a web database application presents a form to the end user, the end user submits it, the application validates the form data, processes the form data and then persists all of the user data to a database.  A user can then retrieve the data (either raw or processed) via another web form.  In this blog post, I replace the traditional back end Relational Database Management System (RDBMS) with the Amazon Simple Storage Service (S3).  RDBMS as a service start at about $10/month.  By using [S3]({tag}s3), we can reduce this cost to pennies per month.

I use [S3 to host this website]({filename}/how-to-configure-s3-websites-to-use-https-part-1.md) and receive about 60,000 - 90,000 hits per month.

![S3 Stat]({static}/images/An_Inexpensive_Web_Database_App_Via_S3_Part_One/01_S3_Stat.png)  

Since I use [S3 to host this site]({filename}/how-to-configure-s3-websites-to-use-https-part-2.md), I only pay ~$0.90/month.

> NOTE: [S3Stat]({filename}/use-s3stat-to-troubleshoot-your-migration-from-wordpress-to-s3.md) provides me with this handly data.
 
The following graphic captures the desired, final Web Database Application architecture.  I will use [AWS Chalice]({filename}/deploy_an_advanced_elasticsearch_proxy_with_lambda.md) to automate the deployment.

![Flask Web DB Architecture]({static}/images/An_Inexpensive_Web_Database_App_Via_S3_Part_One/03_Flask_Web_DB_Architecture.png)

This blog post discusses how to deploy the S3 backed Web Database Application through [Flask]({tag}flask).  Once we get the logic down in Flask, we can easily refactor the code to conform to the Chalice framework.

![Final Web DB Architecture]({static}/images/An_Inexpensive_Web_Database_App_Via_S3_Part_One/02_Final_Web_DB_Architecture.png)
 
## The Flask App
This section describes the Flask implementation of the Web Database application.  Miguel Grinberg wrote the definative book on Flask.  I highly recommend you [purchase his book](https://blog.miguelgrinberg.com/post/about-me).  (You will see a familiar name on page XIV).

![Flask book shout out]({static}/images/An_Inexpensive_Web_Database_App_Via_S3_Part_One/04_Flask_Ack.png)

I have written heavily about Flask on [this very site]({tag}flask).

### The model
We use [Flask WTF]({filename}/part-2-let-internet-facing-forms-update-elasticsearch-via-flask.md) to model the form.  We include a bunch of different form field types to demonstrate validation variety.

```python
# models.py
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, IPAddress

# Form ORM
class QuizForm(FlaskForm):
        agree = BooleanField('Check this box if you would like')
        anumber = IntegerField('Enter a number',validators = [InputRequired()])
        ipaddr = StringField('Enter an IP address', validators=[IPAddress()])
        textblob =  TextAreaField('Who do you think won the console wars of 1991, Sega Genesis or Super Nintendo? (2048 characters)', validators=[InputRequired(),Length(max=2047)] )
        submit = SubmitField('Submit')
```

Note that we accomodate a checkbox, an Integer, an IP Address, a text blob and a submit button.

### The View
Flask uses a **Jinja2** template engine to render the view.  The engine generates client-side Java Script with [hooks to Bootstrap]({filename}/part-3-professional-form-validation-with-bootstrap.md) for pretty forms and client-side validation.  The WTF **quick_form()** method provides a macro to automatically generate a form element for every object in our model above.

```python
# templates/take_quiz_template.html
{% extends "bootstrap/base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block content %}
  <div class="container">
  <h3>Please answer this very important essay</h3>
  <p>If you don't it'll go on your permanent record!.</p>
<hr>
{{ wtf.quick_form(form) }}
<hr>
<p>Copyright 2019 <a href="https://john.soban.ski">John Sobanski</a></p>
</div>
{% endblock %}
```

### The Controller
A Flask object orchestrates the client-side javascript generation and service routing.  The current Web DB App doesn't do much, it just validates form data and returns a static string.

```python
#!/usr/bin/env python
# application.py
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from models import QuizForm

class Config(object):
    SECRET_KEY = '78w0o5tuuGex5Ktk8VvVDF9Pw3jv1MVE'

application = Flask(__name__)
application.config.from_object(Config)

Bootstrap(application)

@application.route('/', methods=['GET', 'POST'])
def take_test():
    form = QuizForm(request.form)
    if not form.validate_on_submit():
        return render_template('take_quiz_template.html', form=form)
    if request.method == 'POST':
        return 'Submitted!'

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
```

Run the application and verify that it works as expected.

If you want to go nuts, you can check the validation by entering incompatible data into the validated fields.

Enter "ABCD" into **IP Address**, for example.

![Client side validation]({static}/images/An_Inexpensive_Web_Database_App_Via_S3_Part_One/05_Client_Side_Validation.png) 

## Persistence
Now we will persist the data to our "database," which happens to be an object store.

### Persist the Data
First, let's import some new standard Python packages.  We will enrich the user's form data with some meta data, to include their IP address, a timestamp and a unique ID.  Notice **choice**,**datetime**,**json** and **string**.  We will also import **boto3** in order to write to S3.

```python
#!/usr/bin/env python
import boto3, json, string
from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from models import QuizForm
from random import choice
```

I wrote a simple key-generation script so that our data will persist with a unique key name.

```python
# Generate a random Object ID
def random_string_gen(size=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_'):
    return ''.join(choice(chars) for _ in range(size))
```

We will create our **s3** resource outside of the route.

```python
s3 = boto3.resource('s3')
```

Finally, you will want to ensure that you point to your bucket.  I use my bucket from a previous blog post about [trancoding mp3 audio]().

```python
S3_BUCKET_NAME = 'transcribe-input-test'
```

Now let's write some code to pull the submitted form data, store it in a dictionary and then encode that dictionary in JSON.  Once we have the JSON object, we will write to **s3** using the **put()** method.

```python
@application.route('/', methods=['GET', 'POST'])
def take_test():
    form = QuizForm(request.form)
    if not form.validate_on_submit():
        return render_template('take_quiz_template.html', form=form)
    if request.method == 'POST':
		# Generate a random key name
        S3_OBJECT_NAME = random_string_gen()
        # Create an empty dict
		completed_quiz = {}
		# Add the form data and enrich with meta data
        completed_quiz['agree'] = request.form.get('agree') completed_quiz['anumber'] = request.form.get('anumber')
        completed_quiz['client_ip_addr'] = request.remote_addr
        completed_quiz['_id'] = S3_OBJECT_NAME
        completed_quiz['ipaddr'] = request.form.get('ipaddr')
        completed_quiz['@timestamp'] = datetime.now().isoformat()
        completed_quiz['textblob'] = request.form.get('textblob')
        # Encode the data in JSON
		S3_OBJECT_JSON = json.dumps(completed_quiz)
        # Write object to your S3 bucket
		s3 = boto3.resource('s3')
        s3.Object(S3_BUCKET_NAME, '{}.json'.format(S3_OBJECT_NAME)).put(Body=S3_OBJECT_JSON)
        # Print a success message to the user
		return 'Submitted!'
```

After you run your application, enter your data and submit your data, take a look at your S3 bucket.  You will see a twenty character filename that ends in **.json**.

```bash
$ aws s3 ls transcribe-input-test
2019-03-28 00:06:57        209 mU93H9iAt3X7FKkmbZFL.json
```

If you pull that object and inspect the content, you will see the user data and meta data encoded in JSON.

```bash
$ aws s3 cp s3://transcribe-input-test/mU93H9iAt3X7FKkmbZFL.json .
download: s3://transcribe-input-test/mU93H9iAt3X7FKkmbZFL.json to ./mU93H9iAt3X7FKkmbZFL.json

$ cat mU93H9iAt3X7FKkmbZFL.json
{
  "anumber": "23",
  "@timestamp": "2019-03-28T00:06:56.604874",
  "ipaddr": "127.0.0.1",
  "client_ip_addr": "47.23.82.43",
  "textblob": "The Turbo Graphix 16 of course.",
  "_id": "mU93H9iAt3X7FKkmbZFL",
  "agree": "y"
}
```

### Retrieve the Data
We can easily add logic to pull the JSON data based on a user provided key.  We will set up a Flask **route** to get the desired Key from the URL.

```python
@application.route('/user/<userkey>')
def show_user_data(userkey):
    S3_OBJECT_NAME = '{}.json'.format(userkey)
    obj = s3.Object(S3_BUCKET_NAME, S3_OBJECT_NAME)
    user_json = obj.get()['Body'].read().decode('utf-8')
    return user_json
```

Now, go to your Flask endpoint and append /user/<Your user key> to the URL.  I run a test server at http://52.54.218.55:5000, and my document has a Key ID of **mU93H9iAt3X7FKkmbZFL**.  Therefore, I entered http://52.54.218.55:5000/user/mU93H9iAt3X7FKkmbZFL into my browser's search bar.  Notice I left the **.json** off of the end.

![Retrieve User Data]({static}/images/An_Inexpensive_Web_Database_App_Via_S3_Part_One/06_Retrieve_User_Data.png) 

### Make the Data Pretty
Since this is Flask, we can make the data pretty by using a **Jinja2** template.

```jinja2
# templates/show_user_data.html
{% extends "bootstrap/base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block content %}
  <div class="container">
  <h3>Here's your data!!!</h3>
<hr>
  {% for key in user_json %}
    <li>{{ key }}: {{ user_json[key] }}</li>
  {% endfor %}
<hr>
<p>Copyright 2019 <a href="https://john.soban.ski">John Sobanski</a></p>
</div>
{% endblock %}
```

This template iterates through each Key in the JSON object and prints it in a bulleted list.

Point your Flask app to this new template.

```python
@application.route('/user/<userkey>')
def show_user_data(userkey):
    S3_OBJECT_NAME = '{}.json'.format(userkey)
    obj = s3.Object(S3_BUCKET_NAME, S3_OBJECT_NAME)
    user_json = obj.get()['Body'].read().decode('utf-8')
    return render_template( 'show_data_template.html', user_json = json.loads(user_json) )
```

When you reload the web page, you will see a bulleted list of key/ value pairs.

![Retrieve User Data Pretty]({static}/images/An_Inexpensive_Web_Database_App_Via_S3_Part_One/07_Retrieve_User_Data_Pretty.png) 

### Daily Bucket
If you don't like the idea of having a single bucket holding every record, you can break up the storage into daily buckets.

Add a string to your **take_test()** route that records the current date and then use this as your S3 sub-bucket name.

```python
	S3_SUB_BUCKET_NAME = datetime.now().strftime('%Y%m%d')
```

Then prepend your object key with this sub-bucket name when you **put()** the object.

```python
        s3.Object(S3_BUCKET_NAME, '{}/{}.json'.format(S3_SUB_BUCKET_NAME,S3_OBJECT_NAME)).put(Body=S3_OBJECT_JSON)
```

Update the **show_user_data()** route to accomodate this new sub-bucket approach.

```python
@application.route('/user/<user_date>/<user_key>')
def show_user_data(user_date,user_key):
    S3_SUB_BUCKET_NAME = user_date
    S3_OBJECT_NAME = user_key
    obj = s3.Object(S3_BUCKET_NAME, '{}/{}.json'.format(S3_SUB_BUCKET_NAME, S3_OBJECT_NAME))
    user_json = obj.get()['Body'].read().decode('utf-8')
    return render_template( 'show_data_template.html', user_json = json.loads(user_json) )
```

This approach organizes all records by date in your parent bucket.

## Code
The entire **application.py** follows:

```python
#!/usr/bin/env python
import boto3, json, string
from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from models import QuizForm
from random import choice

class Config(object):
    SECRET_KEY = '78w0o5tuuGex5Ktk8VvVDF9Pw3jv1MVE'

S3_BUCKET_NAME = 'transcribe-input-test'

# Generate a random Object ID
def random_string_gen(size=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_'):
    return ''.join(choice(chars) for _ in range(size)) 
s3 = boto3.resource('s3')

application = Flask(__name__)
application.config.from_object(Config)

Bootstrap(application)

@application.route('/', methods=['GET', 'POST'])
def take_test():
    form = QuizForm(request.form)
    if not form.validate_on_submit():
        return render_template('take_quiz_template.html', form=form)
    if request.method == 'POST':
        S3_SUB_BUCKET_NAME = datetime.now().strftime('%Y%m%d')
        S3_OBJECT_NAME = random_string_gen()
        completed_quiz = {}
        completed_quiz['agree'] = request.form.get('agree') 
        completed_quiz['anumber'] = request.form.get('anumber')
        completed_quiz['client_ip_addr'] = request.remote_addr
        completed_quiz['_id'] = S3_OBJECT_NAME
        completed_quiz['ipaddr'] = request.form.get('ipaddr')
        completed_quiz['@timestamp'] = datetime.now().isoformat()
        completed_quiz['textblob'] = request.form.get('textblob')
        S3_OBJECT_JSON = json.dumps(completed_quiz)
        s3 = boto3.resource('s3')
        s3.Object(S3_BUCKET_NAME, '{}/{}.json'.format(S3_SUB_BUCKET_NAME,S3_OBJECT_NAME)).put(Body=S3_OBJECT_JSON)
        return 'Your key is {}/{}.'.format(S3_SUB_BUCKET_NAME,S3_OBJECT_NAME)

@application.route('/user/<user_date>/<user_key>')
def show_user_data(user_date,user_key):
    S3_SUB_BUCKET_NAME = user_date
    S3_OBJECT_NAME = user_key
    obj = s3.Object(S3_BUCKET_NAME, '{}/{}.json'.format(S3_SUB_BUCKET_NAME, S3_OBJECT_NAME))
    user_json = obj.get()['Body'].read().decode('utf-8')
    return render_template( 'show_data_template.html', user_json = json.loads(user_json) )

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
```

## Try it out!
I pushed the entire app to [Github](https://github.com/hatdropper1977/web-db-app-w-s3).  Merely clone it, switch to the 'Flask-App' tag, install **requirements.txt** and run it!

```bash
[~]$ git clone git@github.com:hatdropper1977/web-db-app-w-s3.git
[~]$ cd web-db-app-w-s3
[web-db-app-w-s3]$ git checkout Flask-App
[web-db-app-w-s3]$ cd ..
[~]$ virtualenv web-db-app-w-s3
[~]$ cd web-db-app-w-s3
[web-db-app-w-s3]$ source ./bin/activate
(web-db-app-w-s3)[web-db-app-w-s3]$ pip install -U pip
(web-db-app-w-s3)[web-db-app-w-s3]$ pip install -r requirements.txt
(web-db-app-w-s3)[web-db-app-w-s3]$ vim application.py # Set S3_BUCKET_NAME to your bucket
(web-db-app-w-s3)[web-db-app-w-s3]$ ./application.py
 * Serving Flask app "application" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-456-789
```

## Conclusion
We succesfully deployed a Flask application with an S3 backend.  In the next blog post, we will refactor the Web Database App to use [Lambda]({tag}lambda) instead of Flask.
