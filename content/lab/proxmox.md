+++
title = "Proxmox"
weight = 1
description = "Proxmox VE as the bare-metal hypervisor that runs the club lab, and the concepts you need to understand it."
icon = "fa-solid fa-hard-drive"
+++

Proxmox VE is the hypervisor most homelab and club setups reach for when a
laptop stops being enough. It is not the only option, but it is the one
this page explains, because it is the one the lab is most likely to run on.

---

## 1. A Bare-Metal Hypervisor

A **hypervisor** is software that lets one physical machine run several
virtual machines at once. Proxmox is a **type-1**, or **bare-metal**,
hypervisor. It installs directly onto the server's hardware. There is no
underlying Windows, macOS, or Linux desktop underneath it — Proxmox *is*
the operating system on that box.

This is different from running VirtualBox on your laptop. VirtualBox is a
**type-2** hypervisor. It installs as an app on top of an OS you already
use for everything else — browsing, email, homework. Every VM you run
competes with your own desktop for CPU, memory, and disk.

Proxmox skips that layer. The whole machine exists to run VMs, and nothing
else runs on it competing for resources. That is why one Proxmox server can
comfortably host many VMs at once, where a laptop running VirtualBox
struggles past two or three.

---

## 2. VMs vs. LXC Containers

Proxmox can create two different kinds of guest: a full **VM** or an
**LXC container**.

A VM emulates an entire computer. It gets its own virtual CPU, its own
memory, its own virtual disk, and it boots its own kernel — the core
program that talks to hardware. This is true even though the hardware is
virtual. A VM does not know, or care, that it is not real.

An LXC container is lighter. It shares the host server's kernel instead of
booting its own. It still looks like a separate Linux machine from the
inside — its own filesystem, its own processes, its own IP address — but it
starts in a second or two instead of a minute, and uses a fraction of the
memory.

Use a VM when you need a different operating system than the host, such as
Windows, or when you need strong isolation because you are running
something risky. Use an LXC container when you just need a lightweight
Linux service — a DNS server, a small web app — and speed matters more than
isolation.

---

## 3. Storage and Snapshots

Every VM and container needs a disk. Proxmox calls the place that disk
lives **storage** — it can be a local drive on the server, or something
more advanced like a networked storage pool. For a club lab, local storage
on the server is enough to start.

The feature that matters most for a lab is the **snapshot**. A snapshot
freezes a VM's exact state — disk contents, and often memory — at one
moment in time. Restoring a snapshot rewinds the VM back to that moment,
undoing everything that happened after.

This matters because a lab is a place you are *supposed* to break things.
You will misconfigure a service, run an exploit that corrupts a database,
or delete a file you needed. Without a snapshot, that mistake costs you a
full reinstall. With one, it costs you thirty seconds and a click.

Snapshots do not usually copy the whole disk again each time. Proxmox
tracks only the changes made after the snapshot, and discards those
changes on restore. That is why taking one is fast, even on a large VM.

---

## 4. Virtual Networks — Keeping the Lab Off Campus

Proxmox connects VMs to the network through a **virtual bridge** — a
software switch that behaves like a physical network switch, except it
lives entirely inside the hypervisor. A VM's virtual network card plugs
into a bridge the same way a real computer's cable plugs into a real
switch.

This matters more than any other setting on the box. A lab exists so
members can attack things safely — and "safely" means the traffic never
reaches the FAU campus network. A virtual bridge with no path out to the
campus network is what makes that true. Build the lab's VMs on an isolated
bridge, and an exploit, a scan, or a mistake inside the lab has nowhere to
go but the lab.

Do not treat this as optional configuration to get to later. It is the one
setting that turns "a lab" into "a machine that can reach FAU's network,"
which is a very different, and not allowed, thing. If you are setting up a
lab VM and you are not sure which bridge it is on, stop and check before
you do anything else on it.

---

## 5. Templates and Cloning

Building a VM by hand — install the OS, apply updates, install tools — is
slow, and doing it the same way twice by memory is unreliable. Proxmox
solves this with **templates**.

A template is a VM you have already built and configured once, then marked
as read-only. From a template, you **clone** new VMs in seconds instead of
minutes. Each clone starts as an exact copy of the template's disk.

For a lab, this is what makes rebuilding practical. Build one clean Windows
template and one clean Linux template. When a member breaks their VM badly
enough that a snapshot cannot fix it, clone a fresh one from the template
instead of reinstalling from scratch.

---

## 6. Why One Shared Box

A club could ask every member to install a hypervisor on their own laptop
instead. Some members already do, for personal practice — see
[Virtual Machines](/learn/virtual-machines/) for that path. But a shared
club lab is a different goal, and it needs a shared box.

A laptop hypervisor is limited by that one laptop's CPU, memory, and disk.
A range with a domain controller, several clients, and a server (see
[Building an End-to-End Range](./building-a-range)) is heavier than most
laptops can run well, especially alongside the owner's normal schoolwork.

A shared server also means everyone works from the same environment. A
misconfigured VM on one member's laptop is that member's problem alone. The
same VM on a shared, snapshotted, template-backed server is something the
next member can reset and reuse. That reusability is the entire point of a
club lab over a personal one.

---

> [!info] How the Club Uses This
> TBD. The club has not finalized the lab's hardware, its exact network
> layout, or who gets access and how. This page explains Proxmox as a
> concept so that whatever the club settles on, you already understand the
> pieces. Specifics get added here once they exist.
