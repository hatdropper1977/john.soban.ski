Title: A Graphical Introduction to Probabilistic Neural Networks - Normalization and Implementation
Date: 2018-10-30 23:47
Author: john-sobanski
Category: Data Science
Tags: Octave, RCE, Neural Networks, Machine Learning, Data Science
Slug: graphical_intro_to_probabilistic_neural_networks
Status: published

## Introduction
Machine Learning engineers use Probabilistic Neural Networks ([PNN](https://en.wikipedia.org/wiki/Probabilistic_neural_network)) for  classification and pattern recognition tasks.  PNN use a [Parzen Window](https://en.wikipedia.org/wiki/Kernel_density_estimation) along with a non-negative kernel function to estimate the probability distribution function ([PDF](https://en.wikipedia.org/wiki/Probability_density_function)) of each class.  The Parzen approach enables non-parametric estimation of the PDF.

In this blog post I will discuss the following

  -  What is a Parzen PNN?
      -  Animated example of the Parzen algorithm
      -  Animated example of a Parzen Neural Network 
  -  Normalization of Training Data
      -  Trade several approaches
	  -  Effectiveness of approaches - Parzen vs. Nearest Neighbor
  -  Reduced Coulomb Energy Networks
      -  Descriptive Animation
	  -  Visualization of RCE on the normalization approach
	  -  Benefits of Ambiguous Regions
  -  RCE applied to the Bupa Liver disorders data set
  -  Conclusion
	 
##  What is a Parzen PNN?
Mathworks provides a simple definition of a [Parzen Probabilistic Neural Network](https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/11880/versions/1/previews/ParzenPNN/html/demo.html):

> The Parzen Probabilistic Neural Networks (PPNN) are a simple type of neural network used to classify data vectors. This [sic] classifiers are based on the Bayesian theory where the a posteriori probability density function (apo-pdf) is estimated from data using the Parzen window technique.

PPNN allow a non-parametric approach to estimate the required Bayesian Classifier probabilities ***P(x|w<sub>i</sub>)*** and ***P(w<sub>i</sub>)***.

![Bayes Classifier]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/00_Bayes_Classifier.png)

In action, the PPNN mechanics are easy to follow.  The PPNN takes a training vector, dot products it with the weights of the hidden layer vector and then chooses the winning class based on the highest output value.  The  next section includes an Animated cartoon that shows the PPNN visually.

###  Animated example of the Parzen algorithm

Suppose you have three classes, and the following training data:

 ID | Class | Var1 | Var2
---|---|---|---
A | Green | 0.5 | 0.75 
B | Purple | 0.5 | 0.25
C | Purple | 0.25 | 0.75
D | Yellow | 0.75 | 0.5
E | Green | 0.75 | 0.75

You now want to use a PPNN to classify the color of the observation ***( Var1 = 0.75, Var2 = 0.25 )***.

The Cartoon below shows the weights as filled colored boxes.  In Column A, for example, weight one (WA1) is half full (e.g. 0.5) and weight two (WA2) is three quarters full ( e.g. 0.75).  The animation shows the dot product of the test pattern ***( X1 = 0.75, X2 = 0.25)*** with the weight vectors, an activation function, and then the selection of the winner.

![Parzen Cartoon]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/Parzen_Cartoon.gif)

###  Animated example of a Parzen Neural Network 
Now let's take a look at the classification approach using the familiar neural network diagram.  The input layer (bottom) includes our test pattern ***( X1 = 0.75, X2 = 0.25)***, the hidden layer includes weight vectors assigned to classes based on the train patterns.  The PPNN then connects the hidden layer to the appropriate class in the output layer.

![Parzen Cartoon]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/Parzen_Neural_Net_Cartoon.gif)

##  Normalization of Training Data
The Mathworks [PPNN web page](https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/11880/versions/1/previews/ParzenPNN/html/demo.html) specifies that we must normalize both our weight vectors and training vectors.

> The weights on the first [hidden] layer are trained as follows: each sample data is normalized so that its length becomes unitary, each sample data becomes a neuron with the normalized values as weights w.

This next section shows different approaches to normalize the training data.
###  Trade several approaches
I use the following data set for this trade.  

 x | y | class
---|---|---
 2.5 | 2.5 | +
 3 | 1 | +
 4 | 2 | +
 1 | 1 | X
 1 | 2 | X
 2 | 2.5 | X
 
Here is a plot of the training data.
 
![Original Data]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/01_Original.png)
 
*Note that in this toy example, we can set up a simple classifier via a vertical line at ***X = 2.25*** and just use the ***x*** values to decide.  Never mind that, though, since the point of this section is to illustrate different normalization techniques and then look at the effectiveness of different classification approaches.*
 
When we normalize over all the training data, you see that the ***(x, y)*** axis scale to ***( 1, 1 )***.

![Normalized over all training data]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/02_Normalized_Over_All_Training_Data.png)

