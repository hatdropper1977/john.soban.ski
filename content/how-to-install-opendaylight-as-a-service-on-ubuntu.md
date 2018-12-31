Title: How to install OpenDaylight as a Service on Ubuntu 18.04 LTS
Date: 2018-12-31 10:26
Author: john-sobanski
Category: HOWTO
Tags: HOWTO, SD-RAN, SDN, OpenDaylight
Slug: how-to-install-opendaylight-as-a-service-on-ubuntu
Status: published

#Introduction
[OpenDaylight](https://www.opendaylight.org/) allows cloud engineers to programmatically deploy, configure and control virtual network services.  As written on the OpenDaylight website, ODL helps Internet Service Providers, Academics and Cloud Service Providers to enable the following services:

  -  [On-demand service delivery](https://www.opendaylight.org/use-cases-and-users/by-function/automated-service-delivery)
     -  Programmatic acquisition of network transport or Virtual Private Network connections
  -  [Network Function Virtualization](https://www.opendaylight.org/use-cases-and-users/by-function/cloud-and-nfv)
     -  Add new network services to your existing Cloud Provider's (e.g. [OpenStack](https://wiki.opendaylight.org/view/OpenStack_and_OpenDaylight) ) network stack
  -  [Network Resource Optimization](https://www.opendaylight.org/use-cases-and-users/by-function/network-resource-optimization)
     -  Load balance, prioritize and pre-empt traffic to reduce congestion and idle links
  -  [Situational Awareness](https://www.opendaylight.org/use-cases-and-users/by-function/visibility-and-control)
     -  Get granular, instantaneous metrics plumbed from each and every data frame in your networks

![OpenDaylight Logo]({filename}/images/How_To_Install_Opendaylight_On_Centos_Or_Ubuntu/00_ODL.png)

The following outline records the steps necessary to install OpenDaylight on Ubuntu LTS 18.04

  1.  Prepare the operating system
  2.  Install the Java JRE
  3.  Download OpenDaylight
  4.  Install OpenDaylight
  5.  Create a ***systemd*** service configuration file
  6.  Install and enable the ***systemd*** OpenDaylight service

## Prepare operating system
Run an ***apt-get*** update to ensure that your server receives all of the most recent security and application packages.

```bash
$ sudo apt-get update
```

Now, install the following convenience packages, to make life easier.

```bash
$ sudo apt-get -y install unzip vim wget
```

## Install the Java JRE
Installation of OpenDaylight via the release **zip** archive requires the [JAVA 8](https://java.com/en/) runtime environment.  This section explains how to install the JRE.  

> If you would like to build OpenDaylight from source, please refer to this [blog post]({filename}/how-to-install-opendaylight-on-centos-or-ubuntu.md) for detailed instructions

Run the following command to install the JRE.

```bash
$ sudo apt-get -y install openjdk-8-jre
```

Now, ensure that Ubuntu points to ***JAVA 8***.  Run the following command.  If it does not point to ***JAVA 8***, be sure to select version 8 from the list.

```bash
$  sudo update-alternatives --config java
There is only one alternative in link group java (providing /usr/bin/java): /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java
Nothing to configure.
```

Copy the link to the binary above, as you will need this information in the next step.

> My ***JAVA 8*** binary resides in **/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java**.

With the path in hand, run the following command to update your **BASHRC** file.

```bash
$ echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre' >> ~/.bashrc
```

Now ***source*** your ***BASHRC*** file and then check to ensure ***$JAVA_HOME*** lives in the environment.

```bash
$ source ~/.bashrc
```

Double check that ***$JAVA_HOME*** ends with ***/jre***.

```bash
$ echo $JAVA_HOME
/usr/lib/jvm/java-8-openjdk-amd64/jre
```

## Download the OpenDaylight Zip Archive
You can download a complete (all features) release of OpenDaylight using the following links.

Release | Version | Year | Month
----------|--------|-----|------
[Flourine](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.9.1/karaf-0.9.1.zip) | 0.9.1 | 2018 | Nov
[Oxygen](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip) | 0.8.4 | 2018 | Dec
[Nitrogen](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.7.3/karaf-0.7.3.zip) | 0.7.3 | 2018 | May
[Carbon](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.6.4-Carbon/distribution-karaf-0.6.4-Carbon.zip) | 0.6.4 | 2018 | Apr
[Boron](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.5.4-Boron-SR4/distribution-karaf-0.5.4-Boron-SR4.zip) | 0.5.4 | 2017 | Jun
[Beryllium](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.4.4-Beryllium-SR4/distribution-karaf-0.4.4-Beryllium-SR4.zip) | 0.4.4 | 2016 | Nov
[Lithium](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.3.4-Lithium-SR4/distribution-karaf-0.3.4-Lithium-SR4.zip) | 0.3.4 | 2016 | Mar
[Helium](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.2.4-Helium-SR4/distribution-karaf-0.2.4-Helium-SR4.zip) | 0.2.4 | 2015 | Aug

Simply right click the Version name, select 'Copy Link' and then run the following command.  The following example depicts the command you need to execute to download ***Oxygen***.

```bash
$ wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip
--2018-12-29 16:20:10--  https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip
Resolving nexus.opendaylight.org (nexus.opendaylight.org)... 199.204.45.87, 2604:e100:1:0:f816:3eff:fe45:48d6
Connecting to nexus.opendaylight.org (nexus.opendaylight.org)|199.204.45.87|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 368625376 (352M) [application/zip]
Saving to: ‘karaf-0.8.4.zip’

karaf-0.8.4.zip          100%[==================================>] 351.55M  88.7MB/s    in 4.0s

2018-12-29 16:20:14 (86.9 MB/s) - ‘karaf-0.8.4.zip’ saved [368625376/368625376]

FINISHED --2018-12-29 16:20:14--
Total wall clock time: 4.2s
Downloaded: 1 files, 352M in 4.0s (86.9 MB/s)
```

## Install OpenDaylight
Install OpenDaylight into the Operating System.

First, make a directory for the binary.

```bash
$ sudo mkdir /usr/local/karaf
```

Move the zip archive to the install workspace and deflate the archive.  Be sure to use the correct version.  I downloaded version ***0.8.4*** and yours may be different.

```bash
$ sudo mv karaf-0.8.4.zip /usr/local/karaf
$ sudo unzip /usr/local/karaf/karaf-0.8.4.zip -d /usr/local/karaf/
```

Install ***karaf*** into user space.

```bash
$ sudo update-alternatives --install /usr/bin/karaf karaf /usr/local/karaf/karaf-0.8.4/bin/karaf 1
update-alternatives: using /usr/local/karaf/karaf-0.8.4/bin/karaf to provide /usr/bin/karaf (karaf) in auto mode

$ sudo update-alternatives --config karaf
There is only one alternative in link group karaf (providing /usr/bin/karaf): /usr/local/karaf/karaf-0.8.4/bin/karaf
Nothing to configure.

$ which karaf
/usr/bin/karaf
```

Let's do a test run.  OpenDaylight needs to write a ***PID*** file to ***/usr/bin/karaf***, which requires ***sudo*** privaleges.  Execute the ***karaf*** command via sudo and pass the ***-E*** flag to keep the ***$JAVA_HOME*** environment variable.

```bash
$ sudo -E karaf
link: /etc/alternatives/karaf
link: /usr/local/karaf/karaf-0.8.4/bin/karaf
Apache Karaf starting up. Press Enter to open the shell now...
100% [========================================================================]
Karaf started in 1s. Bundle stats: 54 active, 55 total
```

OpenDaylight starts with some radical ASCII art!

![OpenDaylight Splash]({filename}/images/How_To_Install_Opendaylight_As_A_Service_On_Ubuntu/01_ODL_Splash.png)

Now, from the ***Karaf*** command prompt, install the ***DLUX GUI***.

```bash
opendaylight-user@root>feature:install odl-l2switch-switch-ui
opendaylight-user@root>
```

It may take a few minutes to warm up.

You can verify that Karaf runs via a ***netstat***.

```bash
$ sudo netstat -an | grep 8181
tcp6       0      0 :::8181                 :::*                    LISTEN
tcp6       0      0 172.31.18.10:8181       9.20.16.23:44955     ESTABLISHED
tcp6       0      0 172.31.18.10:8181       9.20.16.23:10126     ESTABLISHED
```

Alternatively (assuming your firewall/ security groups permit it), you can go to your URL and log into the DLUX console using credentials ***admin***/***admin***.  Be sure to put your IP address in the following URL (Keep the port as ***8181***).

http://8.7.6.5:8181/index.html#/login

![OpenDaylight DLUX Login]({filename}/images/How_To_Install_Opendaylight_As_A_Service_On_Ubuntu/02_DLUX_LOGIN.png)

If you log in with ***admin***/***admin***, you will see the (pretty boring) ***DLUX*** console.

![OpenDaylight DLUX Console]({filename}/images/How_To_Install_Opendaylight_As_A_Service_On_Ubuntu/03_DLUX.png)

At this point, you can shut down the service by typing ***system:shutdown***.

```bash
opendaylight-user@root>system:shutdown
Confirm: halt instance root (yes/no): yes
opendaylight-user@root>
$
```

## Install the OpenDaylight stop script
Our OpenDaylight service requires a ***stop*** script in order to shut down ***Karaf***.  While we could 'hard code' the path in the ***systemd*** service configuration file, we will follow best practices and instead install the stop script into ***/usr/bin/***.  We will then manage the versions of ***karaf*** and ***stop*** via ***update-alternatives***.

```bash
$ sudo update-alternatives --install /usr/bin/stop stop /usr/local/karaf/karaf-0.8.4/bin/stop 1
update-alternatives: using /usr/local/karaf/karaf-0.8.4/bin/stop to provide /usr/bin/stop (stop) in auto mode

$ sudo update-alternatives --config stop
There is only one alternative in link group stop (providing /usr/bin/stop): /usr/local/karaf/karaf-0.8.4/bin/stop
Nothing to configure.

$ which stop
/usr/bin/stop
```

## Create the ***systemd*** service configuration file
Copy and paste the following ***systemd*** service configuration file into ***/etc/systemd/system/opendaylight.service***.

```bash
$ sudo vim /etc/systemd/system/opendaylight.service
```

```bash
[Unit]
Description=OpenDaylight Controller
After=network.target

[Service]
Type=simple
User=root
Group=root
Environment="JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre"
ExecStart=/usr/bin/karaf server
ExecStop=/usr/bin/stop
Restart=on-failure
RestartSec=60s

[Install]
WantedBy=multi-user.target
```

You will notice that we use the ***karaf*** and ***stop*** binaries in ***/usr/bin*** to start and stop the service.  This approach allows us to upgrade OpenDaylight via ***update-alternatives***.  We will not need to edit this configuration file in the future if we execute upgrades via ***update-alternatives***.

After edits, change the permissions of the service configuration file.

```bash
$ sudo chmod 0644 /etc/systemd/system/opendaylight.service
```

Trigger ***systemd*** to load the new ***opendaylight*** service.

```bash
$ systemctl daemon-reload
```

The ***systemctl enable*** command makes it easy to start the service at bootup.  

```bash
$ sudo systemctl enable opendaylight.service
Created symlink /etc/systemd/system/multi-user.target.wants/opendaylight.service → /etc/systemd/system/opendaylight.service.
```

We have not yet started the service, and a ***status*** command states this.

```bash
$ sudo systemctl status opendaylight
● opendaylight.service - OpenDaylight Controller
   Loaded: loaded (/etc/systemd/system/opendaylight.service; enabled; vendor preset: enabled)
   Active: inactive (dead)
```

You can now Start the service.  Alternatively, if you reboot, the service will start automatically.

```bash
$ sudo systemctl start opendaylight
```

A **ps** shows that Karaf runs.

```bash
$ ps -ef | grep karaf
root     21686     1  0 17:44 ?        00:00:00 /bin/sh /usr/bin/karaf server
root     21770 21686 99 17:44 ?        00:00:40 /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -Djava.security.properties=/usr/local/karaf/karaf-0.8.4/etc/odl.java.security -Xms128M -Xmx2048m -XX:+UnlockDiagnosticVMOptions -XX:+HeapDumpOnOutOfMemoryError -Dcom.sun.management.jmxremote -Djava.security.egd=file:/dev/./urandom -Djava.endorsed.dirs=/usr/lib/jvm/java-8-openjdk-amd64/jre/jre/lib/endorsed:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/endorsed:/usr/local/karaf/karaf-0.8.4/lib/endorsed -Djava.ext.dirs=/usr/lib/jvm/java-8-openjdk-amd64/jre/jre/lib/ext:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/ext:/usr/local/karaf/karaf-0.8.4/lib/ext -Dkaraf.instances=/usr/local/karaf/karaf-0.8.4/instances -Dkaraf.home=/usr/local/karaf/karaf-0.8.4 -Dkaraf.base=/usr/local/karaf/karaf-0.8.4 -Dkaraf.data=/usr/local/karaf/karaf-0.8.4/data -Dkaraf.etc=/usr/local/karaf/karaf-0.8.4/etc -Dkaraf.restart.jvm.supported=true -Djava.io.tmpdir=/usr/local/karaf/karaf-0.8.4/data/tmp -Djava.util.logging.config.file=/usr/local/karaf/karaf-0.8.4/etc/java.util.logging.properties -Dkaraf.startLocalConsole=false -Dkara .startRemoteShell=true -classpath /usr/local/karaf/karaf-0.8.4/lib/boot/org.apache.karaf.diagnostic.boot-4.1.6.jar:/usr/local/karaf/karaf-0.8.4/lib/boot/org.apache.karaf.jaas.boot-4.1.6.jar:/usr/local/karaf/karaf-0.8.4/lib/boot/org.apache.karaf.main-4.1.6.jar:/usr/local/karaf/karaf-0.8.4/lib/boot/org.osgi.core-6.0.0.jar org.apache.karaf.main.Main
ubuntu   21906 19962  0 17:45 pts/1    00:00:00 grep --color=auto karaf
```

***Systemctl*** also provides a status command.

```bash
$ sudo systemctl status opendaylight
● opendaylight.service - OpenDaylight Controller
   Loaded: loaded (/etc/systemd/system/opendaylight.service; enabled; vendor preset: enabled)
   Active: active (running) since Sat 2018-12-29 17:44:39 UTC; 15min ago
 Main PID: 21686 (karaf)
    Tasks: 129 (limit: 4915)
   CGroup: /system.slice/opendaylight.service
           ├─21686 /bin/sh /usr/bin/karaf server
           └─21770 /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -Djava.security.properties=/usr/local/karaf/karaf-0.8.4/etc/

Dec 29 17:44:39 ip-172-31-18-10 systemd[1]: Started OpenDaylight Controller.
Dec 29 17:44:39 ip-172-31-18-10 karaf[21686]: link: /etc/alternatives/karaf
Dec 29 17:44:39 ip-172-31-18-10 karaf[21686]: link: /usr/local/karaf/karaf-0.8.4/bin/karaf
Dec 29 17:44:40 ip-172-31-18-10 karaf[21686]: Apache Karaf starting up. Press Enter to open the shell now...
Dec 29 17:45:01 ip-172-31-18-10 karaf[21686]: [7.8K blob data]
Dec 29 17:45:01 ip-172-31-18-10 karaf[21686]: Karaf started in 20s. Bundle stats: 419 active, 420 total
```

You can stop the service via ***systemctl stop***:

```bash
$ sudo systemctl stop opendaylight
```

With the service stopped, a ***status*** command will report details of the last run.

```bash
$ sudo systemctl status opendaylight
● opendaylight.service - OpenDaylight Controller
   Loaded: loaded (/etc/systemd/system/opendaylight.service; enabled; vendor preset: enabled)
   Active: inactive (dead) since Sat 2018-12-29 18:01:18 UTC; 21s ago
  Process: 22114 ExecStop=/usr/bin/stop (code=exited, status=0/SUCCESS)
  Process: 21686 ExecStart=/usr/bin/karaf server (code=killed, signal=TERM)
 Main PID: 21686 (code=killed, signal=TERM)

Dec 29 17:44:39 ip-172-31-18-10 systemd[1]: Started OpenDaylight Controller.
Dec 29 17:44:39 ip-172-31-18-10 karaf[21686]: link: /etc/alternatives/karaf
Dec 29 17:44:39 ip-172-31-18-10 karaf[21686]: link: /usr/local/karaf/karaf-0.8.4/bin/karaf
Dec 29 17:44:40 ip-172-31-18-10 karaf[21686]: Apache Karaf starting up. Press Enter to open the shell now...
Dec 29 17:45:01 ip-172-31-18-10 karaf[21686]: [7.8K blob data]
Dec 29 17:45:01 ip-172-31-18-10 karaf[21686]: Karaf started in 20s. Bundle stats: 419 active, 420 total
Dec 29 18:01:14 ip-172-31-18-10 systemd[1]: Stopping OpenDaylight Controller...
Dec 29 18:01:14 ip-172-31-18-10 stop[22114]: link: /etc/alternatives/stop
Dec 29 18:01:14 ip-172-31-18-10 stop[22114]: link: /usr/local/karaf/karaf-0.8.4/bin/stop
Dec 29 18:01:18 ip-172-31-18-10 systemd[1]: Stopped OpenDaylight Controller.
```

# Conclusion
Now that you installed OpenDaylight as a service on Ubuntu LTS 18.04, head over to my Oracle Ravello [blog](https://blogs.oracle.com/ravello/opendaylight-on-on-aws) and try out the fun little project that I put together a few years back.

You may be interested in the demo I gave at the Linux Foundation OpenDaylight summit in Santa Clara, Califonia back in 2015.  Find the slides [here](https://www.slideshare.net/JohnSobanski/sobanski-odl-summit2015) or watch the video [here](https://www.youtube.com/watch?v=PGl43xJQQ0g).

If you get stuck, you might find my answers on the OpenDaylight ask [forums](https://ask.opendaylight.org/users/420/runamuck/) useful.
