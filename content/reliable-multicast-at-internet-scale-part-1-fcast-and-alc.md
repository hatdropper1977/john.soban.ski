Title: Reliable Multicast at Internet Scale (Part 1):  FCAST and ALC 
Date: 2016-10-15 01:58 
Author: john-sobanski
Category: IETF
Tags: ALC, FCAST, Reliable Multicast, IETF
Slug: reliable-multicast-at-internet-scale-part-1-fcast-and-alc 
Status: published

Reliable multicast?!? How on earth can you guarantee transport using a unidirectional, asynchronous delivery method? Could you scale your solution to support ten million downstream users, each with a different capacity, varying from dial up to 100GbE metro Ethernet? Surprisingly, you can!

In this series of blog posts I discuss a few interesting technologies that provide massively salable reliable multicast. In summary, you can guarantee reliable multicast using a "data carousel," and can handle the non-uniform capacity issues with the idea of layered coding. Users receive the layers that their capacity supports, the more layers they subscribe to, the higher quality video stream they receive. Read the next few blog posts to dive into the fascinating details.

**Background**

Warner Brothers pictures begins filming the John Carmack biopic (starring Anthony Michael Hall as John Carmack and Dwayne “The Rock” Johnson as John Romero) next month. The film depicts Carmack’s life, from shareware coder to superstar “Doom” engine developer to the founder of Armadillo aerospace. To feed the geek buzz surrounding the picture, Warner Brothers will debut the film on the Internet, providing a one time, free Multicast on December 10th, 2018… the 25th anniversary of the initial release date of “Doom”.

Warner Brothers predicts millions of subscribers to this one time Multicast, and (should) contract Freshlex, LLC to develop the enabling architecture. In other words, Warner Brothers wants to transmit a single video feed to millions of Internet receivers, each with arbitrary network capacity. Warner Brothers needs a reliable, massively scalable solution.

These blog posts demonstrates the use of IETF standard protocols to provide a reliable, massively scalable solution with session management and multiple rate congestion control that stresses network fairness. Our solution looks at FCAST/ Asynchronous Layered Coding (ALC), designed by the IETF Reliable Multicast Transport (RMT) Working Group (WG) to provide just that.

This blog post describes FCAST and ALC, which enable reliable multicast. The next blog post describes the building blocks of ALC: LCT, WEBRC and FEC.

**Reliable Multicast Building Block: FCAST**

**Description**

