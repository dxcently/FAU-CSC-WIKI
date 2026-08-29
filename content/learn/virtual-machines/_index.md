+++
title = "Virtual Machines"
weight = 1
description = "Why virtual machines matter for security practice, how to set one up, and which hypervisor tools to use."
icon = "fa-solid fa-layer-group"
+++

A virtual machine is your lab. All practice happens here — not on your host.

Break it. Reset it. Repeat. That is the whole point.

This section covers why VMs matter, how to get one running, and what tools to use.

---

## The Three Steps

Setting up a VM is three moves, done in order. Learn them once and you can build a fresh lab in minutes for the rest of your time in the club.

### 1. Pick a Hypervisor

A hypervisor is the program that creates and runs a fake computer inside your real one. The fake computer is called a **guest**. Your real machine is the **host**.

High level: you want an isolated computer to practice on, one you cannot damage by accident.

Low level: the hypervisor splits your host's CPU, memory, disk space, and network connection into virtual pieces, then hands those pieces to the guest. The guest OS boots on top of them. It has no way to tell it is not running on real hardware.

Several hypervisors exist. Pick one that fits your hardware — most are free. See [VM Tools](./tools) for the actual options.

### 2. Install a Linux Guest

Once you have a hypervisor, you install an operating system inside it. Most security tooling runs on Linux, so your first guest should be a Linux distribution.

High level: you are installing a real, full operating system. It just lives inside a file on your host disk instead of on a physical drive.

Low level: the installer writes to a **virtual disk** — a large file the hypervisor presents to the guest as if it were a hard drive. Delete that file and the guest is gone. Nothing on your host is touched.

The steps are the same shape no matter which hypervisor you picked. Walk through them in [Setting Up a VM](./setup).

### 3. Snapshot, Break, Restore

A **snapshot** is a saved copy of your VM's exact state — disk, memory, everything — frozen at one moment. Take a snapshot before you try something risky.

High level: this is your undo button. Break the VM on purpose, misconfigure it, run a suspicious file inside it. None of it matters if you can roll back to the snapshot in seconds.

Low level: the hypervisor usually does not copy the whole disk again for each snapshot. It saves only the changes made after the snapshot, then discards those changes on restore. That is why restoring is fast even on a large disk.

This is the whole reason VMs exist for security practice: freedom to break things on purpose and lose nothing. Read [Why Virtual Machines](./why-vms) for the full case.
