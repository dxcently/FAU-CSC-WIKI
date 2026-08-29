+++
title = "HTTP"
weight = 1
description = "How HTTP requests and responses work, and why that matters for web security."
icon = "fa-solid fa-link"
+++

HTTP is the protocol browsers and servers use to communicate. Understanding it is non-negotiable for web security — every web vulnerability lives in an HTTP request or response.

---

## The Request-Response Model

Every HTTP interaction is a request from a client and a response from a server. Both have a structure.

**Request:**
```
GET /login HTTP/1.1
Host: example.com
Cookie: session=abc123
User-Agent: Mozilla/5.0
```

**Response:**
```
HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: session=xyz789

<html>...</html>
```

---

## HTTP Methods

| Method | What it does |
|---|---|
| `GET` | Retrieve a resource |
| `POST` | Submit data to the server |
| `PUT` | Replace a resource |
| `PATCH` | Partially update a resource |
| `DELETE` | Remove a resource |
| `HEAD` | GET but returns only headers |
| `OPTIONS` | Ask what methods are supported |

GET requests should never change state. POST, PUT, PATCH, DELETE should. When this rule is broken, bugs happen.

---

## Status Codes

| Code | Meaning |
|---|---|
| `200 OK` | Success |
| `201 Created` | Resource created |
| `301 / 302` | Redirect |
| `400 Bad Request` | Client sent garbage |
| `401 Unauthorized` | Not authenticated |
| `403 Forbidden` | Authenticated but no permission |
| `404 Not Found` | Resource does not exist |
| `500 Internal Server Error` | Server crashed |

The difference between `401` and `403` matters: `401` means "log in first," `403` means "you are logged in but not allowed." IDOR vulnerabilities often produce `403` but can be bypassed.

---

## Headers

Headers are key-value pairs that carry metadata.

**Common request headers:**

| Header | Purpose |
|---|---|
| `Host` | Which site you're requesting |
| `Cookie` | Session data |
| `Authorization` | Bearer tokens, Basic auth |
| `Content-Type` | Format of the request body |
| `User-Agent` | What client is making the request |
| `Referer` | Where the request came from |

**Common response headers:**

| Header | Purpose |
|---|---|
| `Set-Cookie` | Creates a cookie in the browser |
| `Content-Type` | Format of the response body |
| `Location` | URL to redirect to |
| `Content-Security-Policy` | Restricts where resources can be loaded from |
| `X-Frame-Options` | Prevents the page from being embedded in iframes |

---

## Cookies and Sessions

HTTP is stateless — each request has no memory of previous ones. Cookies solve this.

1. You log in. Server sends `Set-Cookie: session=TOKEN`.
2. Your browser stores the cookie.
3. Every request after that includes `Cookie: session=TOKEN`.
4. Server looks up the token and knows who you are.

**Cookie flags that matter for security:**

| Flag | What it does |
|---|---|
| `HttpOnly` | JavaScript cannot access the cookie. Prevents XSS cookie theft. |
| `Secure` | Cookie only sent over HTTPS. |
| `SameSite` | Controls cross-site cookie behavior. Mitigates CSRF. |

Missing any of these flags is a finding in a security review.

---

## HTTPS and TLS

HTTPS is HTTP inside a TLS (Transport Layer Security) tunnel. The data is encrypted in transit.

TLS does not mean the application is secure. It means your data cannot be read *between you and the server*. The server-side code can still be vulnerable to everything else.

---

## Inspecting HTTP Traffic

- **Browser DevTools** (F12) → Network tab — see every request/response
- **Burp Suite** — intercept and modify requests
- **curl** — make requests from the terminal
- **mitmproxy** — terminal-based intercepting proxy

---

## In CTF Environments

Web CTF challenges live and die on your ability to read and manipulate HTTP. Burp Suite is the tool — it sits between your browser and the target and lets you intercept, modify, and replay every request.

**Reading response headers for hints:**
```bash
# Server headers often reveal the tech stack
curl -I http://target.htb
# Look for: Server, X-Powered-By, Set-Cookie names, custom headers
# A header like X-Debug: true or X-Flag: ... is not unheard of
```

**Cookie manipulation — most common auth bypass pattern:**
```bash
# Get your cookie
curl -c cookies.txt -X POST http://target.htb/login \
    -d "user=guest&pass=guest"

# Inspect what you got
cat cookies.txt

# Replay with a modified cookie (change role=user to role=admin, etc.)
curl -b "session=MODIFIED_TOKEN" http://target.htb/admin
```

**Status code map for web challenges:**
- `403` on a path that exists → try method switching (`POST` instead of `GET`), different `Content-Type`, or removing auth headers entirely
- `302` redirect → follow it with `-L` in curl, or intercept the redirect response itself in Burp (the body often contains the flag)
- `500` → you triggered an error; push harder on the input that caused it

**Checking what methods a server accepts:**
```bash
curl -X OPTIONS http://target.htb/api/users -v
# Look for the Allow: header in the response
```

**Replaying and fuzzing requests with curl:**
```bash
# Test for IDOR — swap out a user ID
for id in {1..50}; do
    result=$(curl -s -b "session=TOKEN" http://target.htb/api/user/$id)
    echo "$id: $result" | grep -v "not found\|unauthorized" && echo "HIT: $id"
done
```

**CCDC / hackathon — hardening HTTP response headers:**

When you are on defense and own the web server, add these to your nginx or Apache config:
```
add_header X-Frame-Options "DENY";
add_header X-Content-Type-Options "nosniff";
add_header Content-Security-Policy "default-src 'self'";
add_header Strict-Transport-Security "max-age=31536000";
```

Missing these headers is a scored finding in CCDC-style competitions.

---

> [!info] How the Club Uses This
> HTTP knowledge shows up in every web CTF challenge and in CCDC when defending web services. The pattern is always the same: intercept the request, understand what the server expects, and manipulate it.

---

**References**

- [MDN HTTP docs](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- [HTTP/1.1 spec (RFC 7230)](https://www.rfc-editor.org/rfc/rfc7230)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