FCAST provides object delivery over asynchronous layered coding (ALC). FCAST uses a lightweight implementation of the user datagram protocl (UDP)/ Internet protocol (IP) protocol stack to provide a highly scalable, reliable object delivery service that limits operational processing and storage requirements. Engineers should not consider FCAST as highly versatile, but for appropriate uses cases (such as the streaming video use case this paper discusses), FCAST is massively scalable and robust. [[RFC6968](https://tools.ietf.org/html/rfc6968) 3]

**Features**

FCAST uses purely unidirectional transport channels for massive scalability. An engineer could hack FCAST to collect reception metrics but this limits scalability. FCAST favors simplicity, sending metadata and object content together in a compound object. The in-band approach, however does not allow a receiver (RX) to decide in advance if an object is of interest until the RX joins the session and processes the metadata portion of the compound object ([RFC6968](https://tools.ietf.org/html/rfc6968) 9). An out-of-band metadata approach would obviate this setback, but remember, the driving requirement of the effort is massive scalability ([RFC6968](https://tools.ietf.org/html/rfc6968) 4). The Reliable Multicast Transport Working Group (RMT WG) designs FCAST to be compatible with ALC and the ALC building blocks: FEC, WEBRC and LCT ([RFC5775](https://tools.ietf.org/html/rfc5775) 1).

**Architecture Definition**

FCAST provides a content delivery service and transmits objects to a (very large) group of receivers in a reliable way. An engineer could use FCAST over negative acknowledgement (NACK) Oriented Reliable Multicast (NORM) but since the RMT WG designed NORM to use NACK, NORM does not fit the spirit of the Architecture. The Architecture, therefore integrates FCAST to use ALC. Nothing about FCAST limits the maximum number of receivers. Using ALC provides the FEC building block and thus a measure of reliability. In addition, FCAST uses the concept of data carousels (described below) and the longer a carousel runs, the more reliable the content delivery service becomes. [[RFC6968](https://tools.ietf.org/html/rfc6968) 6]

Components: The bullets below describe the FCAST components [[RFC6968](https://tools.ietf.org/html/rfc6968) 5]:

  -   Compound Object: Header (Includes metadata) + Object
  -   Carousel: Compound object transmission system
  -   Carousel Instance
    -   Transmission system containing a collection of compound objects
    -   Fixed set of registered compound objects that are sent by the carousel during a certain number of cycles
    -   Note: whenever objects need to be added or removed, a new carousel object is defined
  -   Carousel Instance Object (CIO): List of objects in the carousel instance
    -   Note: The CIO is itself an object
    -   Note: The CIO does not describe the objects themselves (e.g. no metadata)
  -   Carousel Cycle: A period of time when all the objects are sent once
    -   Transmission round within which all the registered objects in a Carousel Instance are transmitted a certain amount of times
    -   By default, objects are sent once per cycle
  -   Transmission Object Identifier (TOI)
    -   The ID number associated to an object at the lower LCT (Transport) layer
  -   FEC Object Transmission Information (FEC TOI)
    -   Information required for coding

**Operations**

On the sender side of FCAST, a user first selects a set of objects to deliver to the receivers and submits the objects and the object metadata to the FCAST application. For each object, FCAST creates the compound object (header, metadata and the original object) and registers the compound object in the carousel instance. The user informs FCAST when he completes submission of all the objects in the set. If the user knows that no other object will be submitted then it informs FCAST accordingly. The user then specifies the desired number of cycles. For the most part the user can correlate the number of cycles with reliability. FCAST, nonetheless, now knows the full list of compound objects that are part of the carousel instance and creates a CIO (if desired) with a complete flag (if appropriate). The FCAST application then defines a TX schedule of these compound objects, including the CIO. The schedule defines which order the packets of the various compound objects are sent. FCAST now starts the carousel transmission for the number of cycles specified and continues until (1) FCAST completes the desired number of TX cycles (2) the user wants to kill FCAST or (3) the user wants to add or remove objects, in which case FCAST must create a new CI. [[RFC6968](https://tools.ietf.org/html/rfc6968) 12]

On the receiver side of FCAST, the RX joins the session and collects encoded symbols. Once the RX receives the header the RX processes the metadata and chooses to continue or not. Once the RX receives the entire object the RX process the headers retrieves the metadata, decodes the metadata and processes the object. When the RX receives a CIO (a compound object with the “I" bit set) the receiver decodes the CIO and retrieves the list of compound objects that are part of the current carousel instance (and can also determine which compound objects have been removed). If the RX receives a CIO with the complete flag set, and the RX has successfully received all the objects of the current carousel instance, the RX can safely exit the current FCAST session. [[RFC6968](https://tools.ietf.org/html/rfc6968) 13]

**Reliable Multicast Building Block: ALC**

**Description**

Asynchronous Layered Coding (ALC) provides massively scalable, asynchronous, multirate, reliable, network friendly content delivery transport to an unlimited number of concurrent receivers from a single sender. Three building blocks comprise ALC: (1) IETF RFC5651 Layered Coding Transport (LCT) for Transport Layer control, (B) IETF RFC3738 Wave and Equation Based Rate Control (WEBRC) for multi-rate congestion control and (3) IETF RFC3454 IP multicast forward error correction (FEC) for reliability [[RFC5775](https://tools.ietf.org/html/rfc5775) 1]. The Reliable Multicast Transport (RMT) working group (WG) designs ALC for IP multicast, although an engineer can use it for unicast. ALC has no dependencies on IP version.

The diagram below shows the FCAST/ALC architecture and packet format.

![ALC Packet]({filename}/images/Reliable_Multicast_at_Internet_Scale_Part_1_FCAST_and_ALC/rm_1_1_fcast_alc_packet-1024x676.png) 

**Features**

ALC has advantageous features. The RMT WG designates scalability as the primary design goal of ALC. IP multicast by design is massively scalable, however, IP multicast only provides a best effort (BE) service devoid of session management, congestion control or reliability. ALC augments IP multicast with session management, congestion control and reliability without sacrificing massive scalability. As a result, the number of concurrent receivers for an object is theoretically infinite, and in practice potentially in the millions. [[RFC5775](https://tools.ietf.org/html/rfc5775) 4]

ALC provides reliable asynchronous transport for a wide range of objects. The aggregate size of delivered objects can vary from hundreds of kilobytes (KB) to terabytes (TB). Each receiver (RX) initiates reception asynchronously and the reception rate for each RX is the maximum fair bandwidth available between the receiver and sender. In other words, each RX believes it has a dedicated session from TX to RX, with rate adjustments that match the available bandwidth at any given time. The building blocks of ALC allow it to perform congestion control, reliable transport and session layer control without the need for any feedback packets. The lack of any channel from receiver to sender enables ALC to be massively scalable. [[RFC5775](https://tools.ietf.org/html/rfc5775) 5]

**Architecture**

ALC transports one or more objects to multiple receivers using a single sender and a single session. An application (such as FCAST) provides data objects to ALC. ALC generates packets from these objects, formats them and then hands them off to the lower layer building blocks. The FEC building block encodes them for reliability. The LCT building block provides in-band session management and places the objects onto multiple transmission channels. The WEBRC building block places the data onto the channels at rates optimized for multiple-rate, feedback free congestion control. The RX joins appropriate channels associated with the session, joins or leaves channels for congestion control and uses the ALC, LCT and FEC information to reliably reconstruct the packets into objects. Thanks to the FEC building block, the RX simply waits for enough packets to arrive to reliably reconstruct the object. The ALC architecture does not provide any ability for a RX to request a re-transmission. Thanks to the focus on massive scalability the rate of transmission out of the TX is independent of the number and individual reception experience of the RX. [[RFC5775](https://tools.ietf.org/html/rfc5775) 7]

**ALC Session**

The concept of an ALC session matches that of LCT. A session contains multiple channels from a single sender used for some period of time to carry packets pertaining to the TX of objects interesting to receivers ([RFCS5651](https://tools.ietf.org/html/rfc5651) 4-5). ALC performs congestion control over the aggregate of the packets sent to channels belonging to a session ([RFC5775](https://tools.ietf.org/html/rfc5775) 7).

**ALC Session Description**

An ALC session requires a session description. Any receiver that wants to join an ALC session must first obtain the session description. A discussion of how to get this session description to the receivers follows in the “integration choices” section of this paper. The session description contains the following information ([RFC5775](https://tools.ietf.org/html/rfc5775) 12):

  -   Sender IP Address
  -   Number of channels in the session
  -   Multicast address and port \# for each channel in the session
  -   Data Rates used for each channel
  -   Length of each packet payload
  -   Transport Session Identifier (TSID) for the session
  -   An indication if the session carries packets for more than one object
  -   Whether the session describes required FEC information ([RFC5052](https://tools.ietf.org/html/rfc5052)) out of band or in-band (using header extensions)
  -   Whether the session uses Header Extensions, and if so the format
  -   Whether the session uses packet authentication, and if so the scheme
  -   The MRCC building block used (The ALC RFC recommends WEBRC, so we use that in this paper)
  -   Mappings between settings and Codepoint Value (for example, if different objects use different FEC or authentication schemes, the Codepoint values distinguish them)
  -   Object metadata such as when the objects will be available and for how long

**Operations**

The integration of three building blocks defines ALC, so first and foremost, the sender follows all operations associated with the LCT, FEC and WEBRC building blocks. ALC nonetheless, first makes available the required session description and FEC Object transmission information. As mentioned earlier, the session description contains the sequence of channels associated with the sender. ALC fills in the congestion control indication (CCI) field with information provided by the WEBRC building block. ALC then sends packets at appropriate rates to the channels as dictated by the WEBRC building block. ALC stamps every packet with the Transport Session ID (TSI), in case the receivers join sessions from other senders. If this particular session contains more than one object, then ALC stamps each packet with the appropriate transport object ID (TOI). ALC stamps the packet payload ID based on information from the FEC building block. As discussed in the “Security Validation” section of this paper, the IETF recommends packet authentication as a precaution. If an ALC instance does use packet authentication, it uses a header extension to carry the authentication information. [[RFC5775](https://tools.ietf.org/html/rfc5775) 16]

The ALC RX also conforms to all operations required by LCT, FEC and WEBRC. The RX first obtains a session description and joins the session. The RX then obtains the in-band FEC Object Transmission Information for each object the RX wants. Upon receiving a packet the RX parses the packet header, and verifies that it is a valid header (discards packet if invalid). The RX verifies that the (Sender IP Address, TSI) tuple matches one of the pairs received in Session Description for the session the RX is currently joined to (if not, discard). The RX then proceeds with packet authentication and discards the packet if invalid. After valid packet authentication, the RX processes and acts on the CCI field in accordance with the WEBRC building block. If ALC carries more than one object in session, the RX verifies the TOI (and discards if not valid). The RX finally processes the remainder of the packet, interpreting other header fields and uses the FEC Payload ID and the encoding symbols in the payload to reconstruct the object. [[RFC5775](https://tools.ietf.org/html/rfc5775) 17]

**Conclusion**

This blog post describes FCAST and ALC, which enable reliable multicast. The next blog post describes the building blocks of ALC: LCT, WEBRC and FEC.

**Bibliography**

[[RFC5651](https://tools.ietf.org/html/rfc5651)] Luby, M., Watson, M. and L. Vicisano, “Layered Coding Transport (LCT) Building Block”, RFC 5651, October 2009.

[[RFC5775](https://tools.ietf.org/html/rfc5775)] Luby, P., Watson, P. and L. Vicisano, “Asynchronous Layered Coding (ALC) Protocol Instantiation”, RFC 5775, April 2010.

[[RFC6968](https://tools.ietf.org/html/rfc6968)] Roca, V. and B. Adamson, “FCAST: Scalable Object Delivery for the ALC and NORM Protocols”, RFC 6968, July 2013. 
