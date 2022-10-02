Title: Turn Your Cellphone into a Secure Shell (SSH) Terminal
Date: 2022-08-28 11:11
Author: john-sobanski
Category: howto
Tags: AWS, Brave, HOWTO, IAM, Linux, Twiddler
Slug: cellphone-ssh
Status: published

Relive the glory days of [dumb terminals](https://en.wikipedia.org/wiki/Computer_terminal#Character-oriented_terminal) with your thousand dollar cellphone!

Programmers used terminals, decades ago, to log into and execute commands on remote computer systems.  The terminal provided a screen and keyboard to computer scientists and phoned home to a multi-million dollar mainframe.  Today, we use [Secure Shell (SSH)](https://en.wikipedia.org/wiki/Secure_Shell) in the same fashion, to log into a remote server that lives in a multi-billion dollar Cloud Service Provider (CSP).

This month I demonstrate how to configure both an Amazon Web Services (AWS) Elastic Compute Cloud (EC2) server and your cellphone to execute SSH commands on the go.

## Launch a Server and Retrieve a Key 
Your SSH client requires the appropriate [Privacy Enhanced Mail (PEM)](https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail) key associated with your server.  If you do not have a PEM key, I will quickly explain how to retrieve one upon server launch.  

I recommend you follow these steps on the cellphone that you wish to use for SSH communications.

First, sign into the AWS console at [aws.amazon.com](https://aws.amazon.com).  You can either enter the email address of your root account (not recommended), or enter your account alias.

Below, I enter my account alias - **Cobra Commander**. 

![Aws Sign]({filename}/images/Cellphone_Ssh/00_Aws_Sign.png)

Enter the username and password of an account that has the correct privileges to launch an EC2 instance.

![Iam Sign]({filename}/images/Cellphone_Ssh/01_Iam_Sign.png)

Click the ICON for **EC2**.

![Select Ec2]({filename}/images/Cellphone_Ssh/02_Select_Ec2.png)

Select **Instances**.

![Click Instances]({filename}/images/Cellphone_Ssh/03_Click_Instances.png)

Select **Launch instances**.

![Launch Instances]({filename}/images/Cellphone_Ssh/04_Launch_Instances.png)

Name your instance.  I name mine **Sobanski Jumpbox**.

![Name Instance]({filename}/images/Cellphone_Ssh/05_Name_Instance.png)

You can leave the defaults for **Amazon Machine Image** and **Instance Type**.  Different **AMI** use different default user names.  I use **Amazon Linux**, which provides a default user name of **ec2-user**.

Select the link that reads **Create new key pair**.

![Create Key]({filename}/images/Cellphone_Ssh/06_Create_Key.png)

Name your key pair.  I name mine **Jumpbox-cellphone**.  You must select the radio button that commands AWS to encode the key into **PEM** format.  Our **SSH Client** requires a **PEM** encoded Key.

Click **Create key pair**.

![Save Pem]({filename}/images/Cellphone_Ssh/07_Save_Pem.png)

Your browser downloads the PEM file to your phone.

Save and protect this file.  Anyone that holds this key can log into your server.  If you lose this key, you can no longer log into your server.

In the example below, I use the [Brave browser]({filename}/brave-verified-creator.md).

![Download File]({filename}/images/Cellphone_Ssh/08_Download_File.png)

For extra security, limit access to your server to the IP address of your cellphone.  If you have not used [Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) before, this may lead to headaches with connectivity.

If you just want to try out the SSH client, you can set the rule to **Anywhere** but keep in mind hoards of bots will try to brute force your server.

![My Ip]({filename}/images/Cellphone_Ssh/09_My_Ip.png)

Launch the instance once the configuration satisfies you.

![Launch Instance]({filename}/images/Cellphone_Ssh/10_Launch_Instance.png)

Amazon provides a splash page for success.

![Launch Success]({filename}/images/Cellphone_Ssh/11_Launch_Success.png)

You can click the hyperlink for the **Instance ID** to learn about your new server's configuration details.

![Success Launch]({filename}/images/Cellphone_Ssh/12_Success_Launch.png)

## Install and Configure JuiceSSH
[JuiceSSH](https://juicessh.com/) provides a **SSH** client for your smart phone.  JuiceSSH also works on Chromebooks.

Their website reads that **75k** new people a month install JuiceSSH!

![Install Juice]({filename}/images/Cellphone_Ssh/13_Install_Juice.png)

JuicsSSH, once installed, displays a modest splash screen.  Click **Manage Connections**.

![Juice Splash]({filename}/images/Cellphone_Ssh/14_Juice_Splash.png)

Click the **plus** sign to add a new connection.

![Click Plus]({filename}/images/Cellphone_Ssh/15_Click_Plus.png)

Your new connection requires an **identity**.  Select **New...** and the app will provide a file picker.  Use the file picker to select the **PEM** you downloaded in step one, above.  The **PEM** provides an identity. 

![New Identity]({filename}/images/Cellphone_Ssh/16_New_Identity.png)

Navigate the file picker to find the **PEM** you downloaded in step one, above.  I select **Downloads**.

![File Browser]({filename}/images/Cellphone_Ssh/17_File_Browser.png)

My **Downloads** folder presents my **Jumpbox-cellphone.pem** file.  I click to select.

![Click Key]({filename}/images/Cellphone_Ssh/18_Click_Key.png)

JuiceSSH recognizes that the **PEM** file contains a **Private Key**.  Since you provided a **Private Key**, you do not need to enter a **Password**.  Leave **Password** blank.

Enter **ec2-user** for **Username** and then select the **Check** icon in the upper right.

![Ec2 User]({filename}/images/Cellphone_Ssh/19_Ec2_User.png)

Navigate back to your [browser]({filename}/brave-verified-creator.md) and view the details of your **EC2** instance.  

Select the **copy** icon to copy the IP (or DNS) address of your Server.

AWS indicates that you copied your **Public IPv4 DNS**.

![Copy Dns]({filename}/images/Cellphone_Ssh/20_Copy_Dns.png)

In JuiceSSH, paste the DNS in the **Address** field of your Connection wizard.

Click the **Check** icon in the upper right.

![Paste Dns]({filename}/images/Cellphone_Ssh/21_Paste_Dns.png)

JuiceSSH presents your new connection.

![All Good]({filename}/images/Cellphone_Ssh/22_All_Good.png)

Click your **Connection** and JuiceSSH connects.

![Connect Ssh]({filename}/images/Cellphone_Ssh/23_Connect_Ssh.png)

Click Accept on the [Host Verification](https://www.ssh.com/academy/ssh/host-key) screen.

![Accept Fingerprint]({filename}/images/Cellphone_Ssh/24_Accept_Fingerprint.png)

Once in, JuiceSSH provides a quick tutorial on how to input text and commands via your phone.

![Cell Tutorial]({filename}/images/Cellphone_Ssh/25_Cell_Tutorial.png)

In the example below, I use my phone to execute an **APT Update**!

![Apt Update]({filename}/images/Cellphone_Ssh/26_Apt_Update.png)

## One Handed Keyboard
I use a small, portable [Chorded Keyboard](https://en.wikipedia.org/wiki/Chorded_keyboard) to overcome the limitations of my Android phone's onscreen keyboard. 

![Twiddler Front]({filename}/images/Cellphone_Ssh/27_Twiddler_Front.png)

The [Twiddler](https://twiddler.tekgear.com/) (Non-affiliate link) provides a full keyboard in a palm sized form-factor.  If you plan to administer your Servers, or write code on your mobile device, I recommend this keyboard.

![Twiddler Top]({filename}/images/Cellphone_Ssh/28_Twiddler_Top.png)

From the website:

> The Twiddler lets you type and navigate faster on your mobile phone, tablet, or wearable without the hindrance of a bulky traditional keyboard. Perfect when you’re away from the office or on your morning commute, the Twiddler can increase your productivity like never before.

To pair the Twiddler, simply select it from your Bluetooth menu.

![Pair Device]({filename}/images/Cellphone_Ssh/29_Pair_Device.png)

Accept the pairing request and type away!

![Pair It]({filename}/images/Cellphone_Ssh/30_Pair_It.png)

# Conclusion
Leverage the power of the cloud wherever you go.  JuiceSSH provides an SSH client on Android devices, and accepts private keys in lieu of insecure passwords.
