+++
title = "Group Policy & Policy Configuration"
weight = 3
description = "How Group Policy pushes configuration to every machine in a domain, and why it decides most CCDC and CyberPatriot scores."
icon = "fa-solid fa-clipboard-list"
+++

You do not walk around to a thousand computers and configure each one by hand. In Active Directory, you configure a setting once, and Group Policy pushes it to every machine that should have it — automatically, and on an ongoing basis.

This page covers what Group Policy can enforce, how it decides which settings win when several apply at once, what a security baseline is, and why so much of CCDC and CyberPatriot scoring comes down to this one topic.

---

## What a GPO Is

A **Group Policy Object** (GPO) is a named bundle of settings — think of it as a rulebook. You build a GPO once, then link it to a domain, a site, or an [organizational unit](active-directory/#organizational-unit-ou), and every computer or user inside that scope picks up the rules automatically the next time policy refreshes.

Windows refreshes policy on a regular interval on its own, and also whenever a computer restarts or a user logs in. You do not have to touch each machine again after the GPO is linked — that is the entire value of the system. Change the GPO once, and every machine in scope gets the update on its next refresh.

On a machine in your lab domain, you do not have to wait for the automatic refresh to see a change take effect. Running `gpupdate /force` from an elevated PowerShell or Command Prompt session tells that machine to pull the latest policy immediately — the standard way to test a GPO change without waiting or rebooting.

---

## What Group Policy Can Enforce

Group Policy's reach is enormous — thousands of individual settings — but almost all of it falls into a handful of categories that matter for security work.

| Category | What it controls |
|---|---|
| **Password policy** | Minimum length, complexity requirements, how often passwords must change |
| **Account lockout policy** | How many failed login attempts before an account locks, and for how long |
| **Audit policy** | Which events get written to the security log — logins, file access, privilege use |
| **Service configuration** | Which services are allowed to run, and how they start |
| **Software restriction** | Which applications are allowed to run at all |
| **User rights assignment** | Who can log in locally, log in over the network, or log in as a service |

A weak password policy is not a small thing. Set the minimum length too low, or skip complexity requirements, and every account in the domain becomes easier to guess or crack the moment an attacker gets a copy of the password hashes. Audit policy is just as easy to get wrong in the other direction: log too little, and there is nothing to look at after an incident; log too much, and the important events drown in noise.

Every GPO is split into two halves: **Computer Configuration** and **User Configuration**. Computer Configuration settings apply to the machine itself, regardless of who logs in — service configuration and most security settings live here. User Configuration settings follow the person, applying no matter which domain-joined machine they log into — things like desktop restrictions. Knowing which half a setting belongs to explains a lot of "why didn't this apply" confusion: a Computer Configuration setting linked to an OU full of user accounts, with no computers in it, will never take effect, because there are no computers in scope to apply it to.

---

## How Policy Applies: Order Matters

A computer can be in scope for more than one GPO at once — one linked to the whole domain, another linked to its specific OU. When two GPOs disagree on the same setting, Windows needs a rule for which one wins.

The short version, in the order policy applies:

1. **Local policy** on the machine itself applies first.
2. **Site-linked** GPOs apply next.
3. **Domain-linked** GPOs apply after that.
4. **OU-linked** GPOs apply last, and closer OUs override further ones.

Later always beats earlier. This is usually shortened to **LSDOU** (Local, Site, Domain, OU) as a memory aid, not a term you need to recite — the idea that matters is: the more specific the scope, the more power it has to override something broader. A domain-wide password policy can be tightened further for one sensitive OU, and that OU's setting wins for the machines inside it.

There is one important exception worth knowing exists: an administrator can mark a GPO setting so nothing more specific is allowed to override it, forcing that setting to apply everywhere regardless of what a closer-scoped GPO says. You will not need this on day one. Know that it exists so a setting that "should have" been overridden and wasn't makes sense later.

**A worked example.** Say the domain-wide GPO sets minimum password length to 8 characters, and a separate GPO linked to the "IT" OU sets it to 14 characters. A user account inside the IT OU is in scope for both. Because OU-linked policy applies last and wins, that user's real minimum is 14 — the domain-wide 8 still applies to everyone outside the IT OU. Nothing was deleted or broken; the more specific rule simply took precedence, exactly as designed.

---

## Security Baselines and Hardening Benchmarks

Figuring out the right value for every setting from scratch, for an entire domain, is not a reasonable task for one person. That is what a **security baseline** is for: a pre-built, vetted set of policy settings, published by an organization that has already done the work of deciding what "reasonably secure" looks like for a given system.

The best-known example is the **CIS Benchmarks**, published by the Center for Internet Security — a free, detailed document for each major operating system that lists every setting worth locking down, why it matters, and what value to set it to. Microsoft publishes its own baselines too, built specifically for Group Policy, that you can import directly instead of configuring thousands of individual settings by hand.

Using a published baseline instead of guessing matters for two reasons. It has been reviewed by people who do this professionally, and it saves you from having to independently research thousands of settings. Start from a baseline, then adjust the handful of settings that do not fit your specific environment — do not start from a blank GPO and improvise.

A small taste of what a baseline actually recommends, to make the idea concrete:

| Setting | A typical baseline value |
|---|---|
| Minimum password length | 14 characters |
| Account lockout threshold | 10 invalid attempts |
| Audit logon events | Success and failure |
| Guest account | Disabled |
| Anonymous SID/name translation | Disabled |

None of these numbers are magic. They are defaults a professional body arrived at after reviewing real attack data. Apply the baseline, understand why each setting exists, and only deviate from it once you have a specific reason to.

---

## Why This Is Most of CCDC and CyberPatriot

Both major club competitions score defense largely by asking one question over and over: **is this setting configured correctly?**

CyberPatriot hands you a Windows image with a list of intentional misconfigurations and vulnerabilities baked in, and scores you automatically as you find and fix them — weak passwords, unnecessary services running, missing audit settings, the works. CCDC does the same thing at the scale of a whole network, live, while a professional red team actively tries to break back in through anything you missed. In both cases, a huge share of the score is decided before the clock even starts moving fast: how much of your baseline hardening did you actually get right?

This is why Group Policy is not a side topic. It is the practical mechanism behind most of what "hardening a Windows network" means in competition, and in a real job.

> [!info] How the Club Uses This
> TODO: Add how FAU CSC uses this in practice — GPO templates the team has built, baseline checklists, CyberPatriot image walkthroughs.

---

**References**

- [Group Policy Overview — Microsoft](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-overview)
- [How Core Group Policy Works — Microsoft](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/core-group-policy-tools-and-settings)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) — free hardening benchmarks for Windows and most major platforms
- [Microsoft Security Compliance Toolkit](https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/security-compliance-toolkit-10) — Microsoft's own importable security baselines
- [CyberPatriot](https://www.uscyberpatriot.org/) and [CCDC](https://www.nationalccdc.org/) — the competitions this page's scoring model refers to
