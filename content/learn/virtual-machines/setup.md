+++
title = "Setting Up a VM"
weight = 2
description = "The universal steps for setting up a virtual machine regardless of hypervisor."
icon = "fa-solid fa-screwdriver-wrench"
+++

Pick a hypervisor (see [Tools](./tools)), download an ISO, create the VM. That is the whole process.

The details differ by tool, but the steps below are universal.

---

## Step 1 — Choose a Guest OS

For security work, start with one of these:

| OS | Why |
|---|---|
| [Kali Linux](https://www.kali.org/) | Comes with most security tools pre-installed |
| [Parrot OS](https://www.parrotsec.org/) | Lighter than Kali, good for older hardware |
| [Ubuntu](https://ubuntu.com/) | Clean slate, you install what you need |

Kali is the default choice for offensive security. Ubuntu is better if you want to learn Linux from scratch without preinstalled noise.

Download the ISO from the official site. Verify the checksum before using it.

---

## Step 2 — Create the VM

In your hypervisor, create a new VM and point it at the ISO. Standard recommended specs:

| Resource | Minimum | Comfortable |
|---|---|---|
| RAM | 2 GB | 4 GB |
| Storage | 20 GB | 40–60 GB |
| CPUs | 1 core | 2 cores |

Do not over-allocate. Your host machine needs resources too.

---

## Step 3 — Network Modes

Choose based on what you need:

| Mode | What it does |
|---|---|
| **NAT** | VM shares host's IP. Can reach the internet. Cannot be reached from outside. |
| **Bridged** | VM gets its own IP on your network. Visible to other devices. |
| **Host-only** | VM talks only to the host. No internet. Good for isolated lab setups. |
| **Internal Network** | Multiple VMs talk to each other. Completely isolated from host and internet. |

Start with NAT. Switch to host-only or internal when you set up attack/defend lab environments.

---

## Step 4 — Take a Snapshot

Before you install anything or run any tools, take a snapshot. Name it something useful like `clean-install`.

When things break — and they will — revert and start from a known good state.

---

## Recommended First Steps After Install

```bash
# Update the system
sudo apt update && sudo apt upgrade -y

# Check your IP address
ip addr show

# Check you can reach the internet
ping -c 4 google.com
```

---

> [!tip] Guest Additions / VMware Tools
> Install the guest additions for your hypervisor after setup. They improve display resolution, clipboard sharing, and file drag-and-drop. Look up the specific steps for your tool.

---

> [!info] How the Club Uses This
> TODO: Add recommended VM setup for club competitions and labs — specific OS versions, network configs, shared snapshots, etc.

---

**References**

- [Kali Linux documentation](https://www.kali.org/docs/)
- [VirtualBox manual](https://www.virtualbox.org/manual/)
- [VMware documentation](https://docs.vmware.com/)
