+++
title = "VM Tools"
weight = 3
description = "A rundown of hypervisor options and how to pick one for your hardware."
icon = "fa-solid fa-cubes"
+++

A hypervisor runs the VM on top of your host OS. There are several. Pick one that fits your hardware and OS.

---

## Options

### VirtualBox

Free. Cross-platform (Windows, macOS, Linux). The most widely used option for beginners.

- Works on almost any hardware
- Solid snapshot support
- Slightly worse performance than VMware
- [Download](https://www.virtualbox.org/)

---

### VMware Workstation Pro / Fusion

VMware Workstation runs on Windows and Linux. VMware Fusion runs on macOS. Both are free for personal use now.

- Better performance than VirtualBox
- Better USB and GPU passthrough
- More polished UI
- [VMware Workstation](https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion) | [VMware Fusion](https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion)

---

### UTM (macOS)

The best option for Apple Silicon Macs. Runs ARM and x86 VMs using QEMU under the hood.

- Free
- Native Apple Silicon support
- Slightly more setup than VirtualBox
- [Download](https://mac.getutm.app/)

---

### QEMU/KVM (Linux)

QEMU is a raw emulator. KVM is the Linux kernel's virtualization module. Together they are very powerful and very manual.

- High performance
- No GUI by default — configure from the terminal or use `virt-manager`
- Best for users already comfortable with Linux
- [QEMU docs](https://www.qemu.org/docs/master/) | [virt-manager](https://virt-manager.org/)

---

### Proxmox VE

A hypervisor built for running on a dedicated server or homelab machine. Not for running on your laptop.

- Free, open source
- Web-based management UI
- Supports both VMs and containers (LXC)
- [proxmox.com](https://www.proxmox.com/)

---

## Quick Comparison

| Tool | Platform | Cost | Best For |
|---|---|---|---|
| VirtualBox | All | Free | Beginners |
| VMware Workstation | Win/Linux | Free (personal) | Intermediate |
| VMware Fusion | macOS | Free (personal) | macOS users |
| UTM | macOS | Free | Apple Silicon |
| QEMU/KVM | Linux | Free | Power users |
| Proxmox | Dedicated server | Free | Homelab |

---

> [!info] How the Club Uses This
> TODO: Add which hypervisor the club standardizes on for lab sessions and competitions.
