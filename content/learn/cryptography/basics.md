+++
title = "The Building Blocks"
weight = 1
description = "The six cryptographic primitives explained by what problem each one solves, not by the math behind it."
icon = "fa-solid fa-key"
+++

---

Six ideas cover almost everything you will run into. Learn what each one
does, what it promises, and what it does not promise. That last part is where
most real mistakes happen.

## The Six Things You Actually Need

### Hashing

A **hash function** takes any input — a file, a password, a whole hard drive
— and produces a fixed-length string of characters. Change one character in
the input and the output looks completely different. Feed it the same input
twice, and you get the same output every time.

Think of it as a fingerprint machine. You cannot rebuild a person from their
fingerprint. You can only check whether two fingerprints match. That is the
whole point of a hash: it proves **integrity** — that a file was not changed
— not secrecy.

A hash is **one-way**. There is no key, and there is no way to reverse it
back to the original input. This is the detail people get wrong constantly:
**hashing is not encryption.** Encryption is meant to be undone by someone
holding the right key. A hash is never meant to be undone by anyone.

This is why password storage uses hashes. A site should never store your
actual password. It stores the hash of it. When you log in, the site hashes
what you typed and compares the two hashes. If the site gets breached, the
attacker gets a pile of hashes, not passwords.

But a plain hash is not enough on its own, for two reasons:

- **Fast hashes get brute-forced.** A general-purpose hash function is built
  to run fast. That is bad for password storage — an attacker with stolen
  hashes can try billions of guesses per second on modern hardware. Password
  storage instead uses **slow hashes**, built to take real time and memory
  per guess, so billions of guesses per second becomes thousands.
- **The same password produces the same hash.** Two users with the password
  `hunter2` end up with identical hashes. An attacker who cracks one instance
  of a common password cracks every account using it. The fix is a **salt**
  — a random value mixed into the hash before it runs, unique per user, so
  identical passwords produce different hashes.

One more term you will hear: a **collision** is two different inputs that
happen to produce the same hash. In plain words, this is like two different
people having the exact same fingerprint. A good hash function makes this
so unlikely you can treat it as impossible. Some older, deprecated hash
functions turned out not to be — researchers found ways to deliberately
construct collisions in them. That is exactly why they were deprecated, and
why modern systems use their replacements instead.

### Symmetric Encryption

**Symmetric encryption** uses one key to lock data and the same key to unlock
it. Both sides need a copy of that key before anything encrypted can be
shared. It is fast, and it is the right tool for encrypting large amounts of
data — a whole file, a video call, a network connection.

The catch is right there in the description: **both sides need the same key
first.** That is the **key distribution problem** — how do you get a secret
key to someone else without an eavesdropper on the line copying it too? If
you could send the key safely, you could probably send the data safely, and
you would not need encryption in the first place. Symmetric encryption alone
does not solve this. Something else has to.

### Asymmetric / Public-Key Encryption

**Asymmetric encryption**, also called **public-key encryption**, uses two
keys instead of one: a **public key** you hand out to anyone, and a
**private key** you never share with anyone. The two are mathematically
linked, but you cannot work out the private key from the public one.

The rule is simple: the public key encrypts, the private key decrypts.
Anyone can lock a message with your public key. Only you can unlock it,
because only you hold the private key. Flip it around and you get a
**signature**, covered next: the private key signs, and the public key
verifies that signature.

This solves the key distribution problem above — you can publish your public
key anywhere, openly, and nobody can do anything with it except send you
things only you can read. Nobody needs to sneak a shared secret past an
eavesdropper first.

The tradeoff is speed. Asymmetric encryption is far slower than symmetric
encryption and does not scale well to large amounts of data. In practice, it
is almost never used to encrypt the actual data. It is used once, at the
start of a connection, to safely hand over a fast, temporary symmetric key.
That handoff is exactly what a TLS handshake does — covered in the next
page.

### Digital Signatures

A **digital signature** proves two things at once: who sent a message, and
that nobody changed it after they sent it. It uses the same public/private
key pair as asymmetric encryption, but backward — the sender signs with
their private key, and anyone can check that signature with the sender's
public key.

Think of it as a wax seal that only one person owns the stamp for, pressed
into something that shows if it was tampered with afterward. Anyone can look
at the seal and confirm it is genuine. Nobody but the sender could have made
it. This is what proves a software update actually came from the vendor, and
not from someone who intercepted it on the way to your machine.

### Key Exchange

**Key exchange** is the answer to the key distribution problem from
symmetric encryption: how do two people agree on a shared secret while an
eavesdropper is watching every message they send?

You do not need the math to get the idea. Picture two people mixing their
own private ingredient into a shared public color of paint, sending the
mixed result to each other in the open, then each mixing in their private
ingredient a second time. Both end up at the same final color. An
eavesdropper who saw every public exchange still cannot work out either
private ingredient, and so cannot reproduce the final result. That final,
shared result becomes the symmetric key both sides use from then on.

The details matter for cryptographers. For you, the property is what
matters: two parties end a key exchange holding an identical secret, and
anyone who watched the whole exchange still does not have it.

### Randomness

Almost every primitive above leans on one hidden ingredient: a source of
**randomness** — keys, salts, and the private ingredients in a key exchange
all need to be unpredictable. If an attacker can guess or predict a value
that was supposed to be random, every guarantee built on top of it collapses.

A computer does not generate true randomness on its own — it is a
deterministic machine, following instructions exactly. A **cryptographically
secure random number generator (CSPRNG)** pulls unpredictability from things
like hardware noise and system timing, and produces output that no attacker
can predict even if they see previous outputs. A **predictable "random"**
generator does the opposite: it looks random, but an attacker who works out
the pattern, or the starting point, can predict every value it will ever
produce.

This has broken real systems. A key generated from predictable randomness is
not really a secret — it is a value an attacker can recompute. That single
weak link undoes encryption, signatures, and key exchange all at once, no
matter how strong the algorithm around it is.

---

Next: [Crypto in the Real World](in-practice/) — where all six of these
show up in an actual HTTPS connection, and the specific mistakes that keep
breaking systems built on top of them.
