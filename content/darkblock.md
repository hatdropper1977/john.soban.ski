Title: Darkblock Levels Up Non Fungible Token (NFT) Distribution and Access
Date: 2021-10-30 6:56
Author: john-sobanski
Category: Coins
Tags: Coins, NFT, Rarible, Darkblock
Slug: darkblock
Status: published

[Darkblock](https://www.darkblock.io) provides a decentralized application that lets creators sell (and manage) digital content directly to consumers without the need for any intermediate, proprietary or bureaucratic services.

Their splash page touts **content access controls for the decentralized creator economy**.

From a tactical perspective, Darkblock allows the creators of [Non Fungible Tokens (NFT)]({filename}/nft-value-prop.md) to attach private, one-of-a-kind, **unlockable** content to an NFT even if they **no longer have possession of that NFT**.

I find this technology fascinating, since it drives a few interesting use-cases.

  -  **Digital Drop**
     -  A rapper sells a collection of NFTs and then, on a given release date, attaches a FLAC of a new song to that NFT.  All the owners of that NFT will now have the song.
  -  **Decentralized Kickstarter**
     -  A movie producer offers a limited amount of NFT to fans.  She creates a contract that states that once all the NFT sell out, she will begin to produce the film and then release it digitally to all of the NFT owners upon completion.
  -  **Digital Scratch off tickets**
     -  Users buy an NFT and a script randomly populates each NFT with a seed phrase to another digital wallet.  The NFT owner uses that seed phrase to see if he won any valuable NFT or crypto currency.  Or the unlocked content provides Geo-coordinates that lead to a pair of popular sneakers.
  -  **Replacement of Current Streaming Services**
     -  Darkblock replaces all the functions of current streaming services. 

I will quickly dive into scenario four to illustrate the benefits of Darkblock.

Consider the current state of creative content delivery.

![Current Streaming Ecosystem]({filename}/images/Darkblock/00_Hbo_Current.png)

A creator develops (or licenses) content to a streaming service (HBO Max, HULU, Prime Video, Netflix, YouTube Red).

Users subscribe to the streaming service through either an external identity provider (Apple ID, Facebook, Google) or the streaming content providers' proprietary identity service (username and password database).

The user enters payment information in the form of a credit card account (American Express, Chase, Barclays), and the financial institution brokers the payment to the streaming content provider.  

The streaming service then provides the access management, or Digital Rights Management (DRM) of the creator's content and gatekeeps which videos the user can view and at what times.

An external cloud platform will provide the hardware, network and caching resources to store and move the video around the Internet.

Each one of these services: Identity, Payment, Content Delivery, Rights Management and Hardware Resources introduce a new organization into the streaming ecosystem.  Each organization will (1) take a cut of creator profits and (2) censor any content that imposes on their ideologies.

Contrast the current streaming ecosystem (above) to the Darkblock ecosystem:

![Blockchain Streaming Approach]({filename}/images/Darkblock/00_Solution_Blockchain.png)

In the Web 3.0, the blockchain (and related DAPPS) provides identity, payment, infrastructure and digital rights management services.

Darkblock writes the following on their [website](https://darkblock.medium.com/darkblock-bridge-to-the-decentralized-digital-frontier-e1ec1eeb5a60):

> Darkblock is a control panel for decentralized content. Contrary to DRM, creators choose how each NFT is distributed, shown, sold, rented, hidden, destroyed, or unlocked. Users can determine sliced ownership, royalty structures, and inherent properties, all while making sure their creations won’t be copied, distributed, or used outside of their intended purpose.
>
> Darkblock will be the decentralized ground layer protocol enabling autonomy in the NFT space.
>
> We call this protocol layer PeRM: Personal Rights Management. We feel that everyone should have control of their own creations and content without the possibility of interference as a matter of principle.

# Create A Darkblock
You must be a creator of an NFT to create a Darkblock.  

You do not, however, need to own the NFT to create a Darkblock.  

## NFT I Created (But Do Not Own)
To demonstrate, I will log into my **Hello World** [Rarible account](https://rarible.com/ultramagnus).

![Um Login]({filename}/images/Darkblock/01_Um_Login.png)

I named this account [Ultra Magnus](https://tfwiki.net/wiki/Ultra_Magnus_(G1)) and [created two NFT]({filename}/create-nft-with-rarible-part-1.md), Isometric Pixel Art renditions of (1) the [Charles and Ray Eames Chair](https://rarible.com/token/0xd07dc4262bcdbf85190c01c996b4c06a461d2430:254537) and (2) a [1990s Media Console](https://rarible.com/token/0x60f80121c31a0d46b5279700f9df786054aa5ee5:351373).  

Find these two NFT under the [created tab](https://rarible.com/ultramagnus?tab=created).

![Um Created]({filename}/images/Darkblock/02_Um_Created.png)

The [Owners](https://rarible.com/token/0xd07dc4262bcdbf85190c01c996b4c06a461d2430:254537?tab=owners) tab shows that **Ultra Magnus** no longer owns the Eames NFT.  [John Sobanski](https://rarible.com/sobanski) (me) and [Mark Discordia](https://rarible.com/markdiscordia?tab=owned) own copies of the NFT.

![All Gone]({filename}/images/Darkblock/03_All_Gone.png)

Ultra Magnus no longer owns the [Partu Media NFT](https://rarible.com/token/0x60f80121c31a0d46b5279700f9df786054aa5ee5:351373?tab=details), since I transferred it to my official John Sobanski account.

![All Gone2]({filename}/images/Darkblock/04_All_Gone2.png)

## The Darkblock App
Navigate to [app.darkblock.io](https://app.darkblock.io).

![App Darkblock]({filename}/images/Darkblock/05_App_Darkblock.png)

Click **Connect Wallet** to connect with MetaMask.

If you do not know how to use MetaMask, I wrote a blog post on [how to create and configure a MetaMask wallet to use Decentralized Applications (dApps)]({filename}/create-nft-with-rarible-part-1.md).

![Connect Wallet]({filename}/images/Darkblock/06_Connect_Wallet.png)

Click **Connect**.

![Click Connect]({filename}/images/Darkblock/07_Click_Connect.png)

The Darkblock App provides tabs to list the NFT you own and the [NFT you created]({filename}/create-nft-with-rarible-part-2.md).

In the last section, we saw that **Ultra Magnus** does not own any NFT.

Darkblock tells us that **Ultra Magnus** does not own any NFT.

![Nuthin In]({filename}/images/Darkblock/08_Nuthin_In.png)

The Darkblock App, however, shows that Ultra Magnus **Created** two NFT, via the **Created By Me** tab.

![My Nfts]({filename}/images/Darkblock/09_My_Nfts.png)

The App notes that Address [0x8f799eeb12521639b20405494082f3d88aec5f8e](https://etherscan.io/address/0x8f799eeb12521639b20405494082f3d88aec5f8e), AKA Mark Discordia owns the [Eames NFT](https://rarible.com/token/0xd07dc4262bcdbf85190c01c996b4c06a461d2430:254537?tab=owners) (and not **Ultra Magnus**).

![Eames Chair]({filename}/images/Darkblock/10_Eames_Chair.png)

Since I (Ultra Magnus) created the NFT, I can create a Darkblock.

![Create Darkblock]({filename}/images/Darkblock/11_Create_Darkblock.png)

I upload content in the form of a High-Res picture into the Darkblock App, and then click **Create Darkblock**.

![Create Darkblock2]({filename}/images/Darkblock/12_Create_Darkblock2.png)

I then sign the request.

![Sign Darkblock]({filename}/images/Darkblock/13_Sign_Darkblock.png)

Darkblock indicates successful creation.  Now, the owners of the NFT ([John Sobanski](https://etherscan.io/address/sobanski.eth) and [Mark Discordia](https://etherscan.io/address/0x8f799eeb12521639b20405494082f3d88aec5f8e)) both have unlockable content to the [Eames NFT](https://rarible.com/token/0xd07dc4262bcdbf85190c01c996b4c06a461d2430:254537?tab=owners).

![Darkblock Created]({filename}/images/Darkblock/14_Darkblock_Created.png)

John and Mark received the [Eames NFT](https://rarible.com/token/0xd07dc4262bcdbf85190c01c996b4c06a461d2430:254537?tab=owners) in [March](https://etherscan.io/tx/0x781b8067bed403570dce3db5a4ac5b122f38da947c7cd764412630a6d02febca).  Now, over 1/2 a year later they received a special **drop** in  the form of unlockable content.

![Darkblock Protected]({filename}/images/Darkblock/15_Darkblock_Protected.png)

If I click back to the Ultra Magnus **created by Me** tab, I now see that the two NFT include **Darkblock** goodies.

![Ultra Darkblocks]({filename}/images/Darkblock/16_Ultra_Darkblocks.png)

I now log out of my [Ultra Magnus](https://rarible.com/ultramagnus) account and into my verified [John Sobanski](https://rarible.com/sobanski) account.

I then click the **My NFT's** tab.

![Sobanski Nft]({filename}/images/Darkblock/17_Sobanski_Nft.png)

In addition to my [NFTP By Charmin NFT](https://rarible.com/token/0x60f80121c31a0d46b5279700f9df786054aa5ee5:489778) and [Taco Bell NFT](https://rarible.com/token/0xd07dc4262bcdbf85190c01c996b4c06a461d2430:236715?tab=owners), I own the Ultra Magnus [Eames](https://rarible.com/token/0xd07dc4262bcdbf85190c01c996b4c06a461d2430:254537?tab=owners) and [Console](https://rarible.com/token/0x60f80121c31a0d46b5279700f9df786054aa5ee5:351373?tab=details) NFT.

Darkblock indicates that I now have digital goodies to unlock.

# View A Darkblock
Darkblock provides an App to view the new, locked digital content.

Today (October 30th, 2021) Darkblock provides an Application for the [Amazon Firestick](https://www.amazon.com/Darkblock-NFT-Display/dp/B09B4FLQZ6/) (They also provide applications for other [Google Media Devices](https://play.google.com/store/apps/details?id=io.darkblock.darkblock&hl=en&gl=US)).

> NOTE:  The following pictures capture the app running on a Vintage TV from 2005.  I apologize for the crappy quality of the pictures.  [Send me some Eth](https://etherscan.io/address/sobanski.eth) so I can upgrade to a [Bang & Olufsen](https://www.bang-olufsen.com/en/de/televisions).

![Darkblock App]({filename}/images/Darkblock/18_Darkblock_App.png)

The Fire Stick App provides a secret code and instructs me to go to [app.darkblock.io/tv](https://app.darkblock.io/tv).

![Tv Code]({filename}/images/Darkblock/19_Tv_Code.png)

On my laptop I enter the code.

![Enter Code]({filename}/images/Darkblock/20_Enter_Code.png)

I sign the login request.

![Sign Request]({filename}/images/Darkblock/21_Sign_Request.png)

This signing request demonstrates how Darkblock uses the blockchain for Identity and Access Management (IAM) of the digital content.

![Goto Tv]({filename}/images/Darkblock/22_Goto_Tv.png)

My (broken) TV (I have some dead pixels in the upper left) shows the NFT I own in this particular account.

![Nft List]({filename}/images/Darkblock/23_Nft_List.png)

This account owns an [Isometric Pixel Art NFT of an Orange Francis Francis X1 Espresso Machine](https://rarible.com/token/0xd07dc4262bcdbf85190c01c996b4c06a461d2430:542004), with unlockable **Darkblock** content.

I click **Decrypt**.

![Click Decrypt]({filename}/images/Darkblock/24_Click_Decrypt.png)

The App decrypts the secret content.

![Decrypt Screen]({filename}/images/Darkblock/25_Decrypt_Screen.png)

The App displays my secret content (a Grey Espresso Machine) along with some display controls and a QR code that links to the public version of the NFT.

In this way, a museum (for example) can tune the display of secret content during an exhibition.

![Secret Art]({filename}/images/Darkblock/26_Secret_Art.png)

Here I change the matte background to corkboard.

![With Borders]({filename}/images/Darkblock/27_With_Borders.png)

# Conclusion
Darkblock provides artists with an NFT control panel for access rights and Creator Rights Management.  Artists can use NFT for media distribution and permissions management, which opens the door for exciting possibilities.

# A Note To Recent (Oct 2021) Rarible Creators
I attempted to [create a brand new NFT](https://rarible.com/token/0xf6793da657495ffeff9ee6350824910abc21356c:69644222009519936378771681436291690114697426885580689206684726473945885179905?tab=details) for this blog post.

I selected **single collectible**.

![Upload Png]({filename}/images/Darkblock/28_Upload_Png.png)

I **disabled** free minting.

![Toggle Free]({filename}/images/Darkblock/29_Toggle_Free.png)

I clicked **Create item** to mint the NFT then and there.

![Click Create]({filename}/images/Darkblock/30_Click_Create.png)

I paid $170.00 to **mint** the item then and there (vs. lazy minting).

![Sign Contract]({filename}/images/Darkblock/31_Sign_Contract.png)

Rarible depicts a successful mint.

![Mint NFT]({filename}/images/Darkblock/32_Mint_NFT.png)

You too can view my [isometric pixel art masterpiece](https://rarible.com/token/0xf6793da657495ffeff9ee6350824910abc21356c:69644222009519936378771681436291690114697426885580689206684726473945885179905?tab=details).

![Nft Minted]({filename}/images/Darkblock/33_Nft_Minted.png)

The Darkblock App, however, does not detect that I, John Sobanski created the NFT.

Darkblock believes [0x3482549fca7511267c9ef7089507c0f16ea1dcc1](https://etherscan.io/address/0x3482549fca7511267c9ef7089507c0f16ea1dcc1) AKA [GayAuburnSeahorseOfAwe](https://opensea.io/GayAuburnSeahorseOfAwe?tab=created) minted the NFT.

![Darkblock Error]({filename}/images/Darkblock/34_Darkblock_Error.png)

OpenSea also believes that [GayAuburnSeahorseOfAwe](https://opensea.io/GayAuburnSeahorseOfAwe?tab=created) created the item, not John Sobanski.

![Auburn Seahorse]({filename}/images/Darkblock/35_Auborn_Seahorse.png)

I reached out to Rarible, and they responded immediately (excellent tech support thank you!)

> Due to the newly created contract for lazy-minting, which is also being used for normal NFTs, the new "profile" on OpenSea hasn't been setup yet.
>
> This should be fixed within the week. If it hasn't by then, please get back to me and I will make sure to escalate this to our management again!

In other words, if you want to use Darkblock today (Oct 2021), either use an old NFT, use OpenSea to mint, or wait until Rarible completes the upgrade of the post-lazy minting indexing on OpenSea.
