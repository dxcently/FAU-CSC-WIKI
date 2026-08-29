+++
title = "HTTP"
weight = 1
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

> [!info] How the Club Uses This
> TODO: Add how HTTP fundamentals apply to web CTF challenges and competition web application attacks the club has seen.

---

**References**

- [MDN HTTP docs](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- [HTTP/1.1 spec (RFC 7230)](https://www.rfc-editor.org/rfc/rfc7230)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
