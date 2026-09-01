+++
title = "Club Lab"
weight = 40
description = "A shared club environment members are allowed to attack — details still being worked out."
icon = "fa-solid fa-server"
+++

The club is standing up a shared lab environment for members to practice on.

Here is why that matters: right now, if you want to practice attacking
something, you either use a public platform or you go looking for a target on
your own. The second option is how people end up somewhere they should not
be, even by accident. A club lab fixes that — it is a machine (or set of
machines) that exists specifically so you are allowed to attack it. No
permission-seeking, no wondering if this is okay. It is the point of the
thing.

That is the entire idea: a safe, shared, explicitly-in-scope target, so
nobody practices on something they should not touch.

---

## What a Lab Actually Is

A lab is not one VM you spin up and poke at. It is three layers stacked on
top of each other, and each layer depends on the one below it.

### The Hardware Layer

Somewhere, real hardware has to run the virtual machines. A **hypervisor**
is the software that turns one physical machine into several virtual ones.
Running it on a dedicated server, instead of everyone's personal laptop,
is what makes a *shared* lab possible in the first place. See
[Proxmox](./proxmox) for how that works.

### The Network Layer

Every machine in the lab needs a network to talk on. That network must stay
separate from the FAU campus network — a lab is where you are allowed to
attack things, and that permission does not extend one inch past the lab's
own network boundary. Both pages below cover how this isolation is built,
because it matters at every layer.

### The Target Layer

One VM is a target. A **range** is several VMs wired together so they
behave like a small, real network — a domain controller, some clients, a
server, somewhere to attack from. This is the part that turns "a VM you can
poke at" into something worth practicing on. See
[Building an End-to-End Range](./building-a-range).

---

## The Two Pages Here

- **[Proxmox](./proxmox)** — the hypervisor that runs the lab's hardware
  layer. VMs vs. containers, storage and snapshots, and the isolated
  networking a shared lab needs.
- **[Building an End-to-End Range](./building-a-range)** — how you take a
  pile of VMs on that hypervisor and wire them into one environment that
  behaves like a real target network.

Read them in that order. The first page is the box the lab runs on. The
second is what you build on top of it.

---

> [!info] Status
> This is a stub. The lab is not live yet. Specifics — what it runs, how you
> get access, what is and is not in scope, how resets work — are still being
> decided. This page will be filled in once those decisions are made.

---

If you want to help shape this, this is a good place to show up and ask
questions. See [Projects & Guides](/projects/) for how to get involved.

---

{{< section-grid >}}
