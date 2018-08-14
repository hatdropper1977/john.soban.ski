Title: Reliable Multicast at Internet Scale (Part 3):  The Architecture
Date: 2017-01-14 01:12
Author: john-sobanski
Category: IETF
Tags: ALC, LCT, WEBRC, IETF
Slug: reliable-multicast-at-internet-scale-part-3-the-architecture
Status: published

Freshlex LLC (should) architect the reliable multicast infrastructure for the putative John Carmack biopic, which will hit the Internet in December of 2018. The [first]({filename}/reliable-multicast-at-internet-scale-part-1-fcast-and-alc.md) blog post discusses two of the enabling technologies, FCAST and ALC. The [second]({filename}/reliable-multicast-at-internet-scale-part-2-lct-webrc-and-fec.md) blog post discusses the three technologies that enable ALC: LCT, WEBRC and the FEC building block. This blog post discusses an Architecture that integrates the five technologies.

**Integration Choices**

Massive scalability drives this integration effort. For the content delivery platform (CDP), we define scalability as the behavior of the CDP in relation to the number of receivers and network paths, their heterogeneity and the ability to accommodate dynamically variable sets of receivers. In general, three factors limit the scalability of a CDP. The three factors that limit the scalability of a CDP are (1) memory or processing requirements, (2) amount of feedback control and (3) redundant data traffic (RFC5651 5). The previous blog posts describe the standards used to create a massively scalable CDP. Standards, however, are not “turn-key” solutions. Engineers must make certain design choices when implementing standards. This blog post discusses the design choices made during this integration effort in order to conform to the spirit of massive scalability.

**FCAST Integration Choices**