If we center the data and normalize, the scale goes from ***-1*** to ***1*** on both axis.

![Centered and normalized over all training data]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/03_Centered_And_Normailzed_Over_All_Training.png)

If we normalize to class specific magnitude, it makes matters worse.  We no longer have clean separation of the classes.

![04_Notmalized_To_Class_Specific_Magnitude]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/04_Notmalized_To_Class_Specific_Magnitude.png)

If we normalize on a per-vector basis, we get build in error.  Pattern ***(0.75, 0.75)*** now belongs to both Class ***X*** and Class ***+***.

![05_Normalized_On_A_Per_Vector_Basis]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/05_Normalized_On_A_Per_Vector_Basis.png)

###  Effectiveness of approaches - Parzen vs. Nearest Neighbor

Now let's look at the effectiveness of PPNN vs. the [*k*-nearest neighbor](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) algorithms.  KNN provides another non-parametric method of classification.  Instead of using a kernel to estimate the parent PDF, it looks at the ***k*** closest neighbors of the same class.  In the graphics below the gray regions depict Class One (***X***) and the white regions depict Class Two (***+***).

First lets look at the case where we normalized each training pattern to class specific magnitude.  If you recall it appeared to look bad, scrunching the two classes close to each other.

![06_Case_1_Normalized_To_Class_Specific_Magnitude]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/06_Case_1_Normalized_To_Class_Specific_Magnitude.png)

KNN, believe it or not, does a good job of classifying the data.

![07_Nearest_Neighbor_Normalized_By_Class]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/07_Nearest_Neighbor_Normalized_By_Class.png)

The PPNN, fails, classifying all of Class 2 as Class 1.

![08_Parzen_Neural_Net_Normalized_By_Class]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/08_Parzen_Neural_Net_Normalized_By_Class.png)

The second case scales the training data to ***(0,1)*** on both axis.

![09_Case_2_Normalized_Over_All_Training_Data]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/09_Case_2_Normalized_Over_All_Training_Data.png)

KNN handles the classification with ease.

![10_Nearest_Neighbor_Over_All_Samples_Norm]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/10_Nearest_Neighbor_Over_All_Samples_Norm.png)

The PPNN (using ***&#963; = <sup>1</sup>/<sub>4</sub>*** ) fails.  It allocates a tiny box region to Class 1, and classifies everything else to Class 2.

![11_Parzen_Neural_Net_Over_All_Samples_Norm]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/11_Parzen_Neural_Net_Over_All_Samples_Norm.png)

Normalizing over a per-sample basis introduces built in error.  Note again the overlap of the ***X*** and ***+*** at ***( 0.75, 0.75)***.

![12_Case_3_Normalized_On_A_Per_Sample_Basis]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/12_Case_3_Normalized_On_A_Per_Sample_Basis.png)

The KNN of course takes a hit due to the build in error.

![13_Nearest_Neighbor_Per_Sample_Norm]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/13_Nearest_Neighbor_Per_Sample_Norm.png)

The PPNN (using ***&#963; = <sup>1</sup>/<sub>4</sub>*** ) misses twice, once for the built in error and once for a Class 1 observation.

![14_Parzen_Over_Per_Sample_Norm]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/14_Parzen_Over_Per_Sample_Norm.png)

The final normalization approaches centers and normalizes the data.

![15_Case_4_Centered_And_Normalized_Over_All_Training_Data]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/15_Case_4_Centered_And_Normalized_Over_All_Training_Data.png)

The KNN handles this with aplomb.

![16_Nearest_Neighbor_Centered_And_Normalized_Over_All_Training_Data]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/16_Nearest_Neighbor_Centered_And_Normalized_Over_All_Training_Data.png)

The PPNN also correctly classifies all observations.

![17_Parzen_Centered_And_Normalized_Over_All_Training_Data]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/17_Parzen_Centered_And_Normalized_Over_All_Training_Data.png)

##  Reduced Coulomb Energy Networks
So far I showed several normalization approaches and then the effectiveness of different non-parametric classification techniques on the normalized data.  I demonstrated, PPNN and KNN effectiveness.  Now I would like to describe a third non-parametric classification algorithm.  The [Reduced Coulomb Energy]({filename}/reduced_coulomb_energy_neural_network_bupa.md) (RCE) net.  

In summary, RCE provide the following benefits:

  -  Rapid learning of class regions that are
     -  Complex
     -  Non-linear
     -  Disjoint
  -  No local minima issues
  -  Performance knobs
     -  Trade training time vs. memory requirements
     -  Trade classifier complexity to training data

If you would like more details, I encourage you to read my [detailed investigation of RCE]({filename}/reduced_coulomb_energy_neural_network_bupa.md).

###  Descriptive Animation
This cartoon shows the simplicity of the RCE algorithm.  For each training point, the RCE algorithm creates a circular footprint with a radius equal to the distance of the nearest training point from the ***other*** class.  To prevent overlap, you can set a maximum radius for each training point.

