+++
title = "Linux"
weight = 2
description = "The Linux fundamentals security work is built on: filesystem, permissions, and processes."
icon = "fa-brands fa-linux"
+++

Security tooling runs on Linux. You don't need to master it — you need to stop being afraid of it.

This section covers the filesystem, permissions, and processes. That is the floor everything else builds on.

---

## The Four Building Blocks

Linux looks intimidating from the outside — a black screen and a blinking cursor. Underneath, it is four ideas. Learn these and the terminal stops being scary.

### 1. Filesystem & Paths

Everything on a Linux system — programs, settings, even hardware devices — is represented as a **file** sitting somewhere in one giant tree of folders. The tree starts at the root folder, written `/`. A **path** is just the address of a file in that tree, like `/home/user/notes.txt`.

High level: if you know how the tree is laid out, you know where to look for anything, on any Linux system, ever.

Low level: even a running program or a USB drive shows up as a file, under folders like `/proc` or `/dev`. Read that file and you are talking directly to the kernel — the core program that manages the hardware.

Walk the tree in [The Filesystem](./filesystem).

### 2. Users & Permissions

Linux is a **multi-user** system by design. It is built to support more than one account at once, even when only one person is sitting at the keyboard.

High level: permissions are how Linux decides who can read, write, or run each file. Get this wrong and you either lock yourself out or leave a door open for an attacker.

Low level: every file carries an owner, a group, and three sets of read/write/execute rules — one set each for the owner, the group, and everyone else. A wrong setting here is a common path to **privilege escalation**, meaning gaining higher access than you started with.

Learn to read and change them in [Permissions & Users](./permissions).

### 3. Processes & Services

A **process** is a program while it runs. Open a text editor and it becomes a process. Close it and the process ends.

High level: knowing what is running, and as which user, tells you whether a system is healthy or already compromised.

Low level: the kernel assigns every process a number, called a **PID**, and tracks which user owns it. A **service** is a process the system starts on its own and keeps running in the background, such as a web server.

Inspect them in [Processes & Services](./processes).

### 4. Package Managers

Software on Linux does not usually come from a website with a download button. It comes from a **package manager** — a tool that fetches, installs, updates, and removes software for you from a trusted source.

High level: this is how you install the tools you actually came here for, such as nmap or Wireshark, with one command instead of a manual hunt across the internet.

Low level: the package manager also tracks **dependencies** — other pieces of software your tool needs to run — and installs those automatically. Every Linux distribution ships one. The command differs (`apt`, `dnf`, `pacman`), but the idea stays the same.

---

{{< section-grid >}}
