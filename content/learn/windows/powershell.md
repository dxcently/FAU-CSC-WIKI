+++
title = "PowerShell"
weight = 1
description = "PowerShell as the Windows shell and scripting language, the object pipeline, and why execution policy is not a security control."
icon = "fa-solid fa-terminal"
+++

PowerShell is the shell and scripting language built into every modern version of Windows. It is the closest thing Windows has to Bash — except it works on a completely different idea, and that difference matters.

This page covers what a cmdlet is, how the PowerShell pipeline actually works, the cmdlets you will reach for constantly, and why PowerShell shows up on both sides of a security incident.

---

## What a Cmdlet Is

A **cmdlet** (pronounced "command-let") is a single PowerShell command. Every cmdlet follows the same naming pattern: `Verb-Noun`.

```powershell
Get-Process       # get the list of running processes
Get-Service        # get the list of services
Stop-Process        # stop a process
New-Item            # create a new file or folder
```

The verb tells you what the cmdlet does. The noun tells you what it acts on. `Get-Process` gets processes. `Stop-Service` stops a service. Once you know this pattern, you can guess a huge number of cmdlet names correctly on the first try — that is the entire point of the naming convention.

Run `Get-Command` to list every cmdlet available on the system. Run `Get-Help <cmdlet-name>` to read the manual for one cmdlet, the same way `man` works on Linux.

```powershell
Get-Command                  # list all available cmdlets
Get-Help Get-Process          # read the manual for one cmdlet
Get-Help Get-Process -Examples   # just the usage examples
```

---

## The Object Pipeline — the Real Conceptual Leap

This is the one idea in this section that is worth slowing down for.

On Linux, a pipe (`|`) sends **plain text** from one command to the next. `ps aux | grep firefox` runs `ps`, gets back a wall of text, and hands that text to `grep`, which searches it line by line for the word "firefox." Every command in that chain has to know how to parse the text it receives, because text is all it ever gets.

PowerShell's pipe sends **objects**, not text. An object is a structured piece of data with named properties — think of a row in a spreadsheet, not a line of text. When you run `Get-Process`, PowerShell does not hand you text that merely *looks like* a process list. It hands you a collection of actual process objects, each one carrying properties like `Name`, `Id`, and `CPU`. The next cmdlet in the pipeline receives those same objects, properties intact, and can filter, sort, or inspect them directly — no parsing required.

```powershell
Get-Process | Where-Object { $_.CPU -gt 100 }   # keep only processes using more than 100 CPU
Get-Process | Sort-Object CPU -Descending        # sort processes by CPU, highest first
Get-Process | Select-Object Name, Id, CPU        # show only these three properties
```

Compare that to the Linux equivalent, which has to scrape columns out of text with tools like `awk` and hope the formatting never changes:

```bash
ps aux | awk '{print $3, $2, $11}' | sort -rn
```

Same goal, different foundation. Text pipes are simple and universal but fragile — reformat the output and every downstream `grep` and `awk` breaks. Object pipes are more structured and far less fragile, but only work within PowerShell's own ecosystem. Neither approach is wrong. They are different answers to the same problem, and once you see PowerShell as "Unix pipes, but every value keeps its shape," the rest of the language stops feeling foreign.

---

## Cmdlets You Will Use Constantly

These cover enumeration — looking around a system to see what is on it — and basic administration.

| Cmdlet | What it returns |
|---|---|
| `Get-Process` | Running processes |
| `Get-Service` | Installed services and their status |
| `Get-LocalUser` | Local user accounts on this machine |
| `Get-LocalGroupMember Administrators` | Members of the local Administrators group |
| `Get-ChildItem` | Files and folders in a directory — the PowerShell equivalent of `ls` |
| `Get-NetIPAddress` | IP addresses configured on this machine |
| `Get-EventLog` / `Get-WinEvent` | Windows event log entries |

`Get-ChildItem` is worth a second look, because it shows the object idea again: `ls` on Linux prints text. `Get-ChildItem` returns file objects with real properties — `Name`, `Length`, `LastWriteTime` — that you can filter and sort the same way you filtered processes above.

```powershell
Get-ChildItem C:\Users | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-1) }
# every item in C:\Users modified in the last day
```

On a machine you administer — your own, or a box in your lab — these cmdlets are how you answer basic questions fast: what is running, what is installed, who has an account, what changed recently.

---

## Execution Policy Is Not a Security Boundary

PowerShell has an **execution policy** setting that controls whether scripts are allowed to run at all.

```powershell
Get-ExecutionPolicy          # see the current policy
Set-ExecutionPolicy RemoteSigned   # a common, less restrictive policy
```

New PowerShell users assume this is a security control, the same way a locked door keeps people out. It is not. Microsoft's own documentation says so directly: execution policy is meant to stop you from running a script *by accident*, not to stop a determined attacker. It is trivially bypassed — running a script's contents through the command line directly, or loading it a different way, skips the check entirely. Do not rely on execution policy to keep a system safe. Real protection comes from the logging and monitoring covered next, plus normal account and patch hygiene.

---

## Logging: How Defenders See What PowerShell Did

PowerShell is a favorite tool for attackers precisely because it is already installed on every Windows machine — nothing extra to bring in, nothing that looks obviously out of place. Security teams call this **living off the land**: using the target's own built-in tools instead of custom malware, which makes the activity blend in with normal admin work.

Because of that, Windows ships PowerShell-specific logging built to catch it:

- **Script block logging** records the actual code PowerShell executes, even code that was built dynamically at runtime or deliberately obfuscated to hide from a quick glance. This is the single most useful log source for catching PowerShell abuse.
- **Module logging** records which PowerShell commands ran and their pipeline output.
- **Transcription** writes a full text transcript of a PowerShell session to a file — every command typed, every result shown, as if someone recorded the screen.

None of these are on by default on a stock installation. Turning them on is usually done through Group Policy — see [Group Policy & Policy Configuration](group-policy/) for how policy gets pushed to every machine in a domain at once. On your lab domain, turn these on, generate some activity, and go read the resulting event logs. That is the fastest way to understand what a real detection actually looks like.

> [!info] How the Club Uses This
> TODO: Add how FAU CSC uses PowerShell in practice — CCDC scripts, lab automation, specific enumeration workflows the team runs.

---

**References**

- [about_Command_Syntax](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_command_syntax) — official cmdlet syntax reference
- [about_Pipelines](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines) — how the object pipeline works
- [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies) — Microsoft's own explanation of why execution policy is not a security boundary
- [PowerShell Logging Guidance — Microsoft](https://learn.microsoft.com/en-us/powershell/scripting/windows-powershell/wmf/whats-new/script-logging) — script block logging and transcription
- [LOLBAS Project](https://lolbas-project.github.io/) — catalog of built-in Windows binaries and scripts abused for living-off-the-land techniques
