# What differed

Same prompt, four times. `1-planning/1-prompt-simple.md`, unchanged.

| | shape | tests | against the working server |
|---|---|---|---|
| run-1 | plain functions | 11 | 11 passed |
| run-2 | fixture + two `parametrize`s | 8 → 12 cases | 12 passed |
| run-3 | four test classes | 9 | 9 passed |
| run-4 | plain functions | 5 | 5 passed |

Four different suites. All green.

## Coverage that came and went

| | run-1 | run-2 | run-3 | run-4 |
|---|:-:|:-:|:-:|:-:|
| asserts 201 on a successful create | ✓ | — | ✓ | ✓ |
| compares a returned value to the value sent | ✓ | — | ✓ | — |
| response has exactly `id`, `title`, `author` | — | ✓ | — | — |
| missing *author* → 400 | ✓ | ✓ | — | — |
| no body at all → 400 | — | ✓ | — | — |
| DELETE returns 204 exactly | ✓ | — | — | ✓ |
| the book is actually gone afterwards | ✓ | ✓ | ✓ | — |
| DELETE on an unknown id → 404 | ✓ | ✓ | ✓ | — |
| ids are unique | — | ✓ | — | — |
| deleting one book spares the other | — | ✓ | — | — |
| unicode / very long input | — | — | ✓ | — |

run-3 hedged its delete assertion to `status_code in (200, 204)`. No other run did.

## Row two is the one to look at

run-2 is the most sophisticated suite here — fixtures, cleanup, parametrized cases, the only run that checks exact field sets and unique ids.

It never compares a value it got back to the value it sent. It asserts that the GET matches the POST. If the server returned the wrong thing, it would return the same wrong thing to both, and this suite would stay green.

run-4 doesn't compare either. It asserts `"title" in response.json()`.

