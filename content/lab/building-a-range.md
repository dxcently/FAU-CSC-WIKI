+++
title = "Building an End-to-End Range"
weight = 2
description = "How individual VMs get wired together into one range that behaves like a small company network."
icon = "fa-solid fa-diagram-project"
+++

One VM is a target. It is not a *range*. A range is what you get when
several VMs stop being separate boxes and start being one small network
that behaves like a real company's — because that is the only way practice
on it teaches you anything close to the real thing.

---

## 1. What a Range Is

A **range** is a set of VMs, networked together, built to imitate a real
environment closely enough that attacking or defending it teaches real
skills.

A single Linux VM teaches you to attack one Linux VM. A range teaches you
to move through a network — get a foothold on one machine, use it to reach
another, find out that the file server trusts the domain controller more
than it trusts you. That movement, called **lateral movement**, is most of
what a real attack or a real defense looks like. You cannot practice it on
one box.

---

## 2. The Standard Pieces

A basic range that stands in for a small company network needs a handful
of roles. None of these need to be powerful machines — small, correctly
configured VMs teach the same lessons as big ones.

| Piece | Role |
|---|---|
| Domain controller | Runs the directory service that other Windows machines trust for logins |
| Windows clients (x2) | Normal user workstations, joined to the domain |
| Linux server | A service host — web app, file share, database, pick one |
| Attacker box | A Linux VM with attack tooling, kept outside the "company" network |

A **domain controller** is a server that runs Windows's directory
service — it holds the list of users and machines, and decides who is
allowed to log in where. Windows networks built around one are common in
the real world, which is why a range built to teach real skills needs one
too.

Start smaller than this table if you need to. Section 6 covers that.

---

## 3. Network Segmentation — Off the Campus Network

A range is not one network. It needs at least two.

The **range network** is where the domain controller, the clients, and the
Linux server live. They talk to each other freely, the way real coworkers'
machines would.

The **attacker network** is where the attacker box sits — connected to the
range network so it can reach its targets, but not bridged out to anything
else.

Neither network may ever touch the FAU campus network. This is the same
isolation rule the hypervisor page covers, and it applies here at the range
level too: every VM in the range sits on a virtual bridge with no path to
campus. A range that can reach the campus network by accident is not a lab
anymore — it is a live attack surface pointed at a real university network,
and that is exactly what the club lab exists to prevent. Check this before
you check anything else when a new range comes online.

---

## 4. How the Pieces Depend on Each Other

The pieces in a range are not independent. Build them in the wrong order
and nothing works, because each one waits on something built before it.

**DNS points at the domain controller first.** DNS is the service that
turns a name, like a computer's hostname, into an IP address. A Windows
domain controller usually runs this service itself. Every other machine in
the range must be told to use the domain controller as its DNS server
*before* anything else is configured — if a client cannot resolve the
domain controller's name, it cannot join the domain at all.

**Clients join the domain after DNS works.** "Joining the domain" means a
Windows client hands over local login control to the domain controller.
This step fails immediately if DNS is not already pointed at the domain
controller — so troubleshooting a failed domain join almost always starts
by checking DNS again.

**The Linux server joins last, if at all.** Depending on what you are
practicing, the Linux server may not need to join the domain at all — it
might just need network reachability from the clients. Decide what role it
plays before you configure it, not after.

Skipping this order is the single most common way a range build stalls out
for hours over what turns out to be a DNS setting.

---

## 5. Building It So You Can Rebuild It

A range you build once by hand and never document is a range you cannot
rebuild when it breaks — and it will break, because breaking it on purpose
is the entire point of a lab.

Use the same tools the hypervisor page covers, at the range level:

- **Templates.** Build one clean domain controller template and one clean
  client template. Clone new range instances from them instead of
  reinstalling every piece by hand.
- **Snapshots.** Take a snapshot of every VM in the range once it is fully
  built and working — domain joined, DNS resolving, services running. That
  snapshot is the range's known-good state. Roll back to it after a
  training session wrecks the range, instead of rebuilding from nothing.
- **Documentation.** Write down the build order from section 4 as an actual
  checklist — which VM gets configured first, second, third. A range with
  no written build order only exists in the head of whoever built it, and
  that does not scale to a club.

A range that takes one person a weekend to build, and thirty minutes to
rebuild from templates and snapshots, is a range the whole club can
actually use.

---

## 6. A Suggested Progression

Do not start with the full table from section 2. Build up to it.

1. **Two VMs.** One Linux target, one Linux attacker box, on an isolated
   network. Get comfortable with the networking and the isolation rules
   before adding Windows into the mix.
2. **Add a domain controller.** Now you have three VMs, and you get to
   learn the DNS-then-join dependency from section 4 firsthand, because it
   will trip you up at least once.
3. **Add clients.** Join one Windows client to the domain. Then a second,
   so you have lateral movement between two client machines to practice,
   not just client-to-server.
4. **Add the Linux server.** Now the range has a mixed Windows-and-Linux
   footprint, which is what most real small networks actually look like.

Each stage is a working range on its own. You do not need stage four to
learn something real from stage one.

---

> [!info] How the Club Uses This
> TBD. The club has not finalized what its actual range looks like, who
> builds and maintains it, or how members get access to it. This page
> explains the concepts so the eventual build makes sense the moment it
> exists. Specifics get added here once they are decided.
