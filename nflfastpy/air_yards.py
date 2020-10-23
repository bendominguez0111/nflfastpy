from nflfastpy import load_pbp_data

def find_top_receiving(year='2020', n=None):
    df = load_pbp_data(year=year)

    df = df.loc[df['pass_attempt'] == 1, ['receiver_player_id', 'receiver_player_name', 'posteam', 'air_yards']]

    df = df.groupby('receiver_player_id', as_index=False)\
    .agg({
        'receiver_player_name': 'first',
        'posteam': 'first',
        'air_yards': 'sum'
    })

    df = df.sort_values(by='air_yards', ascending=False)
    df = df.reset_index(drop=True)

    if n:
        return df[:n]
    else:
        return df

def find_top_passing(year='2020', n=None):
    df = load_pbp_data(year=year)

    df = df.loc[df['pass_attempt'] == 1, ['passer_player_id', 'passer_player_name', 'posteam', 'air_yards']]

    df = df.groupby('passer_player_id', as_index=False)\
    .agg({
        'passer_player_name': 'first',
        'posteam': 'first',
        'air_yards': 'sum'
    })

    df = df.sort_values(by='air_yards', ascending=False)
    df = df.reset_index(drop=True)

    if n:
        return df[:n]
    else:
        return df