Recall that FCAST uses data carousels to send objects to receivers. We have two design choices here, push mode or on demand mode ([RFC6968](https://tools.ietf.org/html/rfc6968) 3). Push mode associates a single carousel instance to a cycle ([RFC6968](https://tools.ietf.org/html/rfc6968) 8). On-demand mode makes compound objects available for a long period of time by using a very large number of transmission cycles. On-demand mode lends itself well to data transport, such as a software updates. A sender could have a carousel cycle for days. Clients then join the session at their leisure and leave once they receive the entire update. Push mode works better for (near) real time streaming video. The clients join at any time, but they will miss any video that occurs before their join. The integrator would need to design how to best implement this push mode. They could, for example, have one carousel instance per hour of video, with l2 minute chunks of data being an object. The carousel instance object lists the transport object ID of the five compound objects, and sets the complete flag, indicating the carousel object has a finite set of compound objects.

Integrators have many options in increasing the reliability of FCAST. For example, when using on-demand mode, an integrator can set the number of cycles to repeat for a period of time that exceeds the typical download time. In this case, you can correlate number of cycles with reliability ([RFC3453](https://tools.ietf.org/html/rfc3453) 2-3). An integrator can use a backchannel for session control, for example the carousel does not stop cycling until every receiver acknowledges full receipt. In this case, FCAST is fully reliable. Of course, the concept of a backchannel is unacceptable for massive scalability.

In our integration, since we’re using push mode we don’t have the luxury of repeating cycles for reliability. For that reason we use a robust FEC building block, which is a requirement of ALC anyway ([RFC5775](https://tools.ietf.org/html/rfc5775) 11).

**ALC Integration Choices**

The ALC standard omits application specific features to keep it massively scalable ([RFC5775](https://tools.ietf.org/html/rfc5775) 5-6). An integrator can tailor the applications (e.g. FCAST) that use ALC to add features and trade scalability if needed. The backchannel mentioned above in the discussion of FCAST design choices is one such example.

The first step of an ALC session entails the receiver acquiring the session description information ([RFC5775](https://tools.ietf.org/html/rfc5775) 17). The transmission of the session description information from ALC sender to the receivers is outside of the scope of the ALC standard. An integrator, regardless, has many options. The sender can describe the session description using SDP as described in RFC4566 or XML metadata in RFC3023 or HTTP/MIME headers defined in RFC2616. The sender, alternatively, can carry the session description in a Session Announcement Protocol (SAP) as per RFC2974.

We will simply have a well-known web page with session description information. When an RX wants to join a session, they go to that web page and download the session description ([RFC5651](https://tools.ietf.org/html/rfc5651) 24).

**FEC Integration Choices**

The main unresolved question for the FEC building block pertains to the use of in-band or out-of-band channels to communicate FEC meta-data to the RX ([RFC5775](https://tools.ietf.org/html/rfc5775) 11). Put another way, how does a receiver decode the following encoded message from a sender: “I’ve encoded this message using this scheme.” The previous statement is a paradox-- the receiver would not be able to decode the message unless they decoded the message to obtain the correct way to decode the message. We solve this problem by providing both the FCAST transmitter and FCAST receiver software to all parties. In order to receive the streaming video, a receiver must use our player. The sender and receiver software use one FEC scheme, LDPC Staircase and Triangle FEC, as described in RFC5170. We will throw the open source zealots a bone and point them to the RFC, if they wish to build their own receiver.

The next design choice deals with the application of FEC codes. For our data carousel we chose a large systemic code from RFC5170. A FEC Data carousel using large block FEC encoder considers all k source symbols of an object as one block and produces n encoding symbols. The carousel transmits the n encoding symbols in packets in the same order in each round. A receiver joins the transmission at any point, and as long as the receiver receives at least k encoding symbols during the transmission of the next n encoding symbols the receiver can completely recover the object ([RFC3453](https://www.ietf.org/rfc/rfc3453.txt) 3).

In the case of our push mode carousel, we partition our stream into objects. The FEC building block turns these objects into source symbols. The FEC building block then encodes these source symbols into encoding symbols and then the sets of the encoding symbols for each object are transmitted to each receiver.

Ideally, the FEC building block creates, encodes and transmits the source blocks in such a way that each received multicast packet is fully useful to reassemble the object independent of previous packet reception. Thus, if some packets are lost in transit between the TX & RX, the receiver uses any subsequent equal number of packets that arrive to reassemble the object (RFC3453 4). We prefer this to the alternatives, such as asking the transmitter for the missed packets (ARQ) or waiting on the carousel to re-send the desired packets (which won’t happen, since we’re in push mode and thus have one cycle per carousel). This property reduces the problems associated with push mode data carousels ([RFC3453](https://www.ietf.org/rfc/rfc3453.txt) 3).

**WEBRC Integration Choices**

The appropriate congestion control for content bulk data transfer differs from the appropriate congestion control for streaming video. For bulk data transfer, the intent is to use all available BW and then drastically back off when there is competing traffic. Streaming delivery applications prefer a lesser, constant rate to bursty peaks, with slight or no backoff.

From the RFC, engineers tuned WEBRC to work best in situations that have a low throughput variation over time, which makes it well suited to telephony or our streaming video where a smooth rate is important. The penalty for smoother throughput, however, is that WEBRC responds more slowly (compared with TCP) to changes in available BW. [[RFC3738](https://tools.ietf.org/html/rfc3738) 4]

Another reason that we use WEBRC for our streaming video application is that WEBRC was designed for applications that use fixed packet size and vary their packet reception rates in response to congestion. In general, WEBRC was designed to be reasonably fair when competing for BW with TCP flows, that is, it’s within a factor or two of the expected RX rate if TCP were used [[RFC3738](https://tools.ietf.org/html/rfc3738) 4].

By default, WEBRC avoids using techniques that are not massively scalable. For example, WEBRC does not provide any mechanisms for sending information from receivers to senders, although this does not rule out protocols that both use WEBRC and that send information from receivers to senders. For massive scalability, nonetheless, we have made the integration choice not to use any backchannels. [[RFC3738](https://tools.ietf.org/html/rfc3738) 1]

**LCT Integration Choices**

Part of the integration effort relies on how to get data objects to the LCT building block. Consider a push model, where we want to push a 50MB file via a carousel. We need to choose how to get those data into LCT. Suppose we break the file into 1KB packets. Then, if we send 50pkts/sec to one channel, it takes each RX 1,000 sec to get the file. A better implementation would be to split the file into multiple layers so that the aggregate rate is 1,000 packets/second.

With no loss, an RX now can complete the file download in 50 seconds by subscribing to all channels. Each channel, however, requires us to register a new multicast IP address with the multicast NW.

We could configure the sender to include Expected Residual Time (ERT) in the packet header extension (RFC5651 22). The ERT indicates the expected remaining time of packet transmission for either the single object carried in the session or for the object identified by the Transmission Object Identifier (TOI) if there are multiple objects carried in the session. While useful for "on- demand" mode, we don’t need to configure this for our push mode. The data we push is one time, “take it or leave it.” The ERT only applies when we send the same object out for multiple cycles. With the “one cycle per carousel” push mode, the ERT field does not provide any useful information ([RFC6968](https://tools.ietf.org/html/rfc6968) 8).

**Conclusion**

This blog post discusses an Architecture that integrates the five enabling reliable multicast technologies. The next and final blog post discusses integration challenges.

**Bibliography**

[[RFC3453](https://www.ietf.org/rfc/rfc3453.txt)] Luby, M., Vicisano, L., Gemmell, J., Rizzo, L., Handley, H. and J. Crowcroft, “The Use of Forward Error Correction (FEC) in Reliable Multicast”, RFC 3453 December 2002.

[[RFC3738](https://tools.ietf.org/html/rfc3738)] Luby, M. and V. Goyal, “Wave and Equation Based Rate Control (WEBRC) Building Block”, RFC 3738, April 2004.

[[RFC5651](https://tools.ietf.org/html/rfc5651)] Luby, M., Watson, M. and L. Vicisano, “Layered Coding Transport (LCT) Building Block”, RFC 5651, October 2009.

[[RFC5775](https://tools.ietf.org/html/rfc5775)] Luby, P., Watson, P. and L. Vicisano, “Asynchronous Layered Coding (ALC) Protocol Instantiation”, RFC 5775, April 2010.

[[RFC5170](https://tools.ietf.org/html/rfc5170)] Roca, V., Neumann, C., and D. Furodet, “Low Density Parity Check (LDPC) Staircase and Triangle Forward Error Correction (FEC) Schemes”, RFC 5170, June 2008.

[[RFC6968](https://tools.ietf.org/html/rfc6968)] Roca, V. and B. Adamson, “FCAST: Scalable Object Delivery for the ALC and NORM Protocols”, RFC 6968, July 2013.
