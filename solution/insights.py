import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def i1_growth_engine(df_fact_table):
    # 1. Aggregate total watch time by season and category
    growth_metrics = df_fact_table.groupby(['season', 'category']).agg(
        total_watch_time_hours=('total_watch_time_hours', 'sum')
    ).reset_index()

    # 2. Create the Visualization
    fig, ax = plt.subplots(figsize=(13, 7))

    # Define colors to make our two key categories pop out
    colors = {'driver-focus': '#1f77b4', 'race-recap': '#d62728'} # Blue and Red

    for category in growth_metrics['category'].unique():
        subset = growth_metrics[growth_metrics['category'] == category]
        
        # Highlight 'driver-focus' and 'race-recap', fade out the rest
        if category in ['driver-focus', 'race-recap']:
            alpha = 1.0
            linewidth = 4.0
            color = colors[category]
            zorder = 5
        else:
            alpha = 0.3
            linewidth = 2.0
            color = 'grey'
            zorder = 2
            
        ax.plot(
            subset['season'].to_numpy(),
            subset['total_watch_time_hours'].to_numpy(),
            marker='o',
            linewidth=linewidth,
            markersize=8,
            color=color,
            alpha=alpha,
            label=category if category in ['driver-focus', 'race-recap'] else ('Other Categories' if category == 'off-season' else ""),
            zorder=zorder
        )

    # 3. Formatter for the Y-axis (e.g. 800k)
    def format_k(x, pos):
        if x >= 1000:
            return f'{int(x/1000)}k'
        return str(int(x))

    ax.yaxis.set_major_formatter(FuncFormatter(format_k))
    ax.set_xticks([2023, 2024, 2025]) # Ensure only full years are shown

    # 4. Add custom annotations (Arrows and Text) to tell the story
    # Annotation for the 'driver-focus' explosion
    val_df_2025 = growth_metrics[(growth_metrics['category'] == 'driver-focus') & (growth_metrics['season'] == 2025)]['total_watch_time_hours'].values[0]
    ax.annotate(
        'EXPLOSION:\nDriver-Focus becomes\nthe main growth engine', 
        xy=(2025, val_df_2025), 
        xytext=(2023.7, val_df_2025), # Position the text box to the left
        arrowprops=dict(facecolor='#1f77b4', shrink=0.05, width=2, headwidth=8),
        fontsize=11, fontweight='bold', color='#1f77b4'
    )

    # Annotation for the 'race-recap' plateau
    val_rr_2024 = growth_metrics[(growth_metrics['category'] == 'race-recap') & (growth_metrics['season'] == 2024)]['total_watch_time_hours'].values[0]
    val_rr_2025 = growth_metrics[(growth_metrics['category'] == 'race-recap') & (growth_metrics['season'] == 2025)]['total_watch_time_hours'].values[0]
    mid_point_rr = (val_rr_2024 + val_rr_2025) / 2

    ax.annotate(
        'PLATEAU:\nRace-Recap slows down', 
        xy=(2024.5, mid_point_rr), 
        xytext=(2023.1, mid_point_rr + 50000), # Position text above the line
        arrowprops=dict(facecolor='#d62728', shrink=0.05, width=2, headwidth=8),
        fontsize=11, fontweight='bold', color='#d62728'
    )

    # 5. Clean up legends and styling
    handles, labels = ax.get_legend_handles_labels()
    # Remove duplicate 'Other Categories' from legend
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), title='Category', fontsize=11, loc='upper left')

    # Removing top and right borders (spines) for a cleaner "consulting" look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_title('Insight 1: The Shift in Growth Engine (2023 - 2025)', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Total Watch Hours', fontsize=12)
    ax.set_xlabel('Season', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    return 0

###############################################################################################################################################################################

def i2_champion_myth(df_results, df_races):
    # Merge to attach season to each race result
    df_championship = df_results.merge(df_races[['raceId', 'season']], on='raceId', how='left')

    plt.savefig("results/Insight1_Growth_Engine.png", dpi=300)
    # Find the driver with the most points per season
    driver_standings = df_championship.groupby(['season', 'driverId'])['points'].sum().reset_index()
    champions = driver_standings.sort_values(by=['season', 'points'], ascending=[True, False]).drop_duplicates(subset=['season'], keep='first')

    # Create dictionary: {Season -> Champion DriverId}
    champion_dict = pd.Series(champions['driverId'].values, index=champions['season']).to_dict()

    # Load the fact table containing video metrics
    df_fact_table = pd.read_csv("results/fact_table.csv")

    # Ensure seasons are available for all videos
    df_fact_table['publishDatetime'] = pd.to_datetime(df_fact_table['publishDatetime'])
    df_fact_table['season'] = df_fact_table['season'].fillna(df_fact_table['publishDatetime'].dt.year).astype(int)

    # Filter only 'driver-focus' videos
    df_driver_focus = df_fact_table[df_fact_table['category'] == 'driver-focus'].copy()

    # Flag whether the video focuses on that season's champion
    df_driver_focus['is_champion'] = df_driver_focus.apply(
        lambda row: row['focusDriverId'] == champion_dict.get(row['season'], -1), 
        axis=1
    )

    # Aggregate metrics
    champion_comparison = df_driver_focus.groupby('is_champion').agg(
        avg_views=('views', 'mean'),
        avg_engagement_rate=('engagement_rate', 'mean')
    ).reset_index()

    # Map boolean to clear labels
    champion_comparison['is_champion'] = champion_comparison['is_champion'].map({False: 'Other Drivers', True: 'Champion'})
    champion_comparison = champion_comparison.sort_values(by='is_champion', ascending=False).reset_index(drop=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # --- Subplot 1: Average Views (The Volume Gap) ---
    bars1 = ax1.bar(
        champion_comparison['is_champion'], 
        champion_comparison['avg_views'], 
        color=['#7f8c8d', '#f1c40f'], # Your original colors: Grey for Others, Gold for Champion
        alpha=0.9,
        width=0.6
    )

    # Keep your original structure (titles and grid)
    ax1.set_title('Average Views: The Attention Gap', fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylabel('Average Views', fontsize=12)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    def format_k_text(x):
        return f"{int(x/1000)}k"

    for bar in bars1:
        ax1.text(
            bar.get_x() + bar.get_width()/2, 
            bar.get_height() + 1500, 
            format_k_text(bar.get_height()), 
            ha='center', va='bottom', fontweight='bold', fontsize=12
        )

    # Insight Annotation 1 (Arrows and text safely positioned)
    views_others = champion_comparison.loc[champion_comparison['is_champion'] == 'Other Drivers', 'avg_views'].values[0]
    ax1.annotate(
        'THE REAL DRIVER:\nRest of the grid brings\n+67% more views', 
        xy=(0, views_others), 
        xytext=(0.55, 65000), # Positioned between the bars
        arrowprops=dict(facecolor='#7f8c8d', shrink=0.05, width=2, headwidth=8, connectionstyle="arc3,rad=-0.2"),
        fontsize=11, fontweight='bold', color='#34495e', ha='center', va='center'
    )


    # --- Subplot 2: Engagement Rate (The Marginal Difference) ---
    bars2 = ax2.bar(
        champion_comparison['is_champion'], 
        champion_comparison['avg_engagement_rate'], 
        color=['#bdc3c7', '#e67e22'], # Your original colors: Lighter Grey and Orange
        alpha=0.9,
        width=0.6
    )

    # Keep your original structure (titles and grid)
    ax2.set_title('Engagement Rate: The Illusion', fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylabel('Avg Engagement Rate (%)', fontsize=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    # Increase Y-axis limit to prevent text overlapping with the title
    ax2.set_ylim(0, 5.5)

    for bar in bars2:
        ax2.text(
            bar.get_x() + bar.get_width()/2, 
            bar.get_height() + 0.1, 
            f"{bar.get_height():.2f}%", 
            ha='center', va='bottom', fontweight='bold', fontsize=12
        )

    # Insight Annotation 2 (Arrows and text safely positioned)
    eng_champ = champion_comparison.loc[champion_comparison['is_champion'] == 'Champion', 'avg_engagement_rate'].values[0]
    ax2.annotate(
        'MARGINAL DIFFERENCE:\n+0.23% engagement does not\njustify a dedicated series', 
        xy=(1, eng_champ), 
        xytext=(0.5, 5.1), # Positioned high up in the center
        arrowprops=dict(facecolor='#e67e22', shrink=0.05, width=2, headwidth=8, connectionstyle="arc3,rad=0.1"),
        fontsize=11, fontweight='bold', color='#d35400', ha='center', va='center'
    )


    # --- Final Styling & Title ---
    plt.suptitle('Insight 2: The "Champion Myth" Debunked', fontsize=18, fontweight='bold', y=1.05)
    fig.text(
        0.5, 0.97, 
        "Trophies don't guarantee attention. Grid personalities and drama drive significantly more reach than a dedicated champion focus.", 
        ha='center', fontsize=13, color='#34495e'
    )

    plt.tight_layout()
    plt.savefig("results/Insight2_Champion_Myth.png", dpi=300, bbox_inches='tight')
    return 0

############################################################################################################################################################################

def i3_offseason_loyalty(df_fact_table):
    # Classify content as 'Off-Season' or 'Race Season'
    df_fact_table['content_period'] = df_fact_table['category'].apply(
        lambda x: 'Off-Season' if x == 'off-season' else 'Race Season'
    )

    # Aggregate metrics
    stacked_metrics = df_fact_table.groupby(['season', 'content_period']).agg(
        total_views=('views', 'sum'),
        total_watch_time_hours=('total_watch_time_hours', 'sum')
    ).reset_index()

    # Pivot the data for stacked bar plotting
    views_pivot = stacked_metrics.pivot(index='season', columns='content_period', values='total_views').fillna(0)
    watch_pivot = stacked_metrics.pivot(index='season', columns='content_period', values='total_watch_time_hours').fillna(0)

    # Reorder columns so 'Race Season' is at the bottom and 'Off-Season' is on top
    column_order = ['Race Season', 'Off-Season']
    views_pivot = views_pivot[column_order]
    watch_pivot = watch_pivot[column_order]

    # Calculate overall yearly totals and YoY growth for the labels
    yearly_metrics = views_pivot.sum(axis=1).to_frame('total_views')
    yearly_metrics['total_watch_time_hours'] = watch_pivot.sum(axis=1)
    yearly_metrics['views_yoy_growth'] = yearly_metrics['total_views'].pct_change() * 100
    yearly_metrics['watch_time_yoy_growth'] = yearly_metrics['total_watch_time_hours'].pct_change() * 100

    # Extract specific 2025 off-season data for the pitch text
    off_season_views_2025 = views_pivot.loc[2025, 'Off-Season']
    off_season_watch_time_2025 = watch_pivot.loc[2025, 'Off-Season']

    # ==============================================================================
    # 2. GENERATE INSIGHT VISUALIZATION
    # ==============================================================================

    # Define formatters
    def format_millions(x, pos):
        return f'{x*1e-6:.1f}M'

    def format_k(x, pos):
        if x >= 1000:
            return f'{int(x/1000)}k'
        return str(int(x))

    # Create the figure (increased height to fit titles and bottom box comfortably)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 9))

    # Use the exact colors from your draft: Light Blue and Orange
    colors = ['#4ba3e3', '#f39c12'] 

    # --- Subplot 1: Total Views (Stacked) ---
    views_pivot.plot(kind='bar', stacked=True, ax=ax1, color=colors, width=0.75, alpha=0.95, edgecolor='white')
    ax1.yaxis.set_major_formatter(FuncFormatter(format_millions))
    ax1.set_title('Channel Total Views per Season', fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylabel('Total Views', fontsize=12)
    ax1.set_xlabel('')
    ax1.tick_params(axis='x', rotation=0) # Keeps years horizontal without '.0'
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.legend(title='Content Period', loc='upper left', framealpha=0.9)

    # YoY labels for Views
    for i, season in enumerate(yearly_metrics.index):
        if i > 0:
            yoy_val = yearly_metrics['views_yoy_growth'].iloc[i]
            total_height = yearly_metrics['total_views'].iloc[i]
            ax1.text(
                i, total_height + (total_height * 0.015), 
                f'+{yoy_val:.1f}% YoY', 
                ha='center', va='bottom', fontweight='bold', fontsize=11, color='#2c3e50'
            )

    # INSIGHT ANNOTATION 1: Pointing to the Off-Season loyalty
    views_race_2025 = views_pivot.loc[2025, 'Race Season']
    views_off_2025 = views_pivot.loc[2025, 'Off-Season']
    mid_orange_y = views_race_2025 + (views_off_2025 / 2)

    ax1.annotate(
        'CAPTIVE AUDIENCE:\nOff-Season drives massive volume,\nproving loyalty beyond race weekends',
        xy=(2, mid_orange_y), # Pointing to the orange block in 2025 (index 2)
        xytext=(0, views_race_2025 * 0.85), # Safely placed in the empty space above 2023
        arrowprops=dict(facecolor='#d35400', shrink=0.05, width=2, headwidth=8, connectionstyle="arc3,rad=-0.1"),
        fontsize=11, fontweight='bold', color='#d35400', ha='left', va='center'
    )


    # --- Subplot 2: Total Watch Time Hours (Stacked) ---
    watch_pivot.plot(kind='bar', stacked=True, ax=ax2, color=colors, width=0.75, alpha=0.95, edgecolor='white')
    ax2.yaxis.set_major_formatter(FuncFormatter(format_k))
    ax2.set_title('Channel Total Watch Time per Season', fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylabel('Total Watch Hours', fontsize=12)
    ax2.set_xlabel('')
    ax2.tick_params(axis='x', rotation=0)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    ax2.legend(title='Content Period', loc='upper left', framealpha=0.9)

    # YoY labels for Watch Time
    for i, season in enumerate(yearly_metrics.index):
        if i > 0:
            yoy_val = yearly_metrics['watch_time_yoy_growth'].iloc[i]
            total_height = yearly_metrics['total_watch_time_hours'].iloc[i]
            ax2.text(
                i, total_height + (total_height * 0.015), 
                f'+{yoy_val:.1f}% YoY', 
                ha='center', va='bottom', fontweight='bold', fontsize=11, color='#2c3e50'
            )

    # INSIGHT ANNOTATION 2: Pointing to compounding growth
    total_watch_2025 = yearly_metrics['total_watch_time_hours'].loc[2025]

    ax2.annotate(
        'COMPOUNDING GROWTH:\nTotal watch time nearly\ndoubles year-over-year',
        xy=(2, total_watch_2025), # Pointing to the top of the 2025 bar
        xytext=(0, total_watch_2025 * 0.85), # Safely placed above 2023 bar
        arrowprops=dict(facecolor='#2c3e50', shrink=0.05, width=2, headwidth=8, connectionstyle="arc3,rad=-0.15"),
        fontsize=11, fontweight='bold', color='#2c3e50', ha='left', va='center'
    )


    # --- Final Styling, Super Title & Pitch Box ---
    plt.suptitle('Insight 3: Year-Round Audience Loyalty', fontsize=18, fontweight='bold', y=1.02)
    fig.text(
        0.5, 0.96, 
        "Box Box Analytics is beyond a 'weekend channel'. The audience is captive and consumes massive content independent of the racing calendar.", 
        ha='center', fontsize=13, color='#34495e'
    )
    plt.savefig("results/Insight3_OffSeason_Loyalty.png", dpi=300, bbox_inches='tight')
    return 0