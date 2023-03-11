Title: Pass Bootstrap HTML attributes to Flask-WTForms
Date: 2017-03-18 11:55
Author: john-sobanski
Category: HOWTO
Tags: Flask, HOWTO, Python
Slug: pass-bootstrap-html-attributes-to-flask-wtforms
Status: published

Flask-WTForms helps us [create and use web]({filename}/part-2-let-internet-facing-forms-update-elasticsearch-via-flask.md) forms with simple Python models. WTForms takes care of the tedious, boring and necessary security required when we want to use data submitted to our web app via a user on the Internet. WTForms makes data validation and Cross Sight Forgery Request (CSFR) avoidane a breeze. Out of the box, however, WTForms creates ugly forms with ugly validation. Flask-Bootstrap provides a professional layer of polish to our forms, with shading, highlights and pop ups.

Flask-Bootstrap also provides a "quick\_form" method, which commands Jinja2 to render an entire web page based on our form model with one line of code.

In the real world, unfortunately, customers have strong opinions about their web pages, and may ask you to tweak the default appearance that "quick\_form" generates. This blog post shows you how to do that.

In this blog post you will:

  -   Deploy a web app with a working form, to include validation and polish
  -   Tweak the appearance of the web page using a Flask-WTF macro
  -   Tweak the appearance of the web page using a Flask-Bootstrap method

