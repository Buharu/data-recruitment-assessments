# Motorsport Analytics Assignment

## Background

Box Box Analytics is a fast-growing YouTube channel covering the Formula Apex championship.
The channel has grown quickly over the last three seasons and wants to put data at the centre
of its content planning. They have engaged our consultancy to help them understand their
performance data and build the foundations of an automated analytics capability.

You have been given three seasons (2023 to 2025) of championship data alongside the channel's
own video statistics.

## Your stakeholders

- **The founder** runs the channel and decides what content gets made. Opinionated,
  time-poor, and very attached to his favourite drivers.
- **The head of production** owns the publishing workflow and schedule.
- **The commercial lead** is preparing sponsorship pitches for the 2026 season.

## Choose your brief

- Data Engineer candidates: [brief-data-engineering.md](brief-data-engineering.md)
- Data Analyst candidates: [brief-data-analytics.md](brief-data-analytics.md)

Both briefs use the same source data and follow the same convention: **Core requirements**
are the substance of the assessment and must be completed; **Stretch requirements** are
optional extensions to attempt once Core is solid. See
[Working on the assignment](#working-on-the-assignment) below for setup and submission.

## The data

All files are in `source-data/`. The data is provided as received from the client and may
contain imperfections; handling them sensibly is part of the assignment.

| File | One row per | Columns |
|---|---|---|
| races.csv | championship race | raceId, season, round, raceName, circuit, country, date, time |
| teams.csv | team | teamId, teamName, engineSupplier |
| drivers.csv | driver | driverId, code, forename, surname, nationality, dateOfBirth |
| results.csv | driver's race classification | resultId, raceId, driverId, teamId, grid, position, points, status, fastestLapTime, gapToWinnerSeconds |
| qualifying.csv | driver's qualifying result | raceId, driverId, qPosition, qBestTime |
| videos.csv | published video | videoId, raceId, focusDriverId, category, title, publishDatetime, durationSeconds, views, likes, comments, avgViewPct |

Notes:

- All dates and times are UTC. Race `date` and `time` are the scheduled race start.
- `results.position` is empty when a driver did not finish; `status` explains why.
- `videos.raceId` links a video to a race where relevant; off-season content has no race link.
- `videos.focusDriverId` is set when a video is about one driver.
- Points are awarded 25-18-15-12-10-8-6-4-2-1 for the top ten finishers.

## Working on the assignment

Clone this repository and work locally, using whatever tools your brief calls for.
Put your deliverables where your brief specifies: final outputs and the deck in
`results/`, your workings and documentation in `solution/`.

## Submitting

Send your completed work back to the person who sent you this assignment: ideally this would
be a link to your copy of the repository hosted in a source control system of your choice, containing
your workings and your results. If you submit via files attached to an email, these will likely be blocked by 
email security - If you submit this way, please follow up with a second, plaintext email to prompt a check for any blocked emails.

Please submit this 24 hours before any follow up meetings to allow time to review. If you have any problems with this assignment or submission, please reach out via email. 

Please do not fork this repository or open pull requests against it — submissions
would be publicly visible to other candidates.
