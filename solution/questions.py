import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

###############################################################################################################################################
##  Founder: "What is actually driving our growth, and what should we double down on for 2026?"
###############################################################################################################################################

#########################################################    Q1_growth_watch_time    ##########################################################

def q1_growth_watch_time(df_fact_table):


    # Group data: Calculate performance by category for each season
    growth_metrics = df_fact_table.groupby(['season', 'category']).agg(
        total_views=('views', 'sum'),
        total_watch_time_hours=('total_watch_time_hours', 'sum'),
        avg_engagement_rate=('engagement_rate', 'mean'),
        avg_retention_pct=('avgViewPct', 'mean'),
        video_count=('videoId', 'count')
    ).reset_index()

    # Round values for visual clarity
    growth_metrics['avg_engagement_rate'] = growth_metrics['avg_engagement_rate'].round(2)
    growth_metrics['avg_retention_pct'] = growth_metrics['avg_retention_pct'].round(2)

    print("--- Performance Table by Category (2023 - 2025) ---")
    # Sort by season and total watch time to see the leaders for each year
    print(growth_metrics.sort_values(by=['season', 'total_watch_time_hours'], ascending=[True, False]))
    print("\n")
    # Define the formatter function to convert numbers to 'k' format
    def format_k(x, pos):
        if x >= 1000:
            return f'{int(x/1000)}k'
        return str(int(x))

    plt.figure(figsize=(12, 7)) # Increased height slightly to fit the text box

    # Iterate through each category to plot the lines
    for category in growth_metrics['category'].unique():
        subset = growth_metrics[growth_metrics['category'] == category]
        
        # Plot the line
        line = plt.plot(
            subset['season'].to_numpy(), 
            subset['total_watch_time_hours'].to_numpy(), 
            marker='o', 
            linewidth=2.5, 
            markersize=8, 
            label=category
        )
        
        # NEW: Add retention percentage annotation for the 2025 data points
        data_2025 = subset[subset['season'] == 2025]
        if not data_2025.empty:
            watch_time_2025 = data_2025['total_watch_time_hours'].values[0]
            retention_2025 = data_2025['avg_retention_pct'].values[0]
            
            # Annotate next to the 2025 point
            plt.annotate(
                f"{retention_2025}% ret.", 
                xy=(2025, watch_time_2025),
                xytext=(10, -5), # Offset the text slightly to the right
                textcoords='offset points',
                fontsize=10,
                fontweight='bold',
                color=line[0].get_color() # Match the text color to the line color
            )

    # Apply the formatter to the Y-axis
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_k))

    # Add a prominent Recommendation Text Box inside the chart
    recommendation_text = (
        "Recommandation for 2026:\n"
        "'Driver-focus' is our primary growth engine.\n"
        "It not only delivered the highest volume (Watch Time)\n"
        "but also maintained superior audience retention in 2025."
    )
    # Place the text box in the upper left area (x=2023.1, y=approx 90% of chart height)
    plt.text(
        2023.05, plt.gca().get_ylim()[1] * 0.85, 
        recommendation_text, 
        fontsize=11, 
        bbox=dict(facecolor='#f8f9fa', alpha=0.9, edgecolor='#ced4da', boxstyle='round,pad=0.6')
    )

    plt.title('Driver-Focus Content Drove Massive Growth and High Retention', fontsize=14, pad=15, fontweight='bold')
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Total Watch Hours', fontsize=12) # Removed '(Thousands)'
    plt.xticks(growth_metrics['season'].unique()) 
    plt.legend(title='Video Category', title_fontsize='11', fontsize='10', loc='center left') # Moved legend to not overlap text
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save and show the chart
    plt.savefig("results/Q1_growth_and_retention.png", dpi=300)
    return 0

def q2_champion_vs_others(df_fact_table, df_results, df_races):
###############################################################################################################################################
##  Founder: "Champion content feels like our bread and butter. Should we invest in a dedicated champion series?"
###############################################################################################################################################

