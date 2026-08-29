+++
title = "Why Virtual Machines"
weight = 1
+++

A VM runs a full operating system inside your current one. It is isolated — what happens inside stays inside.

You can break it completely and roll back to a snapshot in 30 seconds. That is the whole value proposition.

---

## Real-World Uses

Security professionals use VMs constantly.

- **Malware analysts** run suspicious files inside VMs so the malware cannot touch the host.
- **Penetration testers** spin up target VMs to practice exploits before using them on a real engagement.
- **Blue teamers** deploy hardened VMs to test detection rules without touching production systems.
- **Developers** use VMs to replicate a customer's environment exactly.

The common thread: controlled isolation. You can experiment without consequences.

---

## Why You Need One Before Touching Security Tools

Most hacking tools are dual-use. Running them on your host machine is risky — not because you will get in trouble, but because misconfiguration can affect your real system, your real files, and your real network.

A VM gives you permission to be reckless. Break it on purpose. That is how you learn.

---

## Snapshots

Take a snapshot before you start anything significant. A snapshot freezes the VM state. If something goes wrong, you revert and try again.

Think of it as a save point. Use it obsessively.

---

> [!info] How the Club Uses This
> TODO: Add how FAU CSC uses VMs in demos, competitions, and lab sessions.

---

**Up next:** [Setting Up a VM →](./setup)
