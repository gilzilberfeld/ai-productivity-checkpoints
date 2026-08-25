# Test plan

## Happy path
1. Create a book, read it back, delete it — the whole lifecycle in one pass

## Contract
2. The POST response has exactly `id`, `title`, `author` — no more, no less
3. `id` is a non-empty string
4. GET returns the identical object that POST returned

## Validation
5. Bodies missing a required field are rejected — title only, author only, empty object, no body at all

## Not found
6. GET and DELETE on an unknown id → 404

## Data integrity
7. Two books created one after the other get different ids
8. Deleting one book leaves the other one alone
