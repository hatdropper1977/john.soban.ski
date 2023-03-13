Title: Host a 100% Decentralized Website on the Ethereum Platform
Date: 2021-11-25 15:26
Author: john-sobanski
Category: Coins
Tags: Coins, ENS, IPFS, NFT, Rarible, Darkblock
Slug: crypto-website
Status: published

The free and open [Ethereum](https://ethereum.org/en/) platform delivers the following benefits to developers and end-users:

-  Impervious to censorship
-  Native payment system
-  Universal, plug and play Database
-  Global, anonymous login
-  100% Uptime

This blog post demonstrates how to use [InterPlanetary File System (IPFS)](https://ipfs.tech) with [Ethereum Name Service (ENS)](https://ens.domains) to host a static website on the Ethereum platform.

In this demo we will:

-  Get an Ethereum Account (Wallet)
-  Mint a [Non Fungible Token (NFT)]({tag}nft)
-  Host a Website on IPFS 
-  Register an ENS domain
-  Link our ENS domain to our IPFS website

## Get a Wallet
You must get an Ethereum wallet to use the new blockchain-enabled web.  An Ethereum wallet holds your private key and allows you to use Decentralized Applications (dApps).

You can get a wallet from several providers.  In past [blog posts I demonstrated how to use Metamask]({tag}rarible) to get an Ethereum wallet.  In this blog post I will show you how to use the [Brave Browser]({tag}brave) to get an Ethereum wallet.  To get a wallet from [Brave]({filename}/brave-verified-creator.md), simply open Brave, click the Hamburger icon and select **Wallet**.

![Brave Welcome]({static}/images/Crypto_Website/01_Brave_Welcome.png)

Click **Get Started**.

![Get Started]({static}/images/Crypto_Website/02_Get_Started.png)

Click **continue** on the **Back up your crypto wallet** screen. 

![Recovery Phrase]({static}/images/Crypto_Website/03_Recovery_Phrase.png)

Brave displays a 12 word recovery phrase.  Write the phrase down on paper.  The phrase contains your Wallet private key.  If a hacker gets your recovery phrase, she will get all of your coins.

Once you write down your phrase click **next** and Brave will ask you to re-enter the phrase.  Complete this task and click through to the next screen.

After you complete the recovery phrase task, you see an empty wallet. 

![Buy Eth]({static}/images/Crypto_Website/04_Buy_Eth.png)

In order to proceed with the activities below, you will need to fill your wallet with Ethereum.  You can either click the **continue to Wyre** button to buy Ethereum, or use Coinbase to send Ethereum to your wallet.  If you would like to use Coinbase, right click [here]({filename}/create-nft-with-rarible-part-1.md) and open in another tab to see [how to use Coinbase to send Ethereum to your wallet]({filename}/create-nft-with-rarible-part-1.md).

> NOTE: I do not have **any** affiliation with either Wyre or Coinbase

Below, I use Wyre and pay $400 for some ETH.

![Pay Eth]({static}/images/Crypto_Website/05_Pay_Eth.png)

That $400 translates to about 0.08 ETH.

![Eth Bought]({static}/images/Crypto_Website/06_Eth_Bought.png)

## Distributed App Intro - OpenSea
Ethereum drives dApps, which use the global Ethereum blockchain to manage digital identities, content and ownership.

[OpenSea](https://opensea.io), for example provides a Web based user interface to track, manage and sell [Non Fungible Tokens]({tag}nft) on the Ethereum blockchain.

![OpenSea Splash]({static}/images/Crypto_Website/07_Opensea_Splash.png)

Use your digital wallet to log into OpenSea.  Click the **Connect** button and then sign the connection request.

![Connect Metamask]({static}/images/Crypto_Website/08_Connect_Metamask.png)

OpenSea pulls your account info directly from the blockchain.  Right now we do not have any activity on the blockchain, so we do not see anything interesting on the Splash page.

![OpenSea Home]({static}/images/Crypto_Website/09_Opensea_Home.png)

After we get some digital assets in our new wallet, however, we will look at several dApps to demonstrate the global nature of the Ethereum blockchain.  Also, later in this post, we will change the string of hex (**0x84916411a80C9C60AD3433A26aEe49805239Bd04**) that records our Ethereum wallet's address to a human-readable name via the [Ethereum Name Service](https://ens.domains).

## Publish to InterPlanetary File System (IPFS)
The [InterPlanetary File System (IPFS)](https://ipfs.tech) provides a massive, decentralized, distributed file system.  Think of an [Amazon Web Service (AWS) Simple Storage Service (S3)](https://aws.amazon.com/s3/) owned and maintained by the public, vs. a trillion dollar company. (To my stickler nerd friends - the IPFS protocol acts closer in spirt to AWS [CloudFront](https://aws.amazon.com/cloudfront/) vs. AWS S3).

Each IPFS user hosts and receives data, following a protocol similar to [Napster](https://en.wikipedia.org/wiki/Napster) back in the day.  To use IPFS, you must first download and install the IPFS client.  The [IPFS website](https://ipfs.tech/#install) provides a desktop client for Windows, Linux and Mac.

![Install Ipfs]({static}/images/Crypto_Website/10_Install_Ipfs.png)

Github hosts the [IPFS client repository](https://github.com/ipfs/ipfs-desktop/releases/tag/v0.17.0).  Scroll down to find the installer for your system.  Download the **.exe** file, for example, for the Windows installer.

![Ipfs Github]({static}/images/Crypto_Website/11_Ipfs_Github.png)

Click through the Install wizard.

![Installing Ipfs]({static}/images/Crypto_Website/12_Installing_Ipfs.png)

Once you launch the desktop application, upload a website.

I have a web page that points to a copy of my daughter Lia's superhero creation - **Loserman**.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Loserman!  By Lia Sobanski</title>
    <meta
      name="description"
      content="The origin of Loseman."
    />
    <meta name="author" content="Lia Sobanski." />
  </head>
  <body>
  <h1>Behold Loserman and Orange Peeler!</h1>
  <img src="./loserman.png">
  </body>
  </html>
```

I shove the HTML and PNG files into a local folder and then click **+Import Folder** to send my website to IPFS.

![Import Folder]({static}/images/Crypto_Website/13_Import_Folder.png)

The desktop client uploads my website to IPFS.

![Folder Imported]({static}/images/Crypto_Website/14_Folder_Imported.png)

To see the website, click the ellipses next to your uploaded web folder and then select **Share Link**.  IPFS then shows a web address that points to the content of your website.

![Share Link]({static}/images/Crypto_Website/15_Share_Link.png)

Paste this link into any browser to see your website.  Keep in mind that IPFS takes dozens of minutes to catch up.

## Create an NFT
The Ethereum blockchain records both our Ethereum account's actions and our Ethereum account's assets.

Let's create and sell an NFT to add some interesting history to our account.

[OpenSea](https://opensea.io) and [Rarible]({filename}/create-nft-with-rarible-part-1.md) both provide a dApp to create [NFT's]({tag}nft). In OpenSea, for example, click **Create Item**.

![Create Item]({static}/images/Crypto_Website/17_Create_Item.png)

I upload my daughter's picture of **Loserman**.

![Create One]({static}/images/Crypto_Website/18_Create_One.png)

I click through and complete the Wizard.  Once I finish, OpenSea states that I created the digital asset.

![Loserman Nft]({static}/images/Crypto_Website/19_Loserman_Nft.png)

OpenSea and Rarible now use [Lazy Minting](https://search.brave.com/search?q=lazy-minting&source=desktop).  The dApps do not mint the NFT token until a buyer buys the token.  In this method, the buyer pays the (very costly) minting fees.

In order to mint the NFT, therefore, we must sell it.  To sell the item, click the ellipses on the NFT and then click **Sell**.

![Sell Nft]({static}/images/Crypto_Website/20_Sell_Nft.png)

Before you can sell an item, OpenSea requires you to pay a one-time fee to **register your wallet**, which includes a pricey gas fee.  I pay $241.00 for this privilege.

![Sell Two]({static}/images/Crypto_Website/21_Sell_Two.png)

Click through the Wizard and sign the digital paperwork.

![Sell Three]({static}/images/Crypto_Website/22_Sell_Three.png)

After the registration fee, OpenSea lists (but does not mint) your item.

![Sell Four]({static}/images/Crypto_Website/23_Sell_Four.png)

From a [different Ethereum account](https://opensea.io/sobanski.eth) I click on the **Buy Now** button, to buy (and mint) the **Loserman** NFT.

![Lia Buy]({static}/images/Crypto_Website/24_Lia_Buy.png)

I need to pay $117 to mint the item.  I use Metamask to confirm this.

![Pay Mint]({static}/images/Crypto_Website/25_Pay_Mint.png)

OpenSea mints the item and completes the purchase.

![Purchased Nft]({static}/images/Crypto_Website/26_Purchased_Nft.png)

## Shared dApp Ecosystem 
OpenSea used the Ethereum blockchain to mint, manage and sell my NFT.  Other dApps that use the Ethereum blockchain to mint, manage and sell NFTs see the transactions immediately.

[Rarible]({tag}rarible), for example, displays the creation of the NFT.

![On Rarible]({static}/images/Crypto_Website/27_On_Rarible.png)

[Darkblock]({tag}darkblock) also catches the NFT.

![On Darkblock]({static}/images/Crypto_Website/28_On_Darkblock.png)

In a Web 2.0 Architecture, OpenSea, Rarible and Darkblock would each have their own database to track NFT creation, logistics and permissions.  In the Web 3.0 (how long will that name stick?) construct, all three dApps use the same **database** for their back-ends... the Ethereum Blockchain.

## Ethereum Name Service (ENS)
The Internet Domain Name Service (DNS) maps human-readable names to Internet Protocol Addresses.  [John.Soban.Ski](https://john.soban.ski), for example, points to the IP address [65.9.83.48](https://www.nslookup.io/domains/john.soban.ski/dns-records/).

In a similar manner, the [Ethereum Name Service (ENS)](https://ens.domains) maps our forty character Ethereum wallet address to a human readable name.  I will demonstrate this in action.

First, we need to find a name.  The [ENS dApp](https://app.ens.domains) lets us search for available names.  

I decide to look for the name [Gosh Darn It (GDIT) dot ETH ](https://app.ens.domains/search/gdit), and find that I can buy that name.

![Gdit Name]({static}/images/Crypto_Website/29_Gdit_Name.png)

ENS quotes a rough estimate of $300 to buy the domain, with half going to Ethereum gas.

![Pay Fee]({static}/images/Crypto_Website/30_Pay_Fee.png)

I use my wallet to connect to the dApp, and sign the requests.

![Request Register]({static}/images/Crypto_Website/31_Request_Register.png)

I pay $302.19 to snag [gdit.eth](https://gdit.eth.link).

![Pay Alot]({static}/images/Crypto_Website/32_Pay_Alot.png)

I use the ENS dApp and connect [gdit.eth](https://etherscan.io/address/gdit.eth) to my Ethereum wallet address.

![Set Primary]({static}/images/Crypto_Website/33_Set_Primary.png)

I need to pay $68 in gas to associate the name to the wallet.

![Pay More]({static}/images/Crypto_Website/34_Pay_More.png)

[Etherscan](https://etherscan.io/address/gdit.eth) summarizes blockchain activity.

I can use Etherscan to profile my wallet using either my hex address (**0x84916411a80C9C60AD3433A26aEe49805239Bd04**), or my [gdit.eth](https://etherscan.io/address/gdit.eth) name.  Either way, Etherscan replaces the HEX in the transaction log with **gdit.eth**.

![Etherscan Update]({static}/images/Crypto_Website/35_Etherscan_Update.png)

## Decentralized Website Hosting
Our IPFS website (above) lives on the decentralized, distributed, global IPFS file share. We will configure ENS to serve up the content of our IPFS website via a Content ID (CID) number.  The IPFS desktop client provides a Content ID (CID) for the website we launched.

**bafybeia4rjakzczwxbjllzcsx5h3wjmk6qy3hohkxwfwkvgqqjyebry7jq**

To link this CID to our domain name, we must paste this CID in the **Content** section of ENS.  This tells ENS to map **gdit.eth** to the website hosted on IPFS.

> NOTE:  ENS maps one name to several protocols (Ethereum, Bitcoin, IPFS) and knows which one to use based on context

![Set Content]({static}/images/Crypto_Website/36_Set_Content.png)

After another charge of $177 ENS sets the **Content** record for [gdit.eth](https://gdit.eth.link).

![Ipfs Link]({static}/images/Crypto_Website/37_Ipfs_Link.png)

At present time (November 2021) not all browsers support the IPFS protocol.  

Append **.link** to the end of Ethereum domains to use an IPFS proxy and access IPFS websites through **ANY** browser.

![Eth Link]({static}/images/Crypto_Website/38_Eth_Link.png)

## Conclusion
In this demo we used two dApps to host a static website.  Our [website](https://gdit.eth.link) now reaps the benefits of the Ethereum ecosystem, including zero censorship, 100% availability, global reach and immutability.  

If you enjoyed this blog post please click on some of the tags below to find similar content, or check out my NFT's on [Rarible](https://rarible.com/sobanski/owned).
