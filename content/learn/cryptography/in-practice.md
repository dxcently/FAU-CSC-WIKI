+++
title = "Crypto in the Real World"
weight = 2
description = "How the primitives from the last page show up in HTTPS and encrypted messaging, and the specific mistakes that keep breaking them."
icon = "fa-solid fa-file-shield"
+++

---

The last page covered six primitives in isolation. Nothing in the real world
uses just one. A single HTTPS connection uses all six together, in a
specific order, for a specific reason. This page walks through that, then
covers where the whole system actually breaks — almost never the math, and
you should be able to explain exactly why by the end.

## Where This Shows Up

### TLS / HTTPS, End to End

**TLS** (Transport Layer Security) is the encryption behind HTTPS — the "S"
you see in a browser's address bar. When your browser connects to a site, it
runs a **handshake**: a short exchange of messages before any real data
moves, whose whole job is to set up two things.

**First, authenticate the server.** Your browser needs proof that it is
really talking to the site it asked for, not an attacker sitting in the
middle. This is what a **certificate** provides — a signed document, tied to
the site's public key, saying "this public key belongs to this domain." The
signature on that certificate comes from a **certificate authority (CA)**, an
organization your browser already trusts by default. If the signature checks
out, your browser trusts the site's public key.

**Second, agree on a session key.** Once the server is authenticated, both
sides run a key exchange to land on a shared secret, then use that secret as
a fast symmetric key for the rest of the connection. This is exactly the
asymmetric-to-symmetric handoff from the last page: slow public-key crypto
sets things up, fast symmetric crypto carries the actual traffic.

Once the handshake finishes, HTTPS gives you three things: the data is
unreadable to anyone watching the connection, tampering with it in transit
gets detected, and you have real assurance you are talking to the domain you
typed. HTTPS does **not** protect you from a malicious site itself, a
compromised endpoint, or a phishing page that has a perfectly valid
certificate for its own fake domain. The padlock icon means the connection
is private. It says nothing about whether the site on the other end is
trustworthy.

### End-to-End Encryption

**End-to-end encryption (E2EE)** is a stronger, specific property some
messaging apps advertise: only the two endpoints — sender and recipient —
can read the message content. Not an attacker on the network, and not even
the company running the server in the middle.

This works because the encryption and decryption keys live only on the
endpoints' devices. The server routes encrypted data it cannot read. Compare
this to a normal HTTPS connection to a web app: your traffic is encrypted in
transit to the company's server, but the server itself can read the content
once it arrives. E2EE removes that step — the server is a courier for a
sealed envelope, not someone with a key to open it.

Even with E2EE working correctly, the server usually still sees **metadata**
— data about the communication that is not the content itself: who
messaged whom, when, how often, and sometimes message size. Encrypting a
letter's contents does not hide the envelope, the return address, or the
mailbox it was dropped in. Metadata alone can reveal a lot. Do not assume
E2EE means a conversation leaves no trace anywhere.

### How Crypto Actually Fails

Cryptographic algorithms in wide use today have had decades of public
scrutiny from researchers trying to break them. Attacking the math directly
almost never works. Attacking how a system uses that math works constantly.
These are the patterns that keep showing up.

- **Reused keys or nonces.** A **nonce** is a number meant to be used only
  once per encryption operation — the name is short for "number used once."
  Several encryption modes lose their guarantees completely if the same key
  and nonce pair gets reused. This has broken real systems: reusing a
  supposedly one-time value quietly turns strong encryption into something
  an attacker can unravel.
- **Homemade crypto.** Someone decides to write their own cipher or their
  own protocol instead of using a reviewed standard. It looks fine in
  testing. It is almost never fine — real cryptographic algorithms survive
  because thousands of researchers spent years trying to break them and
  failed. A cipher one developer wrote last week has had none of that
  scrutiny. Never design your own algorithm for anything that matters. Use
  an established library instead.
- **Weak or default keys.** Hardware or software shipped with the same
  default password or key on every unit, never changed after setup. A key
  everyone has is not a secret. This single mistake has been behind entire
  classes of real-world breaches.
- **Expired or unvalidated certificates.** Software that skips checking a
  TLS certificate properly — or ignores that it expired — throws away the
  entire "authenticate the server" guarantee from the handshake above. The
  connection is still encrypted. It might just be encrypted straight to an
  attacker.
- **Secrets committed to source code.** An API key, password, or private
  key typed directly into a file and pushed to a repository. Source code
  gets copied, cached, and mirrored in places you do not control, forever.
  A secret in source code should be treated as a leaked secret the moment
  it is committed.

The pattern across all five: the cryptography did its job. A human decision
around it did not.

### Crypto in CTFs

Capture-the-flag competitions run a dedicated crypto category almost every
time, and it is one of the more approachable ones once you know what it is
actually testing. These challenges are not asking you to break real math.
They are testing whether you can recognize a primitive and spot exactly
where the challenge's implementation cut a corner, on purpose, for you to
find.

Common patterns you will run into on a CTF box or lab machine:

- A hash with no salt, or a fast hash used for passwords — crack it.
- A key or nonce reused across multiple encrypted messages.
- A weak or predictable random number generator, so a "random" key turns
  out to be guessable.
- A classic, deliberately weak cipher used somewhere it should not be, as a
  teaching exercise.
- A signature or certificate check the challenge skips or gets wrong.

Notice that every one of these is a version of the mistakes in the section
above. That is not a coincidence — CTF crypto challenges are built to teach
the exact failure modes that show up in real breaches. Practice this on CTF
platforms and lab machines you are meant to be attacking. Never point these
techniques at a system you do not own or have not been given explicit
permission to test.

---

Back to [The Building Blocks](basics/) if any of the terms above need a
second look. That page has the primitives; this page has the failures. Know
both, and "it's encrypted" stops being an answer you accept without a
follow-up question.
