import streamlit as st
import pandas as pd
import requests
import math
import json
from datetime import datetime, timezone, timedelta

now = datetime.now(timezone.utc)  # Current time in GMT
current_min = now.minute
current_hour = now.hour
current_day = now.weekday()  # Monday = 0, Sunday = 6

st.markdown(
    """
    <style>
    [data-testid="stElementToolbar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def fetch_boss_name():
    boss = requests.get("https://data.ninjakiwi.com/btd6/bosses")

    for i in range(0,8):
        if boss.json()['body'][i]['totalScores_standard'] > 1:
            return boss.json()['body'][i]['name']
        
def expire_date(target_day, target_hour, target_minute):
    """
    Calculate the time left until the next occurrence of a target day, hour, and minute.

    :param target_day: Day of the week (0=Monday, 6=Sunday)
    :param target_hour: Target hour (0-23)
    :param target_minute: Target minute (0-59)
    :return: A string indicating the time left with only non-zero values.
    """
    # Get the current time
    now = datetime.now(timezone.utc)

    # Find the next target day
    days_until_target = (target_day - now.weekday() + 7) % 7
    if days_until_target == 0 and (now.hour > target_hour or (now.hour == target_hour and now.minute >= target_minute)):
        days_until_target += 7

    # Calculate the target date and time
    target_datetime = (now + timedelta(days=days_until_target)).replace(
        hour=target_hour, minute=target_minute, second=0, microsecond=0
    )

    # Calculate the time left
    time_left = target_datetime - now

    # Break down the time difference into days, hours, and minutes
    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes = remainder // 60

    # Construct the result string, omitting zero values
    parts = []
    if days == 1:
        parts.append(f"{days} day")
    elif days > 1:
        parts.append(f"{days} days")
    if hours == 1:
        parts.append(f"{hours} hour")
    elif hours > 1:
        parts.append(f"{hours} hours")
    if minutes == 1:
        parts.append(f"{minutes} minute")
    elif minutes > 1:
        parts.append(f"{minutes} minutes")

    return ", ".join(parts) if parts else ""

def calculate_how_long_ago(ms, now, date, hour, min):
    # Reference day (4 = Friday), hour, and minute
    reference_day = date  # Friday
    reference_hour = hour
    reference_minute = min

    # Calculate the current day
    current_day = now.weekday()

    # Calculate the reference datetime
    days_since_reference = (current_day - reference_day) % 7
    reference_datetime = now - timedelta(days=days_since_reference)
    reference_datetime = reference_datetime.replace(hour=reference_hour, minute=reference_minute, second=0, microsecond=0)

    # If the reference time is in the future, go back a week
    if reference_datetime > now:
        reference_datetime -= timedelta(days=7)

    # Calculate the difference in milliseconds
    delta = now - reference_datetime
    elapsed_time_ms = int(delta.total_seconds() * 1000)
    how_long_ago = elapsed_time_ms - ms

    def format_elapsed_time(how_long_ago):
        # Convert milliseconds to a timedelta for easy calculation
        delta = timedelta(milliseconds=how_long_ago)
        days, remainder = divmod(delta.total_seconds(), 86400)  # 1 day = 86400 seconds
        hours, remainder = divmod(remainder, 3600)  # 1 hour = 3600 seconds
        minutes, _ = divmod(remainder, 60)  # 1 minute = 60 seconds
        
        if days > 0:
            return f"{int(days)}d {int(hours)}h"
        elif hours > 0:
            return f"{int(hours)}h {int(minutes)}m"
        else:
            return f"{int(minutes)}m"

    return format_elapsed_time(how_long_ago)

def main():

    # Streamlit title
    st.title("Boss Activity Leaderboard")
    df = pd.read_csv("boss_info.csv")
    if (current_day == 3 and current_hour >= 3) or (current_day == 4) or (current_day == 5 and current_hour < 8):
        st.markdown(f"Boss: __**\"{fetch_boss_name()}\"**__ has ended.", unsafe_allow_html=True)
        st.markdown(f"Activity leaderboard expires in **{expire_date(5,8,0)}**")
        df['last_online'] = -1

    else:
        last_date = df['last_update'].iloc[0]
        last_hour = df['last_update'].iloc[1]
        last_min = df['last_update'].iloc[2]
        st.markdown(f"Current boss: __**\"{fetch_boss_name()}\"**__", unsafe_allow_html=True)
        st.markdown(f"Last update: **{calculate_how_long_ago(0,now,int(last_date),int(last_hour),int(last_min))}** ago")

    df['cash_formatted'] = df['cash'].apply(lambda x: f"{x:,}")
    df['cash_game_time_formatted'] = df['cash_game_time'].apply(lambda ms: f"{ms//3600000}:{(ms//60000)%60:02}:{(ms//1000)%60:02}.{(ms%1000)//10:02}".lstrip("0:").lstrip("0:"))


    # df['cash_game_time_formatted'] = df['cash_game_time'].apply()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["General statistics ℹ️", "Primary count 🪃", "Military count 🪖", "Magic count 🪄", "Support count 🛖", "Hero count 👑"])
        
    with tab1:
        if df['scoringType'].iloc[0] == 'LeastCash':
            df = df.sort_values(by='cash', ascending=True)
            st.dataframe(
                df[['pfp_url', 'name', 'monkeys_placed', 'follower', 'cash_formatted', 'cash_game_time_formatted', 'last_online_time']],
                column_config={
                    'pfp_url': st.column_config.ImageColumn(label="PFP", width=29),  # Profile picture
                    'name': st.column_config.Column(label='Player name 🗨️', width=121, help="Player name"),
                    'monkeys_placed': st.column_config.Column(label='Tower placed 🎮', help="Towers placed since start of boss"),
                    'follower': st.column_config.Column(label='Followers 👥', help="Followers gained"),
                    'cash_formatted': st.column_config.Column(label='PB 💲', help="Cash spent"),
                    'cash_game_time_formatted': st.column_config.Column(label='Run length 🏁', help="Time of winning attempt"),
                    'last_online_time': st.column_config.Column(label='Saves', help="Loaded saves?")
                },
                use_container_width=True,
                hide_index=True,
                on_select="ignore"
            )
        elif df['scoringType'].iloc[0] == 'GameTime':
            df = df.sort_values(by='time', ascending=True)
            st.dataframe(
                df[['pfp_url', 'name', 'monkeys_placed', 'follower', 'time', 'time_game_time', 'last_online_time']],
                column_config={
                    'pfp_url': st.column_config.ImageColumn(label="PFP", width=29),  # Profile picture
                    'name': st.column_config.Column(label='Player name 🗨️', width=121, help="Player name"),
                    'monkeys_placed': st.column_config.Column(label='Play count 🎮', help="Total games played"),
                    'follower': st.column_config.Column(label='Followers 👥', help="Followers gained"),
                    'time': st.column_config.Column(label='PB ⏱️', help="Personal best"),
                    'time_game_time': st.column_config.Column(label='Last PB 🏁', help="Time since last PB"),
                    'last_online_time': st.column_config.Column(label='Active', help="Last active")
                },
                use_container_width=True,
                hide_index=True,
                on_select="ignore"
            )
        elif df['scoringType'].iloc[0] == 'LeastTiers':
            df = df.sort_values(by='tiers', ascending=True)
            st.dataframe(
                df[['pfp_url', 'name', 'monkeys_placed', 'follower', 'tiers', 'tiers_game_count', 'last_online_time']],
                column_config={
                    'pfp_url': st.column_config.ImageColumn(label="PFP", width=29),  # Profile picture
                    'name': st.column_config.Column(label='Player name 🗨️', width=121, help="Player name"),
                    'monkeys_placed': st.column_config.Column(label='Play count 🎮', help="Total games played"),
                    'follower': st.column_config.Column(label='Followers 👥', help="Followers gained"),
                    'tiers': st.column_config.Column(label='PB ⏱️', help="Personal best"),
                    'tiers_game_count': st.column_config.Column(label='Last PB 🏁', help="Time since last PB"),
                    'last_online_time': st.column_config.Column(label='Active', help="Last active")
                },
                use_container_width=True,
                hide_index=True,
                on_select="ignore"
            )
    with tab2:
        st.dataframe(
            df[['pfp_url', 'name', 'dart', 'boomer', 'bomb', 'tack', 'ice', 'glue']],
            column_config={
                'pfp_url': st.column_config.ImageColumn(label="PFP", width=2),  # Profile picture
                'name': st.column_config.Column(label='Player name 🗨️', width=94),
                'dart': st.column_config.NumberColumn(label='Dart'),
                'boomer': st.column_config.NumberColumn(label='Boomer'),
                'bomb': st.column_config.NumberColumn(label='Bomb'),
                'tack': st.column_config.NumberColumn(label='Tack'),
                'ice': st.column_config.NumberColumn(label='Ice'),
                'glue': st.column_config.NumberColumn(label='Glue'),
            },
            use_container_width=True,
            hide_index=True,
        )
    
    with tab3:
        st.dataframe(
            df[['pfp_url', 'name', 'sniper', 'sub', 'boat', 'ace', 'heli', 'mortar', 'dartling']],
            column_config={
                'pfp_url': st.column_config.ImageColumn(label="PFP", width=15),  # Profile picture
                'name': st.column_config.Column(label='Player name 🗨️', width=107),
                'sniper': st.column_config.NumberColumn(label='Sniper'),
                'sub': st.column_config.NumberColumn(label='Sub'),
                'boat': st.column_config.NumberColumn(label='Boat'),
                'ace': st.column_config.NumberColumn(label='Ace'),
                'heli': st.column_config.NumberColumn(label='Heli'),
                'mortar': st.column_config.NumberColumn(label='Mortar'),
                'dartling': st.column_config.NumberColumn(label='Dartling'),
            },
            use_container_width=True,
            hide_index=True,
        )

    with tab4:
        st.dataframe(
            df[['pfp_url', 'name', 'wizard', 'super', 'ninja', 'alch', 'druid', 'merm']],
            column_config={
                'pfp_url': st.column_config.ImageColumn(label="PFP", width=7),  # Profile picture
                'name': st.column_config.Column(label='Player name 🗨️', width=99),
                'wizard': st.column_config.NumberColumn(label='Wizard'),
                'super': st.column_config.NumberColumn(label='Super'),
                'ninja': st.column_config.NumberColumn(label='Ninja'),
                'alch': st.column_config.NumberColumn(label='Alch'),
                'druid': st.column_config.NumberColumn(label='Druid'),
                'merm': st.column_config.NumberColumn(label='Mermonkey'),
            },
            use_container_width=True,
            hide_index=True,
        )

    with tab5:
        st.dataframe(
            df[['pfp_url', 'name', 'farm', 'spac', 'village', 'engie', 'beast']],
            column_config={
                'pfp_url': st.column_config.ImageColumn(label="PFP", width=-1),  # Profile picture
                'name': st.column_config.Column(label='Player name 🗨️', width=91),
                'farm': st.column_config.NumberColumn(label='Farm'),
                'spac': st.column_config.NumberColumn(label='Spactory'),
                'village': st.column_config.NumberColumn(label='Village'),
                'engie': st.column_config.NumberColumn(label='Engineer'),
                'beast': st.column_config.NumberColumn(label='Beast handler'),
            },
            use_container_width=True,
            hide_index=True,
        )
        
    with tab6:
        st.dataframe(
            df[['pfp_url', 'name', 'jones', 'gwendolin', 'benjamin', 'churchill', 'sauda', 'corvus']],
            column_config={
                'pfp_url': st.column_config.ImageColumn(label="PFP", width=16),  # Profile picture
                'name': st.column_config.Column(label='Player name 🗨️', width=108),
                'jones': st.column_config.NumberColumn(label='Striker'),
                'gwendolin': st.column_config.NumberColumn(label='Gwendolin'),
                'benjamin': st.column_config.NumberColumn(label='Benjamin'),
                'churchill': st.column_config.NumberColumn(label='Churchill'),
                'sauda': st.column_config.NumberColumn(label='Sauda'),
                'corvus': st.column_config.NumberColumn(label='Corvus'),
            },
            use_container_width=True,
            hide_index=True,
        )
    st.write(f"Player count: {len(df[['name']])}")

main()