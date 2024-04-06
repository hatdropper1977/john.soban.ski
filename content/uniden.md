Title: Wrangle Bearcat BC125AT Input Data with Excel
Date: 2024-03-30 06:26
Author: john-sobanski
Category: IETF
Tags: HAM Radio, Digital
og_image: images/Uniden/00_Bear_Cat.png
twitter_image: images/Uniden/00_Bear_Cat.png
Slug: uniden
Status: published

Uniden released the **Bearcat BC125AT**, a killer non-digital scanner, in 2011.  This scanner holds 500 channels and covers Ambulance, Aviation, Fire, Marine, NASCAR, NOAA Weather, Police, and Railroad bands.  Uniden provides a desktop application to program the **BC125** with Alpha Tags (human-readable text), Input Frequencies, and Continuous Tone-Coded Squelch System (CTCSS) tone codes.

[Radio Reference](https://www.radioreference.com/) provides a database with frequency information for every county in the United States.  I found that **Radio Reference** uses a different table schema than that of the **Uniden Bearcat BC125AT**.  I must wrangle the **Radio Reference** data for input into the scanner.  Since I travel frequently, I would like a way to simplify the data-wrangling process.

![Radio Ref]({static}/images/Uniden/01_Radio_Ref.png)

In this blog post I show how to wrangle **Bearcat Input** Data via Microsoft Excel.  Microsoft Excel provides an adequate **Data Wrangling** environment for small projects.

## Get Data From Radio Reference
**Radio Reference** provides a frequency Database that you can search by location.  I will soon take a trip to Fairmont, West Virginia, so I type that location into the search bar.

![Search Bar]({static}/images/Uniden/02_Search_Bar.png)

Radio Reference indicates that Fairmont resides in Marion County.  I can click other counties via the GUI.

![Map Pic]({static}/images/Uniden/03_Map_Pic.png)

The Hamburger menu icon in the upper right corner provides a link to the Downloads page for Fairmont, West Virginia.  On this page, you will find Comma Separate Value (CSV) Data Downloads.

![Csv Download]({static}/images/Uniden/04_Csv_Download.png)

## Radio Reference CSV
The downloaded Radio Reference CSV file includes a table with eleven (11) columns.  These include:

- Frequency Output
- Frequency Input
- FCC Callsign
- Agency/Category
- Description
- Alpha Tag
- PL Output Tone
- PL Input Tone
- Mode
- Class Station Code
- Tag

Contrast these Column names to the Uniden Bearcat's seven (7) Column Names:

- Name
- Frequency
- Modulation
- CTCS
- Lockout
- Delay
- Priority

## Data Prep

### Step 1. Drop Columns
The Radio Reference (RR) Schema includes four more columns than the Bearcat (BC) BC125AT Schema.

We must drop columns.

We keep these columns:

- Frequency Output
- Alpha Tag
- PL Output Tone
- Mode

... and drop these columns:

- Frequency Input
- FCC Callsign
- Agency/Category
- Description
- PL Input Tone
- Class Station Code
- Tag

In Excel, use **CTRL + Click** to select the **Frequency Input, FCC Callsign, Agency/Category, Description, PL Input Tone, Class Station Code** and **Tag** columns.  Then, right-click and select **Delete.**

![Drop Columns]({static}/images/Uniden/05_Drop_Columns.png)

### Step 2. Drop Rows
The **BC125AT** only processes **Analog modes**.

We must drop rows.

Keep these **Analog modes**:

- AM
- FM
- FMN

...and drop these **Digital modes**:

- DMR
- LTR
- Motorola
- NXDN
- P25
- P25E
- Project 25

In Excel, select **Data &#8594; Filter** and check **AM, FM, and FMN**.

![Drop Digital]({static}/images/Uniden/06_Drop_Digital.png)

> NOTE:  Your state may not include all Analog Modes

### Step 4.  Reorder Columns
The **Bearcat BC125AT** schema requires the columns to follow a certain order, which follows:

- Alpha Tag
- Frequency Output
- Mode
- PL Output Tone

Use the **Right Click, Cut and Paste** operation in Excel to reorder the columns.

![Reorder Columns]({static}/images/Uniden/07_Reorder_Columns.png)

### Step 5. Rename RR Columns to BC Columns
Again, the **Bearcat BC125AT** schema uses different names than **Radio Reference**.

Rename the columns as follows:

- Name       &#8592; Alpha Tag
- Frequency  &#8592; Frequency Output
- Modulation &#8592; Mode
- CTCS       &#8592; PL Output Tone

Double-click the column headers in Excel to rename.

![Rename Columns]({static}/images/Uniden/08_Rename_Columns.png)

### Step 6. Convert DPL, PL, CSQ
Continuous Tone-Coded Squelch System (CTCSS) tone codes allow **private** channels on a given frequency.  CTCSS circuitry mutes users on the channel that use a different tone code.  

Motorolla calls this tone squelch operation **Private Line**, or **PL**.  **Radio Reference** uses the abbreviation **PL** to indicate these tones.  **Uniden** uses the nomenclature **CTCSS** or **C**.  For our input file to work with the Bearcat, we must convert the **PL** suffix to a **C** prefix.

For Example:

> 192.8 PL &#8594; C192.8

For Digital-Coded Squelch (DCS) systems, **Radio Reference** uses the Motorola name, **Digital Private Line (DPL)**.  In the **BC125AT** input file, we must map the **DPL** suffix to a **DCS** prefix.

For Example:

> 265 DPL &#8594; D265

**Radio Reference**, furthermore, also indicates Constant Squelch, or **CSQ**.  This type of operation does not use a tone.  On the **Bearcat** input file, therefore, we can leave those fields blank.

For Example:

> CSQ &#8594; \<Blank\>

The Excel **TEXTSPLIT** function splits the number from text, where appropriate.

![Text Split]({static}/images/Uniden/09_Text_Split.png)

I select the field for the operation and set the Delimintor to **SPACE**.

```excel
=TEXTSPLIT(D7," ")
```

I use Nested **IF** functions to apply a **C** or **D** prefix, given a **PL** or **DPL** suffix, respectively.

```excel
=IF(F18="PL",CONCAT("C",E18),IF(F18="DPL",CONCAT("D",E18),""))
```

I demonstrate the function on the **Suffolk County, NY** table, since that table includes **PL**, **DPL**, and **CSQ** datum.

![Munge Data]({static}/images/Uniden/10_Munge_Data.png)

### Step 7.  Convert Frequency
**Radio Reference** uses **MHz** and the **Bearcat** uses **Hz** for units.  Multiply the Frequency entries in the **Radio Reference** table by **100,000** or **1e6**.

> Frequency &#8592; Frequency x 1e6

![Multiply Freq]({static}/images/Uniden/11_Multiply_Freq.png)

### Step 8.  Add Bearcat Columns 
Paste in three new columns to match the **Bearcat BC125AT** schema.

- Lockout  &#8592; All "Off"
- Delay    &#8592; All "2"
- Priority &#8592; All "Off"

![New Cols]({static}/images/Uniden/12_New_Cols.png)

### Step 7.  Open the Bearcat Input File
Open the **Bearcat** input file in a text editor to view the format.  You see configurables at the top, followed by ten banks in series.

![Bearcat Text]({static}/images/Uniden/13_Bearcat_Text.png)

Open **Excel** and click **Data &#8594; From File &#8594; From Text/CSV**.

![Get Data]({static}/images/Uniden/14_Get_Data.png)

Select your **Bearcat .bc125_at** file, and Excel previews the data.

![Import Data]({static}/images/Uniden/15_Import_Data.png)

Click **Load** and Excel imports the data.

![Imported Data]({static}/images/Uniden/16_Imported_Data.png)

Scroll down to find an empty bank.  I choose **Bank 7** because I have **DC** frequencies in **Banks 1-5** and **Duck** frequencies in **Banks 9-10**.

![Empty Bank]({static}/images/Uniden/17_Empty_Bank.png)

Open the spreadsheet that includes the **Radio Reference** data that you wrangled into the **Bearcat** format.  Copy the data and paste it into the destination **Bearcat** input file.  In this example, I paste in my **Marion County, WV** data.

![Paste In]({static}/images/Uniden/18_Paste_In.png)

In Excel, Save to **Tab Delimited Text**.  The final file follows.  Note the addition of **Marion County, WV** data in **Bank 7**.

![Bearcat Text]({static}/images/Uniden/19_Bearcat_Text.png)

Change the extension to **.bc125at_ss** and load the file into your **BC125AT SS** application.

![Bearcat Snap]({static}/images/Uniden/20_Bearcat_Snap.png)

Write the data to your Scanner.

![Write To]({static}/images/Uniden/21_Write_To.png)

Your bearcat now includes the new frequencies!

![Bearcat Header]({static}/images/Uniden/00_Bear_Cat.png)
