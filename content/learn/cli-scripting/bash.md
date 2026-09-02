+++
title = "Bash Fundamentals"
weight = 1
description = "The Bash basics needed to automate tasks and chain tools together on the command line."
icon = "fa-solid fa-terminal"
+++

Bash is the default shell on most Linux systems. You use it every time you open a terminal. Knowing the basics means you can automate repetitive tasks and chain tools together.

---

## Variables

```bash
name="alice"
echo $name           # print: alice
echo "Hello $name"   # print: Hello alice

result=$(whoami)     # capture command output
echo $result
```

Use `$()` to capture command output into a variable. This is called command substitution.

---

## Pipes and Redirection

Pipes connect commands. Redirection sends output to files.

```bash
ls -la | grep ".txt"          # pipe ls into grep to filter
cat file.txt | sort | uniq    # sort and deduplicate

command > output.txt          # write stdout to file (overwrite)
command >> output.txt         # append stdout to file
command 2> errors.txt         # write stderr to file
command 2>/dev/null           # throw away errors
```

Piping is how you build data pipelines from small tools. `grep`, `sort`, `cut`, `awk`, and `sed` are all designed to be combined this way.

---

## Conditionals

```bash
if [ condition ]; then
    # do something
elif [ other_condition ]; then
    # do something else
else
    # fallback
fi

# Common conditions
[ -f file.txt ]        # file exists
[ -d /tmp ]            # directory exists
[ $x -eq 5 ]           # equals
[ $x -gt 5 ]           # greater than
[ -z "$var" ]          # variable is empty
```

---

## Loops

```bash
# For loop over a list
for ip in 192.168.1.1 192.168.1.2 192.168.1.3; do
    ping -c 1 $ip
done

# For loop over a range
for i in {1..10}; do
    echo $i
done

# While loop
while [ condition ]; do
    # do something
done
```

---

## Useful One-Liners

```bash
# Search for a string across all files in a directory
grep -r "password" /var/www/

# Find files modified in the last 24 hours
find / -mtime -1 2>/dev/null

# Extract IPs from a log file
grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' logfile.txt

# Count occurrences of each unique line
sort file.txt | uniq -c | sort -rn

# Watch a file grow in real time
tail -f /var/log/auth.log
```

---

## Writing a Script

```bash
#!/bin/bash
# This line tells the OS to use bash to run this script

echo "Starting script..."

for target in "$@"; do      # $@ = all arguments passed to script
    echo "Scanning $target"
    ping -c 1 "$target" > /dev/null && echo "$target is up"
done
```

Save it, then make it executable:

```bash
chmod +x script.sh
./script.sh 192.168.1.1 192.168.1.2
```

---

## Scripts That Fail Loudly

A script that keeps going after an error does damage quietly. Make it stop.

```bash
#!/bin/bash
set -euo pipefail
# -e           exit on the first failed command
# -u           treat an unset variable as an error, not as empty text
# -o pipefail  a pipeline fails if any stage fails, not only the last one
```

Quote every variable. An unquoted variable splits on spaces and expands wildcards like `*`. This is the most common bash bug there is.

```bash
file="my notes.txt"
cat $file      # runs: cat my notes.txt   -> two files, both missing
cat "$file"    # runs: cat "my notes.txt" -> correct
```

Every command returns an exit code. Zero is success. Anything else is failure. Chain on it.

```bash
grep -q "root" /etc/passwd && echo "found" || echo "missing"
some_command; echo "exit code was $?"
```

