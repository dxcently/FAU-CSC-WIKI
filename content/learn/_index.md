+++
title = "Beginner Roadmap"
weight = 2
+++

---

You are probably here because you want to get into cybersecurity but you are not
quite sure where to start, or you came to a meeting, heard words like "lateral
movement" and "privilege escalation," and thought — okay, I need to catch up.

That is completely fine. Everyone starts at zero. The goal of this page is to
give you an honest map of the road ahead so you are not wandering in the dark.

This is not a fast track. It is a real track. The good news is that if you put
in the time consistently, you will surprise yourself with how quickly things
start clicking.

Remember that none of this is linear. So there is **never one right path,** the
best way is one that you've figured out yourself. If you don't have a path to
follow, this is the one we reccommend.

---

## The Roadmap

{{< mermaid >}}
flowchart TD
    A([🖥️ Start Here]) --> B[Set Up a Virtual Machine]
    B --> C[Get Comfortable with Linux]
    C --> D[Learn Basic Networking]
    D --> E[Intro to the Command Line & Scripting]
    E --> F[Web & System Fundamentals]
    F --> G[Try Your First CTF]
    G --> H[Pick a Specialization]
    H --> I([Contributing to the Club])
{{< /mermaid >}}

---

## What Each Stage Actually Means

### Set Up a Virtual Machine

Before you touch anything, you need a safe sandbox to work in. A VM lets you run
a separate operating system inside your computer — break it, reset it, no harm
done. Figure out how to get one running. This is your first real task and it is
intentionally on you to sort out. If you cannot be bothered to set up a VM, the
rest of this is going to be a rough ride.

---

### Get Comfortable with Linux

Most security tooling lives on Linux. You do not need to be a wizard, but you
need to not be lost. Learn how to navigate the filesystem, manage files,
understand permissions, and know what a process is.

Do not ask someone to walk you through it step by step. Sit down, open a
terminal, and figure it out. That discomfort is the point.

---

### Learn Basic Networking

You cannot break or defend something you do not understand. Learn what an IP
address is, what a port does, how TCP/IP works at a basic level, and what DNS is
actually doing when you type a URL.

This stuff is dry but it is load-bearing knowledge. You will use it forever.
Look it up. Read the boring parts.

---

### Intro to the Command Line & Scripting

Get comfortable running tools from the terminal. Learn enough Bash to automate
small tasks. Even a little Python goes a long way — being able to write a quick
script to process output or automate something is a genuine superpower in this
field. Also remember whether you like it or not, we are in now in the age of AI,
use it.

Nobody is going to write your scripts for you. That is the whole lesson here.

---

### Web & System Fundamentals

Understand how a web request works end to end. What is HTTP? What happens when a
browser talks to a server? On the system side, understand users, groups,
processes, and basic privilege concepts. This is where a lot of real-world
vulnerabilities live.

Read. Experiment. Break things. That is the curriculum.

---

### Try Your First CTF

CTFs (Capture the Flag competitions) are practice arenas where you solve
security challenges to find hidden flags. They are the best way to apply what
you have learned in a low-stakes, hands-on environment.

Start with [PicoCTF](https://picoctf.org/) or
[TryHackMe](https://tryhackme.com/). Do not worry about your score. Just work
through challenges and look up what you do not know. That loop — try, fail,
learn, repeat — is the whole game.

---

### Pick a Specialization

Once you have the basics down, cybersecurity branches out. Web exploitation,
binary exploitation, forensics, network defense, malware analysis — each has its
own depth. Start exploring what genuinely interests you and go deep on it.

The club covers a range of these. At this point you should be self-directing.
Nobody is going to tell you what to be good at.

---

### Contributing to the Club

This is where you go from learning to doing. Competing in club events, helping
newer members, contributing writeups, building tooling — this is where things
get genuinely fun and the skills start compounding fast.

---

You do not need permission to start. Pick the first step you have not done yet
and do it tonight. The road is long but it is a good one.
