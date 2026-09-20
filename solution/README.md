# Project Structure

The codebase is modularized to separate data ingestion, cleaning, business logic, and visual output:

* **`main.py`**: The main orchestrator. It executes the data pipeline, calculates key derived metrics (such as `engagement_rate` and `total_watch_time_hours`), merges the datasets into a central `df_fact_table`, and triggers the charting functions.
* **`read_file.py`**: Contains helper functions like `read_all_files()` and `read_file()` to dynamically load all `.csv` files from a given directory into a dictionary of Pandas DataFrames.
* **`clenner.py`**: Houses the ETL and data validation functions for each raw dataset (e.g., `convert_drivers_data()`, `convert_videos_data()`, `convert_results_data()`). It handles type coercion, null value filling, and datetime parsing.
* **`questions.py`**: Contains the analytical functions (`q1_growth_watch_time()`, `q2_champion_vs_others()`, `q3_channel_yoy_growth()`) to answer the three core stakeholder questions directly, outputting standard matplotlib charts.
* **`insights.py`**: Produces refined, executive-style charts with integrated data storytelling (custom annotations, strategic coloring) via functions like `i1_growth_engine()`, `i2_champion_myth()`, and `i3_offseason_loyalty()` designed specifically for the stakeholder deck.
* **`explore_data.py`**: Ad-hoc EDA script used initially to understand data structures, unique values, and check for duplicates across the raw DataFrames (e.g., `df_drivers`, `df_races`, `df_videos`).

---

## Handling Data Quirks & Imperfections

During the ETL phase, several imperfections in the source data were identified and resolved to ensure accurate metrics:

* **Orphaned Off-Season Content:** Off-season videos are not tied to specific races, resulting in null values for their `season` mapping. 
  * *Resolution:* The script dynamically extracts the year from the `publishDatetime` variable and backfills the missing season column using `df_fact_table["season"].fillna(df_fact_table["publishDatetime"].dt.year)`.
* **Missing Driver IDs in Generic Content:** Videos focusing on general topics (like `tech-analysis` or `race-recap`) naturally lacked a `focusDriverId`. 
  * *Resolution:* Filled missing `focusDriverId` values with `-1` during the cleaning phase inside `convert_videos_data()`. This allowed these videos to be safely excluded from the "Champion vs. Others" driver analysis while retaining them for overall channel growth metrics.
* **Data Type Coercion & Null Handling:** Several numeric columns (like `durationSeconds`, `views`, `likes`, `points`) contained nulls or formatting issues that would break metric calculations. 
  * *Resolution:* Implemented strict parsing via `pd.to_numeric()` with the `errors='coerce'` parameter and chained `.fillna(0)` in `clenner.py` to ensure mathematical stability across all DataFrames.
* **Dynamic Champion Identification:** Instead of hardcoding the yearly champions based on external intuition, the solution calculates them dynamically. The `i2_champion_myth()` function aggregates race points per `driverId` per season using `df_results` and `df_races`. This guarantees the analysis strictly follows the evidence.

---

## Data Limitations

While the provided data offers strong signals regarding audience behavior, the following limitations constrain deeper analysis:

* **No Impression or Click-Through Rate (CTR) Data:** The analysis measures success strictly through downstream metrics like `views` and `total_watch_time_hours`. Without CTR data, we cannot evaluate the true effectiveness of video thumbnails or titles.
* **Demographic Blindspots:** We can prove the audience is highly captive and loyal year-round (high retention in `category == 'off-season'` content), but we lack demographic breakdowns (age, gender, geography). This limits the commercial team's ability to segment and price highly targeted sponsorship packages.