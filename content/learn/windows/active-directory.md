+++
title = "Active Directory"
weight = 2
description = "How Active Directory organizes an enterprise network, how Windows authentication works, and why Active Directory is the top target for attackers."
icon = "fa-solid fa-users-gear"
+++

Active Directory is the directory service that runs most corporate and school networks. It is one central system that tracks every user, every computer, and who is allowed to do what. Log into a work laptop, print to a shared printer, or open a file on a network drive — Active Directory is usually the thing that made that possible.

This page covers the core objects, how authentication actually works, and why Active Directory is the single highest-value target on any enterprise network — explained so you can recognize and defend the paths attackers take, not so you can walk them against a system you don't own.

---

## The Building Blocks

Four words carry almost all of the concept. Get these, and Active Directory stops looking like alphabet soup.

### Domain

A **domain** is one administrative unit — one set of users, computers, and policies, managed together under a shared name like `corp.local`. Think of it as one company's entire network, organized under a single roof. Everything else in this page happens inside a domain.

### Domain Controller

A **domain controller** (DC) is the server that holds the actual Active Directory database and answers login requests for the domain. Every domain has at least one. When a user logs into any computer in the domain, that computer asks the domain controller: "is this password correct, and what is this user allowed to do?"

The domain controller is the most important machine on the network. If an attacker fully controls a domain controller, they control the domain — every account, every password hash, every computer that trusts it.

### Forest

A **forest** is a collection of one or more domains that trust each other and share a common structure. A small organization might run one domain in one forest. A large university or corporation might run several domains — one per department or region — all inside the same forest. You do not need to go deeper than this for now: know that a forest is the container domains live inside, and that trust between domains in the same forest is usually automatic.

### Organizational Unit (OU)

An **organizational unit** (OU) is a folder inside the domain used to organize users and computers — for example, an "Accounting" OU and an "IT" OU, each with different rules applied to it. OUs exist so an administrator can apply different settings to different groups of machines or people without touching the whole domain at once. [Group Policy & Policy Configuration](group-policy/) covers exactly how those settings get applied through OUs.

| Term | Plain-English answer to "what is it" |
|---|---|
| Domain | One company's network, managed as a unit |
| Domain Controller | The server that checks logins for the domain |
| Forest | A group of domains that trust each other |
| OU | A folder for organizing users and computers inside a domain |

---

## Objects: Users, Computers, Groups

Everything Active Directory tracks is an **object** — a record in the directory with a name and a set of properties. Three object types matter most.

- **User objects** represent a person: a username, a password hash, group memberships, and account settings like whether the account is disabled.
- **Computer objects** represent a machine joined to the domain. Every domain-joined computer has its own object and its own set of credentials, separate from any user.
- **Group objects** are collections of users or computers, used to grant permissions in bulk instead of one account at a time. Add a user to the "Domain Admins" group, and that user inherits every permission the group carries — full administrative control over the domain.

Managing permission through group membership instead of per-user settings is the entire point of Active Directory. Grant access to a group once, add and remove members as people join or leave, and you never touch the underlying permission again. It also means a single misconfigured group can quietly hand out far more access than anyone intended — a recurring theme in real-world Active Directory compromises.

---

## Kerberos: How Login Actually Works

**Kerberos** is the authentication protocol Active Directory uses to verify who you are and what you're allowed to touch, without sending your password across the network every time you access something.

The core idea is a **ticket**: proof that you already proved your identity once, so you don't have to prove it again for every single request. Here is the plain version of the flow:

1. You log in. Your computer proves your identity to the domain controller one time, using your password.
2. The domain controller hands back a **Ticket Granting Ticket** (TGT) — a signed token that says "this user already authenticated successfully," valid for a limited time.
3. When you want to access something — a file server, a printer, an application — your computer shows the TGT to the domain controller and asks for a **service ticket** for that specific resource.
4. The domain controller issues a service ticket. You hand that ticket to the file server, the file server trusts it because it trusts the domain controller, and you're in.

```
You            Domain Controller         File Server
 |  1. login (password)   |                    |
 |------------------------>|                    |
 |  2. TGT issued          |                    |
 |<------------------------|                    |
 |  3. "give me a ticket for the file server"    |
 |------------------------>|                    |
 |  4. service ticket issued                     |
 |<------------------------|                    |
 |  5. present service ticket                    |
 |----------------------------------------------->|
 |  6. access granted                             |
 |<-----------------------------------------------|
```

