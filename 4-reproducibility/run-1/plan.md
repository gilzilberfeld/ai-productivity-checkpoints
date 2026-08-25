# Test plan

## POST /books
1. Valid title and author → 201, response has `id`, `title`, `author`
2. Response `title` and `author` match the request
3. Missing `title` → 400
4. Missing `author` → 400
5. Empty body → 400

## GET /books/{id}
6. Existing book → 200, body matches what was created
7. Unknown id → 404

## DELETE /books/{id}
8. Existing book → 204
9. The book is gone afterwards — GET returns 404
10. Unknown id → 404
