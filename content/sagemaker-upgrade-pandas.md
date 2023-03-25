Title: Upgrade SageMaker JupyterLab Notebooks to the Latest Pandas
Date: 2022-10-29 10:29
Author: john-sobanski
Category: Data Science
Tags: AWS, Python, HOWTO, Machine Learning
Slug: sagemaker-upgrade-pandas
Status: published

[Amazon Web Services (AWS) SageMaker Notebook Instances](https://aws.amazon.com/sagemaker/) provide fully managed Jupyter Notebooks, tailored for Data Science and Machine Learning (ML) use cases.

These notebooks allow Data Scientists and ML Engineers to explore, operationalize and share data, algorithms and pipelines.

Pandas contributes a critical piece to the Data Scientists' toolbox, via the Data Frame construct.  Each new version of Pandas provides improvements, upgrades and new conveniences.

![Python Pandas]({static}/images/Sagemaker_Upgrade_Pandas/00_Pandas_Python.png)

I run into an issue with my **AWS SageMaker Notebook**, however, when I try to upgrade Pandas.

If I attempt to Upgrade [Pandas](https://pandas.pydata.org/) above version **1.1.5** on my **AWS Sagemaker** provided [JupyterLab notebook](https://jupyter.org/) I receive the error **No Matching Distribution Found**.

```python
import sys
!{sys.executable} -m pip install --pre --upgrade pandas==1.3.5
```

```bash
ERROR: Could not find a version that satisfies the requirement pandas==1.3.5 (from versions: 0.1, 0.2, 0.3.0, 0.4.0, 0.4.1, 0.4.2, 0.4.3, 0.5.0, 0.6.0, 0.6.1, 0.7.0, 0.7.1, 0.7.2, 0.7.3, 0.8.0, 0.8.1, 0.9.0, 0.9.1, 0.10.0, 0.10.1, 0.11.0, 0.12.0, 0.13.0, 0.13.1, 0.14.0, 0.14.1, 0.15.0, 0.15.1, 0.15.2, 0.16.0, 0.16.1, 0.16.2, 0.17.0, 0.17.1, 0.18.0, 0.18.1, 0.19.0, 0.19.1, 0.19.2, 0.20.0, 0.20.1, 0.20.2, 0.20.3, 0.21.0, 0.21.1, 0.22.0, 0.23.0, 0.23.1, 0.23.2, 0.23.3, 0.23.4, 0.24.0, 0.24.1, 0.24.2, 0.25.0, 0.25.1, 0.25.2, 0.25.3, 1.0.0, 1.0.1, 1.0.2, 1.0.3, 1.0.4, 1.0.5, 1.1.0, 1.1.1, 1.1.2, 1.1.3, 1.1.4, 1.1.5)
ERROR: No matching distribution found for pandas==1.3.5
```

I receive the following error:

> ERROR: No matching distribution found for pandas==1.3.5

## Background
I created a Notebook instance from the AWS Console via **AWS Sagemaker -> Notebook instances -> Create Notebook instance**.

I then selected the Kernel **conda_Python3**.

I use **sys.executable** to show the Kernel's Python, Pip and Pandas version.

```python
!{sys.executable} -version
Python 3.6.13

!{sys.executable} -m pip show pip
Name: pip
Version: 21.3.1
Summary: The PyPA recommended tool for installing Python packages.
Home-page: https://pip.pypa.io/
Author: The pip developers
Author-email: distutils-sig@python.org
License: MIT
Location: /home/ec2-user/anaconda3/envs/python3/lib/python3.6/site-packages
Requires: 
Required-by: 

!{sys.executable} -m pip show pandas
Name: pandas
Version: 1.1.5
Summary: Powerful data structures for data analysis, time series, and statistics
Home-page: https://pandas.pydata.org
Author: 
Author-email: 
License: BSD
Location: /home/ec2-user/anaconda3/envs/python3/lib/python3.6/site-packages
Requires: numpy, python-dateutil, pytz
Required-by: autovizwidget, awswrangler, hdijupyterutils, odo, sagemaker, seaborn, shap, smclarify, sparkmagic, statsmodels
```

I cannot upgrade **Pandas**.

```python
!{sys.executable} -m pip install --pre --upgrade pandas
Requirement already satisfied: pandas in /home/ec2-user/anaconda3/envs/python3/lib/python3.6/site-packages (1.1.5)
Requirement already satisfied: python-dateutil>=2.7.3 in /home/ec2-user/anaconda3/envs/python3/lib/python3.6/site-packages (from pandas) (2.8.1)
Requirement already satisfied: pytz>=2017.2 in /home/ec2-user/anaconda3/envs/python3/lib/python3.6/site-packages (from pandas) (2021.1)
Requirement already satisfied: numpy>=1.15.4 in /home/ec2-user/anaconda3/envs/python3/lib/python3.6/site-packages (from pandas) (1.18.5)
Requirement already satisfied: six>=1.5 in /home/ec2-user/anaconda3/envs/python3/lib/python3.6/site-packages (from python-dateutil>=2.7.3->pandas) (1.15.0)
```

### Root Cause Analysis
**Pandas** does not provide support for **Python 3.6** beyond Pandas version **1.1.5**.  

Earlier versions of **AWS SageMaker JupyterLab Notebooks** delivered **Python 3.6** Kernels by default, via their **Platform identifier** configuration item.

Upon launch of my notebook, I selected **Amazon Linux 1** for my **Platform identifier**, which limited my Notebook to the **Python 3.6 Kernel** which in turn caps the version of **Pandas** to **1.1.5**

I verified that my Notebook runs the **Amazon Linux 1** Operating System via the **Amazon SageMaker --> Notebook Instances --> Notebook instance settings** Console page.

![AWS Sagemaker Instance Amazon Linux 1]({static}/images/Sagemaker_Upgrade_Pandas/01_Old_Version.png)

### Solution
Through trial and error, I identified the solution to my problem.

To install the most recent version of **Pandas** into a **SageMaker JupyterLab Notebook**, I must install the most recent version of **Python**.

To install the most recent version of Python to my JupyterLab environment, I must do the following upon launch:

1.  Select the Amazon Linux 2 Operating System
2.  Select JupyterLab Version 3.0+

### Select the Amazon Linux 2 Operating System
AWS released [Amazon Linux](https://aws.amazon.com/amazon-linux-ami/) in 2010 and then an improved [Amazon Linux 2](https://aws.amazon.com/about-aws/whats-new/2017/12/introducing-amazon-linux-2/) in 2017.  

AWS [End of Life'ed (EOL)](https://aws.amazon.com/blogs/aws/update-on-amazon-linux-ami-end-of-life/) their standard support for the original Amazon Linux in late 2020.

SageMaker notebooks, however, ran on the 2010 version of Amazon Linux until August 2021, when AWS provided the option to run Sagemaker JupyterLab Notebooks on [Amazon Linux 2](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-notebook-instance-now-supports-amazon-linux-2/).

I recommend that you create SageMaker JupyterLab Notebooks with **Amazon Linux 2 based notebook instances**.

These **Amazon Linux 2 based notebook instances** support the **Python 3.8** kernel, unlike the older versions of **Amazon Linux (2010) based notebook instances**, which cap at **Python 3.6**.

The AWS developer guides catalog all the differences between [Amazon Linux 2 and Amazon Linux (2010) notebook instances](https://docs.aws.amazon.com/sagemaker/latest/dg/nbi-al2.html).

#### Execution
Upon Launch of your SageMaker JupyterLab Notebook Instance, navigate to the **Platform identifier** option.

The dropdown box provides three choices for **Platform identifier**.

![Pick Amazon Linux 2]({static}/images/Sagemaker_Upgrade_Pandas/02_Pick_Two.png)

If you select an **Amazon Linux 1** based notebook instance, the Console alerts you to the End of Life (EOL) support.

![End of Life Amazon Linux 1]({static}/images/Sagemaker_Upgrade_Pandas/03_One_Eol.png)

Select **Amazon Linux 2, JupyterLab 3**.

### Select JupyterLab Version 3.0+
Amazon SageMaker notebooks provide the JupyterLab service.  JupyterLab features a web-based Integrated Development Environment (IDE) for Python code, data and models.

Upon launch of your Notebook, AWS allows you to [choose either JupyterLab Version 1 or JupyterLab Version 3](https://docs.aws.amazon.com/sagemaker/latest/dg/nbi-jl.html)

I recommend Jupyter Lab 3, which delivers a [half dozen new  features](https://search.brave.com/search?q=jupyter+lab+3.0+features), which include:

  - Graphical Debug
    - Desktop Integrated Development Environments (IDE) ship graphical debuggers.  JupyterLab 3.0 provides a visual debugger for your Notebook.
  - Outline View/ Table of Contents (TOC)
    - Provides an Outline view for your Notebook.  Jump to different sections with the click of a mouse.
  - Wide Selection of Display Languages.
    - Install the [language pack of your choice](https://github.com/jupyterlab/language-packs/).
  - Improved Single-Document Mode
    - Remove the clutter of all the extraneous tabs and widgets.
  - Easy Extension Install
    - Install extensions without JupyterLab recompilation via Pip or Conda.

To enjoy the above features, select **Amazon Linux 2, JupyterLab 3**

![Select Amazon Linux 2, JupyterLab 3]({static}/images/Sagemaker_Upgrade_Pandas/04_Lab_Three.png)

## Success
After I launch my new **AWS SageMaker JupyterLab Notebook** I select the **conda_Python3** environment from the launcher.

![Select conda_Python3]({static}/images/Sagemaker_Upgrade_Pandas/05_Conda_Three.png)

In my notebook I check for the Python version and the output reads **3.8**.

Good Sign!

```python
!{sys.executable} --version
Python 3.8.12
```

Pip and Pandas read version **22.0.4** and **1.3.4** respectively.

```python
!{sys.executable} -m pip show pip
Name: pip
Version: 22.0.4
Summary: The PyPA recommended tool for installing Python packages.
Home-page: https://pip.pypa.io/
Author: The pip developers
Author-email: distutils-sig@python.org
License: MIT
Location: /home/ec2-user/anaconda3/envs/python3/lib/python3.8/site-packages
Requires: 
Required-by: 

!{sys.executable} -m pip show pandas
Name: pandas
Version: 1.3.4
Summary: Powerful data structures for data analysis, time series, and statistics
Home-page: https://pandas.pydata.org
Author: The Pandas Development Team
Author-email: pandas-dev@python.org
License: BSD-3-Clause
Location: /home/ec2-user/anaconda3/envs/python3/lib/python3.8/site-packages
Requires: numpy, python-dateutil, pytz
Required-by: autovizwidget, hdijupyterutils, sagemaker, seaborn, shap, smclarify, sparkmagic, statsmodels
```

I use the notebook to upgrade **Pandas**.

```python
!{sys.executable} -m pip install --pre --upgrade pandas
Looking in indexes: https://pypi.org/simple, https://pip.repos.neuron.amazonaws.com
Requirement already satisfied: pandas in /home/ec2-user/anaconda3/envs/python3/lib/python3.8/site-packages (1.3.4)
Collecting pandas
  Downloading pandas-1.5.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (12.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.2/12.2 MB 48.4 MB/s eta 0:00:0000:0100:01
Requirement already satisfied: numpy>=1.20.3 in /home/ec2-user/anaconda3/envs/python3/lib/python3.8/site-packages (from pandas) (1.20.3)
Requirement already satisfied: python-dateutil>=2.8.1 in /home/ec2-user/anaconda3/envs/python3/lib/python3.8/site-packages (from pandas) (2.8.2)
Requirement already satisfied: pytz>=2020.1 in /home/ec2-user/anaconda3/envs/python3/lib/python3.8/site-packages (from pandas) (2021.3)
Requirement already satisfied: six>=1.5 in /home/ec2-user/anaconda3/envs/python3/lib/python3.8/site-packages (from python-dateutil>=2.8.1->pandas) (1.16.0)
Installing collected packages: pandas
  Attempting uninstall: pandas
    Found existing installation: pandas 1.3.4
    Uninstalling pandas-1.3.4:
      Successfully uninstalled pandas-1.3.4
Successfully installed pandas-1.5.1
```

The output reads:

> Successfully installed pandas-1.5.1

Success!!!

### Create a Lifecycle Config
A Sagemaker Lifecycle Configuration allows you to upgrade Pandas at launch.

When you log into your Notebook for the first time, the Notebook will present to you the most recent version of Pandas.

In Amazon Sagemaker, click **Lifecycle configurations --> Notebook Instance --> Create Configuration**.

![Create Configuration]({static}/images/Sagemaker_Upgrade_Pandas/06_Create_Config.png)

I name my lifecycle config **sobanski-update-pandas**.

![Paste in Bash Script]({static}/images/Sagemaker_Upgrade_Pandas/07_Lifecycle_Config.png)

Paste the following script under **Start notebook**.

```bash
#!/bin/bash

set -e

# OVERVIEW
# This script installs a single pip package in a single SageMaker conda environments.

sudo -u ec2-user -i <<'EOF'
# PARAMETERS
PACKAGE=pandas
ENVIRONMENT=python3
source /home/ec2-user/anaconda3/bin/activate "$ENVIRONMENT"
pip install --upgrade "$PACKAGE"
source /home/ec2-user/anaconda3/bin/deactivate
EOF
```

The script upgrades **Pandas** in the **conda_Python3** environment.

Under **Amazon SageMaker --> Notebook instances --> Notebook instance settings** select **Edit** and set **Lifecycle configuration** to the name of your file.

![Select your config]({static}/images/Sagemaker_Upgrade_Pandas/08_Select_Config.png)

When you launch the notebook, AWS will run the upgrade script.

## Conclusion
**AWS SageMaker Notebook Instances** host and manage **JupyterLab Notebooks**.  In this blog post we discussed how to configure your **Notebook Instance** to maximize the available features in Pandas and JupyterLab.

![Python Pandas]({static}/images/Sagemaker_Upgrade_Pandas/09_Pet_Python.png)

Note:  I created the Panda/ Python artwork with Jasper AI Art, see workflow [here]({filename}/jasper-art.md)