Why go through all this instead of just sending your password every time? Two reasons. Your actual password never travels across the network after the initial login, which limits how often it can be intercepted. And tickets expire, so a stolen ticket is only useful for a limited window — unlike a stolen password, which stays useful until someone changes it.

This is also exactly why tickets are worth stealing. A ticket is portable proof of identity. Steal one, and for as long as it stays valid, you can act as the user it belongs to without ever knowing their password. That single fact underpins most of the attack concepts below.

---

## Why Active Directory Is the Crown Jewel

Compromise one laptop, and an attacker has one laptop. Compromise Active Directory, and an attacker has the entire domain — every account, every server, every file share that domain controls. That difference in scale is why Active Directory is the number one target in almost every real intrusion that goes beyond a single machine, and why "Domain Admin" — membership in the group with unrestricted control over the domain — is the standard end goal attackers work toward once they have a foothold.

Understanding the shape of that path is defensive knowledge. You cannot recognize an intrusion in progress, or design a network that resists one, if you have never seen how these pieces connect.

### Credential Theft

Once an attacker has any foothold on a domain-joined machine, they look for credentials sitting in memory, in configuration files, or cached from a previous login. Windows keeps authentication material available in memory so users don't have to re-enter passwords constantly — useful for legitimate logins, and just as useful to whoever gets local access to that memory first. This is why limiting who has administrative rights on any given machine matters: a low-privilege foothold on a box where a domain admin recently logged in can be far more dangerous than it looks.

Two named techniques come up constantly in this space, worth recognizing by name even at a purely conceptual level. **Pass-the-hash** is using a stolen password hash directly to authenticate, without ever cracking it back into the plaintext password. **Kerberoasting** targets service accounts specifically: any authenticated user can request a service ticket for any service in the domain, and that ticket is encrypted with the service account's password hash — so an attacker requests a batch of these tickets, takes them off-network, and tries to crack the hash at their own pace. Both are reasons weak service-account passwords and standing local-admin credentials are treated as serious findings during a security review, not cosmetic ones.

### Lateral Movement

**Lateral movement** is using one compromised machine or account to reach another one, spreading sideways across the network instead of just digging deeper into the first box. A stolen set of credentials or a stolen Kerberos ticket, valid on one machine, is often valid on several others — especially where the same local administrator account is reused across many computers, a common and avoidable misconfiguration.

### Privilege Escalation Paths

Active Directory permissions are complex, and complexity hides mistakes. A **privilege escalation path** is a chain of ordinary-looking misconfigurations — a user with rights to reset another user's password, a group nested inside another group, a service account with excessive permissions — that, strung together, lead from a low-privilege account all the way to Domain Admin. No single step looks alarming on its own. That is exactly why these paths are dangerous and why security teams map them proactively, looking for the chain before an attacker finds it first.

### Why Domain Admin Is the Goal

Domain Admin means unrestricted control over every user, computer, and policy in the domain — the practical end state of a full compromise. Once an attacker holds it, they can create new accounts, disable security tooling, and access anything the domain touches. Defending Active Directory means treating every step on the way to Domain Admin as worth stopping, not just the last one.

Do not confuse this with the **local Administrator** account. Local Administrator controls one machine. Domain Admin controls every machine in the domain at once. An attacker with local admin on your laptop has your laptop. An attacker with Domain Admin has the company.

---

## Practice This Safely

Everything above is a map, not a set of instructions. Do not attempt any of these concepts against a network you do not own or are not explicitly authorized to test — that includes any FAU network, any club member's machine, and anything else outside a lab you built yourself.

The right way to learn this hands-on: build a small lab domain as described in [Windows & Active Directory](/learn/windows/), with one domain controller and one or two joined machines, all inside virtual machines you control. Practice detection and defense in that lab — set up logging, watch how normal authentication looks in the event log, and only then look at what an attack path looks like from the defender's chair. Platforms built specifically for this, like a dedicated Active Directory attack lab range, are a safer and more structured next step than improvising against your own lab once you're past the basics.

> [!info] How the Club Uses This
> TODO: Add how FAU CSC uses this in practice — the club's lab domain setup, CCDC AD scenarios, walkthroughs the team has done.

---

**References**

- [Active Directory Domain Services Overview — Microsoft](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview)
- [How the Kerberos Version 5 Authentication Protocol Works — Microsoft](https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-authentication-overview)
- [Active Directory Security Groups — Microsoft](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups)
- [MITRE ATT&CK — Lateral Movement](https://attack.mitre.org/tactics/TA0008/)
- [MITRE ATT&CK — Credential Access](https://attack.mitre.org/tactics/TA0006/)
