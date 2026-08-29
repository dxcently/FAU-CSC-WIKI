+++
title = "Cheat Sheets"
weight = 3
description = "Quick reference for the commands, ports, and triage steps club members look up constantly."
icon = "fa-solid fa-file-lines"
+++

This page is not for learning. It is for the moment mid-CTF or mid-lab when
you know the concept and just need the exact command. Bookmark it.

## Linux Commands by Task

### Finding Things

| Task | Command |
| --- | --- |
| Find a file by name | `find / -name "filename" 2>/dev/null` |
| Find SUID binaries | `find / -perm -4000 2>/dev/null` |
| Search file contents for a string | `grep -r "search term" /path` |
| Find recently modified files | `find / -mmin -60 2>/dev/null` |
| List all listening ports | `ss -tulnp` |
| Show running processes | `ps aux` |

### Users & Permissions

| Task | Command |
| --- | --- |
| Show your current user and groups | `id` |
| Show what you can run as root | `sudo -l` |
| Switch to another user | `su - username` |
| Change file owner | `chown user:group file` |
| Change file permissions | `chmod 750 file` |
| Add a user | `useradd username` |

### Networking

| Task | Command |
| --- | --- |
| Show IP addresses on this machine | `ip a` |
| Show the routing table | `ip route` |
| Test connectivity to a host | `ping -c 4 target` |
| Fetch a URL from the terminal | `curl -s URL` |
| Start a simple file server | `python3 -m http.server 8000` |
| Copy a file over SSH | `scp file user@host:/path` |
| Set up a listener for a reverse shell | `nc -lvnp 4444` |

### Compression & Transfer

| Task | Command |
| --- | --- |
| Extract a `.tar.gz` | `tar -xzvf file.tar.gz` |
| Create a `.tar.gz` | `tar -czvf out.tar.gz folder/` |
| Extract a `.zip` | `unzip file.zip` |

## Permission Notation

Linux permissions show as three groups of three: **owner, group, other**.
Each group is **read (r), write (w), execute (x)** — or `-` if absent.

```
-rwxr-xr--
 │└┬┘└┬┘└┬┘
 │ │  │  └── other: r-- (read only)
 │ │  └───── group: r-x (read + execute)
 │ └──────── owner: rwx (read + write + execute)
 └────────── file type (- = file, d = directory, l = symlink)
```

Numeric mode is the same thing added up: r=4, w=2, x=1 per group.

| Numeric | Meaning |
| --- | --- |
| `755` | owner: rwx, group: r-x, other: r-x — typical for a script |
| `644` | owner: rw-, group: r--, other: r-- — typical for a regular file |
| `700` | owner: rwx, group/other: none — private to the owner |
| `4755` | same as 755, plus the SUID bit — runs as the file's owner, not the caller |

The leading `4` in `4755` is the SUID bit. If a binary has it set and is
owned by root, it runs with root privileges no matter who calls it. That's
why `find / -perm -4000` is one of the first things you run on a new box.

## Common Ports

| Port | Protocol | What it usually means on a box |
| --- | --- | --- |
| 21 | FTP | File transfer, often allows anonymous login — always try it |
| 22 | SSH | Remote login. Check the version for known vulnerabilities |
| 23 | Telnet | Unencrypted remote login. Rare now; a red flag when present |
| 25 | SMTP | Mail server |
| 53 | DNS | Name resolution. Zone transfers (`AXFR`) sometimes leak hostnames |
| 80 | HTTP | Web, plain text. Always check the source and `robots.txt` |
| 88 | Kerberos | Authentication in Active Directory environments |
| 110 | POP3 | Mail retrieval |
| 139/445 | SMB | Windows file sharing. Check for null sessions and open shares |
| 143 | IMAP | Mail retrieval |
| 443 | HTTPS | Web, encrypted |
| 389/636 | LDAP / LDAPS | Directory services, common in AD environments |
| 3306 | MySQL | Database. Try default and weak credentials |
| 3389 | RDP | Windows remote desktop |
| 5432 | PostgreSQL | Database |
| 5985/5986 | WinRM | Windows remote management |
| 8080 | HTTP (alt) | A second web service, often an admin panel or dev server |

## PowerShell Cmdlets

For when the box is Windows and `cmd.exe` isn't enough.

| Task | Cmdlet |
| --- | --- |
| List files in a directory | `Get-ChildItem` (alias `ls`, `dir`) |
| Read a file | `Get-Content file.txt` (alias `cat`) |
| Search file contents | `Select-String "term" file.txt` |
| List running processes | `Get-Process` |
| List local users | `Get-LocalUser` |
| List local groups | `Get-LocalGroup` |
| Show current user's group membership | `whoami /groups` |
| List services | `Get-Service` |
| Download a file from the internet | `Invoke-WebRequest -Uri URL -OutFile file` |
| Run a command as another user | `Start-Process -Credential (Get-Credential) cmd` |
| Show installed software | `Get-WmiObject -Class Win32_Product` |
| Check execution policy | `Get-ExecutionPolicy` |
| View PowerShell command history | `Get-History` |

## Where Do I Even Start? — CTF Triage

Stuck looking at a challenge with no idea what to try first? Work through
this list in order.

1. **Read the challenge name and description again.** CTF authors leave
   hints there on purpose. A pun in the title is usually a real clue.
2. **Identify the file type.** Run `file <filename>` before anything else.
   Do not assume the extension is honest.
3. **For a binary:** run `checksec` on it. Note if it's 32 or 64-bit, and
   which protections (NX, PIE, canary) are on. That decides your exploit
   class.
4. **For a web challenge:** view the page source. Check `robots.txt`. Open
   the browser's network tab and watch what requests actually happen.
5. **For an unknown file:** run `strings` on it and skim the output. Look
   for URLs, flags, function names, or a format signature.
6. **For anything that looks encoded:** try CyberChef's "Magic" wand first.
   It guesses the encoding chain faster than you can by hand.
7. **For a network capture (`.pcap`):** open it in Wireshark, sort by
   protocol, and follow any suspicious TCP or HTTP stream.
8. **Still stuck?** Google the exact challenge category plus one distinct
   detail from the description — someone has hit this pattern before you.
9. **Really stuck?** Step away for ten minutes. Half of CTF is noticing the
   thing you walked past three times.

Full reference on tools per category: [Links](/toolbox/links/).
