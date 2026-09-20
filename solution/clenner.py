import pandas as pd

def convert_drivers_data(df_drivers):
    #columns:     driverId code   forename    surname   nationality dateOfBirth

        # convert the columns in the correct format
    try:
        df_drivers["driverId"] = pd.to_numeric(df_drivers["driverId"])
    except ValueError as e:
        print(f"df_drivers has errors on driverId column: {e}")
        return -1
    
    df_drivers["code"] = df_drivers["code"].astype('category')
    df_drivers["forename"] = df_drivers["forename"].astype('category')
    df_drivers["surname"] = df_drivers["surname"].astype('category')
    df_drivers["nationality"] = df_drivers["nationality"].astype('category')

    try:
        df_drivers["dateOfBirth"] = pd.to_datetime(df_drivers["dateOfBirth"], format='%Y-%m-%d')
    except ValueError as e:
        print(f"df_drivers has errors on dateOfBirth column: {e}")
        return -1
    return df_drivers

def convert_qualifying_data(df_qualifying):
    #columns:    raceId  driverId  qPosition qBestTime

        # convert the columns in the correct format

    # raceId
    try:
        df_qualifying["raceId"] = pd.to_numeric(df_qualifying["raceId"])
    except ValueError as e:
        print(f"df_qualifying has errors on raceId column: {e}")
        return -1
    
    # driverId
    try:
        df_qualifying["driverId"] = pd.to_numeric(df_qualifying["driverId"])
    except ValueError as e:
        print(f"df_qualifying has errors on driverId column: {e}")
        return -1

    # qPosition
    try:
        df_qualifying["qPosition"] = pd.to_numeric(df_qualifying["qPosition"])
    except ValueError as e:
        print(f"df_qualifying has errors on qPosition column: {e}")
        return -1

    # qBestTime
    try:
        df_qualifying["qBestTime"] = df_qualifying["qBestTime"].fillna("00:00:00.000")
        df_qualifying["qBestTime"] = pd.to_timedelta("00:" + df_qualifying["qBestTime"])
    except ValueError as e:
        print(f"df_qualifying has errors on qBestTime column: {e}")
        return -1   
    
    return df_qualifying

def convert_races_data(df_races):
    #Columns:   raceId  season  round  raceName  circuit  country  date  time

    # convert the columns in the correct format

    # raceId
    try:
        df_races["raceId"] = pd.to_numeric(df_races["raceId"])
    except ValueError as e:
        print(f"df_qualifying has errors on raceId column: {e}")
        return -1
    
    # season
    try:
        df_races["season"] = pd.to_numeric(df_races["season"])
    except ValueError as e:
        print(f"df_qualifying has errors on season column: {e}")
        return -1

    # round
    try:
        df_races["round"] = pd.to_numeric(df_races["round"])
    except ValueError as e:
        print(f"df_qualifying has errors on qPosition column: {e}")
        return -1
    
    # raceName  
    df_races["raceName"] = df_races["raceName"].astype('category')
    # circuit
    df_races["circuit"] = df_races["circuit"].astype('category') 
    # country
    df_races["country"] = df_races["country"].astype('category') 

    # date
    try:
        df_races["date"] = pd.to_datetime(df_races["date"], format = '%Y-%m-%d')
    except ValueError as e:
        print(f"df_qualifying has errors on date column: {e}")
        return -1   

    # time
    df_races["time"] = df_races["time"].fillna("00:00:00")
    try:
        df_races["time"] = pd.to_timedelta(df_races["time"])
    except ValueError as e:
        print(f"df_qualifying has errors on time column: {e}")
        return -1     
    return df_races

def convert_results_data(df_results):
#Columns: resultId raceId driverId teamId grid position points status fastestLapTime  gapToWinnerSeconds
# convert the columns in the correct format

    # resultId
    try:
        df_results["resultId"] = pd.to_numeric(df_results["resultId"])
    except ValueError as e:
        print(f"df_results has errors on resultId column: {e}")
        return -1
    
    # raceId
    try:
        df_results["raceId"] = pd.to_numeric(df_results["raceId"])
    except ValueError as e:
        print(f"df_results has errors on raceId column: {e}")
        return -1

    # driverId
    try:
        df_results["driverId"] = pd.to_numeric(df_results["driverId"])
    except ValueError as e:
        print(f"df_results has errors on driverId column: {e}")
        return -1

    # teamId
    try:
        df_results["teamId"] = pd.to_numeric(df_results["teamId"])
    except ValueError as e:
        print(f"df_results has errors on teamId column: {e}")
        return -1

    # grid
    try:
        df_results["grid"] = pd.to_numeric(df_results["grid"])
    except ValueError as e:
        print(f"df_results has errors on grid column: {e}")
        return -1

    # position
    df_results["position"] = df_results["position"].fillna(-1)
    try:
        df_results["position"] = pd.to_numeric(df_results["position"])
    except ValueError as e:
        print(f"df_results has errors on position column: {e}")
        return -1

    # points
    try:
        df_results["points"] = pd.to_numeric(df_results["points"])
    except ValueError as e:
        print(f"df_results has errors on points column: {e}")
        return -1
    
    # raceName  
    df_results["status"] = df_results["status"].astype('category')

    # fastestLapTime
    df_results["fastestLapTime"] = df_results["fastestLapTime"].fillna("00:00.0")
    try:
        df_results["fastestLapTime"] = pd.to_timedelta("00:0" + df_results["fastestLapTime"].astype(str))
    except ValueError as e:
        print(f"df_results has errors on fastestLapTime column: {e}")
        return -1 
    
    # gapToWinnerSeconds
    try:
        df_results["gapToWinnerSeconds"] = pd.to_numeric(df_results["gapToWinnerSeconds"])
    except ValueError as e:
        print(f"df_results has errors on gapToWinnerSeconds column: {e}")
        return -1

    return df_results

