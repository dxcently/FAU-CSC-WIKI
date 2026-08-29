+++
title = "Networking"
weight = 3
description = "IP addressing, protocols, and the tools used to inspect network traffic."
icon = "fa-solid fa-network-wired"
+++

You cannot hack or defend something you do not understand. Networking is load-bearing knowledge.

This section covers IP, protocols, and the tools used to inspect traffic.

---

## The Four Things You Actually Need

Networking drags a huge amount of trivia behind it. Ignore most of that for
now. Four ideas carry almost all of the weight — get these, and the
deep-dive pages below stop looking like a wall of acronyms.

### IP Addresses & Ports

An **IP address** is a number that identifies one device on a network — the
street address. A **port** is a number from 0 to 65535 that picks which
program on that device gets the data — the apartment number. The IP gets a
packet to the right building. The port gets it to the right door.

You will see addresses like `192.168.1.10` constantly — four numbers, each
0–255, separated by dots. A few ports are worth memorizing on sight: 22 is
SSH (remote login), 80 is HTTP (web, plain text), 443 is HTTPS (web, encrypted). Full breakdown,
including subnets and the private ranges you see on every VM and CTF box:
[IP, Ports & Subnets](fundamentals/).

### TCP / UDP Handshakes

Data does not just appear at its destination. Something has to package it
and agree on how it is sent — that is **TCP** and **UDP**, the two ways.

TCP is a phone call: both sides perform a **handshake** first — three
packets, `SYN` → `SYN-ACK` → `ACK` — to confirm they are ready, and every
packet after that is guaranteed to arrive, in order. UDP is a postcard: you
send it and do not wait for confirmation. No handshake, no guarantee, just
speed — that is why video calls and DNS use it.

This matters daily because a **port scan** — the first thing you run
against any box — works by sending TCP `SYN` packets and watching who
answers `SYN-ACK`. That is the whole trick behind `nmap`. Full comparison
and what the handshake looks like on the wire: [Protocols](protocols/).

### DNS Resolution

You type `google.com`. Your computer needs an IP address to actually send
anything — names are for humans, addresses are for machines. **DNS**
(Domain Name System) is the lookup that turns one into the other, and it
runs almost every time you load anything.

Your machine asks a **resolver** (usually your router or ISP), the resolver
asks the internet's directory of name servers, and an address comes back in
milliseconds. You never see this happen — until it breaks. "The site is
down" is, half the time, "DNS is down." `dig` and `nslookup` run this
lookup by hand so you can watch each step. Full walkthrough:
[Protocols](protocols/).

### Read Live Traffic

Everything above is invisible unless you go looking. **Packet capture**
tools watch the actual bytes moving across a network interface in real
time — handshakes, DNS queries, anything not encrypted.

`tcpdump` does this from the terminal. Wireshark does the same thing with a
window and color-coded packets — an easier way to see what a handshake
actually looks like the first few times. On your lab VM, start a capture,
load a web page, and watch the packets appear.

Tool details and example commands: [Networking Tools](tools/).