![RCE Cartoon]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/RCE_Cartoon.gif)

###  Visualization of RCE on the normalization approach
The following animation shows the classification footprints for the centered and normalized training data.  Note that dark gray represents class one, light gray represents class two and white indicates an "ambiguous region" (no class).

![Center Norm Lambda]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/Center_Norm_Lambda.gif)

The next animation shows the RCE classification footprints on the non-centered all samples normalized training data.

![All Samples Norm]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/All_Samples_Norm.gif)

Normalized by class increases the amount of ambiguous regions.

![Norm by class]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/RCE_Norm_Per_Class.png)

Once more, the built in error of the normalize by per-sample magnitude approach results in a miss.

![Norm by per sample]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/RCE_Norm_Per_Sample.png)

###  Benefits of Ambiguous Regions
RCE provides the benefit of ambiguous regions.  Ambiguous regions pinpoint areas that would provide useful training samples.  The data scientist can then execute observations in those regions to fill in the gaps.

![18_Good_Ambiguous_Regions]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/18_Good_Ambiguous_Regions.png)

The following graphic shows how additional training observations filled in the ambiguity.

![19_Useful_Training_Samples]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/19_Useful_Training_Samples.png)


##  RCE applied to the Bupa Liver disorders data set
The final section summarizes my approaches to separating the training data I input into my [detailed investigation of RCE]({filename}/reduced_coulomb_energy_neural_network_bupa.md).

For my investigation, I looked at the [BUPA Liver Disorders](http://archive.ics.uci.edu/ml/machine-learning-databases/liver-disorders/bupa.data) data set.

The data includes six features and two classes.

  -  mcv: mean corpuscular volume
  -  Four Chemical Markers
     -  alkphos: alkaline phosphotase
     -  sgpt: alamine aminotransferase
     -  sgot: aspartate aminotransferase
     -  gammagt: gamma-glutamyl transpeptidase
  -  drinks # of half-pint equivalents of alcohol per day

I then wrangled the data set in order to increase the success rate of my classification.  I used the following method:

  -  Normalize the data
  -  Quantify separability using
     -  Divergence
     -  Bhattacharyya distance
     -  Scatter Matricies

For the two feature case, separation analysis showed the best feature combination for class detection includes ***gamma-glutamyl*** and ***number of drinks***.

Out of the box, you can see these two are poorly separable.
	 
![20_Poor_Two_Feature_Separability]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/20_Poor_Two_Feature_Separability.png)

For the three feature case, the scatter method (left) added ***alkphos*** to the mix, whereas divergence and Bhattacharyya added ***sgpt***.

![21_Three_Feature_Separability]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/21_Three_Feature_Separability.png)

The following diagrams show the three dimensional separation approaches based on a normalized test set.  I used the training ***&#956;*** and ***&#963;*** to normalize the test set.

![22_Further_Three_D_Separability_Approaches]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/22_Further_Three_D_Separability_Approaches.png)

This graphic shows the same approach, only using the test set's ***&#956;*** and ***&#963;*** to normalize the test set.

![23_Three_D_Separability_On_Train_Set]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/23_Three_D_Separability_On_Train_Set.png)

The following graphic shows the classification footprints using a normalized, two feature (***gamma-glutamyl*** and ***number of drinks***) train and test set.

![24_Results_Of_Two_Feature_Two_Five]({filename}/images/Graphical_Intro_To_Probabilistic_Neural_Networks/24_Results_Of_Two_Feature_Two_Five.png)

For detailed results of my investigation, I encourage you to read my [detailed investigation of RCE]({filename}/reduced_coulomb_energy_neural_network_bupa.md) applied to the BUPA liver disorders data set.

##  Conclusion	
I leave you with convenient bullet points summarizing the work we accomplished today.

  -  Frame PNN as a simple series of steps
     -  Dot product (or distance)
     -  Non-linear transform
     -  Summation and voting
  -  Be cognizant of normalization approach
  -  Sometimes feature reduction yields classes with common patterns
  -  RCE rapidly learns class regions
     -  Complex
     -  Non-linear
     -  Disjoint
  -  RCE can ID ambiguous regions
     -  ID regions of useful training patterns
     -  Does not classify as a known class, in the case that there may be unknown classes

If you enjoyed this blog post, please check out these related blog posts:

- [Exploratory Factor Analysis (EFA) Workflow and Interpretation]({filename}/big-data-idol-how-i-crunched-the-numbers.md)
- [EFA - The Math and Algorithms]({filename}/big-data-idol-the-math.md)
- [Reduced Columb Energy (RCE) - An alternative to KNN]({filename}/reduced_coulomb_energy_neural_network_bupa.md)
- [Vision model w/ FAST AI]({filename}/fastai-flask.md)
- [Vision model w/ Google AutoML]({filename}/gcp-automl-vision.md)
- [Google AutoML Tables Beta]({filename}/fast-and-easy-automl-optimize.md)
