Title: Data Exploration with Data Viz Cheat Sheet
Date: 2023-09-30 10:26
Author: john-sobanski
Category: Data Science
Tags: Python, Pandas, Machine Learning, Data Science
og_image: images/Analytics_Cheat_Sheet/07_Twentyfive_Bins.png
twitter_image: images/Analytics_Cheat_Sheet/07_Twentyfive_Bins.png
Slug: analytics-cheat-sheet
Status: published 

Today I collect and organize useful data visualization (Data Viz) tools that aid data exploration.  

I illustrate the use of the tools via the classic **Abalone** database, hosted on the University of California, Irvine (UCI) Machine Learning repository website.

I recommend you bookmark this and return to it when you need to find the syntax and semantics of popular data viz constructs.

## Get the Data
PhD student David Aha created the University of California, Irvine (UCI) Machine Learning repository in 1987 in the form of a File Transfer Protocol (FTP) site.  The Repo collects databases, domain theories, and data generators.  Today I use the [Abalone](https://archive.ics.uci.edu/dataset/1/abalone) database.

The **Abalone** database provides a table of four thousand observations, which each contain one categorical feature, seven continuous features, and one target:

  -  Features, Categorical
     -  Sex: Male, Female, and Infant		
  -  Features, Continuous
     -  Length: Longest shell measurement (mm)
     -  Diameter: Perpendicular to length (mm)
     -  Height: With meat in the shell (mm)
     -  Whole_weight: Whole abalone (grams)
     -  Shucked_weight: Weight of meat (grams)
     -  Viscera_weight:	Gut weight after bleeding (grams)
     -  Shell_weight: After being dried (grams)
  -  Target, Integer
     -  Rings: +1.5 gives the age in years		


I use the Python **requests** library to pull the data straight from the UCI repo and stuff it into a Pandas DataFrame.

I import the required libraries.

```python
import pandas as pd
import numpy as np
import io
import requests
import seaborn as sns
```

I set the **url** (String) and **column_name** (List) variables to match the **Abalone** database schema.

```
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data'
column_names = ['Sex',
                'Length',
                'Diameter',
                'Height',
                'Whole_weight',
                'Shucked_weight',
                'Viscera_weight',
                'Shell_weight',
                'Rings']
```

**Requests** downloads the HTTP object, **StringIO** decodes it and **Pandas** loads the decoded data into a DataFrame.

```
r = requests.get(url).content
abalone_df = pd.read_csv(io.StringIO(r.decode('utf-8')),
                      names = column_names)
```

## One-Dimensional Statistical Summaries
We first explore the data in one dimension.

### Histograms
Histograms provide a visual shorthand for the distribution of numerical data.  Think of a **connect four** board, where you stack chips in different columns (or buckets).  Each chip represents a number in that bucket. 

Pandas provides a built-in **hist()** method.

```python
abalone_df['Rings'].hist()
```

We use Pandas to draw a Histogram of our target variable, **Rings**.

![Rings Hist]({static}/images/Analytics_Cheat_Sheet/01_Rings_Hist.png)

Most **Abalone** include between 7.5 and 12.5 Rings.

Pandas also accommodates our **Categorical** feature.

```python
abalone_df['Sex'].hist()
```

![Sex Hist]({static}/images/Analytics_Cheat_Sheet/02_Sex_Hist.png)

The corpus of data includes roughly equal observations for **Male, Female** and **Infant**.

Pandas allows us to run **histograms** on all **features**.  The method ignores the **Categorical** feature.

```python
abalone_df.plot.hist(subplots=True,layout=(4,2))
```

![All Hist]({static}/images/Analytics_Cheat_Sheet/03_All_Hist.png)

The results illustrate the need to **Normalize** the data, since all the Categorical features clock in under a value of **one** (1), and the target feature includes ranges up to **thirty** (30).

### Hist with tags
[InfluxDB]({tag}influxdb) uses the nomenclature **Tags** and **Measurements** to describe **Categorical** and **Continuous** variables.

Tags provide a new dimension of visual data, **slicing and dicing** the data into different categories.

Seaborn provides the option to color by **Tag** with their **hue** parameter.

```python
sns.histplot(data=abalone_df, x='Rings',hue='Sex')
```

![Sex Hue]({static}/images/Analytics_Cheat_Sheet/04_Sex_Hue.png)

**Hue** does not make sense with **Measurements**:

```python
sns.histplot(data=abalone_df, x='Rings',hue='Rings')
```

![Stupid Hist]({static}/images/Analytics_Cheat_Sheet/05_Stupid_Hist.png)

### Kernel Density Estimation (KDE)
Kernel Density Estimation (KDE) smooths the Histograms.  Instead of discrete buckets, we see continuous lines that represent the distribution.

I used the analogy above of a Histogram stacking chips on a connect four board.  KDE pours sand at each point, enough to fill a Standard Normal Distribution.  KDE in a sense stacks Standard Normal Distributions at each point, which leads to the smoothness of the plot.

If you reduce the bucket size to a very small number, you can see the idea in action.

```python
abalone_df['Whole_weight'].hist()
```

![Default Bins]({static}/images/Analytics_Cheat_Sheet/06_Default_Bins.png)

```python
abalone_df['Whole_weight'].hist(bins=25)
```

![Twentyfive Bins]({static}/images/Analytics_Cheat_Sheet/07_Twentyfive_Bins.png)

```python
abalone_df['Whole_weight'].hist(bins=50)
```

![Fifty Bins]({static}/images/Analytics_Cheat_Sheet/08_Fifty_Bins.png)

```python
abalone_df['Whole_weight'].plot.kde()
```

![Infinite Bins]({static}/images/Analytics_Cheat_Sheet/09_Infinite_Bins.png)

SNS will plot the KDE over the histogram if you instruct it to do so:

```python
sns.histplot(data=abalone_df, x="Whole_weight", kde=True)
```

![Kde Hist]({static}/images/Analytics_Cheat_Sheet/10_Kde_Hist.png)

Pandas plots all features' distribution with KDE.

```python
abalone_df.plot.kde(subplots=True,layout=(4,2))
```

![All Kde]({static}/images/Analytics_Cheat_Sheet/11_All_Kde.png)

## Boxplots
A glance at a Boxplot tells you the median, 25th percentile, 75th percentile, and outliers.

The box shows the First and Third quartiles and the whiskers show data points that lie 1.5 times the Interquartile range (IQR) (for both top and bottom).

```python
sns.boxplot(data=abalone_df, x='Whole_weight')
```

![Weight Box]({static}/images/Analytics_Cheat_Sheet/12_Weight_Box.png)

SNS allows you to separate the chart by **Tag**.  If you set **y** equal to **Sex**, for example, you see the distributions split by **Male, Female, and Infant**.

```python
sns.boxplot(data=abalone_df, x='Whole_weight',y='Sex')
```

![Sex Box]({static}/images/Analytics_Cheat_Sheet/13_Sex_Box.png)

In the Boxplot above, we see that Female **Abalone** weigh slightly more than Male **Abalone**.

### Special Note: Enrich Data.
Remember that we have a **target** variable named **Rings**, which encompasses a range of numbers between one (1) and thirty (30).  I recommend you enrich the **Rings** data with a new **Tag**.

The following code uses the **Rings** value to set a new **Tag**, which I named **Age**.  The code splits the data into three ranges and applies to a given observation the tag **Young, Middle_Age or Old** based on the value of **Rings**.

```
abalone_df['Age'] = pd.qcut(abalone_df['Rings'],q=3,labels=['Young','Middle_Age','Old'])
abalone_df.head()
```

This new tag provides a new dimension to slice and dice our Boxplot.

```python
sns.boxplot(data=abalone_df, x='Whole_weight',y='Sex',hue='Age')
```

![Age Box]({static}/images/Analytics_Cheat_Sheet/14_Age_Box.png)

We now see the relationship between **Whole_weight**, **Sex** and **Age** at a glance.

## Violinplots
A Violinplot mirrors the Distribution, which gives the plot a Violin-like shape.

```python
sns.violinplot(x=abalone_df['Rings'])
```

![Rings Violin]({static}/images/Analytics_Cheat_Sheet/15_Rings_Violin.png)

Violinplots also accommodate Tags.

```python
sns.violinplot(data=abalone_df,x='Sex',y='Whole_weight',hue='Age')
```
![Violin Tags]({static}/images/Analytics_Cheat_Sheet/16_Violin_Tags.png)

## Two-dimensional Plots
Python provides tools to explore Bivariate data sets.

Seaborn (SNS) provides two-dimensional Histograms and two-dimensional KDE tools.

### Two-dimensional Histogram
Note that SNS only shows the top-down view for histograms.

```python
sns.displot(abalone_df, x="Length", y="Height")
```

![Two Hist]({static}/images/Analytics_Cheat_Sheet/17_Two_Hist.png)

The SNS Bivariate Histograms accommodate tags.

```python
sns.displot(abalone_df, x="Length", y="Height", hue="Age")
```

![Two Tag]({static}/images/Analytics_Cheat_Sheet/18_Two_Tag.png)

### Two-dimensional KDE
SNS also provides two-dimensional KDE plots, with **Tags**.

```python
sns.displot(abalone_df, x="Length", y="Height", hue="Age", kind="kde")
```

![Two Kde]({static}/images/Analytics_Cheat_Sheet/19_Two_Kde.png)

## Look for Correlation
The Data Scientist looks for correlation between features and the target during the Data Exploration phase of the Machine Learning Pipeline

### Data prep
In the Data Prep stage, we encode the **Tags** (String) into **numeric values** (float32).

The Pandas method **get_dummies** one-hot-encodes the **Sex** variable into Orthogonal dimensions.  This increases the dimensionality of our data set.

We also use the **factorize** method to convert **Young, Middle_Aged and Old** into the integers **0,1 and 2**.

 
```python
abalone_reg_df = abalone_df.join(pd.get_dummies(abalone_df['Sex']))
abalone_reg_df['Age_Bucket'] = pd.factorize(abalone_df['Age'],sort=True)[0]
abalone_reg_df = abalone_reg_df.drop(['Sex','Age'],axis=1).astype(np.float32)
```

We pop off the labels for later use.

**class_labels** stores the target vector for **Classification** models, and **reg_labels** stores the target vector for **Regression** models.

```python
class_labels = abalone_reg_df.pop('Age_Bucket')
reg_labels = abalone_reg_df.pop('Rings')
```

I also create vectors to pull like **Features** from the DataFrame (Measurements, Tags, Target).

```python
metric_vars = ['Length',
               'Diameter',
               'Height',
               'Whole_weight',
               'Shucked_weight',
               'Viscera_weight',
               'Shell_weight']

encoded_vars = ['F',
                'I',
                'M']
				
y_vars = ['Rings']
```


### Heatmap correlation
SNS provides a **Heatmap** matrix for correlation.

```python
import matplotlib as plt

corr = abalone_reg_df.corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr,
                            dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 
                             20,
                             as_cmap=True)

# Draw the heatmap with the mask and 
# correct aspect ratio
sns.heatmap(corr, 
            mask=mask,
            cmap=cmap,
            vmax=1,
            center=0,
            square=True,
            linewidths=.5,
            cbar_kws={"shrink": .5})
```

![Corr Matrix]({static}/images/Analytics_Cheat_Sheet/20_Corr_Matrix.png)

We see that **Diameter** and **Length** have significant correlation and so do all of the **weight** features.


### Pairgrid Correlation
This SNS Pairgrid plot shows the correlation between the features and the target, **Rings**.

```python
g = sns.PairGrid(abalone_df,
                 x_vars = metric_vars,
                 y_vars = y_vars)
g.map_offdiag(sns.kdeplot)
g.add_legend()
```

![Pair Grid]({static}/images/Analytics_Cheat_Sheet/21_Pair_Grid.png)

All **features** depict a correlation slope close to around 25 degrees or so, which indicates Correlation.

### Scatterplot with Regression
SNS plots the ML 101 favorite, Linear Regression right on the screen with the **regplot** action.

```python
sns.regplot(x = abalone_df['Viscera_weight'],
                y = abalone_df['Rings'])
```

![Reg Plot]({static}/images/Analytics_Cheat_Sheet/22_Reg_Plot.png)

We see positive slope with pretty tight error bands, which indicates **Viscera_weight** predicts **Rings**.

### Fancy Tilted 3d Plots
Remember that SNS only graphs **top-down** views.  I wrote the following **matplotlib** function to show an isometric view of the data.

```python
def plot_3d(df, target, feature1, 
            feature2, feature3):
    target_list = list(set(df[target]))
    fig = plt.figure(figsize = (12, 12))
    ax1 = fig.add_subplot(111, 
                          projection='3d')

    x3 = df.loc[df[target] == target_list[0]][feature1]
    y3 = df.loc[df[target] == target_list[0]][feature2]
    z3 = df.loc[df[target] == target_list[0]][feature3]
    ax1.scatter(x3, 
                y3,
                z3,
                label = target_list[0],
                color = "red")

    x3 = df.loc[df[target] == target_list[1]][feature1]
    y3 = df.loc[df[target] == target_list[1]][feature2]
    z3 = df.loc[df[target] == target_list[1]][feature3]
    ax1.scatter(x3,
                y3,
                z3,
                label = target_list[1],
                color = "green")
    
    x3 = df.loc[df[target] == target_list[2]][feature1]
    y3 = df.loc[df[target] == target_list[2]][feature2]
    z3 = df.loc[df[target] == target_list[2]][feature3]
    ax1.scatter(x3,
                y3,
                z3,
                label = target_list[2],
                color = "blue")

    ax1.legend()
```

I call the function with the **Abalone** data.

```python
plot_3d(abalone_df,
        'Age',
        'Height',
        'Viscera_weight',
        'Length')
```

![Three Dee]({static}/images/Analytics_Cheat_Sheet/23_Three_Dee.png)

## Dimensionality Reduction
Note my Graph above requires me to choose **three** (out of the possible **eight**) features at a time.  This fact drives two questions:

- Which features do I use?
- How can I plot all the features at once?

Principal Component Analysis (PCA) collapses the information held in **eight** features into **three**, **two** or even **one** feature.

I write about PCA in my blog post on [Regression with Keras and TensorFlow]({filename}/fast-and-easy-regression-with-tensorflow-part-2.md)

> If you stick a magnet at each point in the data space, and then stick a telescoping iron bar at the origin, the magnets will pull the bar into position and stretch the bar. The bar will wiggle a bit at first and then eventually settle into a static position. The final direction and length of the bar represent a principal component. We can map the higher dimensionality space to the principal component by connecting a string directly from each magnet to the bar. Where the string hits (taut) we make a mark. The marks represent the mapped vector space.

George Dallas also writes an excellent blog post that [explains PCA](https://georgemdallas.wordpress.com/2013/10/30/principal-component-analysis-4-dummies-eigenvectors-eigenvalues-and-dimension-reduction/).

### Normalize
First Normalize the Data.  TensorFlow provides a **normalizer**.

```python
from tensorflow.keras.layers.experimental import preprocessing

normalizer = preprocessing.Normalization()
```

Fit the **normalizer** to our **measurements** (exclude the encoded tags).

```
normalizer.adapt(np.array(abalone_reg_df[metric_vars]))
```

### One Principal Component
SciKitLearn provides **PCA**.

```python
from sklearn.decomposition import PCA
```

The following code collapses all seven **features** into one **Principal Component**.

```python
pca = PCA(n_components=1)
pca.fit(normalizer(abalone_reg_df[metric_vars]))
pca_abalone_df = pd.DataFrame(pca.transform(normalizer(abalone_reg_df[metric_vars])),
                                     columns = ['princomp1'],
                                     index=abalone_reg_df.index)
```

SNS shows the utility of this **Principal Component** on the separability of the **Classes**.

```python
sns.histplot( x = pca_abalone_df['princomp1'],
              hue = class_labels)
```	  

![One Princomp]({static}/images/Analytics_Cheat_Sheet/24_One_Princomp.png)
	  
## Two Principal Components
Now derive two principal components.

```python
pca = PCA(n_components=2)
pca.fit(normalizer(abalone_reg_df[metric_vars]))
pca_train_features_df = pd.DataFrame(pca.transform(normalizer(abalone_reg_df[metric_vars])),
                                     columns = ['princomp1',
                                                'princomp2'],
                                     index=abalone_reg_df.index)
```

A KDE plot shows the three classes in relation to the two **Principal Components**.

```python			
sns.kdeplot( data = pca_train_features_df,
             x = pca_train_features_df['princomp1'],
             y = pca_train_features_df['princomp2'],
             hue = class_labels,
             fill = False)
```	 

![Two Princomp]({static}/images/Analytics_Cheat_Sheet/25_Two_Princomp.png)

## 3 Principal Components
Astute readers anticipate the slight code modifications required to derive three **Principal Components**.

```python
pca = PCA(n_components=3)
pca.fit(normalizer(abalone_reg_df[metric_vars]))
pca_train_features_df = pd.DataFrame(pca.transform(normalizer(abalone_reg_df[metric_vars])),
                                     columns = ['princomp1',
                                                'princomp2',
												'princomp3'],
                                     index=abalone_reg_df.index)
```

We use the **3d** plot to see the separation of classes in relation to three **Principal Components**.

```python			 
data_df = pca_train_features_df.assign(outcome=class_labels)
plot_3d(data_df,
        'outcome',
        'princomp1',
        'princomp2',
        'princomp3')
```

![Three Princomp]({static}/images/Analytics_Cheat_Sheet/26_Three_Princomp.png)

If you include one-hot encoded variables in your PCA, you may see weird results.

For example, we encoded the **Categorical** **Sex** feature into three **Orthogonal** numeric vectors, one for **M, F and I**.  If you keep these vectors in the PCA you will see the following:

![Sex Princomp]({static}/images/Analytics_Cheat_Sheet/27_Sex_Princomp.png)

## Conclusion
Bookmark this page for future reference.  It provides a handy **Cheat Sheet** for useful Python Data Exploration and Data Viz tools.