def convert_teams_data(df_teams):
    #Columns: teamId teamName engineSupplier

    # teamId
    try:
        df_teams['teamId'] = pd.to_numeric(df_teams["teamId"], errors = 'coerce')
    except ValueError as e:
        print(f"df_teams has errors on teamId column: {e}")

    # teamName
    df_teams['teamName'] = df_teams['teamName'].astype('category')

    # engineSupplier
    df_teams['engineSupplier'] = df_teams['engineSupplier'].astype('category')

    return df_teams

def convert_videos_data(df_videos):
    #Columns:   'videoId', 'raceId', 'focusDriverId', 'category', 'title','publishDatetime'
    #           'durationSeconds', 'views', 'likes', 'comments','avgViewPct'

    # videoId
    try:
        df_videos["videoId"] = pd.to_numeric(df_videos["videoId"], errors="coerce")
    except ValueError as e:
        print(f"df_videos has errors on videoId column: {e}")

    # raceId
    try:
        df_videos["raceId"] = pd.to_numeric(df_videos["raceId"], errors="coerce")
    except ValueError as e:
        print(f"df_videos has errors on raceId column: {e}")

    # focusDriverId
    try:
        df_videos["focusDriverId"] = df_videos["focusDriverId"].fillna(-1)
        df_videos["focusDriverId"] = pd.to_numeric(df_videos["focusDriverId"], errors= 'coerce')
    except ValueError as e:
        print(f"df_videos has errors on raceId column: {e}")
    
    # category
    df_videos["category"] = df_videos["category"].astype('category')
    # title
    df_videos["title"] = df_videos["title"].astype('category')

    # publishDatetime
    try:
        df_videos["publishDatetime"] = pd.to_datetime(df_videos["publishDatetime"])
    except ValueError as e:
        print(f"df_videos has errors on publishDatetime column: {e}")
    
    # durationSeconds
    try:
        df_videos["durationSeconds"] = df_videos["durationSeconds"].fillna(0)
        df_videos["durationSeconds"] = pd.to_numeric(df_videos["durationSeconds"])
    except ValueError as e:
        print(f"df_videos has errors on durationSeconds column: {e}")

    # views
    try:
        df_videos["views"] = df_videos["views"].fillna(0)
        df_videos["views"] = pd.to_numeric(df_videos["views"])
    except ValueError as e:
        print(f"df_videos has errors on views column: {e}")

    # likes
    try:
        df_videos["likes"] = df_videos["likes"].fillna(0)
        df_videos["likes"] = pd.to_numeric(df_videos["likes"])
    except ValueError as e:
        print(f"df_videos has errors on likes column: {e}")

    # comments
    try:
        df_videos["comments"] = df_videos["comments"].fillna(0)
        df_videos["comments"] = pd.to_numeric(df_videos["comments"])
    except ValueError as e:
        print(f"df_videos has errors on comments column: {e}")

    # avgViewPct
    try:
        df_videos["avgViewPct"] = df_videos["avgViewPct"].fillna(0)
        df_videos["avgViewPct"] = pd.to_numeric(df_videos["avgViewPct"])
    except ValueError as e:
        print(f"df_videos has errors on avgViewPct column: {e}")

    return df_videos

def visual_check(df_drivers, df_qualifying, df_races, df_results, df_teams, df_videos):
    list_of_dfs = []

    if not df_drivers.empty:
        list_of_dfs.append(df_drivers)
    if not df_qualifying.empty:
        list_of_dfs.append(df_qualifying)
    if not df_races.empty:
        list_of_dfs.append(df_races)
    if not df_results.empty:
        list_of_dfs.append(df_results)
    if not df_teams.empty:
        list_of_dfs.append(df_teams)
    if not df_videos.empty:
        list_of_dfs.append(df_videos)

    for item in list_of_dfs:
        for column in item.columns:
            print(column + ":" + str(item[column].dtype))
        print("\n")

