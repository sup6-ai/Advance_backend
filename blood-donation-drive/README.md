
## Problem statement
PROBLEM STATEMENT : NSS needs simple way to run blood donation drive without paper registration . In app students are able to register as donors and book the slot and cancel with roll no , weight and blood group . Day of donating they should record each appointment as donated . They want to see how many litres of blood collected for each group. Call the particular blood group donors who have ability to donate .

rules for drive -> donor must wait 90 days of donation, 1 donor can book 1 slot they cant book more than 10 people per slot reject the invalid input (unknown blood group , underweight , past dates , double roll no )with clear error message .

We have to build backend with 9 endpoints , frontend and it should show API's error message.


## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Supriya |E1,E2 |Yes  | E3 | No |
| Day 1 | Naidile |E1  | Yes |E2  |No  |
| Day 1 | Amruta | create database and table and seed_data | yes  | Endpoints | no |

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 2 | Supriya | testing endpoints and app.jsx| yes |Donor component  | no |
| Day 2 | Naidile | endpoints | yes | forntend | yes |
| Day 2 | Amruta |Endpoints and app.jsx | yes | frontend componet | no |

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 3 | Supriya | frontend donate debugging| no |  | yes |
| Day 3 | Naidile | forntend blood bank debugging | no |  | yes |
| Day 3 | Amruta |testing the backend as the whole | no | frontend debugging as whole | yes|

| # | What it does | Method + path | Success code | Error code | Status |
|---|---|---|---|---|---|
| E1 | Get all donors, can be filtered by blood group | GET /donors | 200  | 400  |  |
| E2 | Get one donor by roll number, with appointments | GET /donors/{roll_no} | 200  | 404  |  |
| E3 | Register a donor: roll no, name, BG and weight | POST /donors | 201  | 400  |  |
| E4 | Book appointment: roll no, drive date,slot  | POST /appointments | 201 | 404  |  |
| E5 | Cancel appointment | PATCH /appointments/id/cancel | 200  | 404 |  |
| E6 | Mark appointment donated or no_show | PATCH /appointments/{id}/status | 200 | 400 |  |
| E7 | Appointments for a date, morning first | GET /appointments | 200 | 400  |  |
| E8 | Units collected per blood group | GET /stats | 200  | |  |
| E9 | Donors of a blood group who can donate now | GET /donors/eligible| 200 | 400 |  |

### Rules checklist (section 4 of the PRD)

| Rule | Expected status | Tested in /docs |
|---|---|---|
| Roll number already registered | 400 | yes |
| Booking less than 90 days after last donation | 400 | yes |
| Donor already has a booked appointment | 400 | yes |
| Slot already has 10 booked donors | 400 | no |
| Cancelling an appointment that is not booked | 400 | yes|
| Marking an appointment that is not booked, or before its date | 400 | yes|
| Roll number or appointment id doesn't exist | 404 | yes|
| Missing or empty field, invalid blood group, invalid slot | 422 | no|
| Weight under 50 kg or over 200 kg | 422 | yes |
| Date not YYYY-MM-DD, or drive date in the past | 422 | yes |

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Uses | Shows the data | Buttons work | Shows API errors | Who |
|---|---|---|---|---|---|
| Donate (register form, Show, Book, Cancel) | E2, E3, E4, E5 | yes| partialy |  | supriya |
| Drive desk (date picker, Donated / No-show) | E6, E7 | yes | partialy|  | amruta |
| Blood bank (units per group, donors, Who can donate?) | E1, E8, E9 | yes | partialy |  | naidile |

## 4. Done when

- [ ] All 9 endpoints work in `/docs`.
- [ ] Each rule in section 4 gives the right status code.
- [ ] Marking an appointment donated updates units collected and removes the donor from "Who can donate?", without a refresh.
- [ ] Booking too soon after a donation shows the API's message on the page.
- [ ] The data is still there after restarting the API.

**Bonus (optional):** seats left per slot · "Rare group" label for negative blood groups · pytest tests for the rules.

## 5. Blockers and help needed

- 

## 6. How to run our app

Fill this in by the end of Day 2. Someone who has never seen your code should be able to follow it.

**Backend**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

## 7. Proof of work

Save a screenshot of `/docs` or your app as `screenshot.png` in this branch. It shows here:

