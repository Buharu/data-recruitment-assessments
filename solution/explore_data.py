from read_file import read_all_files
import pandas as pd

folder_path = 'source-data'

dfs = read_all_files(folder_path)
# print(dfs.keys())
# output: 
#   dict_keys(['df_drivers', 'df_qualifying', 'df_races', 'df_results', 'df_teams', 'df_videos'])


df_drivers = dfs["df_drivers"]
df_qualifying = dfs["df_qualifying"]
df_races = dfs["df_races"]
df_results = dfs["df_results"]
df_teams = dfs["df_teams"]
df_videos = dfs["df_videos"]

### Explore Data Drivers
## the top 10 values from every DataFram exist in the dictionary "dfs"

# print(dfs["df_drivers"])
#     driverId code   forename    surname   nationality dateOfBirth
# 0          1  REN     Kasper       Renn        Danish  1994-03-12
# 1          2  VID      Mateo      Vidal       Spanish  1996-08-02
# 2          3  IMA       Luca       Imai      Japanese  2003-11-30
# 3          4  MAR     Elodie   Marchand        French  1995-05-19
# 4          5  OKE     Tobias    Okereke      Nigerian  1997-01-25
# 5          6  LND     Willem  Lindqvist       Swedish  1993-09-08
# 6          7  CAV      Bruno  Cavallaro       Italian  1998-04-14
# 7          8  DUF       Rhys      Duffy         Irish  1999-12-01
# 8          9  SOL        Ana     Solano       Mexican  1997-07-22
# 9         10  KOV       Petr  Kovalenko     Ukrainian  1994-10-17
# 10        11  ASH     Daniel   Ashworth       British  1992-02-09

## identify the duplicates if exist

# driver_duplicates = df_drivers.duplicated(subset = ["driverId"])
# print(driver_duplicates.describe()) # no duplicates

# print(dfs["df_qualifying"][:10])
#    raceId  driverId  qPosition qBestTime
# 0  202301         1          1  1:29.294
# 1  202301         2          2  1:29.476
# 2  202301         4          3  1:29.939
# 3  202301        21          8  1:30.197
# 4  202301         5          4  1:29.948
# 5  202301         6          5  1:29.993
# 6  202301         7          7  1:30.139
# 7  202301         8          9  1:30.236
# 8  202301         9         11  1:30.303
# 9  202301        10         15  1:30.401

# print(dfs["df_races"][:10])   
#    raceId  season  round                 raceName                     circuit               country        date      time
# 0  202301    2023      1    Silverpine Grand Prix          Silverpine Circuit        United Kingdom  2023-03-05  13:00:00
# 1  202302    2023      2    Costa Azul Grand Prix        Autodromo Costa Azul                 Spain  2023-03-18       NaN
# 2  202303    2023      3        Sakura Grand Prix        Sakura International                 Japan  2023-03-31  05:00:00
# 3  202304    2023      4      Redstone Grand Prix               Redstone Park         United States  2023-04-13  19:00:00
# 4  202305    2023      5   Lago Bianco Grand Prix        Circuito Lago Bianco                 Italy  2023-04-26       NaN
# 5  202306    2023      6      Nordbahn Grand Prix                Nordbahnring               Germany  2023-05-09       NaN
# 6  202307    2023      7   Harbourside Grand Prix  Harbourside Street Circuit             Australia  2023-05-22       NaN
# 7  202308    2023      8  Vallee Verte Grand Prix  Circuit de la Vallee Verte                France  2023-06-04  13:00:00
# 8  202309    2023      9        Aurora Grand Prix              Aurora Raceway                Canada  2023-06-17  18:00:00
# 9  202310    2023     10     Al Dhafra Grand Prix           Al Dhafra Circuit  United Arab Emirates  2023-06-30       NaN

## identify the duplicates if exist
# race_duplicates = df_races.duplicated(subset = ["raceId"], keep = False)
# print(race_duplicates.describe()) # no duplicates

# print(dfs["df_results"][:10])
#    resultId  raceId  driverId  teamId  grid  position  points    status fastestLapTime  gapToWinnerSeconds
# 0     10001  202301         1       1     1       3.0      15  Finished         1:31.5                 8.0
# 1     10002  202301         2       1     2       1.0      25  Finished         1:31.0                 0.0
# 2     10003  202301         4       2     3       2.0      18  Finished         1:31.3                 6.3
# 3     10004  202301        21       2     8       9.0       2  Finished            NaN                42.1
# 4     10005  202301         5       3     4      17.0       0  Finished            NaN                79.3
# 5     10006  202301         6       3     5       NaN       0    Engine            NaN                 NaN
# 6     10007  202301         7       4     7      11.0       0  Finished         1:32.8                43.9
# 7     10008  202301         8       4     9       7.0       6  Finished         1:32.1                39.2
# 8     10009  202301         9       5    11      15.0       0  Finished         1:31.8                55.2
# 9     10010  202301        10       5    15       4.0      12  Finished         1:32.3                23.3