Run [shellcheck](https://www.shellcheck.net/) on every script before you trust it. It catches quoting mistakes, unset variables, and wrong test syntax that bash itself never warns you about.

```bash
shellcheck script.sh
```

---

## The Text Toolkit

Most CTF work is text processing. Learn these five and you stop writing Python for jobs a one-liner does.

```bash
cut -d':' -f1 /etc/passwd             # column 1, split on ':'
awk -F: '{print $1, $7}' /etc/passwd  # columns 1 and 7
sed 's/old/new/g' file.txt            # replace every 'old' with 'new'
sort -u file.txt                      # sort and drop duplicates
tr 'a-z' 'A-Z' < file.txt             # translate characters

# combined: the top talkers in a web log
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head
```

Two glue tools you will use every day:

```bash
find / -name "*.conf" 2>/dev/null | xargs grep -l "password"   # run a command on every result
nmap -sV 10.10.10.5 | tee scan.txt                              # see the output AND save it
```

The [GNU coreutils manual](https://www.gnu.org/software/coreutils/manual/) is the reference for all of these.

---

## Shell Reflexes

These are not script commands. They are habits that save minutes every hour.

```bash
# Ctrl-R            search your history backwards as you type
history | grep nmap   # find that command you ran an hour ago
sudo !!               # rerun the last command as root
cd -                  # jump back to the previous directory
```

Your history is saved to `~/.bash_history`. On a CTF box, it is the first place to look for credentials that were typed into commands.

---

## In CTF Environments

Bash is the glue that holds CTF tooling together. You rarely use one tool in isolation — you pipe output between them.

**Extracting a flag from tool output:**
```bash
# nmap scan, pull out open ports only
nmap -p- 10.10.10.5 | grep "open" | cut -d'/' -f1

# grab all URLs from a page source
curl -s http://target.htb | grep -oP 'href="\K[^"]+'

# extract flag-shaped strings from a binary
strings challenge | grep -E 'flag\{[^}]+\}'

# decode base64 output from a service
echo "aGVsbG8gd29ybGQ=" | base64 -d
```

**Automating a brute force loop:**
```bash
# try passwords from a wordlist against a login endpoint
while IFS= read -r pass; do
    result=$(curl -s -X POST http://target.htb/login \
        -d "user=admin&pass=$pass")
    if echo "$result" | grep -q "Welcome"; then
        echo "Found: $pass"
        break
    fi
done < /usr/share/wordlists/rockyou.txt
```

**Port knocking / sequential connection script:**
```bash
for port in 1234 5678 9012; do
    nmap -Pn --host-timeout 100 --max-retries 0 -p $port target.htb
done
```

**Processing nmap XML output:**
```bash
nmap -oX scan.xml target.htb
# extract just the open port numbers
grep 'state="open"' scan.xml | grep -oP 'portid="\K[0-9]+'
```

---

## Using AI

AI is genuinely useful for Bash — not because it writes your scripts for you, but because it accelerates the parts that are slow.

**Where it helps:**

- **Explaining unfamiliar commands:** Paste a one-liner you found in a writeup. Ask what each part does. Faster than reading five man pages.
- **Generating boilerplate:** "Write a bash script that takes a wordlist and tries each word as a password against this curl command." Use it as a starting point, not a final answer.
- **Debugging:** Paste the script and the error. AI is good at spotting quoting issues, off-by-one errors, and wrong flags.
- **Regex help:** `grep -oP` regex is finicky. Describe what you want to extract and let AI draft the pattern.
- **Converting tool output:** "I have nmap output in this format. Write a bash one-liner to extract just the open ports." This is mechanical work — offload it.

**Where it fails:**

- It will confidently produce scripts that do not work. Always test.
- It does not know your specific target's behavior. The logic has to come from you.
- Complex pipelines with process substitution and edge cases need manual review.

Treat AI output as a draft. Read it, understand it, then run it.

---

> [!info] How the Club Uses This
> TODO: Add examples of scripts the club has written for CTF automation, competition tooling, or demo exercises.

---

**References**

- [Bash scripting guide](https://tldp.org/LDP/abs/html/)
- [shellcheck.net](https://www.shellcheck.net/) — paste your script and get linting feedback
- [explainshell.com](https://explainshell.com/) — explains any shell command
- [Bash cheat sheet](https://devhints.io/bash)
