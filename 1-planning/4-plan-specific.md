# Test plan 

## Workflows
1. Create → GET returns it → DELETE → GET returns 404. One book, full lifecycle.
2. Create a book, post 3 reviews to it, delete the book → `GET /books/{id}/reviews` now returns 404
3. After that delete, `GET /reviews` contains none of those 3 reviews — `store.delete_book` pops the review list, so this is a real assertion
4. Create books A and B, delete A → B and B's reviews are untouched
5. Delete a book, then create another → the new book gets a fresh id, never the deleted one's
6. Create → delete → create again with the same title and author → two distinct ids, the first is still gone

## Security
7. `POST /books` with no `Authorization` header → succeeds. Reviews require a token. Books do not.
8. `POST /books` with an unrecognised token → same result as with no token: it still works
9. `DELETE /books/{id}` with no token → anyone at all can delete any book
10. User-2 deletes a book User-1 created and destroys User-1's reviews as collateral — no 401, no 403
11. Compare with reviews: PUT and DELETE there enforce ownership with 403. Books enforce nothing. Decide whether that gap is a bug or a decision, and write the test for the answer.

## Concurrency
12. 10 threads `POST /books` simultaneously → all 10 return 201
13. All 10 returned ids are distinct — the counter bump and the dict insert must be atomic *together*
14. GET all 10 ids → each holds its own title and author, no cross-request mixing
15. 10 threads DELETE the same book at once → exactly one 204, exactly nine 404s
16. Concurrent DELETE and GET on one book → GET returns the whole book or 404, never a partial body
17. Concurrent create and delete → `_books` and `_reviews` never drift out of sync
18. Repeat 12–14 one hundred times — a race that shows up once in fifty runs is still a bug

## Single-call basics
19. Valid POST → 201 with id/title/author; missing title or author → 400; no body → 400
20. `GET /books/{id}` → 200 and matching; unknown id → 404
21. `DELETE /books/{id}` → 204 empty body; unknown id → 404; same book twice → second is 404
22. Unicode and very long title/author → stored and returned unchanged, never a 500
