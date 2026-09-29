# Test Plan

| ID | Scenario | Input | Expected Result | Pass/Fail |
|---|---|---|---|---|
| T01 | New registration | New email | 201 and user created | |
| T02 | Existing email | Same email twice | 409 | |
| T03 | Valid login | Correct credentials | JWT returned | |
| T04 | Invalid login | Wrong password | 401 | |
| T05 | Unauthorized dashboard/API | No token | 401 | |
| T06 | Profile creation | Valid profile | 200 | |
| T07 | Plan generation | Vegetarian profile | Plan returned | |
| T08 | Vegan preference | Vegan profile | Vegan meal examples | |
| T09 | Different goal | Fitness-oriented demo | General summary reflects goal | |
| T10 | AI API failure | Invalid/unavailable API | Local fallback used | |
| T11 | Save plan | Valid generated plan | 201 | |
| T12 | Retrieve plan | Existing plan | 200 | |
| T13 | Upload file | Allowed file | 201 | |
| T14 | Retrieve files | Authenticated user | Own files only | |
| T15 | Invalid file | Unsupported extension | 400 | |
| T16 | User isolation | User A requests User B resource | Not accessible | |
| T17 | Logout | Remove token client-side | Protected calls fail without token | |
| T18 | Database failure | Simulated unavailable DB | Error handled/logged | |

For screenshots, capture actual results and fill in Actual Result + Pass/Fail after execution.
