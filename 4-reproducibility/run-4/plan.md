# Test plan

1. `POST /books` with valid data → 201
2. `POST /books` with missing fields → 400
3. `GET /books/{id}` → returns the book
4. `GET /books/{id}` with an unknown id → 404
5. `DELETE /books/{id}` → 204
