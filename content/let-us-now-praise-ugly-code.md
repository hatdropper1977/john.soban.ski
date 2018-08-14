Title: Let us now praise ugly code!
Date: 2017-07-15 01:18
Author: john-sobanski
Category: Data Science
Tags: R Programming, Data Science
Slug: let-us-now-praise-ugly-code
Status: published

In this blog post I will revisit the first piece of code I wrote with the [R Programming language](https://www.r-project.org/about.html), back in the early part of this decade.

Coming from an [Octave](https://www.gnu.org/software/octave/)/[MATLAB](http://www.mathworks.com/products/matlab/) background, I really enjoyed the [functional](https://en.wikipedia.org/wiki/Functional_programming) nature of R. I imagined flinging vectors into Matrices, collapsing them with dot-products, Tetris like. I refused to write a single for loop... I framed everything as functions and maps. As I gained experience with R, I found [pipes](https://cran.r-project.org/web/packages/magrittr/vignettes/magrittr.html) and [data wrangling](https://cran.r-project.org/web/packages/tidyr/index.html) libraries, but early on, my code was pretty ugly, as you will see shortly.

I have a project that keeps track of comic books, their publishers, their prices and their customers. The model stores data in excel and to make things readable, I use a columnar store. In this way, I can quickly add new entries to the table by adding columns.  Each column has an arbitrary number of rows. I know this might not be the best way to store data, but bear with me here. This blog looks at the processing of that data, not the storing of the data. Besides, in the real world, you sometimes have no choice but to start with ugly data.

### **The Ugly Way...**

Let us proceed. First, take a look at Titles:

```R
> Titles.orig <- data.frame(DC=c('Batman','Superman','Captain_Marvel',''),
                          Image=c('Youngblood','Spawn','',''),
                          Marvel=c('Spiderman','Iron_Man','Cable','Doctor_Strange'),
                          stringsAsFactors = FALSE)

> Titles.orig

              DC      Image         Marvel
1         Batman Youngblood      Spiderman
2       Superman      Spawn       Iron_Man
3 Captain_Marvel                     Cable
4                           Doctor_Strange
```

Notice that a rotation doesn't really buy us anything. Instead of an arbitrary number of rows for each entry, a rotation gets us an arbitrary number of columns.

```R
> t(Titles.orig)
       [,1]         [,2]       [,3]             [,4]            
DC     "Batman"     "Superman" "Captain_Marvel" ""              
Image  "Youngblood" "Spawn"    ""               ""              
Marvel "Spiderman"  "Iron_Man" "Cable"          "Doctor_Strange"
```

When I process *Titles.orig* in R, I first transform it to a key-value store. My approach relies on data frame index logic (commands inside the [] brackets).

In my original approach, I create two vectors, one that repeats the column several times, and another that un-packs (unlists) the data. When I put them together, I get key-value pairs (with some empties).

My first vector repeats each column name *n* times, with *n* being the number of rows. Since the data frame has four rows, I repeat each column name four times. I first try the ***rep()*** function.


```R
> Titles <- Titles.orig
> rep(names(Titles),nrow(Titles))
 [1] "DC"     "Image"  "Marvel" "DC"     "Image"  "Marvel" "DC"     "Image"  "Marvel" "DC"    
[11] "Image"  "Marvel"
```

This attempt fails. I want it in the form: 'DC, DC, DC, DC, Image, Image etc.'

After a few Google searches, I find that ***matrix()***allows us to stack rows, so I stuff the repeat statement into ***matrix()***:

``` {style="margin: 0; line-height: 125%;"}
> matrix(rep(names(Titles),nrow(Titles)),nrow=nrow(Titles))

     [,1]     [,2]     [,3]    
[1,] "DC"     "Image"  "Marvel"
[2,] "Image"  "Marvel" "DC"    
[3,] "Marvel" "DC"     "Image" 
[4,] "DC"     "Image"  "Marvel"
```

Close, but not quite what I need. I then add the *byrow* flag:

```R
> matrix(rep(names(Titles),nrow(Titles)),nrow=nrow(Titles),byrow='T')

     [,1] [,2]    [,3]    
[1,] "DC" "Image" "Marvel"
[2,] "DC" "Image" "Marvel"
[3,] "DC" "Image" "Marvel"
[4,] "DC" "Image" "Marvel"
```

From here, we convert to a vector:

```R
> as.vector(matrix(rep(names(Titles),nrow(Titles)),nrow=nrow(Titles),byrow='T'))

 [1] "DC"     "DC"     "DC"     "DC"     "Image"  "Image"  "Image"  "Image"  "Marvel" "Marvel"
[11] "Marvel" "Marvel"
```

As you can see, vector works "down the column" by default (which makes sense, since columns are vectors).

Let's move past the titles. To create a vector from our data, we need to ***unlist()*** the data first and then vectorize it:

```R
> as.vector(unlist(Titles))

 [1] "Batman"         "Superman"       "Captain_Marvel" ""               "Youngblood"    
 [6] "Spawn"          ""               ""               "Spiderman"      "Iron_Man"      
[11] "Cable"          "Doctor_Strange"
```

I bind these two vectors together as columns and then create a data frame.

```R
> Titles <-  data.frame(cbind(as.vector(matrix(rep(names(Titles),nrow(Titles)),
                                             nrow=nrow(Titles),byrow='T')),
                            as.vector(unlist(Titles))))
> Titles

       X1             X2
1      DC         Batman
2      DC       Superman
3      DC Captain_Marvel
4      DC               
5   Image     Youngblood
6   Image          Spawn
7   Image               
8   Image               
9  Marvel      Spiderman
10 Marvel       Iron_Man
11 Marvel          Cable
12 Marvel Doctor_Strange
```

I give names to the data:

```R
> names(Titles) <- c('publisher','title')
```

And then remove the empty rows. A lot of my early code follows this convention. I scan a data frame with index logic, using a comma to separate row and column logic. In the line below, I scan the index to return only rows that have a non-empty title, and return all columns. Such syntax appears a little confusing, as I reference the data frame ***Titles*** in three separate parts.

```R
> Titles <- Titles[which(Titles$title != ""),]

> Titles
   publisher          title
1         DC         Batman
2         DC       Superman
3         DC Captain_Marvel
5      Image     Youngblood
6      Image          Spawn
9     Marvel      Spiderman
10    Marvel       Iron_Man
11    Marvel          Cable
12    Marvel Doctor_Strange
```

### **The Pretty Way...**

Let's recap. We had nested hell to transform the columnar table to a key-value table, and then we needed two more commands to name the data frame columns and remove the empties.

With pipes (***dplyr*** and ***magrittr***) and ***tidyr***, we can produce the ***same result*** with ***one line of code***.

```R
> library("dplyr")
> library("magrittr")
> library("tidyr")
> Titles <- Titles.orig
> Titles %>% gather(publisher,title) %>% filter(nzchar(title))

  publisher          title
1        DC         Batman
2        DC       Superman
3        DC Captain_Marvel
4     Image     Youngblood
5     Image          Spawn
6    Marvel      Spiderman
7    Marvel       Iron_Man
8    Marvel          Cable
9    Marvel Doctor_Strange
```

To dump and then set the variable, we use the ***%\<\>%*** pipe.

```R
> Titles %<>% gather(publisher,title) %>% filter(nzchar(title))
```

### **More Pretty Code**

Now we have a separate table of customers. This is a more traditional table, and we can arbitrarily add columns and rows as we see fit.

```R
> Customers <- data.frame(title = c('Batman','Superman','Captain_Marvel',
                                  'Youngblood','Spawn','Spiderman','Iron_Man','Cable','Doctor_Strange'),
                        Micky = c(2,0,0,0,0,0,2,0,1),Mike = c(5,1,1,1,1,1,1,1,1),
                        Peter = c(1,1,0,0,0,1,1,2,0),
                        Davy = c(2,7,1,5,1,2,0,0,1),
                        stringsAsFactors=FALSE)
> Customers

           title Micky Mike Peter Davy
1         Batman     2    5     1    2
2       Superman     0    1     1    7
3 Captain_Marvel     0    1     0    1
4     Youngblood     0    1     0    5
5          Spawn     0    1     0    1
6      Spiderman     0    1     1    2
7       Iron_Man     2    1     1    0
8          Cable     0    1     2    0
9 Doctor_Strange     1    1     0    1
```

Let's try the gather function on this table to see what we get. We want each row to contain the comic title, the customer name, and the quantity they want to purchase.

```R
> Customers %>% gather(customer,qty) %>% suppressWarnings %>% head(12)

   customer            qty
1     title         Batman
2     title       Superman
3     title Captain_Marvel
4     title     Youngblood
5     title          Spawn
6     title      Spiderman
7     title       Iron_Man
8     title          Cable
9     title Doctor_Strange
10    Micky              2
11    Micky              0
12    Micky              0
```

As you can see, this is not what we want. For correct syntax, we need to specify a start and end column.

```R
> Customers %>% gather(customer,qty,Micky:Davy) %>% head(12)

            title customer qty
1          Batman    Micky   2
2        Superman    Micky   0
3  Captain_Marvel    Micky   0
4      Youngblood    Micky   0
5           Spawn    Micky   0
6       Spiderman    Micky   0
7        Iron_Man    Micky   2
8           Cable    Micky   0
9  Doctor_Strange    Micky   1
10         Batman     Mike   5
11       Superman     Mike   1
12 Captain_Marvel     Mike   1
```

I have an issue with this code in that I need to refactor it each time I add a new customer.

To future proof, we modify the code as follows:

```R
> Customers %>% gather(customer,qty,2:ncol(Customers)) %>% head(12)
```

In a separate table I have prices for each title.

```R
> Price <- data.frame(title = c('Batman','Superman','Captain_Marvel','Youngblood',
                              'Spawn','Spiderman','Iron_Man','Cable','Doctor_Strange'), 
                    price = c(1.95,1.95,2.95,2.95,1.75,1.75,3.95,3.95,1.95), 
                    stringsAsFactors = FALSE )
> Price

           title price
1         Batman  1.95
2       Superman  1.95
3 Captain_Marvel  2.95
4     Youngblood  2.95
5          Spawn  1.75
6      Spiderman  1.75
7       Iron_Man  3.95
8          Cable  3.95
9 Doctor_Strange  1.95
```

We can easily add a price column to Customers with the ***merge()*** function:

```R
> Customers %>% merge(Price)

           title Micky Mike Peter Davy price
1         Batman     2    5     1    2  1.95
2          Cable     0    1     2    0  3.95
3 Captain_Marvel     0    1     0    1  2.95
4 Doctor_Strange     1    1     0    1  1.95
5       Iron_Man     2    1     1    0  3.95
6          Spawn     0    1     0    1  1.75
7      Spiderman     0    1     1    2  1.75
8       Superman     0    1     1    7  1.95
9     Youngblood     0    1     0    5  2.95
```

### **Pretty Showdown:  Hard vs. Easy**

How do we find per customer totals? I'll show a hard way and an easy way. Let's look at the **pipe/ dplyr/ tydr** method first.

First, we narrow the table and merge with price:

```R
> Customers %>% gather(customer,qty,2:ncol(Customers)) %>% 
  merge(Price) %>% head(12)

            title customer qty price
1          Batman    Micky   2  1.95
2          Batman     Davy   2  1.95
3          Batman    Peter   1  1.95
4          Batman     Mike   5  1.95
5           Cable     Davy   0  3.95
6           Cable    Peter   2  3.95
7           Cable     Mike   1  3.95
8           Cable    Micky   0  3.95
9  Captain_Marvel     Davy   1  2.95
10 Captain_Marvel    Peter   0  2.95
11 Captain_Marvel     Mike   1  2.95
12 Captain_Marvel    Micky   0  2.95
```

Then, we add a fifth column that calculates the subtotal:

```R
> Customers %>% gather(customer,qty,2:ncol(Customers)) %>% 
  merge(Price) %>% mutate(subtotal= qty * price) %>% 
  head(12)

            title customer qty price subtotal
1          Batman    Micky   2  1.95     3.90
2          Batman     Davy   2  1.95     3.90
3          Batman    Peter   1  1.95     1.95
4          Batman     Mike   5  1.95     9.75
5           Cable     Davy   0  3.95     0.00
6           Cable    Peter   2  3.95     7.90
7           Cable     Mike   1  3.95     3.95
8           Cable    Micky   0  3.95     0.00
9  Captain_Marvel     Davy   1  2.95     2.95
10 Captain_Marvel    Peter   0  2.95     0.00
11 Captain_Marvel     Mike   1  2.95     2.95
12 Captain_Marvel    Micky   0  2.95     0.00
```

Then, we sum the subtotal for each customer. We can achieve this with ease using the ***group\_by()*** and ***summarize()*** functions:

```R
> Customers %>% gather(customer,qty,2:ncol(Customers)) %>% 
  merge(Price) %>% mutate(subtotal= qty * price) %>% 
  group_by(customer) %>% summarize(sum(subtotal))

# A tibble: 4 x 2
  customer sum(subtotal)
     <chr>         <dbl>
1     Davy         42.45
2    Micky         13.75
3     Mike         30.95
4    Peter         17.50
```

POP quiz... did we just execute the hard or easy method to find the totals? I will show you the easy way next and you can decide for yourself. In short, we can solve this problem with simple linear algebra.

We first create our vector

```R
> x <- Price$price
```

Then our matrix

```R
> A <- Customers %>% select(Micky:Davy) %>% as.matrix()
```

We do a simple dot product and we're done:

```R
> x %*% A

     Micky  Mike Peter  Davy
[1,] 13.75 30.95  17.5 42.45
```

We could also do it in one line:

```R
> Price$price %*% (Customers %>% select(Micky:Davy) %>% as.matrix())

     Micky  Mike Peter  Davy
[1,] 13.75 30.95  17.5 42.45
```

My Octave/ MATLAB experience led me to use linear algebra right out of the gate. Sometimes, even in the face of fancy new functions, it turns out I produce beautiful code on the first try.