#########################################################    Q2_champion_vs_others    ##########################################################

    # Merge results with races to attach the 'season' column to each race result
    df_championship = df_results.merge(df_races[['raceId', 'season']], on='raceId', how='left')

    # Aggregate total points for each driver per season
    driver_standings = df_championship.groupby(['season', 'driverId'])['points'].sum().reset_index()

    # Find the champion for each season (sort by points descending, keep the top driver per season)
    champions = driver_standings.sort_values(by=['season', 'points'], ascending=[True, False]).drop_duplicates(subset=['season'], keep='first')

    # Create a dictionary to easily map: {Season -> Champion's DriverId}
    # e.g., {2023: 2.0, 2024: 1.0}
    champion_dict = pd.Series(champions['driverId'].values, index=champions['season']).to_dict()

    print("--- Champions per Season ---")
    print(champions)

    # STEP 2: SEGMENT VIDEOS (CHAMPION vs. NON-CHAMPION)

    # Filter ONLY 'driver-focus' videos, because off-season/race-recaps don't focus on a single driver
    df_driver_focus = df_fact_table[df_fact_table['category'] == 'driver-focus'].copy()

    # Label the videos: Is this video specifically about the season's champion?
    # We check if the focusDriverId matches the champion's ID for that specific season
    df_driver_focus['is_champion'] = df_driver_focus.apply(
        lambda row: row['focusDriverId'] == champion_dict.get(row['season'], -1), 
        axis=1
    )

    # STEP 3: COMPARE METRICS & VISUALIZE

    # Calculate average performance for Champions vs. Other Drivers
    champion_comparison = df_driver_focus.groupby('is_champion').agg(
        avg_views=('views', 'mean'),
        avg_engagement_rate=('engagement_rate', 'mean'),
        video_count=('videoId', 'count') # To see sample size
    ).reset_index()

    # Rename the boolean values to readable strings for the chart
    champion_comparison['is_champion'] = champion_comparison['is_champion'].map({True: 'Champion', False: 'Other Drivers'})

    print("\n--- Performance: Champion vs. Other Drivers ---")
    print(champion_comparison)
    # --- SLIDE DECK VISUALIZATION ---
    # Increased the height from 6 to 8 to make room for the text box at the bottom
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))

    # Subplot 1: Average Views Comparison
    bars1 = ax1.bar(
        champion_comparison['is_champion'], 
        champion_comparison['avg_views'], 
        color=['#7f8c8d', '#f1c40f'], # Grey for Others, Gold for Champion
        alpha=0.9
    )
    ax1.set_title('Average Views: Champions vs. Other Drivers', fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylabel('Average Views', fontsize=12)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Formatter helper to display e.g. 500k instead of 500000
    def format_k_text(x):
        return f"{int(x/1000)}k"

    # Add data labels directly on top of the bars
    for bar in bars1:
        ax1.text(
            bar.get_x() + bar.get_width()/2, 
            bar.get_height() + 2000, 
            format_k_text(bar.get_height()), 
            ha='center', 
            va='bottom', 
            fontweight='bold', 
            fontsize=12
        )

    # Subplot 2: Average Engagement Rate Comparison
    bars2 = ax2.bar(
        champion_comparison['is_champion'], 
        champion_comparison['avg_engagement_rate'], 
        color=['#bdc3c7', '#e67e22'], # Lighter Grey and Orange
        alpha=0.9
    )
    ax2.set_title('Engagement Rate (%): Champions vs. Other Drivers', fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylabel('Avg Engagement Rate (%)', fontsize=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars2:
        ax2.text(
            bar.get_x() + bar.get_width()/2, 
            bar.get_height() + 0.1, 
            f"{bar.get_height():.2f}%", 
            ha='center', 
            va='bottom', 
            fontweight='bold', 
            fontsize=12
        )

    # Super Title for the entire figure to state the core business question
    plt.suptitle('Q: Should We Invest in a Dedicated Champion Series?', fontsize=16, fontweight='bold', y=0.98)

    # Adjust layout to leave the bottom 20% empty for our conclusion text box
    plt.tight_layout(rect=[0, 0.2, 1, 0.95])

    # --- ADDING THE CONCLUSION TEXT BOX ---
    verdict_text = (
        "Answer: No.\n"
        "The data contradicts the initial intuition. Although champion-focused content has a marginally better engagement rate (4.62% vs. 4.39%),\n"
        "videos focused on the rest of the grid (\"Other Drivers\") generate on average 67% more views (82k vs. 49k).\n"
        "A series dedicated exclusively to champions would actually limit our reach; therefore, we should continue to focus on the diverse personalities across the grid."
    )

    # Place the text box centered at the bottom of the figure
    fig.text(
        0.5, 0.05, # x, y coordinates relative to the figure size (0.5 is center, 0.05 is near the bottom)
        verdict_text, 
        ha='center', 
        va='bottom', 
        fontsize=12, 
        linespacing=1.6, # Space out the lines slightly for readability
        bbox=dict(facecolor='#f8f9fa', alpha=0.9, edgecolor='#ced4da', boxstyle='round,pad=1')
    )

    # Save the final chart
    plt.savefig("results/Q2_champion_vs_others.png", dpi=300, bbox_inches='tight')
    return 0

def q3_channel_yoy_growth(df_fact_table):
###############################################################################################################################################
##  Commercial lead: "We are pitching sponsors for 2026. What evidence-backed story about our audience's appetite can we tell?"
###############################################################################################################################################

########################################################    Q3_channel_yoy_growth    #########################################################

    # 1. Classify content as 'Off-Season' or 'Race Season'
    df_fact_table['content_period'] = df_fact_table['category'].apply(
        lambda x: 'Off-Season' if x == 'off-season' else 'Race Season'
    )

    # 2. Aggregate metrics by season AND content period for stacked charts
    stacked_metrics = df_fact_table.groupby(['season', 'content_period']).agg(
        total_views=('views', 'sum'),
        total_watch_time_hours=('total_watch_time_hours', 'sum')
    ).reset_index()

    # 3. Pivot the data to make it ready for stacked bar plotting
    views_pivot = stacked_metrics.pivot(index='season', columns='content_period', values='total_views').fillna(0)
    watch_pivot = stacked_metrics.pivot(index='season', columns='content_period', values='total_watch_time_hours').fillna(0)

    # Reorder columns so 'Race Season' is at the bottom and 'Off-Season' is on top
    column_order = ['Race Season', 'Off-Season']
    views_pivot = views_pivot[column_order]
    watch_pivot = watch_pivot[column_order]

    # 4. Calculate overall yearly totals and YoY growth for the labels
    yearly_metrics = views_pivot.sum(axis=1).to_frame('total_views')
    yearly_metrics['total_watch_time_hours'] = watch_pivot.sum(axis=1)
    yearly_metrics['views_yoy_growth'] = yearly_metrics['total_views'].pct_change() * 100
    yearly_metrics['watch_time_yoy_growth'] = yearly_metrics['total_watch_time_hours'].pct_change() * 100

    # Extract specific 2025 off-season data for the pitch text
    off_season_views_2025 = views_pivot.loc[2025, 'Off-Season']
    off_season_watch_time_2025 = watch_pivot.loc[2025, 'Off-Season']

    # 5. Define formatters for the charts
    def format_millions(x, pos):
        return f'{x*1e-6:.1f}M'

    def format_k(x, pos):
        if x >= 1000:
            return f'{int(x/1000)}k'
        return str(int(x))

    # 6. Create the visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8.5))
    colors = ['#3498db', '#e67e22'] # Blue for Race Season, Orange for Off-Season

    # --- Subplot 1: Total Views (Stacked) ---
    views_pivot.plot(kind='bar', stacked=True, ax=ax1, color=colors, width=0.8, alpha=0.9, edgecolor='white')
    ax1.yaxis.set_major_formatter(FuncFormatter(format_millions))
    ax1.set_title('Channel Total Views per Season', fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylabel('Total Views', fontsize=12)
    ax1.set_xlabel('')
    ax1.tick_params(axis='x', rotation=0) # Keep years horizontal
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    ax1.legend(title='Content Period', loc='upper left')

    # Add YoY growth labels on top of the stacked bars for Views
    for i, season in enumerate(yearly_metrics.index):
        if i > 0:
            yoy_val = yearly_metrics['views_yoy_growth'].iloc[i]
            total_height = yearly_metrics['total_views'].iloc[i]
            ax1.text(
                i, total_height, 
                f'+{yoy_val:.1f}% YoY', 
                ha='center', va='bottom', 
                fontweight='bold', fontsize=11, color='#2c3e50'
            )

    # --- Subplot 2: Total Watch Time Hours (Stacked) ---
    watch_pivot.plot(kind='bar', stacked=True, ax=ax2, color=colors, width=0.8, alpha=0.9, edgecolor='white')
    ax2.yaxis.set_major_formatter(FuncFormatter(format_k))
    ax2.set_title('Channel Total Watch Time per Season', fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylabel('Total Watch Hours', fontsize=12)
    ax2.set_xlabel('')
    ax2.tick_params(axis='x', rotation=0)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    ax2.legend(title='Content Period', loc='upper left')

    # Add YoY growth labels on top of the stacked bars for Watch Time
    for i, season in enumerate(yearly_metrics.index):
        if i > 0:
            yoy_val = yearly_metrics['watch_time_yoy_growth'].iloc[i]
            total_height = yearly_metrics['total_watch_time_hours'].iloc[i]
            ax2.text(
                i, total_height, 
                f'+{yoy_val:.1f}% YoY', 
                ha='center', va='bottom', 
                fontweight='bold', fontsize=11, color='#2c3e50'
            )

    # Adjust layout to leave the bottom 25% empty for our sponsor pitch text box
    plt.tight_layout(rect=[0, 0.25, 1, 1])

    # --- ADDING THE SPONSOR PITCH TEXT BOX ---
    pitch_text = (
        "For Sponsors: Proven Year-Round Loyalty\n"
        "Our channel offers massive, compounding growth. But more importantly, our fans are highly loyal year-round:\n"
        f"As shown in orange, 'Off-Season' content in 2025 alone generated {off_season_views_2025*1e-6:.1f}M views and {int(off_season_watch_time_2025/1000)}k hours of watch time.\n"
        "A partnership with us guarantees constant visibility and high engagement throughout the entire year, not just on race weekends."
    )

    fig.text(
        0.5, 0.05, 
        pitch_text, 
        ha='center', 
        va='bottom', 
        fontsize=12, 
        linespacing=1.6, 
        bbox=dict(facecolor='#f8f9fa', alpha=0.9, edgecolor='#ced4da', boxstyle='round,pad=1')
    )

    # Save and show
    plt.savefig("results/Q3_channel_yoy_growth_stacked.png", dpi=300, bbox_inches='tight')
    return 0