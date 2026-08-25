Write a test plan for the book endpoints of this API - create a book, get a book, delete a book. The code is in `server/routes_books.py`, the storage layer is in `server/store.py`, and auth is in `server/auth.py`.

Cover these three things explicitly:

**Workflows** — not just single calls. Create a book, read it back, delete it, read it again. Create a book, add reviews to it, then delete the book and check what happened to the reviews.

**Security** — who is allowed to create, read and delete a book? Compare that against how the review endpoints handle auth and ownership.

**Concurrency** — the store is an in-memory dict guarded by a `threading.Lock`, book IDs come from an integer counter, and Flask runs in threaded mode. Several clients creating or deleting books at the same moment.