## The Baseline App
The following code shows the baseline Flask application, which uses "quick\_form" to render the form's web page. Keep in mind that this application doesn't do anything, although you can easily extend it to persist data using an [ORM](https://www.sqlalchemy.org/) (for example). I based the web app on the following Architecture:

![Architecture]({static}/images/Pass_Bootstrap_HTML_attributes_to_Flask-WTForms/ff_1_architecture-1024x611.jpg)  

The web app contains ***models.py*** (contains form model), ***take\_quiz\_template.html*** (renders the web page) and ***application.py*** (the web app that can route to functions based on URL and parse the form data).

```bash
[ec2-user@ip-192-168-10-134 ~]$ tree flask_bootstrap/
flask_bootstrap/
├── application.py
├── models.py
├── requirements.txt
└── templates
    └── take_quiz_template.html

1 directory, 4 files
[ec2-user@ip-192-168-10-134 ~]$ 
```

I put the files for this baseline [Flask](http://flask.pocoo.org/) ***app*** on [GitHub](https://github.com/).  

[https://github.com/hatdropper1977/flask_bootstrap](https://github.com/hatdropper1977/flask_bootstrap)

Clone my project and take a look at the files I created.  Be sure to checkout the ***baseline*** tag.

```bash
[centos@ip-172-31-1-82 ~]$ git clone git@github.com:hatdropper1977/flask_bootstrap.git
Cloning into 'flask_bootstrap'...
remote: Counting objects: 25, done.
remote: Compressing objects: 100% (20/20), done.
remote: Total 25 (delta 6), reused 19 (delta 4), pack-reused 0
Receiving objects: 100% (25/25), 8.12 KiB | 0 bytes/s, done.
Resolving deltas: 100% (6/6), done.
[centos@ip-172-31-1-82 ~]$
```

Once you clone the repo, enter the directory and checkout the ***baseline*** tag:

```bash
[centos@ip-172-31-1-82 ~]$ cd flask_bootstrap/
[centos@ip-172-31-1-82 flask_bootstrap]$ git checkout baseline
Previous HEAD position was b80045c... form_field
HEAD is now at 22b9bcc... baseline
[centos@ip-172-31-1-82 flask_bootstrap]$ 
```

***Baseline*** includes the following files.

<p>
<script src="https://gist.github.com/hatdropper1977/08cddbb13d50bbd28a45ac0c28925d9b.js"></script>
</p>

<p>
<script src="https://gist.github.com/hatdropper1977/aa124c7909fa99fff0833db4dd15264f.js"></script>
</p>

<p>
<script src="https://gist.github.com/hatdropper1977/a9ed733d45bfc5022ee6340bd58188bd.js"></script>
</p>

Create and activate your virtual environment and then install the required libraries.

```bash
[ec2-user@ip-192-168-10-134 flask_bootstrap]$ cd ..
[ec2-user@ip-192-168-10-134 ~]$ virtualenv flask_bootstrap/
New python executable in flask_bootstrap/bin/python2.7
Also creating executable in flask_bootstrap/bin/python
Installing setuptools, pip...done.
[ec2-user@ip-192-168-10-134 ~]$ . flask_bootstrap/bin/activate
(flask_bootstrap)[ec2-user@ip-192-168-10-134 ~]$ pip install -r flask_bootstrap/requirements.txt

  ...

Successfully installed Flask-0.11.1 Flask-Bootstrap-3.3.7.0 Flask-WTF-0.13.1 Jinja2-2.8 MarkupSafe-0.23 WTForms-2.1 Werkzeug-0.11.11 click-6.6 dominate-2.3.1 itsdangerous-0.24 visitor-0.1.3
(flask_bootstrap)[ec2-user@ip-192-168-10-134 ~]$ 
```

Start your flask application and then navigate to your IP address. Since this is just a dev application, you will need to access port ***5000***.  

```bash
(flask_bootstrap)[ec2-user@ip-192-168-10-134 ~]$ cd flask_bootstrap/
(flask_bootstrap)[ec2-user@ip-192-168-10-134 flask_bootstrap]$ ./application.py 
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 417-431-486
```

This application uses the ***quick\_form*** method to generate a web page. Note that the application includes all sorts of goodies, such as CSFR avoidance, professional looking highlights and validation. Play around with the page to look at the different validation pop-ups and warnings.

Now imagine that your customer wants to change the look of the ***submit*** button, or add some default text. In this situation, the ***quick\_form*** does not suffice.

## Attempt 1: Use a Flask-WTF Macro
We can use vanilla Flask-WTF (vs. Flask-Bootstrap) to pass Bootstrap HTML attributes to WTForms.  

To see this in action, check out the second version of the ***app*** via its Git [tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging).

```bash
[centos@ip-172-31-1-82 flask_bootstrap]$ git checkout formhelpers
D       app.py
Previous HEAD position was ada8bff... form_field
HEAD is now at f029a55... formhelpers
[centos@ip-172-31-1-82 flask_bootstrap]
```

The Flask-WTF [docs](http://flask.pocoo.org/docs/1.0/patterns/wtforms/#forms-in-templates) describe a Macro named ***render\_field*** which allows us to pass HTML attributes to Jinja2. We save this macro in a file named ***\_formhelpers.html*** and stick it in the same templates folder as ***take\_quiz\_template.html***.  

```jinja2
{% macro render_field(field) %}
  <dt>{{ field.label }}
  <dd>{{ field(**kwargs)|safe }}
  {% if field.errors %}
    <ul class=errors>
    {% for error in field.errors %}
      <li>{{ error }}</li>
    {% endfor %}
    </ul>
  {% endif %}
  </dd>
{% endmacro %}
```

Now, update the ***take\_quiz\_template.html*** template to use the new macro. Note that we lose the ***quick\_form*** shortcut and need to spell out each form field.  In addition, we need to add HTML for the form an CSFR token.

```jinjia2
{% extends "bootstrap/base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% from "_formhelpers.html" import render_field %}
{% block content %}
  <div class="container">
  <h3>Please answer this very important essay</h3>
  <p>If you don't it'll go on your permanent record!.</p>
<hr>
<form action="" method="post" class="form" role="form">
  {{ form.csrf_token() }}
 <d1>
   {{ render_field(form.essay_question, class='form-control', placeholder='Write down your thoughts here...') }}
   {{ render_field(form.email_addr, class='form-control', placeholder='Enter email') }}
 </d1>
 <p><input type=submit class='btn btn-warning btn-block'>
</form>
<hr>
<p>Copyright 2018 <a href="https://john.soban.ski">Freshlex, LLC</a></p>
</div>
{% endblock %}
```

When you go to your web page you will see the default text we added to the input fields via ***render_field***:

```jinja2
   {{ render_field(form.essay_question, class='form-control', placeholder='Write down your thoughts here...') }}
   {{ render_field(form.email_addr, class='form-control', placeholder='Enter email') }}
```

You will also see an orange submit button that spans the width of the page:

```jinja2
 <p><input type=submit class='btn btn-warning btn-block'>
```

You can see both of these changes on the web page:

![Custom Submit Box No Validation]({static}/images/Pass_Bootstrap_HTML_attributes_to_Flask-WTForms/ff_custom_submit_box_no_validation.jpg)

Unfortunately, if you click submit without entering any text, you will notice that we have reverted to ugly validations.

![Custom Submit Box With Ugly Validation]({static}/images/Pass_Bootstrap_HTML_attributes_to_Flask-WTForms/ff_custom_submit_box_w_ugly_validation.jpg)

## Attempt 2: Use Flask-Bootstrap
In this attempt, we will use [Flask-Bootstap](https://pythonhosted.org/Flask-Bootstrap/) directly to pass the attributes to Flask-WTF, thus obviating the need for the ***\_formhelpers.html*** macro.

Although pretty much hidden in the Flask-Bootstrap documents, it turns out you can add extra HTML elements directly to the template engine using ***form\_field***.

Check out the third version of the ***app***, using the Git tag.

```bash
[centos@ip-172-31-1-82 flask_bootstrap]$ git checkout form_field
D       app.py
Previous HEAD position was 0ba0f8a... baseline
HEAD is now at ada8bff... form_field
[centos@ip-172-31-1-82 flask_bootstrap]$
```

The new template does not need to import the ***render_field*** macro from ***\_formhelpers.html***:

```jinja2
{% extends "bootstrap/base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block content %}
  <div class="container">
  <h3>Please answer this very important essay</h3>
  <p>If you don't it'll go on your permanent record!.</p>
<hr>
<form action="" method="post" class="form" role="form">
  {{ form.csrf_token() }}
 <d1>
  {{ wtf.form_field(form.essay_question, class='form-control', placeholder='Write down your thoughts here...') }}
  {{ wtf.form_field(form.email_addr, class='form-control', placeholder='your@email.com') }}
 </d1>
 <p><input type=submit class='btn btn-warning btn-block'>
</form>
<hr>
<p>Copyright 2018 <a href="https://john.soban.ski">Freshlex, LLC</a></p>
</div>
{% endblock %}
```

As before, we add default text with "placeholder:"

```jinja2
{{ wtf.form_field(form.essay_question, class='form-control', placeholder='Write down your thoughts here...') }}
{{ wtf.form_field(form.email_addr, class='form-control', placeholder='your@email.com') }}
```

We then customize the submit button. You can customize the button however you would like. Take a look [here](https://v4-alpha.getbootstrap.com/components/buttons/) for more ideas.

```jinja2
 <p><input type=submit class='btn btn-warning btn-block'>
```

This gives us a bootstrap rendered page with pretty validation:

![Custom Submit Box With Pretty Validation]({static}/images/Pass_Bootstrap_HTML_attributes_to_Flask-WTForms/ff_custom_submit_box_w_pretty_validation.jpg)

As you can see, we get a popup if we attempt to submit without entering text, submit without entering an email, or enter an invalid email address.

## Conclusion
You now have a working web application that easily renders professional looking forms with validation and pop-ups. In the future you can trade ease of deployment against customability.

If you enjoyed this blog post, you may be interested in how to [quickly add reCAPTCHA to your app using Flask-WTF]({filename}/add-recaptcha-to-your-flask-application.md), how to use the Flask-like [Chalice](https://github.com/aws/chalice) to [quickly deploy a web app to Lambda]({filename}/connect_aws_lambda_to_elasticsearch.md), or  my five part series on how to deploy a Flask application (with an [Elasticsearch](https://aws.amazon.com/elasticsearch-service/) back-end) to the Amazon Web Services ecosystem:

  - [Part One:]({filename}/part-1-connect-ec2-to-the-amazon-elasticsearch-service.md)
    - Deploy an [Amazon Web Service (AWS) Elasticsearch (ES)](https://aws.amazon.com/elasticsearch-service/) domain
    - Use [Identity and Access Management (IAM)](https://aws.amazon.com/iam/) roles, IAM profiles and the [boto](https://aws.amazon.com/sdk-for-python/) library to connect a server to the ES domain
  - [Part Two:]({filename}/part-2-let-internet-facing-forms-update-elasticsearch-via-flask.md)
    - Deploy a [Flask](http://flask.pocoo.org/) web server
    - Program the Flask web server to proxy and filter user inputs to ES
    - Learn the Python [WTForms](https://wtforms.readthedocs.io/en/latest/) library and the Python [Elasticsearch Domain Specific Language (DSL)](http://elasticsearch-dsl.readthedocs.io/en/latest/)
  - [Part Three:]({filename}/part-3-professional-form-validation-with-bootstrap.md)
    - Use [Bootstrap](http://getbootstrap.com/) for form validation
    - Give the Proxy a professional, polished appearance
  - [Part Four:]({filename}/part-4-connect-elasticbeanstalk-to-elasticsearch-aws-identity-and-access-management-iam.md)
    - Connect [Elastic Beanstalk (EBS)](https://aws.amazon.com/elasticbeanstalk/) to Elasticsearch via AWS Identity and Access Management
    - Deploy the Flask server to EBS
  - [Part Five:]({filename}/part-5-asynchronous-tasks-with-aws-elasticsearch-sqs-flask-and-celery.md)
    - Learn the benefits of [asynchronous](https://en.wikipedia.org/wiki/Message_queue#Synchronous_vs._asynchronous) tasks
    - Deploy an [Amazon Simple Queue Service (SQS)](https://aws.amazon.com/sqs/) message Queue
    - Make [Celery](http://www.celeryproject.org/) on our Flask controller
    - Deploy Celery worker nodes
    - Call a remote web service via a Representative State Transfer (REST) Application Programming Interface (API)

