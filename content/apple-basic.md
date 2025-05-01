Title: My Childhood Apple II Computer Programs (1986)
Date: 2025-04-26 07:17
Author: john-sobanski
Category: HOWTO
Tags: Basic
og_image: images/Apple_Basic/04_Blue_Lion.png
twitter_image: images/Apple_Basic/04_Blue_Lion.png
Slug: apple-basic
Status: published

My Dad ran the first computer lab at [Division Avenue High School](https://www.levittownschools.com/division/) in Levittown, NY.  The lab held a bank of Apple II computers.  He bought an Apple II for our house and then showed us how run games and program basic.

This year I cleaned out ancient drawers from my childhood bedroom and found a floppy disk from 1986.  

![A picture of an old floppy disk that reads "John Sobanski's Disk - Hands Off!]({static}/images/Apple_Basic/01_Floppy_Disk.jpg)

I had my friend at work, [Mike Shields](https://www.linkedin.com/in/mikeshields88/), execute some disk recovery wizardry.  He sent me the files in text.

Today I will revisit my old code.  Keep in mind, a fourth grader wrote these programs back in 1986.  I have not run them in nearly forty years.

## Car Trip
The first program uses a numeric variable to calculate car trip distance.  


```basic
 90  HOME 
 100  PRINT "MILES"
 110  INPUT M
 120  PRINT "SPEED"
 130  INPUT S
 140  LET T = M / S
 150  PRINT "HOURS: ";T
```

I assume that I found this program in a basic programming book.

![A picture that shows a text prompt that leads the user through a trip time calculation]({static}/images/Apple_Basic/02_Car_Trip.png)

## DDDFG
The next program, which I named **DDDFG** spits gibberish out on an eye-searing turquoise screen.

```basic
 10  HOME 
 20  INVERSE 
 25  SPEED= 1
 30  PRINT "----------------------------"
 40  PRINT "8TJGFJFYYMFJKJJJJJG8UJUJJJJJ"
 50  PRINT "$%$%%%%%&&&&%%%%'''''''''''''"
 60  PRINT "'''''''''''''''''''''''''''''"
 70  PRINT "000000000JOHN WAS HERE0000000"
 75  SPEED= 234
 80  GOTO 30
```

I loved to write **John was here** in Sharpie on my desks at school.  This program captures my nine-year-old personality, so we can assume that I did not copy it from a book.

![A picture that shows black text on a turquoise background, that reads "John Was Here"]({static}/images/Apple_Basic/03_John_Here.png)

## Blue Lion
I tried my hand at **Low Res** graphics.  I drew a **lion** with plot instructions.

```basic
 5  GR 
 10  COLOR= 2
 15  VLIN 7,12 AT 8
 20  HLIN 7,8 AT 8
 25  HLIN 6,8 AT 9
 30  HLIN 12,6 AT 3
 35  HLIN 6,10 AT 4
 40  HLIN 12,16 AT 4
 45  HLIN 6,16 AT 5
 50  HLIN 6,7 AT 6
 55  HLIN 9,12 AT 6
 60  HLIN 14,16 AT 6
 65  HLIN 6,16 AT 7
 70  HLIN 6,7 AT 8
 75  HLIN 15,16 AT 8
 80  HLIN 6,16 AT 9
 85  HLIN 6,22 AT 10
 90  HLIN 22,26 AT 9
 95  HLIN 6,22 AT 11
 100  HLIN 6,22 AT 12
 105  HLIN 6,22 AT 13
 110  VLIN 14,19 AT 7
 115  VLIN 14,19 AT 8
 120  VLIN 14,19 AT 11
 125  VLIN 14,19 AT 12
 130  VLIN 14,19 AT 15
 135  VLIN 14,19 AT 16
 140  VLIN 14,19 AT 19
 145  VLIN 14,19 AT 20
 150  COLOR= 15
 155  HLIN 1,5 AT 5
 160  HLIN 1,5 AT 7
 165  HLIN 17,21 AT 5
 170  HLIN 17,21 AT 7
```

Do you think my art looks like a lion, or something else?

![A picture of a charming lion, created by a child]({static}/images/Apple_Basic/04_Blue_Lion.png)

I have several versions of this program, which change lines **10** and **150** to paint the lion different colors.

## Hi
This program prints a cheerful, low-res **bear** on the screen.

```basic
 10  GR 
 15  COLOR= 15
 20  HLIN 9,14 AT 7
 30  VLIN 7,15 AT 8
 40  HLIN 11,12 AT 8
 50  VLIN 7,15 AT 15
 60  HLIN 9,14 AT 9
 70  HLIN 9,10 AT 10
 80  HLIN 13,14 AT 10
 90  HLIN 9,10 AT 11
 100  HLIN 13,14 AT 11
 110  HLIN 9,14 AT 12
 120  HLIN 10,13 AT 13
 130  PLOT 14,14
 140  PLOT 9,14
 150  HLIN 9,14 AT 15
 160  COLOR= 8
 170  HLIN 9,14 AT 4
 180  HLIN 7,16 AT 5
 190  HLIN 7,16 AT 6
 200  VLIN 4,15 AT 16
 210  VLIN 4,15 AT 7
 220  HLIN 7,16 AT 16
 230  HLIN 7,16 AT 17
 240  VLIN 4,5 AT 17
 250  VLIN 4,5 AT 6
 260  COLOR= 3
 270  VLIN 3,6 AT 1
 280  VLIN 3,6 AT 3
 290  PLOT 2,5
 300  HLIN 1,3 AT 8
 310  VLIN 9,11 AT 2
 320  HLIN 1,3 AT 12
 330  HLIN 20,22 AT 3
 340  HLIN 20,22 AT 7
 350  VLIN 4,7 AT 20
 360  PLOT 21,5
 370  VLIN 9,10 AT 20
 380  VLIN 9,10 AT 22
 390  PLOT 21,11
 400  PLOT 20,13
 410  PLOT 22,13
 420  VLIN 14,16 AT 21
```

The bear likes to quote **the Fonz**, he shouts **Eyy!**.

![A Low Res picture of a smiling bear, that says "Hi Eyy"]({static}/images/Apple_Basic/05_The_Bear.png)

## JFS
This program captures my humor.  I just insult the player.

```basic
 10  PRINT "UGLY GAME!"
 20  PRINT "YOU UGLY?"
 22  INPUT A$
 30  IF A$ = "YES" GOTO 70
 40  IF A$ = "NO" GOTO 60
 50  PRINT "PLEASE ANSWER YES OR NO"
 52  GOTO 20
 60  PRINT "BULLS**T"
 62  PRINT "DON'T TELL ME I SEE YOU"
 63  GOTO 90
 70  PRINT "PLEASE PROVE IT THANK YOU"
 75  GOTO 90
 90  END 
```

This program demonstrates the use of **input strings**.

![Green text that walks a player through an insulting game]({static}/images/Apple_Basic/06_You_Ugly.png)

## One Eyed Multi Lion
This program prints a putative lion.

```basic
 5  GR 
 10  COLOR= 1
 15  HLIN 6,8 AT 4
 20  HLIN 5,9 AT 5
 25  COLOR= 2
 30  HLIN 12,14 AT 4
 35  HLIN 11,15 AT 5
 40  COLOR= 3
 45  HLIN 5,15 AT 6
 50  VLIN 7,9 AT 5
 55  VLIN 7,9 AT 6
 60  VLIN 7,9 AT 7
 65  COLOR= 4
 70  PLOT 7,8
 75  PLOT 7,11
 80  COLOR= 5
 85  HLIN 5,15 AT 6
 90  COLOR= 6
 95  VLIN 6,9 AT 13
 100  VLIN 6,9 AT 14
 105  VLIN 6,9 AT 15
 110  HLIN 8,15 AT 9
 115  COLOR= 7
 120  HLIN 1,4 AT 7
 125  COLOR= 15
 130  HLIN 1,41 AT 10
```

It looks more like an acid trip.

![An abstract picture of a lion with one green eye]({static}/images/Apple_Basic/07_Multi_Lion.png)

## Password
This program also uses input strings and string concatenation.

```basic
 1  HOME 
 5  SPEED= 90
 10  PRINT "THE PASS WORD IS FWABB !"
 20  PRINT "WHAT IS YOUR NAME"
 30  INPUT A$
 40  PRINT "GOOD ";A$;" THE PASS WORD IS FWABB!"
 50  PRINT "WHAT DO YOU WANT YOUR PASSWORD TO BE "
 60  INPUT F$
 70  PRINT "OK ";A$;" MY PASSWORD IS FWABB AND YOURS IS ";F$
 80  PRINT "NOW THAT YOU KNOW MINE AND I KNOW YOURS WHAT IS YOUR FRIEND'S NAME"
 90  INPUT H$
 100  PRINT "OK ";A$;"'S FRIEND ";H$" WHAT IS YOUR PASSWORD"
 110  INPUT S$
 120  PRINT "NOW TO GET THIS RIGHT MY WORD IS FWABB ";A$;"'S IS ";F$;" AND ";H$;"'S IS ";S$
```
 
 I must have learned these techniques in a book, and put my spin on it.
 
 ![Green text that asks for names and passwords]({static}/images/Apple_Basic/08_Password_Game.png)

## Rating Game
This game **matches** the user with a date.  At the end, it prints stars that equal the user's rating.  This might show the first time in my life I used an **iterative loop** in one of my programs.

```basic
 10  REM  FOR/NEXT
 20  HOME 
 30  PRINT "THIS IS THE RATING GAME"
 32  PRINT "I AM YOUR HOST JACK SAYPAT"
 35  PRINT "YOU WILL MEET THE CONTESTANTS, HEAR WHAT THEY HAVE TO SAY , AND THEN RATE THEM"
 38  PRINT "WHAT IS YOUR NAME?"
 40  INPUT A$
 50  PRINT "OKAY ";A$;" HERE WE GO..."
 51  PRINT "READY?"
 52  INPUT B$
 53  HOME 
 54  PRINT "  "
 55  PRINT "  "
 56  PRINT "   "
 57  PRINT "  "
 60  PRINT "XXXXXXX0XXXXXXX"
 62  PRINT "XXXXXX0X0XXXXXX"
 64  PRINT "XXXX0XXXXX0XXXX"
 66  PRINT "XXX0XXIXXIXX0XX"
 68  PRINT "XXXX0XXXXXX0XXX"
 70  PRINT "XXXXXX0XXX0XXXX"
 72  PRINT "XXXXXXX0X0XXXXX"
 74  PRINT "XXXXXXXX0XXXXXX"
 75  PRINT "  "
 76  PRINT "   "
 77  PRINT "  "
 78  PRINT "  "
 79  PRINT "  "
 80  PRINT "HELLO MY NAME IS HERMAN SHERMAN DERMAN WORMEN TERMAN.I LIKE BARRY MANILOW MUSIC, MY FAVORITE SHOW IS THE LOVE BOAT, AND I LOVE SKIPPING."
 81  PRINT "   "
 82  PRINT "  "
 83  PRINT "   "
 85  PRINT "YOUR RATE (1-10) ="
 87  INPUT A
 97  HOME 
 100  PRINT "HI YO.MY NAME IS DELTA VELTA.I AM A COAL DIGGER,AND A GOLD SEARCHER.I HAVE BEEN SEEN WITH BART CONNER"
 105  PRINT "YOUR RATE ="
 110  INPUT B
 111  HOME 
 115  PRINT "ER MY NAME IS JOE, OOPS I MEAN MARY MOOSE. I WORK AT A GLASS FACTORY SWEEPING CEILINGS."
 120  INPUT C
 125  HOME 
 130  PRINT "UM,I AM MARTY STINK. I AM A PRINCIPLE OF A COMPUTER SCHOOL. I SHAVE MY HEAD.I HAVE A PET CANARY NAMED BUCTRICK."
 135  PRINT "YOUR RATE="
 138  INPUT D
 140  HOME 
 145  PRINT "HERE ARE THE RESULTS..."
 146  HOME 
 147  PRINT "HERMAN "
 150  FOR X = 1 TO A
 153  PRINT "*";
 155  NEXT X
 156  PRINT "  "
 160  PRINT "DELTA "
 162  FOR Y = 1 TO B
 163  PRINT "*";
 165  NEXT Y
 166  PRINT " "
 167  PRINT "MARY "
 169  FOR Z = 1 TO C
 170  PRINT "*";
 172  NEXT Z
 173  PRINT "  "
 174  PRINT "MARTY "
 176  FOR W = 1 TO D
 178  PRINT "*";
 180  NEXT W
 182  PRINT "  "
 185  PRINT "JACK SAYPAT HERE. SURPRISE,SURPRISE. THE PERSON WITH THE MOST POINTS IS MOVING IN WITH YOU FOR A MONTH. CONGRATULATIONS TO BOTH OF YOU. "
 186  PRINT "BYE!!"
 190  END 
```

I believe I stole the joke **Jack Saypat** from Cracked Magazine.  If you grew up in the 80's, you might see the play on words.  Think of the name of the man who hosted **the** most popular 80's game show.

![Green text that shows the splash page for a rating game]({static}/images/Apple_Basic/09_Rating_Game.png)

## AI Dog (Low Res)
I had a dozen or so other programs, which include repeats with minor color changes.

For example, a version of the lion that the Apple colors at random.

![The green lion from above, now mult-colored]({static}/images/Apple_Basic/10_Wild_Lion.png)

I then had a thought.  Can one of the modern **LLMs** draw a **Low Res** dog in the style of my fourth-grade **lion**?

I asked **Grok** and the **LLM** produced the following code:

```basic
1   HOME
5   GR
10  COLOR=13
15  HLIN 6,14 AT 10
20  HLIN 6,14 AT 11
25  HLIN 6,14 AT 12
30  VLIN 13,15 AT 6
35  VLIN 13,15 AT 9
40  VLIN 13,15 AT 11
45  VLIN 13,15 AT 14
50  HLIN 15,18 AT 9
55  HLIN 15,18 AT 10
60  HLIN 15,18 AT 11
65  VLIN 7,8 AT 16
70  VLIN 7,8 AT 17
75  COLOR=15
80  PLOT 17,11
85  HLIN 12,13 AT 14
```

I find it interesting that **Grok** understands how to manipulate Apple II basic graphics.  Its code paints a decent picture.

![AI generated graphic of a green dog]({static}/images/Apple_Basic/11_Grok_Dog.png)

I asked it to write code to draw a lion.  It produced the following:

![AI generated graphic of a Lion's face]({static}/images/Apple_Basic/12_Grok_Lion.png)

## AI Lion (High Res)
Apple II also provides a **High Res** graphic mode.  Grok produced the following code for a **High Res** lion.

```basic
5 HGR
10 HCOLOR=0
15 HPLOT 0,0 TO 279,0 TO 279,191 TO 0,191 TO 0,0
20 HCOLOR=3
25 HPLOT 100,50 TO 180,50 TO 200,70 TO 220,100 TO 200,130 TO 180,150 TO 100,150 TO 80,130 TO 60,100 TO 80,70 TO 100,50
30 HPLOT 90,40 TO 110,30 TO 130,25 TO 150,30 TO 170,40 TO 190,50
35 HPLOT 80,50 TO 60,40 TO 40,50 TO 50,60 TO 70,70
40 HPLOT 200,50 TO 220,40 TO 240,50 TO 230,60 TO 210,70
45 HPLOT 70,80 TO 50,70 TO 30,80 TO 40,90 TO 60,100
50 HPLOT 210,80 TO 230,70 TO 250,80 TO 240,90 TO 220,100
55 HCOLOR=1
60 HPLOT 120,80 TO 140,80 TO 140,100 TO 120,100 TO 120,80
65 HPLOT 160,80 TO 180,80 TO 180,100 TO 160,100 TO 160,80
70 HCOLOR=2
75 HPLOT 140,110 TO 160,110 TO 150,130 TO 140,110
80 HPLOT 130,140 TO 170,140
85 HPLOT 140,150 TO 160,150
```

Behold the masterpiece:

![AI generated graphic of a High Res Lion]({static}/images/Apple_Basic/13_High_Res.png)

## Conclusion
Today's exercise provided me with novelty and nostalgia.  I had brief, subtle recollections of nearly forty-year-old memories.  I got to see my first attempt at iterative loops, computer graphics, user input, and string concatenation.  I also got a peek into my weird, slightly obnoxious nine-year-old sense of humor.
