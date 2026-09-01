+++
title = "CLI & Scripting"
weight = 4
description = "Bash fundamentals and enough Python to automate real work from the terminal."
icon = "fa-solid fa-terminal"
+++

The terminal is where real work happens. Scripting is the difference between doing something once and automating it forever.

This section covers Bash fundamentals and enough Python to be dangerous.

---

## Three Skills, In Order

You do not need to be a programmer to be dangerous here. You need three
things, stacked in this order — each one makes the next one worth learning.

### Shell Fluency & Pipes

The **shell** is the program that reads what you type and runs it — Bash is
the shell almost every Linux system hands you by default. Fluency just means
you stop thinking about the syntax and start thinking about the task. The
one idea worth learning early is the **pipe** (`|`): it takes the output of
one command and feeds it straight in as the input to the next, no temporary
files, no copy-paste.

```bash
ls -la | grep ".txt"
```

`ls -la` lists files. `grep ".txt"` reads that list and keeps only lines
containing `.txt`. Neither command knows about the other — the shell wires
one's output into the other's input. Small tools, chained together, doing
something neither does alone. That is the whole philosophy of the command
line. Full reference: [Bash Fundamentals](bash/).

### Bash: Automate One Chore

A **script** is a list of commands saved in a file so you can run them
again without retyping them. That is all "automation" means at this
level — you are recording your own hands, not writing software. Pick one
thing you do more than once and put it in a file:

```bash
#!/bin/bash
for ip in 192.168.1.1 192.168.1.2 192.168.1.3; do
    ping -c 1 "$ip"
done
```

The first line tells the OS which program runs this file. The `for` loop
repeats the command once per address. Run `chmod +x script.sh` to make it
executable, then `./script.sh` runs the whole chore in one shot on your
lab VM. You do not learn Bash by reading about loops — you learn it by
automating one real, small, annoying chore. Conditionals and more
one-liners: [Bash Fundamentals](bash/).

### Python: Glue Tool Output

Bash is great at chaining whole programs together. It gets painful the
moment you need to actually parse something — pull one field out of JSON,
loop over structured data. That is where **Python** takes over. Think of it
as glue: most security tools already exist and already work, and Python's
job is rarely to reimplement them — it takes the output of one tool,
reshapes it, and feeds it into the next step. Read a wordlist file line by
line. Pull the open ports out of an `nmap` scan.

```python
with open("wordlist.txt", "r") as f:
    for line in f:
        word = line.strip()
        print(word)
```

Open the file, walk it one line at a time, strip the trailing newline off
each word. That pattern — open something, loop over it, do a small thing
per item — covers a surprising share of real scripting work. Full
reference: [Python for Security](python-scripting/).

---

Learn shell fluency first — you use it every session. Add Bash scripting
the first time retyping something gets annoying. Reach for Python the
first time Bash's text-munging starts fighting you.

---

{{< section-grid >}}
