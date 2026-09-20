from read_file import read_all_files
from clenner import convert_drivers_data, convert_qualifying_data, convert_races_data, convert_results_data, convert_teams_data, convert_videos_data, visual_check
from questions import q1_growth_watch_time, q2_champion_vs_others, q3_channel_yoy_growth
from insights import i1_growth_engine, i2_champion_myth, i3_offseason_loyalty
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

folder_path = 'source-data'

dfs = read_all_files(folder_path)

# declare the DataFrames for every file from the folder
df_drivers = dfs["df_drivers"]
df_qualifying = dfs["df_qualifying"]
df_races = dfs["df_races"]
df_results = dfs["df_results"]
df_teams = dfs["df_teams"]
df_videos = dfs["df_videos"]

df_drivers = convert_drivers_data(df_drivers)
df_qualifying = convert_qualifying_data(df_qualifying)
df_races = convert_races_data(df_races)
df_results = convert_results_data(df_results)
df_teams = convert_teams_data(df_teams)
df_videos = convert_videos_data(df_videos)

# calculate the engagement_rate to know how has the best score on likes and comments
df_videos["engagement_rate"] = round(((df_videos["likes"] + df_videos["comments"]) / df_videos["views"]) * 100, 2)

# calculate the total_watch_time_hours to know how has the best score on keep the spectators with eyes on the screen
df_videos['total_watch_time_hours'] = round((df_videos['views'] * (df_videos['durationSeconds'] * df_videos['avgViewPct'] / 100)) / 3600,0)

# bring the season in the df_videos
df_videos_races = df_videos.merge(df_races[["raceId", "season", "country"]],on = "raceId",how = "left")
# bring the point in df_video_races
df_fact_table = df_videos_races.merge(
df_results[["raceId", "driverId", "teamId", "position", "points", "status"]], 
left_on = ["raceId", "focusDriverId"],
right_on = ["raceId", "driverId"],
how = "left")

df_fact_table["season"] = df_fact_table["season"].fillna(df_fact_table["publishDatetime"].dt.year)

q1_growth_watch_time(df_fact_table)
q2_champion_vs_others(df_fact_table, df_results, df_races)
q3_channel_yoy_growth(df_fact_table)

i1_growth_engine(df_fact_table)
i2_champion_myth(df_results, df_races)
i3_offseason_loyalty(df_fact_table)

df_fact_table.to_csv("results/fact_table.csv", index=False)