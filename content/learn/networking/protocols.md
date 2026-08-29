+++
title = "Protocols"
weight = 2
+++

Protocols are agreed-upon rules for how data is sent and received. You do not need to memorize RFCs — you need to understand what each one does and when it is relevant.

---

## TCP vs UDP

These are the two main transport-layer protocols.

| | TCP | UDP |
|---|---|---|
| Connection | Yes — three-way handshake | No — fire and forget |
| Reliability | Guaranteed delivery | No guarantee |
| Speed | Slower | Faster |
| Use cases | HTTP, SSH, FTP | DNS, VoIP, streaming |

The **TCP three-way handshake**: `SYN` → `SYN-ACK` → `ACK`. This is how a connection is established. A port scan works by sending SYN packets and seeing what responds.

---

## DNS

DNS (Domain Name System) translates human-readable names (`google.com`) into IP addresses.

**How it works:**
1. You type `google.com` in a browser.
2. Your OS asks a DNS resolver (usually your router or ISP).
3. The resolver queries root servers, then TLD servers, then authoritative servers.
4. You get back an IP address.

```bash
nslookup google.com       # basic DNS lookup
dig google.com            # detailed DNS query
dig google.com MX         # look up mail records
dig @8.8.8.8 google.com   # query a specific DNS server
```

DNS misconfigurations are frequent findings. Zone transfers (`AXFR`) on misconfigured servers can leak the entire DNS zone.

---

## HTTP / HTTPS

HTTP is the protocol your browser uses to talk to web servers. HTTPS is HTTP over TLS (encrypted).

Every HTTP transaction is a **request** and a **response**. Both have a method (or status code), headers, and optionally a body.

See the [HTTP page](/web-fundamentals/http) for full details.

---

## ICMP

ICMP is used for network diagnostics. `ping` uses it.

```bash
ping -c 4 192.168.1.1   # send 4 ICMP echo requests
```

Some firewalls block ICMP. A host not responding to ping does not mean it is offline.

---

## ARP

ARP (Address Resolution Protocol) maps IP addresses to MAC addresses on a local network.

```bash
arp -a          # view the ARP table
```

ARP spoofing is a classic local network attack — you convince other devices that your MAC is the router's MAC, intercepting traffic.

---

## DHCP

DHCP automatically assigns IP addresses to devices on a network. When you connect to Wi-Fi, your device gets an IP from the DHCP server (usually your router).

Rogue DHCP servers are a real attack. If you can respond to DHCP requests faster than the legitimate server, you control what IP and DNS server clients use.

---

> [!info] How the Club Uses This
> TODO: Add protocol-related CTF challenges or competition scenarios (DNS exploitation, ARP spoofing labs, etc.).

---

**References**

- [Cloudflare — How DNS works](https://www.cloudflare.com/learning/dns/what-is-dns/)
- [Wireshark protocol docs](https://wiki.wireshark.org/ProtocolReference)
- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/)