# print(df_results.describe())
#             resultId         raceId     driverId       teamId         grid     position       points  gapToWinnerSeconds
# count    1323.000000    1323.000000  1323.000000  1323.000000  1323.000000  1220.000000  1323.000000         1220.000000
# mean    11445.951625  202411.359033    11.654573     5.501134    10.496599     9.743443     5.059713           41.285738
# std      4802.480003      81.921831     6.551272     2.874420     5.769182     5.372178     7.171145           22.418160
# min     10001.000000  202301.000000     1.000000     1.000000     1.000000     1.000000     0.000000            0.000000
# 25%     10331.500000  202317.000000     6.000000     3.000000     5.500000     5.000000     0.000000           26.800000
# 50%     11222.000000  202411.000000    12.000000     6.000000    10.000000    10.000000     1.000000           41.550000
# 75%     12112.500000  202506.000000    17.000000     8.000000    15.500000    14.000000    10.000000           55.425000
# max    111383.000000  202522.000000    24.000000    10.000000    20.000000    20.000000    25.000000          109.800000

# print(dfs["df_teams"][:10])
#    teamId              teamName  engineSupplier
# 0       1       Meridian Racing  Meridian Power
# 1       2           Voltaire GP        Voltaire
# 2       3      Aurora Autosport       Kobayashi
# 3       4        Halcyon Racing  Meridian Power
# 4       5  Concordia Motorsport           Titan
# 5       6      Redline Dynamics           Titan
# 6       7          Sable Racing       Kobayashi
# 7       8        Polaris Racing        Voltaire
# 8       9    Tempest Motorsport           Titan
# 9      10       Ironwood Racing  Meridian Power

## identify the duplicates if exist
# video_duplicates = df_videos.duplicated(subset = ["videoId"], keep = False)
# print(video_duplicates.describe()) # no duplicates

# print(df_videos[:10])
#    videoId  raceId  focusDriverId    category                                   title  ... durationSeconds    views   likes  comments  avgViewPct
# 0     5001     NaN            NaN  off-season  Technical regulations deep dive | 2023  ...             660  16182.0   735.0      51.0        45.2
# 1     5002     NaN            NaN  off-season                 Drivers to watch | 2023  ...            1485  12153.0   534.0      45.0        45.4
# 2     5003     NaN            NaN  off-season           Rule changes explained | 2023  ...            1140  11549.0   439.0      46.0        47.5
# 3     5004     NaN            NaN  off-season                   Season preview | 2023  ...            1245  19425.0   932.0      67.0        47.6
# 4     5005     NaN            NaN  off-season       Engine suppliers explained | 2023  ...            1305   9844.0   441.0      37.0        50.4
# 5     5006     NaN            NaN  off-season      Pre-season testing analysis | 2023  ...            1185  15123.0   559.0      37.0        48.4
# 6     5007     NaN            NaN  off-season              Team launch roundup | 2023  ...            1455  11029.0   508.0      29.0        49.8
# 7     5008     NaN            NaN  off-season                 Predictions show | 2023  ...            1005  15373.0   636.0      64.0        45.5
# 8     5009     NaN            NaN  off-season            Fantasy league launch | 2023  ...             630  17468.0   756.0      74.0        48.8
# 9     5010     NaN            NaN  off-season                   Calendar guide | 2023  ...            1395  21998.0  1058.0      90.0        48.4

# print(df_videos.describe())
#            videoId         raceId  focusDriverId  durationSeconds          views         likes     comments  avgViewPct
# count   305.000000     275.000000     132.000000       305.000000     300.000000    300.000000   300.000000  305.000000
# mean   5153.000000  202413.818182       6.939394       994.868852   82882.303333   3408.343333   256.886667   47.730164
# std      88.190136      84.121586       6.291588       299.034877   61495.396190   2592.950666   202.315527    5.313594
# min    5001.000000  202301.000000       1.000000       480.000000    9844.000000    439.000000    29.000000   32.200000
# 25%    5077.000000  202316.500000       2.000000       765.000000   39143.500000   1603.000000   114.500000   44.200000
# 50%    5153.000000  202412.000000       4.000000      1005.000000   63623.500000   2725.000000   182.000000   47.700000
# 75%    5229.000000  202507.000000       8.500000      1275.000000  106074.250000   4323.000000   336.000000   51.100000
# max    5305.000000  202522.000000      21.000000      1485.000000  352117.000000  17480.000000  1089.000000   66.800000

# print(df_videos["focusDriverId"].unique())
# [nan  1.  2.  4. 21. 10. 12. 14. 20.  6.  8.  3.]


# print(df_videos["raceId"].unique())
# [    nan 202301. 202302. 202303. 202304. 202305. 202306. 202307. 202308.
#  202309. 202310. 202311. 202312. 202313. 202314. 202315. 202316. 202317.
#  202318. 202319. 202320. 202321. 202322. 202401. 202402. 202403. 202404.
#  202405. 202406. 202407. 202408. 202409. 202410. 202411. 202412. 202413.
#  202414. 202415. 202416. 202417. 202418. 202419. 202420. 202421. 202422.
#  202501. 202502. 202503. 202504. 202505. 202506. 202507. 202508. 202509.
#  202510. 202511. 202512. 202513. 202514. 202515. 202516. 202517. 202518.
#  202519. 202520. 202521. 202522.]


#print(df_videos["category"].unique())
# 'off-season' 'qualifying-report' 'driver-focus' 'race-recap' 'tech-analysis'