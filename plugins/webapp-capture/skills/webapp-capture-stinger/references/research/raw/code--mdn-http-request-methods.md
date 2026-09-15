# HTTP request methods - HTTP | MDN

- URL: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): not shown on fetched content

## List of HTTP Request Methods

1. **GET** - The `GET` method requests a representation of the specified resource. Requests using `GET` should only retrieve data and should not contain a request content.
2. **HEAD** - The `HEAD` method asks for a response identical to a `GET` request, but without a response body.
3. **POST** - The `POST` method submits an entity to the specified resource, often causing a change in state or side effects on the server.
4. **PUT** - The `PUT` method replaces all current representations of the target resource with the request content.
5. **DELETE** - The `DELETE` method deletes the specified resource.
6. **CONNECT** - The `CONNECT` method establishes a tunnel to the server identified by the target resource.
7. **OPTIONS** - The `OPTIONS` method describes the communication options for the target resource.
8. **TRACE** - The `TRACE` method performs a message loop-back test along the path to the target resource.
9. **PATCH** - The `PATCH` method applies partial modifications to a resource.

## Safe, Idempotent, and Cacheable Methods

### Definitions

- **Safe**: A request method is safe if it only retrieves data and does not modify server state.
- **Idempotent**: A method is idempotent if making the same request multiple times produces the same result as making it once.
- **Cacheable**: The response can be stored and reused for subsequent identical requests.

### Methods Classification Table

| Method | Safe | Idempotent | Cacheable |
|--------|------|-----------|-----------|
| GET | Yes | Yes | Yes |
| HEAD | Yes | Yes | Yes |
| OPTIONS | Yes | Yes | No |
| TRACE | Yes | Yes | No |
| PUT | No | Yes | No |
| DELETE | No | Yes | No |
| POST | No | No | Conditional* |
| PATCH | No | No | Conditional* |
| CONNECT | No | No | No |

*`POST` and `PATCH` are cacheable when responses explicitly include freshness information and a matching `Content-Location` header.

## Relevance to capture-tool safety

This table is the grounding reference for a capture tool's safety rule: only `GET`/`HEAD`-style navigation and read-only interactions (clicking links/tabs, scrolling) are guaranteed not to change server state. A capture tool should never submit forms or trigger actions that issue `POST`, `PUT`, `DELETE`, or `PATCH` requests, since those methods are neither safe nor guaranteed idempotent.
