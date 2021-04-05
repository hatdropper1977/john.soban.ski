Title: Create Your First Non Fungible Token (NFT) with Rarible (Part 1)
Date: 2021-02-28 10:26
Author: john-sobanski
Category: Coins
Tags: Coins
Slug: create-nft-with-rarible-part-1
Status: published

Non Fungible Tokens (NFT) allow collectors to own unique, scarce digital assets.  NFT protocols record ownership and provenance on the Ethereum Blockchain.  Recent offerings from Jack Dorsey, Logan Paul and Lindsey Lohan helped fuel the current **mania** for digital collectibles.

The NFT landscape in early 2021 attracted manic investors, eager to invest thousands of dollars into unlikely and esoteric investments.  A certain experienced Data Scientist and Cloud Professional, for example, bid nearly $900 on a Taco Gif.

![Idiotic Bid]({filename}/images/Create_Nft_With_Rarible_Part_1/01_Idiotic_Bid.png)

This blog will demonstrate how to mint a digital collectible on the [Rarible](https://rarible.com/) NFT marketplace over the course of two posts.

- Part 1: Create an Account on Rarible
- Part 2: [Create an NFT token]({filename}/create-nft-with-rarible-part-2.md)

This post describes how to create an account on Rarible.  The following bulleted list records the high-level steps required to create a Rarible account.

- Install Metamask
- Create an Ethereum Wallet
- Send Ethereum to your Wallet
- Connect to Rarible
- Customize your account

# Background
The Rarible marketplace allows creators and collectors to sell and purchase digital goods.  Rarible puts buyers directly in front of sellers via an Ethereum fueled distributed network.  This Ethereum foundation enables peer-to-peer transactions, separate from Rarible.  Since the transactions do not require Rarible in the loop, Rarible does not force users trust their site or use Rarible web servers to prove their identity.  Rarible, rather, leverages the identity services provided by Ethereum protocols.

[MetaMask](https://metamask.io) explains the Ethereum philosophy regarding account management on their website:

> Why Use MetaMask? MetaMask grants you control of your account through your browser! You don't need to ask for permission from a server with unknown location to authenticate you. MetaMask enables you to visit Ethereum enabled websites and interact with the blockchain through the website's user interface.

In summary, you don't need to give Rarible your email address or create a password to buy, sell or manage digital goods.  You do, however, need a way to connect the Rarible website to your Ethereum digital wallet.  The process to connect a digital wallet to a web page may appear cumbersome at first, but overall it provides a more secure and authoritative way to buy, sell and manage your digital goods.

# Install MetaMask
MetaMask provides a digital wallet to store Ethereum.  You create a wallet, and populate the wallet with Ethereum tokens.  MetaMask then allows you to manage your account and goods on Rarible using these Ethereum tokens.

To install MetaMask, simply go to the Chrome web store and browse for the [MetaMask Chrome extension](https://chrome.google.com/webstore/search/metamask).  Click the icon, click **Install** and Click **Add Extension**.

![Add Metamask]({filename}/images/Create_Nft_With_Rarible_Part_1/03_Add_Metamask.png)

Upon Successful installation, MetaMask will provide a welcome splash screen.

![Welcome To]({filename}/images/Create_Nft_With_Rarible_Part_1/04_Welcome_To.png)

# Create A Wallet
To create a new wallet, click **Get Started** and then click **Create a Wallet**.

![Create Wallet]({filename}/images/Create_Nft_With_Rarible_Part_1/05_Create_Wallet.png)

MetaMask then explains their data privacy policiy.  Read the policy and click **I Agree**. 

![I Agree]({filename}/images/Create_Nft_With_Rarible_Part_1/06_I_Agree.png)

Create a password.  The password provides a shortcut to allow you to log into MetaMask without needing to re-enter your seed phrase (described below) or private key.

![Create Password]({filename}/images/Create_Nft_With_Rarible_Part_1/07_Create_Password.png)

The seed phrase, common amongst most if not all cryptos, provides a human-readable version of your private key.  Click the button that reads **CLICK HERE TO REVEAL SECRET WORDS**.

![Seed Phrase]({filename}/images/Create_Nft_With_Rarible_Part_1/08_Seed_Phrase.png)

Guard your seed phrase with your life.  Whoever owns the seed phrase owns all of the tokens and digital goods associated with your wallet.  Write the seed phrase down, put it in an envelope and put that envelope in a safe deposit box.  Make several copies.  If you lose your seed phrase you could lose all of your coins.

![Super Secret]({filename}/images/Create_Nft_With_Rarible_Part_1/09_Super_Secret.png)

MetaMask requires you to re-input your seed phrase.  Drag the boxes in the correct order to proceed.

![Click Confirm]({filename}/images/Create_Nft_With_Rarible_Part_1/10_Click_Confirm.png)

MetaMask provides some suggestions for preserving and protecting your seed phrase.  Click **All Done**.

![Congrats Splash]({filename}/images/Create_Nft_With_Rarible_Part_1/11_Congrats_Splash.png)

Close out the **Token Swap** window.

![Token Swap]({filename}/images/Create_Nft_With_Rarible_Part_1/12_Token_Swap.png)

MetaMask now re-directs the web page to your empty wallet.  Click the **buy** icon.  You will need Ethereum to mint NFTs (e.g. create digital art and sell it on Rarible).

![Your Wallet]({filename}/images/Create_Nft_With_Rarible_Part_1/13_Your_Wallet.png)

Select **Directly Deposit Ether** and then click **View Account**.

![Select Deposit]({filename}/images/Create_Nft_With_Rarible_Part_1/14_Select_Deposit.png)

MetaMask now provides you with your Ethernet wallet address.  Copy this address.  You will send Ethereum to this address.

![Copy Address]({filename}/images/Create_Nft_With_Rarible_Part_1/15_Copy_Address.png)

# Send Ethereum to Your Wallet
Go to [Coinbase](https://www.coinbase.com/) to purchase Ethereum.  If you need help with creating an account, then open [this link](https://help.coinbase.com/en/coinbase/getting-started/getting-started-with-coinbase/create-a-coinbase-account) in a new tab and follow the directions.  

> Note:  I do not get any referrals from Coinbase or Rarible

Once you log in and have funds, click **Buy/Sell**

![Click Buy]({filename}/images/Create_Nft_With_Rarible_Part_1/16_Click_Buy.png)

Select Ethereum (Bitcoin won't do) and buy some Ethereum.  Around 0.050 Ethereum suffices, but buy some more if you would like to buy artwork.

![Buy Ethereum]({filename}/images/Create_Nft_With_Rarible_Part_1/17_Buy_Ethereum.png)

Coinbase converts the Dollars to Ethereum.  Click **Buy Now**.

![Confirm Buy]({filename}/images/Create_Nft_With_Rarible_Part_1/18_Confirm_Buy.png)

Close the window and Click **Send/ Recieve** (next to the **Buy/Sell** button).

In the send form, copy and paste your wallet address into the **to** field.  This will send money to MetaMask.  You will keep this money. Click **Continue**.

![Send Eth]({filename}/images/Create_Nft_With_Rarible_Part_1/19_Send_Eth.png)

Click **Send Now**.

![Send Now]({filename}/images/Create_Nft_With_Rarible_Part_1/20_Send_Now.png)

Coinbase confirms the transaction.

![Send Confirmed]({filename}/images/Create_Nft_With_Rarible_Part_1/21_Send_Confirmed.png)

Wait a few minutes and return to your MetaMask wallet.  MetaMask will now show your balance.

![Money Wallet]({filename}/images/Create_Nft_With_Rarible_Part_1/22_Money_Wallet.png)

# Connect to Rarible
Navigate to the [Rarible web page](https://rarible.com).  Click **Connect Wallet** in the upper right corner.

![Click Connect]({filename}/images/Create_Nft_With_Rarible_Part_1/23_Click_Connect.png)

Select MetaMask from the list of providers.

![Select Mm]({filename}/images/Create_Nft_With_Rarible_Part_1/24_Select_Mm.png)

Click **Next** on the MetaMask Pop-Up.

![Click Next]({filename}/images/Create_Nft_With_Rarible_Part_1/25_Click_Next.png)

Click **Proceed** to accept the terms of service.

![Click ToS]({filename}/images/Create_Nft_With_Rarible_Part_1/26_Click_ToS.png)

You just created and logged into an account on Rarible.

# Customize Your Profile
Click your picture in the upper right (looks like an Atari 2600 sprite) and then click **Edit Profile**
![Edit Profile]({filename}/images/Create_Nft_With_Rarible_Part_1/27_Edit_Profile.png)

Fill out your profile and Upload a picture.

![Config Profile]({filename}/images/Create_Nft_With_Rarible_Part_1/28_Config_Profile.png)

Once you click **submit**, MetaMask will prompt you for a **Sign** request.  MetaMask will use your private key to digitally sign the update request and post the change to the Ethernet blockchain.

![Sign Profile]({filename}/images/Create_Nft_With_Rarible_Part_1/29_Sign_Profile.png)

You now have an account on Rarible with a username and Avatar picture.

# Conclusion
NFTs provide an exciting and fun investment vehicle.  With Rarible you can buy and manage digital creations.  At this point you can buy NFTs, which you will own in perpetuity.

Since you have an account on Rarible and some Ethereum in your wallet, you may want to purchase some of my digital artwork.  I created [isometric pixel art of the Eames Lounge Chair and Ottoman](https://rarible.com/token/0xd07dc4262bcdbf85190c01c996b4c06a461d2430:254537:0x011ffdd17a0232b017d51d9d7d29a936c36f0dfa) in MS paint.

![For Sale]({filename}/images/Create_Nft_With_Rarible_Part_1/30_For_Sale.png)

[Next month]({filename}/create-nft-with-rarible-part-2.md) I will provide a fun, straightforward HOWTO on how to create and sell your own NFTs.
