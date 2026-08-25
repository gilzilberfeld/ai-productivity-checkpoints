# Test plan 

## Create — `POST /books`
1. Valid title and author → 201, body has `id`, `title`, `author`
2. Returned `id` is a non-empty string
3. Returned `title` and `author` match what was sent
4. Missing `title` → 400 with an `error` field
5. Missing `author` → 400
6. Empty JSON object → 400
7. No body at all → 400
8. Two books created one after the other get different ids

## Get — `GET /books/{id}`
9. Existing book → 200, body identical to what create returned
10. Unknown id → 404 with an `error` field
11. Same book fetched twice → identical body both times

## Delete — `DELETE /books/{id}`
12. Existing book → 204 with an empty body
13. GET after the delete → 404
14. Unknown id → 404
15. Deleting the same book twice → the second call returns 404

## Input edge cases
16. Very long `title` and `author` strings → handled, never a 500
17. Unicode in `title` and `author` → stored and returned unchanged
18. Extra unexpected fields in the body → ignored, never a 500
19. Non-string `title` (number, null, list) → handled, never a 500
