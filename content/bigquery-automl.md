Title: Juice Your In-Situ Machine Learning with BigQuery AutoML
Date: 2021-06-26 01:23
Author: john-sobanski
Category: Data Science
Tags: GCP, Neural Networks, Machine Learning, Data Science
Slug: bigquery-automl
Status: published

Data Scientists need skill and experience to create useful Machine Learning (ML) models.  ML activities include tool selection, training logistic decisions (move data to training vs. train in-situ), data acquisition, data cleaning, data quality checks, feature engineering, algorithm selection and hyperparameter tuning.

Algorithm selection and hyperparameter tuning drive tedious manual processes where the Data Scientist must flip a switch, turn a knob, train the model and then cross her fingers.  The Google Cloud Platform (GCP) Big Query Machine Learning (BQML) service provides two wins for Data Scientists:

1. The ability to train data in place (a must for PetaByte scale **Big Data** sets)
2. The ability to execute AutoML in place

This blog post demonstrates how to execute AutoML in-situ via the [GCP BQML](https://cloud.google.com/bigquery-ml/docs) service.

## Background
In previous blog posts I used several platforms to train models on tabular data: TensorFlow, Google Cloud Platform (GCP) AutoML Tables, and BigQuery BQML.

-  [Fast and Easy Regression with Keras and TensorFlow 2.3 (Part 1 - Data Exploration & First Models)]({filename}/fast-and-easy-regression-with-tensorflow.md)
-  [Fast and Easy Regression with Keras and TensorFlow 2.3 (Part 2 - Dimensionality Reduction)]({filename}/fast-and-easy-regression-with-tensorflow-part-2.md)
-  [Fast and Easy ML Optimization with GCP AutoML Tables (Beta)]({filename}/fast-and-easy-automl-optimize.md)
-  [Don't Move Your Data! In-Situ Machine Learning via BigQuery]({filename}/bigquery-ml.md)

The blog posts above capture a variety model training approaches:

-  Hand crafted models using Python Objects (Tensorflow)
-  AutoML using a GCP Application Programming Interface (API) (AutoML tables)
-  Hand crafted models using SQL commands (BigQuery)

This blog post demonstrates how to use the BigQuery BQML service to trigger AutoML workflows in-situ.  The AutoML service runs through a variety of ML Algorithms and iterates through a range of hyperparameter settings for each algorithm.  The service then keeps and serves the **winning** approach.

## AutoML Regressor
[Last month]({filename}/bigquery-ml.md) we used SQL syntax to command BigQuery to train a linear regression model in-situ. Open [that blog]({filename}/bigquery-ml.md) post in a new tab to review the steps required to train models in BigQuery.

We used the following SQL statement to train a linear regression model, with the **model_type** set to **LINEAR_REG** in the SQL **OPTIONS** :

```sql
CREATE MODEL `shining-chain.wine_dataset.model`
OPTIONS(model_type='LINEAR_REG') AS 
SELECT 
  alcohol,
  chlorides,
  citric_acid,
  density,
  fixed_acidity,
  free_sulfur_dioxide,
  ph,
  quality AS label,
  residual_sugar,
  sulphates,
  total_sulfur_dioxide,
  volatile_acidity
FROM
  `shining-chain.wine_dataset.model.wine_red`
```

Our model kept the default parameters for the training algorithm.

We can improve model performance through **hyper parameter** tuning.  In the old days, we needed to tune these parameters by hand.  [GCP, however, provides AutoML services (e.g. AutoML tables)]({filename}/fast-and-easy-automl-optimize.md) to automatically tune these parameters.

> BigQuery now provides a Beta service to execute in-situ AutoML.

To use BigQuery AutoML, simply set your SQL OPTIONS to **AUTOML_REGRESSOR**.

![Automl Query]({filename}/images/Bigquery_Automl/19_Automl_Query.png)

> Note: We direct BigQuery to save the new model under the name **automl_model**.

```sql
CREATE MODEL `shining-chain.wine_dataset.automl_model`
OPTIONS(model_type='AUTOML_REGRESSOR') AS 
SELECT 
  alcohol,
  chlorides,
  citric_acid,
  density,
  fixed_acidity,
  free_sulfur_dioxide,
  ph,
  quality AS label,
  residual_sugar,
  sulphates,
  total_sulfur_dioxide,
  volatile_acidity
FROM
  `shining-chain.wine_dataset.wine_red`
```

BigQuery AutoML iterates through many hyperparameter scenarios, each which investigate the effects of choices related to learning rate, regularization and optimizers.  You will notice that AutoML consumes a much larger portion of **wall clock** time in comparison to our single Regression model above.

![Training Pic]({filename}/images/Bigquery_Automl/20_Training.png)

Click **Execution Details** to get more status information.

![Training Pic 2]({filename}/images/Bigquery_Automl/21_Training_2.png)

Upon completion, BigQuery stores our new **automl_model** in the **wine_dataset** Dataset, which lives in the **shining_chain** project.

The AutoML process completes in about fifty (50) or so minutes.

![AutoML Done]({filename}/images/Bigquery_Automl/22_AutoML_Done.png)

## AutoML Regressor Results
The **results** tab reports a reduction in Mean Square Error (MSE), compared to the prior Linear Regression model that used default parameters.

![Automl Results]({filename}/images/Bigquery_Automl/23_Automl_Results.png)

The MSE maps to a Root Mean Square Error (RMSE) of about 0.6393.

Several months ago [we used TensorFlow and Google Cloud Platform AutoML to train several models on the Wine Quality Dataset]({filename}/fast-and-easy-automl-optimize.md) and compare the results.  In January, we used [BigQuery Linear Regression with default Hyperparameters]({filename}/bigquery-ml.md) to train the Wine Quality Dataset.

Let's compare the RMSE of **BQML'S AUTOML_REGRESSOR** (0.6393) against these prior experiments.

The following table captures the results:

Rank | Platform | Approach | Dims | RMSE
-|-|-|-|-
1 | GCP | AutoML Tables | 11 | 0.598
2 | TensorFlow | Linear Model | 7 | 0.633
3 | BigQuery   | AutoML | 11 | 0.639
4 | TensorFlow | DNN | 7 | 0.645
5 | TensorFlow | DNN | 11 | 0.648
6 | BigQuery | Linear | 11 | 0.661
7 | TensorFlow | Linear Model | 11 | 0.706
8 | TensorFlow | Linear Model | 2 | 0.735
9 |Pandas | Guess Mean | N/A | 0.801

BigQuery AutoML under-performs compared to [GCP AutoML Tables]({filename}/fast-and-easy-automl-optimize.md) and a [dimensionality reduced TensorFlow model]({filename}/fast-and-easy-regression-with-tensorflow-part-2.md).

## Serve Model
After training, BigQuery saves and serves the new model in place.

We use **SQL** to use the served model.  In the BigQuery console, click **QUERY MODEL**.

![Query Model]({filename}/images/Bigquery_Automl/24_Query_Model.png)

The following SQL command pulls the first record out of the Wine Quality data set and then sets the **alcohol** parameter to 80%.

```sql
SELECT
  80 AS alcohol,
  chlorides,
  citric_acid,
  density,
  fixed_acidity,
  free_sulfur_dioxide,
  ph,
  residual_sugar,
  sulphates,
  total_sulfur_dioxide,
  volatile_acidity
FROM 
    `shining-chain.wine_dataset.wine_red`
LIMIT 1
```

The above **QUERY** returns the following **JSON.**

```json
[
  {
    "alcohol": "80",
    "chlorides": "0.074",
    "citric_acid": "0.66",
    "density": "1.0008",
    "fixed_acidity": "11.6",
    "free_sulfur_dioxide": "10.0",
    "ph": "3.25",
    "residual_sugar": "2.2",
    "sulphates": "0.57",
    "total_sulfur_dioxide": "47.0",
    "volatile_acidity": "0.58"
  }
]
```

The following screengrab captures the console view of this **QUERY**:

![Predict Data]({filename}/images/Bigquery_Automl/25_Predict_Data.png)

The **SQL QUERY** below pulls and modifies the first record from the Wine Quality data set and then pipes it to the **automl_model** we trained via **AUTOML_REGRESSOR**.

At a high level, we **SELECT** the predicted score of a wine with 80% alcohol **FROM** our model:

```sql
SELECT
  predicted_label
FROM
  ML.PREDICT(MODEL `shining-chain.wine_dataset.automl_model`, (
SELECT
  80 AS alcohol,
  chlorides,
  citric_acid,
  density,
  fixed_acidity,
  free_sulfur_dioxide,
  ph,
  residual_sugar,
  sulphates,
  total_sulfur_dioxide,
  volatile_acidity
FROM 
    `shining-chain.wine_dataset.wine_red`
LIMIT 1
  ) )
```

The console returns the predicted **quality**.

![Predicted API]({filename}/images/Bigquery_Automl/26_Predicted_API.png)

The model predicts a **quality** score (taste) of 1.7 out of 10 for a wine with 80% alcohol, which I consider reasonable.

```json
[
  {
    "predicted_label": "1.7691493034362793"
  }
]
```

## Boosted Tree
For fun, let's look at the success of an [ensemble method](https://en.wikipedia.org/wiki/Ensemble_learning).  

BQML provides a **BOOSTED_TREE_REGRESSOR**, which we select via **SQL OPTIONS**.  

```sql
CREATE MODEL `shining-chain.wine_dataset.boost_model`
OPTIONS(model_type='BOOSTED_TREE_REGRESSOR') AS 
SELECT 
  alcohol,
  chlorides,
  citric_acid,
  density,
  fixed_acidity,
  free_sulfur_dioxide,
  ph,
  quality AS label,
  residual_sugar,
  sulphates,
  total_sulfur_dioxide,
  volatile_acidity
FROM `shining-chain.wine_dataset.wine_red`
```

The model takes six minutes to train.

![Boost Model]({filename}/images/Bigquery_Automl/27_Boost_Model.png)

The model results in an MSE of 0.3419, with an RMSE of 0.5847.

![Boost Results]({filename}/images/Bigquery_Automl/28_Boost_Results.png)

The **BQML BOOSTED_TREE_REGRESSOR** bests **GCP AutoML Tables** and lands in first place!

Rank | Platform | Approach | Dims | RMSE
-|-|-|-|-
1 | BigQuery | Boosted Tree | 11 | 0.585
2 | GCP | AutoML Tables | 11 | 0.598
3 | TensorFlow | Linear Model | 7 | 0.633
4 | BigQuery   | AutoML | 11 | 0.639
5 | TensorFlow | DNN | 7 | 0.645
6 | TensorFlow | DNN | 11 | 0.648
7 | BigQuery | Linear | 11 | 0.661
8 | TensorFlow | Linear Model | 11 | 0.706
9 | TensorFlow | Linear Model | 2 | 0.735
10 |Pandas | Guess Mean | N/A | 0.801

## Dimensionality Reduced BQML
Too many features drive over-fitting which increases RMSE.

In a past blog post, we demonstrated that [dimensionality reduction through Principal Component Analysis (PCA) reduces over-fitting and reduces RMSE]({filename}/fast-and-easy-regression-with-tensorflow-part-2.md)

The last part of this blog post feeds a dimensionality reduced **Wine Quality Dataset** to the **BQML BOOSTED_TREE_REGRESSOR** algorithm.

We will briefly run through the steps to apply PCA to the **Wine Quality Dataset.**

First, import the necessary Python libraries and then pull the data off the University of Irvine's website and stuff it into a **Pandas Data Frame**.

```python
import pandas as pd
import numpy as np
import io
import requests
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
r = requests.get(url).content
column_names = ['fixed_acidity',
                'volatile_acidity',
                'citric_acid',
                'residual_sugar',
                'chlorides',
                'free_sulfur_dioxide',
                'total_sulfur_dioxide',
                'density',
                'ph',
                'sulphates',
                'alcohol',
                'quality']
wine_df = pd.read_csv(io.StringIO(r.decode('utf-8')), 
                      sep =";",
                      header = 0,
                      names= column_names).astype(np.float32)
```

Next, separate the Dataframe into a **features** Dataframe and **label** series.

```python
wine_features_df = wine_df.copy()
wine_labels_series = wine_features_df.pop('quality')
```

TensorFlow allows us to create a normalization engine for our **features** Dataframe.

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

normalizer = preprocessing.Normalization()
normalizer.adapt(np.array(wine_features_df))
```

**Sklearn** provides a PCA engine.  We pipe the **features** Dataframe to the normalization engine and then to the PCA engine, and request the first seven principal components.

```python
from sklearn.decomposition import PCA
pca = PCA(n_components=7)
pca.fit(normalizer(wine_features_df))
pca_features_df = pd.DataFrame(pca.transform(normalizer(wine_features_df)),
                                     columns = ['princomp1',
                                                'princomp2',
                                                'princomp3',
                                                'princomp4',
                                                'princomp5',
                                                'princomp6',
                                                'princomp7',
                                               ],
                                     index=wine_features_df.index)

```

We then pop the labels back onto the normalized, dimensionality reduced Dataframe and save it in a Comma Separated Value (CSV) encoded file.

```python
pca_wine_df = pca_features_df.assign(quality=wine_labels_series)
pca_wine_df.to_csv('pca_wine_df.csv',index=False)
```

The following output records the first ten lines of the CSV:

```csv
princomp1,princomp2,princomp3,princomp4,princomp5,princomp6,princomp7,quality
-1.6195179763728917,0.4509726853737244,-1.7744612972264329,0.04374371633307103,0.0670156612925275,-0.9139218906561226,-0.1610332757006941,5.0
-0.7991612763626295,1.856561351520203,-0.9116754264684358,0.5480739949151788,-0.01839571398165714,0.929709236000912,-1.0098350218068104,5.0
-0.7484768531031628,0.8820469715571214,-1.1713842697588999,0.41102911926788793,-0.043535655196972736,0.40147666614026,-0.539553150939102,5.0
2.357677805002114,-0.269982797056245,0.24348912259870834,-0.9284469679531109,-1.4991502738904028,-0.13102232409979334,0.34428774245741034,6.0
-1.6195179763728917,0.4509726853737244,-1.7744612972264329,0.04374371633307103,0.0670156612925275,-0.9139218906561226,-0.1610332757006941,5.0
-1.583695657944522,0.5692157167619253,-1.5382922454632044,0.02375291374041369,-0.11007403103710495,-0.993628380100469,-0.10964916626917803,5.0
-1.1014601399705353,0.6080257636816654,-1.0759111926105813,-0.343950360931988,-1.1333873126112808,0.1750035123630711,0.26101076781023663,5.0
-2.2487136084125905,-0.4168236213171013,-0.9868407617813321,-0.0011977615992119378,-0.7804374122971008,0.2860584721236257,0.1314469559051279,7.0
-1.0868804709342004,-0.3085531414570113,-1.5181578596509828,0.003318878620501723,-0.22672738691574854,-0.5126291605993216,0.2496169604878968,7.0
```

We [upload the CSV into BigQuery using the console]({filename}/bigquery-ml.md) and execute the following SQL to train a **BOOSTED_TREE_REGRESSOR** model on the dimensionality reduced dataset.

```sql
CREATE MODEL `shining-chain.pca_wine.pca_boost_model`
OPTIONS(model_type='BOOSTED_TREE_REGRESSOR') AS 
SELECT 
  princomp1,
  princomp2,
  princomp3,
  princomp4,
  princomp5,
  princomp6,
  princomp7,
  quality AS label
FROM `shining-chain.pca_wine.pca_wine`
```

The model takes six minutes to train.

![Boost Model on PCA Data]({filename}/images/Bigquery_Automl/29_Pca_Boost.png)

Click the Evaluation tab to find a **MSE** of **0.3771**, which maps to an **RMSE** of **0.6140**.

![Boost Model on PCA Evaluation]({filename}/images/Bigquery_Automl/30_Pca_Eval.png)

The dimensionality reduced data set proves less successful than the full featured data set, and lands in third place.

Rank | Platform | Approach | Dims | RMSE
-|-|-|-|-
1 | BigQuery | Boosted Tree | 11 | 0.585
2 | GCP | AutoML Tables | 11 | 0.598
3 | BigQuery | Boosted Tree | 7 | 0.614
4 | TensorFlow | Linear Model | 7 | 0.633
5 | BigQuery   | AutoML | 11 | 0.639
6 | TensorFlow | DNN | 7 | 0.645
7 | TensorFlow | DNN | 11 | 0.648
8 | BigQuery | Linear | 11 | 0.661
9 | TensorFlow | Linear Model | 11 | 0.706
10 | TensorFlow | Linear Model | 2 | 0.735
11 |Pandas | Guess Mean | N/A | 0.801

## Conclusion
Data Scientists have a plethora of tools and approaches to train models.  BigQuery provides in-situ Machine Learning and in-situ AutoML.  This blog post compared the BQML **AUTOML_REGRESSOR** algorithm against the **BOOSTED_TREE_REGRESSOR**, for both a complete and dimensionality reduced data set.
