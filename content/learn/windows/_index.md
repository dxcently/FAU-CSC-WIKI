+++
title = "Windows & Active Directory"
weight = 7
description = "Why Windows and Active Directory matter for security work, and what this section covers."
icon = "fa-brands fa-windows"
+++

Every security tool you have used so far runs on Linux. That is fine for tools. It is not how the real world runs.

Most businesses, schools, and government offices run Windows on the desktop and Active Directory behind it. If you defend networks for a living, you are defending Windows networks. If you attack networks for a living — with permission, on an engagement — you are attacking Windows networks. Linux is where your tools live. Windows is where the target lives.

This section covers the floor everything else builds on.

---

## Why This Is the Priority

Three reasons, in order of how often you will run into them.

**The club competes on Windows.** CCDC hands your team a live Windows domain and a professional red team that breaks in within the hour. CyberPatriot scores you on how well you lock down a Windows image. Both competitions live and die on the skills in this section. If you walk into either one without Active Directory and Group Policy under your belt, you are guessing.

**Real intrusions happen in Active Directory.** A ransomware crew does not stop at one laptop. They land on one machine, then use Active Directory to become Domain Admin and lock down the entire company overnight. Understanding how that path works — not to walk it yourself against something you don't own, but to recognize it and block it — is the single highest-value skill in defense right now.

**The enterprise is Windows.** Ask any working sysadmin what they touch daily. It is Active Directory, Group Policy, and PowerShell. That is not a niche skill set. It is the job.

---

## What's in This Section

Three pages, in the order you should read them.

### [PowerShell](powershell/)

The shell and scripting language built into every modern Windows machine. Start here — you need it to look at anything else in this section. Covers cmdlets, the object pipeline, and how PowerShell shows up on both sides of a security incident: defenders log it, attackers abuse it.

### [Active Directory](active-directory/)

The directory service that runs the enterprise: one place that tracks every user, computer, and permission on the network. Covers the core objects, how Windows authentication actually works, and why Active Directory is the single most valuable target on the network — explained so you can defend it, not attack anything you don't own.

### [Group Policy & Policy Configuration](group-policy/)

The mechanism that pushes settings — password rules, audit logging, service configuration — to every machine in the domain at once. This is most of what CCDC and CyberPatriot actually score. Get this page, and hardening a Windows box stops being a mystery.

---

## Before You Start

You need a lab. Do not read this section and then go poke at a machine you do not own — that is not what any of this is for.

The cheapest way in: spin up a Windows Server virtual machine (Microsoft offers free evaluation ISOs for this exact purpose), promote it to a domain controller, and join a Windows 10 or 11 VM to that domain. Now you have a real, small Active Directory environment that is entirely yours. Everything in this section assumes you are working inside something like that — your lab domain, not anyone else's.

If you have not set up a VM yet, start at [Virtual Machines](/learn/virtual-machines/) first.

> [!info] How the Club Uses This
> TODO: Add how FAU CSC uses this in practice — CCDC prep, a standing lab domain, CyberPatriot image walkthroughs, etc.
