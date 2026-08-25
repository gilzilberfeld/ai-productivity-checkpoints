# Test plan

## Book creation
1. Valid data → 201 and the book comes back
2. Unicode in title and author → stored and returned unchanged
3. Very long title → handled, never a 500
4. Missing fields → 400

## Book retrieval
5. Existing book → 200 with matching data
6. Nonexistent book → 404 with an error message

## Book deletion
7. Existing book → the delete succeeds
8. Nonexistent book → 404

## Workflow
9. Create → get → delete → get, in sequence
