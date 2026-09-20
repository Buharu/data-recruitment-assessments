# Data Engineering Brief

Box Box Analytics wants automated pipelines that transform incoming championship data
immediately after each race, feeding both their analysts and their video production team.

## Core requirements

Build a Python pipeline that reads the files in `source-data/` and produces the outputs
below in the `results/` folder.

### 1. Race statistics: `stats_{season}.json`

One file per season (for example `stats_2024.json`), containing a list ordered by round.
Each element describes one race:

```json
{
    "Race Name": "Silverpine Grand Prix",
    "Race Round": 1,
    "Race Datetime": "2024-03-10T13:00:00.000",
    "Race Winning driverId": 2,
    "Race Fastest Lap": "1:24.6"
}
```

- The winning driver is the one classified in position 1 for that race.
- "Race Fastest Lap" is the fastest lap recorded by any driver in that race, or null if
  none was recorded.
- If the race time is not available, use `00:00:00`.
- If a JSON value is always a number, represent it as a number rather than a string.

### 2. Driver standings: `standings_{season}.json`

One file per season, containing the final championship standings as a list ordered by
position. Each element:

```json
{
    "position": 1,
    "driverId": 1,
    "driverName": "Kasper Renn",
    "teamName": "Meridian Racing",
    "points": 389,
    "wins": 10
}
```

- Ties on points are resolved by number of wins, then number of second places, and so on
  down the finishing positions.
- `teamName` is the team the driver most recently drove for in that season.

### General requirements

- The solution must be built in Python inside the `solution/` folder, with a `main.py`
  that runs the full pipeline.
- Treat the source data as untrusted client data: investigate it before you rely on it,
  and make your handling decisions explicit in your README.
- Include a `README.md` in `solution/` documenting how to run the pipeline and the
  decisions you made.

## Stretch requirements

- Unit tests for all functions.
- A short data quality report: what you found in the source data and how your pipeline
  treats it.
- Notes on how you would deploy this pipeline to a cloud provider of your choice, and the
  considerations involved.

## Evaluation criteria

Code quality and readability; correctness and completeness of outputs; scalability of the
approach; testing; documentation.
