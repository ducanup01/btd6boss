import csv
import os
import requests
import pandas as pd
from datetime import datetime, timezone


boss_info = 'boss_elite_info.csv'

def check_and_create_boss_info():
    columns = [
        'static', 'update', 'url', 'pfp_url', 'init_game', 'init_monkey', 'init_bloon', 'name',
        'game_count', 'monkeys_placed', 'bloons_popped',
        'time', 'time_game_time', 'tiers', 'tiers_game_time', 'cash', 'cash_game_time',
        'daily_chest', 'init_follower', 'follower', 'time_ago', 'init_dart', 'init_boomer', 'init_bomb', 'init_tack', 'init_ice', 'init_glue', 'init_sniper', 'init_sub', 'init_boat', 'init_ace', 'init_heli', 'init_mortar', 'init_dartling', 'init_wizard', 'init_super', 'init_ninja', 'init_alch', 'init_druid', 'init_merm', 'init_farm', 'init_spac', 'init_village', 'init_engie', 'init_beast', 'init_brickell', 'init_adora', 'init_benjamin', 'init_churchill', 'init_corvus', 'init_etienne', 'init_ezili', 'init_geraldo', 'init_gwendolin', 'init_obyn', 'init_pat', 'init_psi' ,'init_quincy', 'init_rosalia', 'init_sauda', 'init_jones', 'dart', 'boomer', 'bomb', 'tack', 'ice', 'glue', 'sniper', 'sub', 'boat', 'ace', 'heli', 'mortar', 'dartling', 'wizard', 'super', 'ninja', 'alch', 'druid', 'merm', 'farm', 'spac', 'village', 'engie', 'beast', 'brickell', 'adora', 'benjamin', 'churchill', 'corvus', 'etienne', 'ezili', 'geraldo', 'gwendolin', 'obyn', 'pat', 'psi', 'quincy', 'rosalia', 'sauda', 'jones', 'last_online', 'last_online_time', 'last_update'
    ]

    if not os.path.isfile(boss_info):
        with open(boss_info, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(columns)
        print(f"File '{boss_info}' created with specified columns.")

def fetch_latest_leaderboard_data():
    bosses = requests.get("https://data.ninjakiwi.com/btd6/bosses")
    for i in range(8):
        if bosses.json()['body'][i]['totalScores_elite'] > 1:
            leaderboard_url = bosses.json()['body'][i]['leaderboard_elite_players_1']
            scoringType = bosses.json()['body'][i]['scoringType']
            latest_leaderboard_data = requests.get(leaderboard_url).json()
            return latest_leaderboard_data, scoringType

def cast_column_types(df):
    df['name'] = df['name'].astype(str)
    df['url'] = df['url'].astype(str)
    df['pfp_url'] = df['pfp_url'].astype(str)
    df['daily_chest'] = pd.to_numeric(df['daily_chest'], errors='coerce').fillna(0).astype(int)

    df['init_game'] = pd.to_numeric(df['init_game'], errors='coerce').fillna(0).astype(int)
    df['init_monkey'] = pd.to_numeric(df['init_monkey'], errors='coerce').fillna(0).astype(int)
    df['init_bloon'] = pd.to_numeric(df['init_bloon'], errors='coerce').fillna(0).astype(int)
    df['init_follower'] = pd.to_numeric(df['init_follower'], errors='coerce').fillna(0).astype(int)

    df['init_dart'] = pd.to_numeric(df['init_dart'], errors='coerce').fillna(0).astype(int)
    df['init_boomer'] = pd.to_numeric(df['init_boomer'], errors='coerce').fillna(0).astype(int)
    df['init_bomb'] = pd.to_numeric(df['init_bomb'], errors='coerce').fillna(0).astype(int)
    df['init_tack'] = pd.to_numeric(df['init_tack'], errors='coerce').fillna(0).astype(int)
    df['init_ice'] = pd.to_numeric(df['init_ice'], errors='coerce').fillna(0).astype(int)
    df['init_glue'] = pd.to_numeric(df['init_glue'], errors='coerce').fillna(0).astype(int)
    df['init_sniper'] = pd.to_numeric(df['init_sniper'], errors='coerce').fillna(0).astype(int)
    df['init_sub'] = pd.to_numeric(df['init_sub'], errors='coerce').fillna(0).astype(int)
    df['init_boat'] = pd.to_numeric(df['init_boat'], errors='coerce').fillna(0).astype(int)
    df['init_ace'] = pd.to_numeric(df['init_ace'], errors='coerce').fillna(0).astype(int)
    df['init_heli'] = pd.to_numeric(df['init_heli'], errors='coerce').fillna(0).astype(int)
    df['init_mortar'] = pd.to_numeric(df['init_mortar'], errors='coerce').fillna(0).astype(int)
    df['init_dartling'] = pd.to_numeric(df['init_dartling'], errors='coerce').fillna(0).astype(int)
    df['init_wizard'] = pd.to_numeric(df['init_wizard'], errors='coerce').fillna(0).astype(int)
    df['init_super'] = pd.to_numeric(df['init_super'], errors='coerce').fillna(0).astype(int)
    df['init_ninja'] = pd.to_numeric(df['init_ninja'], errors='coerce').fillna(0).astype(int)
    df['init_alch'] = pd.to_numeric(df['init_alch'], errors='coerce').fillna(0).astype(int)
    df['init_druid'] = pd.to_numeric(df['init_druid'], errors='coerce').fillna(0).astype(int)
    df['init_merm'] = pd.to_numeric(df['init_merm'], errors='coerce').fillna(0).astype(int)
    df['init_farm'] = pd.to_numeric(df['init_farm'], errors='coerce').fillna(0).astype(int)
    df['init_spac'] = pd.to_numeric(df['init_spac'], errors='coerce').fillna(0).astype(int)
    df['init_village'] = pd.to_numeric(df['init_village'], errors='coerce').fillna(0).astype(int)
    df['init_engie'] = pd.to_numeric(df['init_engie'], errors='coerce').fillna(0).astype(int)
    df['init_beast'] = pd.to_numeric(df['init_beast'], errors='coerce').fillna(0).astype(int)
    df['init_brickell'] = pd.to_numeric(df['init_brickell'], errors='coerce').fillna(0).astype(int)
    df['init_adora'] = pd.to_numeric(df['init_adora'], errors='coerce').fillna(0).astype(int)
    df['init_benjamin'] = pd.to_numeric(df['init_benjamin'], errors='coerce').fillna(0).astype(int)
    df['init_churchill'] = pd.to_numeric(df['init_churchill'], errors='coerce').fillna(0).astype(int)
    df['init_corvus'] = pd.to_numeric(df['init_corvus'], errors='coerce').fillna(0).astype(int)
    df['init_etienne'] = pd.to_numeric(df['init_etienne'], errors='coerce').fillna(0).astype(int)
    df['init_ezili'] = pd.to_numeric(df['init_ezili'], errors='coerce').fillna(0).astype(int)
    df['init_geraldo'] = pd.to_numeric(df['init_geraldo'], errors='coerce').fillna(0).astype(int)
    df['init_gwendolin'] = pd.to_numeric(df['init_gwendolin'], errors='coerce').fillna(0).astype(int)
    df['init_obyn'] = pd.to_numeric(df['init_obyn'], errors='coerce').fillna(0).astype(int)
    df['init_pat'] = pd.to_numeric(df['init_pat'], errors='coerce').fillna(0).astype(int)
    df['init_psi'] = pd.to_numeric(df['init_psi'], errors='coerce').fillna(0).astype(int)
    df['init_quincy'] = pd.to_numeric(df['init_quincy'], errors='coerce').fillna(0).astype(int)
    df['init_rosalia'] = pd.to_numeric(df['init_rosalia'], errors='coerce').fillna(0).astype(int)
    df['init_sauda'] = pd.to_numeric(df['init_sauda'], errors='coerce').fillna(0).astype(int)
    df['init_jones'] = pd.to_numeric(df['init_jones'], errors='coerce').fillna(0).astype(int)

    df['game_count'] = pd.to_numeric(df['game_count'], errors='coerce').fillna(0).astype(int)
    df['monkeys_placed'] = pd.to_numeric(df['monkeys_placed'], errors='coerce').fillna(0).astype(int)
    df['bloons_popped'] = pd.to_numeric(df['bloons_popped'], errors='coerce').fillna(0).astype(int)
    df['follower'] = pd.to_numeric(df['follower'], errors='coerce').fillna(0).astype(int)

    df['dart'] = pd.to_numeric(df['dart'], errors='coerce').fillna(0).astype(int)
    df['boomer'] = pd.to_numeric(df['boomer'], errors='coerce').fillna(0).astype(int)
    df['bomb'] = pd.to_numeric(df['bomb'], errors='coerce').fillna(0).astype(int)
    df['tack'] = pd.to_numeric(df['tack'], errors='coerce').fillna(0).astype(int)
    df['ice'] = pd.to_numeric(df['ice'], errors='coerce').fillna(0).astype(int)
    df['glue'] = pd.to_numeric(df['glue'], errors='coerce').fillna(0).astype(int)
    df['sniper'] = pd.to_numeric(df['sniper'], errors='coerce').fillna(0).astype(int)
    df['sub'] = pd.to_numeric(df['sub'], errors='coerce').fillna(0).astype(int)
    df['boat'] = pd.to_numeric(df['boat'], errors='coerce').fillna(0).astype(int)
    df['ace'] = pd.to_numeric(df['ace'], errors='coerce').fillna(0).astype(int)
    df['heli'] = pd.to_numeric(df['heli'], errors='coerce').fillna(0).astype(int)
    df['mortar'] = pd.to_numeric(df['mortar'], errors='coerce').fillna(0).astype(int)
    df['dartling'] = pd.to_numeric(df['dartling'], errors='coerce').fillna(0).astype(int)
    df['wizard'] = pd.to_numeric(df['wizard'], errors='coerce').fillna(0).astype(int)
    df['super'] = pd.to_numeric(df['super'], errors='coerce').fillna(0).astype(int)
    df['ninja'] = pd.to_numeric(df['ninja'], errors='coerce').fillna(0).astype(int)
    df['alch'] = pd.to_numeric(df['alch'], errors='coerce').fillna(0).astype(int)
    df['druid'] = pd.to_numeric(df['druid'], errors='coerce').fillna(0).astype(int)
    df['merm'] = pd.to_numeric(df['merm'], errors='coerce').fillna(0).astype(int)
    df['farm'] = pd.to_numeric(df['farm'], errors='coerce').fillna(0).astype(int)
    df['spac'] = pd.to_numeric(df['spac'], errors='coerce').fillna(0).astype(int)
    df['village'] = pd.to_numeric(df['village'], errors='coerce').fillna(0).astype(int)
    df['engie'] = pd.to_numeric(df['engie'], errors='coerce').fillna(0).astype(int)
    df['beast'] = pd.to_numeric(df['beast'], errors='coerce').fillna(0).astype(int)
    df['brickell'] = pd.to_numeric(df['brickell'], errors='coerce').fillna(0).astype(int)
    df['adora'] = pd.to_numeric(df['adora'], errors='coerce').fillna(0).astype(int)
    df['benjamin'] = pd.to_numeric(df['benjamin'], errors='coerce').fillna(0).astype(int)
    df['churchill'] = pd.to_numeric(df['churchill'], errors='coerce').fillna(0).astype(int)
    df['corvus'] = pd.to_numeric(df['corvus'], errors='coerce').fillna(0).astype(int)
    df['etienne'] = pd.to_numeric(df['etienne'], errors='coerce').fillna(0).astype(int)
    df['ezili'] = pd.to_numeric(df['ezili'], errors='coerce').fillna(0).astype(int)
    df['geraldo'] = pd.to_numeric(df['geraldo'], errors='coerce').fillna(0).astype(int)
    df['gwendolin'] = pd.to_numeric(df['gwendolin'], errors='coerce').fillna(0).astype(int)
    df['obyn'] = pd.to_numeric(df['obyn'], errors='coerce').fillna(0).astype(int)
    df['pat'] = pd.to_numeric(df['pat'], errors='coerce').fillna(0).astype(int)
    df['psi'] = pd.to_numeric(df['psi'], errors='coerce').fillna(0).astype(int)
    df['quincy'] = pd.to_numeric(df['quincy'], errors='coerce').fillna(0).astype(int)
    df['rosalia'] = pd.to_numeric(df['rosalia'], errors='coerce').fillna(0).astype(int)
    df['sauda'] = pd.to_numeric(df['sauda'], errors='coerce').fillna(0).astype(int)
    df['jones'] = pd.to_numeric(df['jones'], errors='coerce').fillna(0).astype(int)


    df['time'] = pd.to_numeric(df['time'], errors='coerce').fillna(0).astype(int)   
    df['time_game_time'] = pd.to_numeric(df['time_game_time'], errors='coerce').fillna(0).astype(int)
    df['tiers'] = pd.to_numeric(df['tiers'], errors='coerce').fillna(0).astype(int)
    df['tiers_game_time'] = pd.to_numeric(df['tiers_game_time'], errors='coerce').fillna(0).astype(int)
    df['cash'] = pd.to_numeric(df['cash'], errors='coerce').fillna(0).astype(int)
    df['cash_game_time'] = pd.to_numeric(df['cash_game_time'], errors='coerce').fillna(0).astype(int)


    df['last_online'] = pd.to_numeric(df['last_online'], errors='coerce').fillna(0).astype(int)
    df['last_update'] = pd.to_numeric(df['last_update'], errors='coerce').fillna(0).astype(int)

def fetch_player_data(url, timeout=5):
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        
        # Check if 'body' exists in the response
        if 'body' in data:
            return data
        
        print(f"'body' key missing in response for URL: {url}")
    except (requests.RequestException, ValueError) as e:
        print(f"Request failed for URL: {url}, Error: {e}")
    
    print(f"Failed to fetch valid data for URL: {url}")
    return None

def update_new_players(df):
    latest_leaderboard_data, scoringType = fetch_latest_leaderboard_data()
    now = datetime.now(timezone.utc)
    count_players = len(latest_leaderboard_data.get('body', []))
    for i in range(count_players):
        player_url = latest_leaderboard_data.get('body', [{}])[i].get('profile', None)
        if not player_url:
            print(f"Missing 'profile' URL for player {i+1}")
            continue

        # Fetch player data with retries
        player_data = fetch_player_data(player_url)
        if not player_data:
            print(f"Skipping player {i+1} due to missing valid data")
            continue
        # Safely access 'body' and process data
        try:
            towers = player_data['body']['towersPlaced']
            heroes = player_data['body']['heroesPlaced']
        except KeyError as e:
            print(f"Key error for player {i+1}, missing key: {e}")
            continue

        follower = player_data['body']['followers']

        dart = towers['DartMonkey']
        boomer = towers['BoomerangMonkey']
        bomb = towers['BombShooter']
        tack = towers['TackShooter']
        ice = towers['IceMonkey']
        glue = towers['GlueGunner']
        sniper = towers['SniperMonkey']
        sub = towers['MonkeySub']
        boat = towers['MonkeyBuccaneer']
        ace = towers['MonkeyAce']
        heli = towers['HeliPilot']
        mortar = towers['MortarMonkey']
        dartling = towers['DartlingGunner']
        wizard = towers['WizardMonkey']
        super = towers['SuperMonkey']
        ninja = towers['NinjaMonkey']
        alch = towers['Alchemist']
        druid = towers['Druid']
        merm = towers['Mermonkey']
        farm = towers['BananaFarm']
        spac = towers['SpikeFactory']
        village = towers['MonkeyVillage']
        engie = towers['EngineerMonkey']
        beast = towers['BeastHandler']

        brickell = heroes['AdmiralBrickell']
        adora = heroes['Adora']
        benjamin = heroes['Benjamin']
        churchill = heroes['CaptainChurchill']
        corvus = heroes['Corvus']
        etienne = heroes['Etienne']
        ezili = heroes['Ezili']
        geraldo = heroes['Geraldo']
        gwendolin = heroes['Gwendolin']
        obyn = heroes['ObynGreenfoot']
        pat = heroes['PatFusty']
        psi = heroes['Psi']
        quincy = heroes['Quincy']
        rosalia = heroes['Rosalia']
        sauda = heroes['Sauda']
        jones = heroes['StrikerJones']

        if scoringType == 'GameTime':
            time = latest_leaderboard_data['body'][i]['scoreParts'][1]['score']
            time_game_time = latest_leaderboard_data['body'][i]['scoreParts'][2]['score']
            tiers = tiers_game_time = cash = cash_game_time = None
        elif scoringType == 'LeastTiers':
            tiers = latest_leaderboard_data['body'][i]['scoreParts'][0]['score']
            tiers_game_time = latest_leaderboard_data['body'][i]['scoreParts'][1]['score']
            time = time_game_time = cash = cash_game_time = None
        elif scoringType == 'LeastCash':
            cash = latest_leaderboard_data['body'][i]['scoreParts'][1]['score']
            cash_game_time = latest_leaderboard_data['body'][i]['scoreParts'][2]['score']
            time = time_game_time = tiers = tiers_game_time = None

        if player_url not in df['url'].values:
            # Add new player data
            game = player_data.get('body', {}).get('gameplay', {}).get('gameCount', 0)
            monkey = player_data.get('body', {}).get('gameplay', {}).get('monkeysPlaced', 0)
            bloon = player_data.get('body', {}).get('bloonsPopped', {}).get('bloonsPopped', 0)
            init_follower = player_data.get('body', {}).get('followers', 0)


            df.loc[len(df)] = {
                'url': player_url,
                'init_game': game,
                'init_monkey': monkey,
                'init_bloon': bloon,
                'init_follower': init_follower,

                'init_dart': dart,
                'init_boomer': boomer,
                'init_bomb': bomb,
                'init_tack': tack,
                'init_ice': ice,
                'init_glue': glue,
                'init_sniper': sniper,
                'init_sub': sub,
                'init_boat': boat,
                'init_ace': ace,
                'init_heli': heli,
                'init_mortar': mortar,
                'init_dartling': dartling,
                'init_wizard': wizard,
                'init_super': super,
                'init_ninja': ninja,
                'init_alch': alch,
                'init_druid': druid,
                'init_merm': merm,
                'init_farm': farm,
                'init_spac': spac,
                'init_village': village,
                'init_engie': engie,
                'init_beast': beast,

                'init_brickell': brickell,
                'init_adora': adora,
                'init_benjamin': benjamin,
                'init_churchill': churchill,
                'init_corvus': corvus,
                'init_etienne': etienne,
                'init_ezili': ezili,
                'init_geraldo': geraldo,
                'init_gwendolin': gwendolin,
                'init_obyn': obyn,
                'init_pat': pat,
                'init_psi': psi,
                'init_quincy': quincy,
                'init_rosalia': rosalia,
                'init_sauda': sauda,
                'init_jones': jones,
                'last_online': int(0),

                'time': time,
                'time_game_time': time_game_time,
                'tiers': tiers,
                'tiers_game_time': tiers_game_time,
                'cash': cash,
                'cash_game_time': cash_game_time
            }   
        else:
            # Update existing player data
            row_index = df[df['url'] == player_url].index[0]
            game = player_data.get('body', {}).get('gameplay', {}).get('gameCount', 0) - df.at[row_index, 'init_game']


            if game > df.at[row_index, 'game_count']:
                df.at[row_index, 'last_online'] = 0
            else:
                last_update_date = int(df.at[0, 'last_update'])
                last_update_hour = int(df.at[1, 'last_update'])
                last_update_minute = int(df.at[2, 'last_update'])
                this_update_date = int(now.weekday())
                this_update_hour = int(now.hour)
                this_update_minute = int(now.minute)
                if this_update_date < last_update_date:
                    this_update_date += 7
                minute_difference = this_update_date*1440 + this_update_hour*60 + this_update_minute - (last_update_date*1440 + last_update_hour*60 + last_update_minute)
                df.at[row_index, 'last_online'] += minute_difference

            df.at[row_index, 'pfp_url'] = player_data.get('body', {}).get('avatarURL', None)
            df.at[row_index, 'name'] = player_data.get('body', {}).get('displayName', None)
            df.at[row_index, 'game_count'] = game

            df.at[row_index, 'monkeys_placed'] = player_data.get('body', {}).get('gameplay', {}).get('monkeysPlaced', 0) - df.at[row_index, 'init_monkey']

            df.at[row_index, 'bloons_popped'] = player_data.get('body', {}).get('bloonsPopped', {}).get('bloonsPopped', 0) - df.at[row_index, 'init_bloon']

            df.at[row_index, 'follower'] = follower - df.at[row_index, 'init_follower']

            df.at[row_index, 'daily_chest'] = player_data.get('body', {}).get('gameplay', {}).get('dailyRewards', None)

            # df.at[row_index, 'time'] = format_time(latest_leaderboard_data['body'][i]['score'])
            # df.at[row_index, 'time_left'] = latest_leaderboard_data['body'][i]['scoreParts'][1]['score']

            df.at[row_index, 'time'] = time
            df.at[row_index, 'time_game_time'] = time_game_time
            df.at[row_index, 'tiers'] = tiers
            df.at[row_index, 'tiers_game_time'] = tiers_game_time
            df.at[row_index, 'cash'] = cash
            df.at[row_index, 'cash_game_time'] = cash_game_time


            df.at[row_index, 'dart'] = dart - df.at[row_index, 'init_dart']
            df.at[row_index, 'boomer'] = boomer - df.at[row_index, 'init_boomer']
            df.at[row_index, 'bomb'] = bomb - df.at[row_index, 'init_bomb']
            df.at[row_index, 'tack'] = tack - df.at[row_index, 'init_tack']
            df.at[row_index, 'ice'] = ice - df.at[row_index, 'init_ice']
            df.at[row_index, 'glue'] = glue - df.at[row_index, 'init_glue']
            df.at[row_index, 'sniper'] = sniper - df.at[row_index, 'init_sniper']
            df.at[row_index, 'sub'] = sub - df.at[row_index, 'init_sub']
            df.at[row_index, 'boat'] = boat - df.at[row_index, 'init_boat']
            df.at[row_index, 'ace'] = ace - df.at[row_index, 'init_ace']
            df.at[row_index, 'heli'] = heli - df.at[row_index, 'init_heli']
            df.at[row_index, 'mortar'] = mortar - df.at[row_index, 'init_mortar']
            df.at[row_index, 'dartling'] = dartling - df.at[row_index, 'init_dartling']
            df.at[row_index, 'wizard'] = wizard - df.at[row_index, 'init_wizard']
            df.at[row_index, 'super'] = super - df.at[row_index, 'init_super']
            df.at[row_index, 'ninja'] = ninja - df.at[row_index, 'init_ninja']
            df.at[row_index, 'alch'] = alch - df.at[row_index, 'init_alch']
            df.at[row_index, 'druid'] = druid - df.at[row_index, 'init_druid']
            df.at[row_index, 'merm'] = merm - df.at[row_index, 'init_merm']
            df.at[row_index, 'farm'] = farm - df.at[row_index, 'init_farm']
            df.at[row_index, 'spac'] = spac - df.at[row_index, 'init_spac']
            df.at[row_index, 'village'] = village - df.at[row_index, 'init_village']
            df.at[row_index, 'engie'] = engie - df.at[row_index, 'init_engie']
            df.at[row_index, 'beast'] = beast - df.at[row_index, 'init_beast']

            df.at[row_index, 'brickell'] = brickell - df.at[row_index, 'init_brickell']
            df.at[row_index, 'adora'] = adora - df.at[row_index, 'init_adora']
            df.at[row_index, 'benjamin'] = benjamin - df.at[row_index, 'init_benjamin']
            df.at[row_index, 'churchill'] = churchill - df.at[row_index, 'init_churchill']
            df.at[row_index, 'corvus'] = corvus - df.at[row_index, 'init_corvus']
            df.at[row_index, 'etienne'] = etienne - df.at[row_index, 'init_etienne']
            df.at[row_index, 'ezili'] = ezili - df.at[row_index, 'init_ezili']
            df.at[row_index, 'geraldo'] = geraldo - df.at[row_index, 'init_geraldo']
            df.at[row_index, 'gwendolin'] = gwendolin - df.at[row_index, 'init_gwendolin']
            df.at[row_index, 'obyn'] = obyn - df.at[row_index, 'init_obyn']
            df.at[row_index, 'pat'] = pat - df.at[row_index, 'init_pat']
            df.at[row_index, 'psi'] = psi - df.at[row_index, 'init_psi']
            df.at[row_index, 'quincy'] = quincy - df.at[row_index, 'init_quincy']
            df.at[row_index, 'rosalia'] = rosalia - df.at[row_index, 'init_rosalia']
            df.at[row_index, 'sauda'] = sauda - df.at[row_index, 'init_sauda']
            df.at[row_index, 'jones'] = jones - df.at[row_index, 'init_jones']
        print(f"{i+1}/25")
    df.at[0, 'last_update'] = int(now.weekday())
    df.at[1, 'last_update'] = int(now.hour)
    df.at[2, 'last_update'] = int(now.minute)
    df.at[3, 'last_update'] = scoringType

def main(boss_info):

    check_and_create_boss_info()

    df = pd.read_csv(boss_info)

    cast_column_types(df)

    print("Updating player IDs...")
    update_new_players(df)

    # print("Updating player statistics...")
    # update_existing_players(df, latest_leaderboard_data)

    df.to_csv(boss_info, index=False)
    print("Boss information updated!")
    
main(boss_info)