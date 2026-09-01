+++
title = "Start Here"
# linkTitle is what LINKS to this page call it — the home card, the sidebar,
# the breadcrumb. The page's own heading stays "Start Here".
linkTitle = "New?"
weight = 10
description = "Start here! What the club is, what it offers, and the roadmap from knowing nothing to competing."
icon = "fa-solid fa-door-open"
+++

---

Welcome to the FAU Cyber Security Club Wiki! This is where you find quick
information about the club, current events, and the guides that get you from "I
don't know anything" to actually doing the work.

We strongly encourage an open environment of learning, so _NEVER_ be afraid to
ask questions. It is ok if you don't know something — remember that we are all
learning. And the best way to learn is to fail!

![The GIF didn't load lol](https://github.com/dxcently/fau-cyber-security-club-wiki/blob/main/assets/error_220.gif?raw=true)

_It is hard to write a simple definition of something as varied as hacking, but
I think what these activities have in common is playfulness, cleverness, and
exploration. Thus, hacking means exploring the limits of what is possible, in a
spirit of playful cleverness. Activities that display playful cleverness have
"hack value."_

_-- Richard Stallman_

---

## What the Club Does and Provides

- Weekly demos and lessons on things related to cyber security and hacking.
- Hackathons and competitions. We are often joining in competition and it is
  _HIGHLY_ recommended to attend even if you aren't participating because they
  will be the best way to learn.
- Real hands-on experience with hacking.
- Networking opportunities with real cyber security professionals.
- It'll look good on the resume.

---

The rest of this page is the **roadmap** — an honest map of the road from
knowing nothing to competing. It is the thing to read once, properly, before
you go picking sections at random.

---

You are probably here because you want to get into cybersecurity but you are not
quite sure where to start, or you came to a meeting, heard words like "lateral
movement" and "privilege escalation," and thought — okay, I need to catch up.

That is completely fine. Everyone starts at zero. The goal of this page is to
give you an honest map of the road ahead so you are not wandering in the dark.

This is not a fast track. It is a real track. The good news is that if you put
in the time consistently, you will surprise yourself with how quickly things
start clicking.

The road has two parts. First a **shared core** — the fundamentals every
security person needs, no matter what they end up doing. Then a **fork**: blue
team or red team. You defend systems, or you break them. The club competes in
both, and the fork is where you pick your first color. Not your only color —
your first.

---

## The Map

{{< mermaid >}}
flowchart TD
    A([Start Here]) --> VM

    subgraph VM["1 · Virtual Machine"]
      direction LR
      vm1[Pick a hypervisor] --> vm2[Install a Linux guest] --> vm3[Snapshot, break, restore]
    end
    VM --> LX

    subgraph LX["2 · Linux"]
      direction LR
      lx1[Filesystem & paths] --> lx2[Users & permissions] --> lx3[Processes & services] --> lx4[Package managers]
    end
    LX --> NET

    subgraph NET["3 · Networking"]
      direction LR
      n1[IP addresses & ports] --> n2[TCP / UDP handshakes] --> n3[DNS resolution] --> n4[Read live traffic]
    end
    NET --> CLI

    subgraph CLI["4 · CLI & Scripting"]
      direction LR
      c1[Shell fluency & pipes] --> c2[Bash: automate one chore] --> c3[Python: glue tool output]
    end
    CLI --> WEB

    subgraph WEB["5 · Web & System"]
      direction LR
      w1[HTTP request / response] --> w2[Cookies, sessions, auth] --> w3[Privileges & what runs as root]
    end
    WEB --> WIN

    subgraph WIN["6 · Windows & Active Directory"]
      direction LR
      d1[PowerShell & the object pipeline] --> d2[Domains, DCs & Kerberos] --> d3[Group Policy & hardening]
    end
    WIN -.-> CR

    %% Crypto hangs off the spine on DOTTED edges, not solid ones: it is not a
    %% stage you finish before the fork, it is a thing both branches keep
    %% using. The incoming edge from WIN is what matters for layout — without
    %% one, mermaid treats CR as a second root and parks it in its own column
    %% down the whole left edge of the chart.
    CR[["Cryptography — used by both sides"]]
    CR -.-> G{Pick a Color}

    G --> BLUE
    subgraph BLUE["🔵 Defense"]
      direction TB
      b1[Harden: users, services, firewall, updates] --> b2[Baseline: know what normal looks like]
      b2 --> b3[Monitor: logs, processes, connections]
      b3 --> b4[Respond: detect → contain → recover]
    end
    BLUE --> H3([CCDC / CyberPatriot])

    G --> RED
    subgraph RED["🔴 Offense"]
      direction TB
      r1[Enumerate: map the attack surface] --> r2[Exploit: own one bug class deeply]
      r2 --> r3[Escalate & pivot: foothold to root]
      r3 --> r4[Write it up: solved ≠ understood]
    end
    RED --> R3([CTF Competitions])

    H3 --> Z([Compete & Contribute])
    R3 --> Z

    classDef core stroke:#00BB00,stroke-width:2px
    classDef blue stroke:#1E90FF,stroke-width:2px
    classDef red stroke:#CC0000,stroke-width:2px
    classDef sub fill:transparent
    class A,G,Z,CR,d1,d2,d3,WIN,vm1,vm2,vm3,lx1,lx2,lx3,lx4,n1,n2,n3,n4,c1,c2,c3,w1,w2,w3 core
    class VM,LX,NET,CLI,WEB core
    class b1,b2,b3,b4,H3,BLUE blue
    class r1,r2,r3,r4,R3,RED red
    class VM,LX,NET,CLI,WEB,BLUE,RED sub
{{< /mermaid >}}

Each box is a primitive — one concrete thing you can sit down and learn in a
week or two. A stage is done when its boxes stop feeling like magic words. Do
not aim for mastery before moving on; aim for "I have done this once with my
own hands."

None of this is linear and there is never one right path. If you already have a
path, follow yours. If you do not, this is the one we recommend.

---

## The Shared Core

Everyone walks this part. Blue teamers who skip networking cannot read their
own logs. Red teamers who skip Linux cannot use their own tools. There is no
version of this field where the fundamentals are optional.

### Set Up a Virtual Machine

Before you touch anything, you need a safe sandbox. A VM lets you run a
separate operating system inside your computer — break it, reset it, no harm
done. This is your first real task and it is intentionally on you to sort out.
Start in [Virtual Machines](/learn/virtual-machines/).

### Get Comfortable with Linux

Most security tooling lives on Linux. You do not need to be a wizard, but you
need to not be lost. Filesystem, permissions, processes — that is the floor.
Sit down, open a terminal, and figure it out. That discomfort is the point.
Start in [Linux](/learn/linux/).

### Learn Basic Networking

You cannot break or defend something you do not understand. IP addresses,
ports, TCP/IP, DNS. This stuff is dry but it is load-bearing knowledge — you
will use it forever, on either side of the fork.
Start in [Networking](/learn/networking/).

### Command Line & Scripting

Get comfortable running tools from the terminal. Learn enough Bash to automate
small tasks. A little Python is a genuine superpower in this field. Nobody is
going to write your scripts for you — that is the whole lesson.
Start in [CLI & Scripting](/learn/cli-scripting/).

### Web & System Fundamentals

How a web request works end to end. Users, groups, privileges on the system
side. This is where a huge share of real-world vulnerabilities live, and it is
the last stop before the fork.
Start in [Web & System Fundamentals](/learn/web-fundamentals/).

### Windows & Active Directory

The enterprise runs on Windows, and it authenticates through Active Directory.
CCDC and CyberPatriot are largely Windows defense, and most real intrusions
happen inside AD. Learn PowerShell, learn what a domain is, learn how policy
gets pushed to every machine.
Start in [Windows & Active Directory](/learn/windows/).

### Cryptography

Not a stage so much as a thing that shows up everywhere — in every CTF, in
every HTTPS connection, and in a large share of real vulnerabilities where
someone used it wrong. You do not need the math. You need to know what each
piece guarantees.
Start in [Cryptography](/learn/cryptography/).

---

## The Fork

Here is the honest version of the choice:

**Blue team is a job description. Red team is a sport that teaches you the
job.** Most security careers are defense. But offense is the fastest way to
understand what you are defending against — you cannot stop an attack you have
never seen work.

| | 🔵 Blue — Defense | 🔴 Red — Offense |
|---|---|---|
| The game | Keep systems alive while someone breaks in | Break in before someone stops you |
| Feels like | Running a server room during a fire drill | Solving puzzles that fight back |
| Club comps | [CCDC, CyberPatriot](/compete/) | [CTFs](/compete/ctf/) |
| Core skills | Hardening, monitoring, incident response | Exploitation, reversing, enumeration |
| Start with | [Network Defense](/learn/specializations/network-defense/) | [CTF Getting Started](/compete/ctf/getting-started/) |

Do not agonize over the pick. You will cross over — everyone does. Choose the
one that sounds more fun **this semester** and start walking.

### 🔵 The Blue Track

You inherit systems you did not build and keep them alive under attack.

1. **Hardening & sysadmin.** Learn to lock down a Linux box and a Windows box:
   users, services, firewalls, updates, backups. Most of defense is doing the
   boring parts properly before anyone attacks you.
2. **Monitoring & incident response.** Logs, processes, network connections —
   know what normal looks like so you can spot abnormal fast. Then practice
   the drill: detect, contain, eradicate, recover.
3. **Compete.** [CCDC](/compete/) hands your team a broken network and a live
   professional red team. [CyberPatriot](/compete/) is the same instinct in
   image-hardening form. Nothing teaches defense faster.

Start: [Network Defense](/learn/specializations/network-defense/), then
[Forensics](/learn/specializations/forensics/) when you want to know what the
attacker left behind.

### 🔴 The Red Track

You are handed something broken and your job is to break it further until a
flag falls out.

1. **Your first CTFs.** Jeopardy-style challenges, self-paced, low stakes.
   Try, fail, look it up, repeat — that loop is the whole game.
   [How to start](/compete/ctf/getting-started/).
2. **Go deep on one category.** [Web exploitation](/learn/specializations/web-exploitation/)
   has the gentlest ramp. [Binary exploitation](/learn/specializations/binary-exploitation/)
   is the deepest rabbit hole. [Forensics](/learn/specializations/forensics/) sits
   between the colors. Pick what pulls you.
3. **Compete.** Join the club's CTF teams. Do not worry about the score —
   watching a teammate solve something you could not is the fastest way up.

---

## Where the Tracks Meet

The best defenders think like attackers, and the best attackers understand the
systems they break well enough to run them. Give it a year and you will not
remember which color you started with. The club runs both tracks precisely
because each one makes the other make sense.

When you are competing, building, or writing things down for the next person —
that is [Compete](/compete/) and [Projects & Guides](/projects/). That is the
end of this map and the start of the actual fun.

---

Every stage above is a section in [Learn](/learn/). Go straight there when you
know what you are looking for.

{{< topic-cards for="/learn" >}}
