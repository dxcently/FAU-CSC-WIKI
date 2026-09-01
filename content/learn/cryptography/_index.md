+++
title = "Cryptography"
weight = 8
description = "What cryptography actually guarantees, why it matters even if you never write your own, and where it shows up in CTFs and real breaches."
icon = "fa-solid fa-lock"
+++

---

Cryptography gets taught as math homework — long proofs, Greek letters,
modular arithmetic. Forget that. This section is not that. You do not need to
build a cipher. You need to know what each tool does, what it promises, and
what happens when someone uses it wrong. That last part is the one that gets
people fired.

Here is why you should care, even if you never implement a single algorithm
yourself.

**It is what makes the internet trustworthy.** Every time you log into a site
over HTTPS, cryptography is doing three jobs at once: proving the site is who
it says it is, keeping your password unreadable in transit, and catching
anyone who tries to tamper with the data. Without it, the internet is a room
where everyone can hear and edit everyone else's mail.

**It shows up in every CTF.** Capture-the-flag competitions run a
**cryptography (crypto)** category almost every time — a challenge track built
entirely around this stuff. You do not need to be a mathematician to solve
these. You need to recognize the primitive, know what it promises, and spot
where a real implementation cut a corner.

**Misusing it is one of the most common real-world vulnerabilities.** Broken
cryptography rarely means someone found a flaw in the math. The math is
usually fine — mathematicians have beaten on these algorithms for decades. It
fails because someone reused a key, rolled their own cipher, or hardcoded a
password in the source code. That is a mistake you can learn to spot, and
avoid, without ever touching a proof.

---

## What's In This Section

Two pages. Read them in order — the first gives you the vocabulary, the
second shows you where it is actually used and how it actually breaks.

### The Building Blocks

The primitives: hashing, symmetric encryption, asymmetric (public-key)
encryption, digital signatures, key exchange, and randomness. Each one
explained by the problem it solves, not by the equation behind it. Start
here: [The Building Blocks](basics/).

### Crypto in the Real World

Where those primitives actually show up: TLS (the "S" in HTTPS), end-to-end
encrypted messaging, and the CTF crypto category. Then the part that matters
most — how crypto fails in practice, and it is almost never the math.
Continue to: [Crypto in the Real World](in-practice/).

---

One honest warning before you start: this section will not make you able to
design a cryptographic algorithm. Nobody should be doing that outside of
academic research — that is exactly the mistake covered in the second page.
The goal here is smaller and more useful: read a system, know what protects
it, and know what to ask when someone tells you it is "encrypted."

---

{{< section-grid >}}
