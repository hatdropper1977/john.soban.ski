Title: Install OpenDaylight on Ubuntu 24.04 LTS (Quick and Easy!)
Date: 2024-04-25 23:33
Author: john-sobanski
Category: HOWTO
Tags: HOWTO, SD-RAN, SDN, OpenDaylight
Slug: odl-ubuntu-lts-24-04
Status: published

**Infrastructure Architects** at Internet Service Providers (ISP), Cloud Service Providers (CSP) and Academic Institutions use the [OpenDaylight (ODL) platform](https://www.opendaylight.org/) to command, control, monitor and automate computer networks.

![OpenDaylight Logo]({static}/images/How_To_Install_Opendaylight_On_Centos_Or_Ubuntu/00_ODL.png)

These **Infrastructure Architects** use ODL for the following activities:

  *  Service Delivery Automation
     * Program circuit provisioning and virtual private networks on-demand.  Replace your Cisco certified technician with code.    
  *  Cloud and NFV
     * Follow the lead of Amazon Web Services (AWS) and launch your own Virtual Private Clouds (VPC), replete with path discovery and attack surface reduction.
  *  Network Resources Optimization (NRO)
     * Prioritize and provision throughput based on load and state.  Un-jam packet traffic.
  *  Visibility and Control
     * Make correct Capital Expenditure (CAPEX) decisions thanks to bountiful usage information.

Based on Search query data, Infrastructure Architects prefer to install OpenDaylight on [Ubuntu Linux](https://ubuntu.com/).

Ubuntu 24.04 LTS "Noble Numbat" improves the Graphical User Interface (GUI), App Center Organization and choice of Security features.  Ubuntu will also support Noble Numbat until 2036.
  
For [Six Years]({tag}opendaylight) I have provided the authoritative guide on  HOWTO easily install OpenDaylight without a headache.  I present the **clearest** and **simplest** method to install ODL.  

To install OpenDaylight on Ubuntu LTS 24.04, simply:

  1.  Prepare the Operating System (OS)
  2.  Install the Java Development Kit (JDK)
  3.  Set JAVA_HOME
  4.  Download the OpenDaylight Zip
  5.  Unzip OpenDaylight
  6.  Start OpenDaylight
  7.  Bonus: How do I install DLUX?
 
My field-tested approach reduces **time-to-OpenDaylight**.

For advanced use cases, please consider my other blog posts:

- [Compile OpenDaylight from Scratch]({filename}/how-to-install-opendaylight-on-centos-or-ubuntu.md)
- [Deploy an OpenDaylight **systemd** Service]({filename}/how-to-install-opendaylight-as-a-service-on-ubuntu.md)

## 1. Prepare the Operating System (OS)
Use the **apt** package manager to patch the Ubuntu Operating System and update your applications.

**apt-get update** updates the package index with recent data.

```bash
$ sudo apt-get -y update
```

The **upgrade** flag commands Ubuntu to download and install packages.

```bash
$ sudo apt-get -y upgrade
```

We need **unzip** to extract software from the ODL archive.

```bash
$ sudo apt-get -y install unzip
```

## 2.  Install the Java Development Kit (JDK)
OpenDaylight runs on the cross-platform Java Development Kit (JDK).

To comply with security best practices, use the most recent JDK.

> NOTE:  Oracle and the Java foundation stopped offering a Java Runtime Environment (JRE) at Java 11

Use **apt-cache search** to find the available versions of **openjdk**.

```bash
sudo apt-cache search openjdk
```

The command outputs an assortment of **JAVA** versions.

```bash
~$ sudo apt-cache search openjdk
default-jdk - Standard Java or Java compatible Development Kit
default-jre - Standard Java or Java compatible Runtime
openjdk-17-jdk - OpenJDK Development Kit (JDK)
openjdk-17-jre - OpenJDK Java runtime, using Hotspot JIT
openjdk-11-jdk - OpenJDK Development Kit (JDK)
openjdk-11-jre - OpenJDK Java runtime, using Hotspot JIT
openjdk-19-jdk - OpenJDK Development Kit (JDK)
openjdk-19-jre - OpenJDK Java runtime, using Hotspot JIT
openjdk-20-jdk - OpenJDK Development Kit (JDK)
openjdk-20-jre - OpenJDK Java runtime, using Hotspot JIT
openjdk-21-jdk - OpenJDK Development Kit (JDK)
openjdk-21-jre - OpenJDK Java runtime, using Hotspot JIT
openjdk-22-jdk - OpenJDK Development Kit (JDK)
openjdk-22-jre - OpenJDK Java runtime, using Hotspot JIT
openjdk-8-jdk - OpenJDK Development Kit (JDK)
openjdk-8-jre - OpenJDK Java runtime, using Hotspot JIT
```

Choose and install a version.  I choose **openjdk-22-jre**.

The following command installs the **JAVA 22** JDK.

```bash
$ sudo apt-get -y install openjdk-22-jre
```

> Note: Even though we requested the **JRE** Ubuntu installs a **JDK** (The Java foundation discontinued the JRE - see note above)

To configure **ODL**, we need to record the full path to the **JAVA JDK**.

**update-alternatives** finds this path.  

```bash
$  sudo update-alternatives --config java
There is 1 choice for the alternative java (providing /usr/bin/java).

  Selection    Path                                         Priority   Status
------------------------------------------------------------
* 0            /usr/lib/jvm/java-22-openjdk-amd64/bin/java   2211      auto mode
  1            /usr/lib/jvm/java-22-openjdk-amd64/bin/java   2211      manual mode

Press <enter> to keep the current choice[*], or type selection number:
```

Hit **enter** to keep the current choice.

> NOTE:  If you see more than one option for the **java** command, select **JAVA 22**

**update-alternatives** outputs the full path to your **JAVA** executable.  You need this full path to set the **JAVA_HOME** environment variable.  **OpenDaylight** requires this information.  Copy the full path for the next section.

## 3. Set JAVA_HOME
Get the full path to your **JAVA** executable:

```bash
~$ ls -l /etc/alternatives/java
lrwxrwxrwx 1 root root 43 Sep 26  2023 /etc/alternatives/java -> /usr/lib/jvm/java-22-openjdk-amd64/bin/java

```

OpenDaylight requires that **JAVA_HOME** points to the parent **JAVA** directory and **NOT** the **JAVA** executable.  

To accommodate, remove **bin/java** from the path.  

> On Ubuntu LTS 24.04, the **JAVA 22** JDK resides in **/usr/lib/jvm/java-22-openjdk-amd64**

Edit your **BASH resource file** to persist the **JAVA_HOME** environment variable.

```bash
$ echo 'export JAVA_HOME=/usr/lib/jvm/java-22-openjdk-amd64' >> ~/.bashrc
```

Ubuntu will load your **BASH resource file** at each login.  

If you want to load the **JAVA_HOME** environment variable, you can (1) exit your shell and log back in or (2) **source** your **.bashrc**:

```bash
$ source ~/.bashrc
```

Double check that ***$JAVA_HOME*** ends at ***/java-22-openjdk-amd64***. It must not include **/bin/java**.

```bash
$ echo $JAVA_HOME
/usr/lib/jvm/java-22-openjdk-amd64
```

## 4. Download the OpenDaylight Zip Archive
To download the **Zip** archive, you can either (1) use OpenDaylight website, or (2) use my **priceless** download table.  

> WARNING:  The ODL website includes curveballs (see below) that will aggravate you.  I recommend you use my table to get the **Zip**.

### Option 1:  The [John Sobanski](https://john.soban.ski) Table Method
OpenDaylight hides the required, pre-compiled controller binaries.  

To make life easy (for you), I located the binaries and recorded their URL in the following table.

> NOTE: You're welcome!

Post a comment at the end of this blog post if you run into any issues.

Release | Version | Year | Month
----------|--------|-----|------
[Scandium-SR0](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.21.0/karaf-0.21.0.zip) | 0.21.0 | 2024 | Sept
[Calcium-SR2](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.20.2/karaf-0.20.2.zip) | 0.20.2 | 2024 | Sept
[Potassium](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.19.3/karaf-0.19.3.zip) | 0.19.3 | 2024 | Jun
[Argon](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.18.3/karaf-0.18.3.zip) | 0.18.3 | 2023 | Nov
[Chlorine](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.17.3/karaf-0.17.3.zip) | 0.17.3 | 2023 | Jun
[Sulfur](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.16.3/karaf-0.16.3.zip) | 0.16.3 | 2022 | Dec
[Phosphorus](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.15.3/karaf-0.15.3.zip) | 0.15.3 | 2022 | May
[Silicon](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.14.4/karaf-0.14.4.zip) | 0.14.4 | 2022 | Jan
[Aluminum](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.13.4/karaf-0.13.4.zip) | 0.13.4 | 2021 | Jun
[Magnesium](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.12.3/karaf-0.12.3.zip) | 0.12.3 | 2020 | Dec
[Sodium](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.11.4/karaf-0.11.4.zip) | 0.11.4 | 2020 | Aug
[Neon](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.10.3/karaf-0.10.3.zip) | 0.10.3 | 2019 | Dec
[Fluorine](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.9.3/karaf-0.9.3.zip)| 0.9.3 | 2019 | Jun
[Oxygen](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip) | 0.8.4 | 2018 | Dec
[Nitrogen](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.7.3/karaf-0.7.3.zip) | 0.7.3 | 2018 | May
[Carbon](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.6.4-Carbon/distribution-karaf-0.6.4-Carbon.zip) | 0.6.4 | 2018 | Apr
[Boron](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.5.4-Boron-SR4/distribution-karaf-0.5.4-Boron-SR4.zip) | 0.5.4 | 2017 | Jun
[Beryllium](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.4.4-Beryllium-SR4/distribution-karaf-0.4.4-Beryllium-SR4.zip) | 0.4.4 | 2016 | Nov
[Lithium](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.3.4-Lithium-SR4/distribution-karaf-0.3.4-Lithium-SR4.zip) | 0.3.4 | 2016 | Mar
[Helium](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.2.4-Helium-SR4/distribution-karaf-0.2.4-Helium-SR4.zip) | 0.2.4 | 2015 | Aug

Copy the link to your desired release.  Right click the version, and select **Copy link address**. 

![Right Click my Table]({static}/images/Install_Opendaylight_Ubuntu_Lts_Fast/08_Table_Right_Click.png)

Use a **CURL** command with capital **O** ("Oscar" - **Not** Zero) to yank the **Zip** from the copied link.

In the example below, I download the **Potassium** release.

```bash
$ curl -XGET -O https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.19.2/karaf-0.19.2.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  252M  100  252M    0     0   138M      0  0:00:01  0:00:01 --:--:--  138M
```

> NOTE:  You want the **Zip's** name to begin with **karaf** and not **opendaylight**.

If you have the right **Zip** in hand, then skip the next section.

### Option 2: Navigate the OpenDaylight Download page.
From the OpenDaylight project's [home page](https://www.opendaylight.org) and click **Developer**.

> NOTE: If you completed the section above, then skip this option.

From the Hamburger Menu (Three Horizontal Bars), click **Get Started**.

![Click Hamburger]({static}/images/Odl_Ubuntu_Lts_24_04/01_Click_Hamburger.png)

Click **Download**.

![Click the Download]({static}/images/Odl_Ubuntu_Lts_24_04/02_Select_Download.png)

Scroll down to the section that reads **Archived Releases**.

![Archived Releases]({static}/images/Odl_Ubuntu_Lts_24_04/03_Scroll_Down.png)

Do not click on **Fluorine and Newer**, since that links to the source code.

If you hover over the link, you will not see **karaf** in the path.  This lack of **karaf** in the path indicates source code.

![Source Code Releases]({static}/images/Odl_Ubuntu_Lts_24_04/04_Bad_Download.png)

> **BEWARE:**  Avoid the **Fluorine and Newer** link.  You want precompiled binaries, and not source code.

Look for links in the **Archived Releases** section that include the word **karaf**.  Paths that include **karaf** indicate precompiled binaries.  You can find all releases in these folders, including **Potassium** and **Argon**. 

![Binary Releases]({static}/images/Odl_Ubuntu_Lts_24_04/05_Good_Download.png)

Click a link that [leads to precompiled binaries](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/).

Copy the link to your desired release.  Right click the version, and select **Copy link address**. 

![Binary]({static}/images/Install_Opendaylight_Ubuntu_Lts_Fast/07_The_Bin.png)

Use a **CURL** command with capital **O** ("Oscar" - **Not** Zero) to yank the **Zip** from the copied link.

```bash
$ curl -XGET -O https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.12.2/karaf-0.12.2.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  260M  100  260M    0     0  32.5M      0  0:00:07  0:00:07 --:--:-- 35.6M
```
## 5. Install OpenDaylight
Use the Ubuntu **ls** command to validate the **CURL** download.

> NOTE:  You may see a different version number.

```bash
$ ls
karaf-0.19.2.zip
```

> NOTE:  The **Zip** name must start with **karaf** and not **opendaylight**.  If you do not see the word **karaf** in your **Zip's** name then return to **Step 4**

**unzip** the **Zip archive**.

```bash
$ unzip karaf-0.19.2.zip 
```

If you enter the un-zipped directory and list the contents, you should see a **bin** directory.

```bash
~$ :~$ cd karaf-0.19.2/
~/karaf-0.19.2$ ls
CONTRIBUTING.md  LICENSE  README.md
bin  configuration  data  deploy
etc  lib  system

```
## 6. Start OpenDaylight
Start **OpenDaylight** with the **karaf** command.

```bash
Apache Karaf starting up. Press Enter to open the shell now...
100% [========================================================================]

Karaf started in 0s. Bundle stats: 20 active, 20 total

    ________                       ________                .__  .__       .__     __
    \_____  \ ______   ____   ____ \______ \ _____  ___.__.|  | |__| ____ |  |___/  |_
     /   |   \\____ \_/ __ \ /    \ |    |  \\__  \<   |  ||  | |  |/ ___\|  |  \   __\
    /    |    \  |_> >  ___/|   |  \|    `   \/ __ \\___  ||  |_|  / /_/  >   Y  \  |
    \_______  /   __/ \___  >___|  /_______  (____  / ____||____/__\___  /|___|  /__|
            \/|__|        \/     \/        \/     \/\/            /_____/      \/


Hit '<tab>' for a list of available commands
and '[cmd] --help' for help on a specific command.
Hit '<ctrl-d>' or type 'system:shutdown' or 'logout' to shutdown OpenDaylight.

opendaylight-user@root>
                                            
```

![OpenDaylight Splash!]({static}/images/Install_Opendaylight_Ubuntu_Lts_22_04/07_Odl_Splash.png)

The **release** distributions provide **all** features for install.

```bash
opendaylight-user@root>feature:list
```

![OpenDaylight List!]({static}/images/Install_Opendaylight_Ubuntu_Lts_22_04/08_Feature_List.png)

## 7.  How do I install DLUX?
OpenDaylight stopped support of the [OpenDaylight User Experience (DLUX) User Interface (UI)](https://docs.opendaylight.org/en/stable-nitrogen/getting-started-guide/common-features/dlux.html) in 2019.

If you attempt to install **DLUX** on a post-Oxygen release, Karaf will bark: **Error executing command: No matching features for odl-l2switch-switch-ui**.

```bash
opendaylight-user@root>feature:install odl-l2switch-switch-ui
Error executing command: No matching features for odl-l2switch-switch-ui/0
opendaylight-user@root>
```   

To use the **DLUX** UI, install [Oxygen](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip) or earlier.

[Oxygen](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip), [Helium](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.2.4-Helium-SR4/distribution-karaf-0.2.4-Helium-SR4.zip), [Lithium](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.3.4-Lithium-SR4/distribution-karaf-0.3.4-Lithium-SR4.zip), [Beryllium](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.4.4-Beryllium-SR4/distribution-karaf-0.4.4-Beryllium-SR4.zip), [Boron](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.5.4-Boron-SR4/distribution-karaf-0.5.4-Boron-SR4.zip), [Carbon](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.6.4-Carbon/distribution-karaf-0.6.4-Carbon.zip) and [Nitrogen](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.7.3/karaf-0.7.3.zip) all support **DLUX**.

### Install a version that supports **DLUX**
Press **Control+D** to stop your **Karaf** session.

Download a **DLUX** compliant version into your home dir.

```bash
~/karaf-0.19.2$ cd ~
~$ curl -O https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  351M  100  351M    0     0  70.8M      0  0:00:04  0:00:04 --:--:-- 75.8M
```

Unzip the **Zip** file.

```bash
~$ unzip karaf-0.8.4.zip 
```

Enter the new directory and start the service.

```bash
~$ cd karaf-0.8.4/
~/karaf-0.8.4$ ./bin/karaf 
Error occurred during initialization of boot layer
java.lang.module.FindException: Module java.xml.bind not found
```

You might see the error:  

> Error occurred during initialization of boot layer   
> java.lang.module.FindException: Module java.xml.bind not found

The Java foundation removed **java.xml.bind** from the **JAVA JDK** in 2018.

The Java 11 release (2018) reads:

> java.xml.bind (JAXB) - REMOVED
> 
> - Java 8 - OK
> - Java 9 - DEPRECATED
> - Java 10 - DEPRECATED
> - Java 11 - REMOVED

If you install **JAVA 10** or earlier, you will fix the OpenDaylight issue **java.lang.module.FindException: Module java.xml.bind not found**.

**JAVA 8**, for example, fixes the issue.

```bash
$ sudo apt-get install openjdk-8-jre
```

Configure Ubuntu to use **JAVA 8** instead of **JAVA 22** with the  **update-alternatives** command.

> NOTE: Ubuntu accommodates multiple versions of **JAVA** without any problems

Select **JAVA 8** from the menu.  In the example below I choose **option 2**.

```bash
$ sudo update-alternatives --config java
There are 2 choices for the alternative java (providing /usr/bin/java).

  Selection    Path                                            Priority   Status
------------------------------------------------------------
* 0            /usr/lib/jvm/java-22-openjdk-amd64/bin/java      2211      auto mode
  1            /usr/lib/jvm/java-22-openjdk-amd64/bin/java      2211      manual mode
  2            /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java   1081      manual mode


Press <enter> to keep the current choice[*], or type selection number: 2
update-alternatives: using /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java to provide /usr/bin/java (java) in manual mode
```

Verify that Ubuntu registered the older version:

```bash
$ java -version
openjdk version "1.8.0_402"
OpenJDK Runtime Environment (build 1.8.0_402-8u402-ga-2ubuntu1~23.10.1-b06)
OpenJDK 64-Bit Server VM (build 25.402-b06, mixed mode)
```

>  NOTE:  If you see **Error: Could not create the Java Virtual Machine.** check that you did not use two dashes for **-version**
```
Update your **bashrc** file.

Find the path to the new (old) **JAVA 8**.

```bash
$ ls -l /etc/alternatives/java
lrwxrwxrwx 1 root root 46 Jul 30 14:31 /etc/alternatives/java -> /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java
```

In **JAVA_HOME**, remove the **bin/java** suffix.

Turn the path:

> /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java

Into:

> /usr/lib/jvm/java-8-openjdk-amd64/jre


**vim** the ~/.bashrc file.

```bash
~$: vim ~/.bashrc
```

Change:

> export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

To:

> export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre

...and source the file.

```bash
~$ source ~/.bashrc
```

**echo** your **JAVA_HOME** environment variable.

```bash
~$ echo $JAVA_HOME 
/usr/lib/jvm/java-8-openjdk-amd64/jre
```

Enter the directory that contains the new (old) **DLUX** compliant version of **ODL**.

```bash
$ cd ~/karaf-0.8.4/
~/karaf-0.8.4$ 
```

Start the OpenDaylight application.

```bash
:~/karaf-0.8.4$ ./bin/karaf 
Apache Karaf starting up. Press Enter to open the shell now...
100% [========================================================================]

Karaf started in 0s. Bundle stats: 13 active, 13 total
                                                                                           
    ________                       ________                .__  .__       .__     __       
    \_____  \ ______   ____   ____ \______ \ _____  ___.__.|  | |__| ____ |  |___/  |_     
     /   |   \\____ \_/ __ \ /    \ |    |  \\__  \<   |  ||  | |  |/ ___\|  |  \   __\    
    /    |    \  |_> >  ___/|   |  \|    `   \/ __ \\___  ||  |_|  / /_/  >   Y  \  |      
    \_______  /   __/ \___  >___|  /_______  (____  / ____||____/__\___  /|___|  /__|      
            \/|__|        \/     \/        \/     \/\/            /_____/      \/          
                                                                                           

Hit '<tab>' for a list of available commands
and '[cmd] --help' for help on a specific command.
Hit '<ctrl-d>' or type 'system:shutdown' or 'logout' to shutdown OpenDaylight.
```

Autocomplete provides hints:

```bash
opendaylight-user@root>feature:install odl-l2switch-
odl-l2switch-all                       (OpenDaylight :: L2Switch :: All)   odl-l2switch-loopremover       (OpenDaylight :: L2Switch :: LoopRemover)
odl-l2switch-switch                 (OpenDaylight :: L2Switch :: Switch)   odl-l2switch-switch-rest       (OpenDaylight :: L2Switch :: Switch REST)
odl-l2switch-switch-ui           (OpenDaylight :: L2Switch :: Switch UI)   odl-l2switch-packethandler   (OpenDaylight :: L2Switch :: PacketHandler)
odl-l2switch-arphandler         (OpenDaylight :: L2Switch :: ArpHandler)   odl-l2switch-addresstracker (OpenDaylight :: L2Switch :: AddressTracker)
odl-l2switch-hosttracker       (OpenDaylight :: L2Switch :: HostTracker)
```

Install the **DLUX** UI feature:

An empty command prompt indicates installation success of **DLUX**.

```bash
opendaylight-user@root>feature:install odl-l2switch-switch-ui 
opendaylight-user@root>      
```

The DLUX console uses default credentials **admin**/**admin**.

Modify the following URL with your IP address (Keep port **8181**).

> http://<your ip address here\>:8181/index.html#/login

![OpenDaylight DLUX Login]({static}/images/How_To_Install_Opendaylight_As_A_Service_On_Ubuntu/02_DLUX_LOGIN.png)

After login, **DLUX** launches the **DLUX** console.

![OpenDaylight DLUX Console]({static}/images/How_To_Install_Opendaylight_As_A_Service_On_Ubuntu/03_DLUX.png)

## Conclusion
Today you installed and configured OpenDaylight (ODL).  

For advanced use cases, please consider my other blog posts:

- [Compile OpenDaylight from Scratch]({filename}/how-to-install-opendaylight-on-centos-or-ubuntu.md)
- [Deploy an OpenDaylight **systemd** Service]({filename}/how-to-install-opendaylight-as-a-service-on-ubuntu.md)

I recommend you watch my OpenDaylight presentation at the [Linux Foundation OpenDaylight summit in Santa Clara, California](https://youtu.be/PGl43xJQQ0g?feature=shared&t=93).

Find my slides on [SlideShare](https://www.slideshare.net/JohnSobanski/sobanski-odl-summit2015).
