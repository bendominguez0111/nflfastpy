import codecs
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def convert_to_gsis_id(new_id):
    """
    Convert new player id columns to old gsis id
    """
    if type(new_id) == float:
        return new_id

    return codecs.decode(new_id[4:-8].replace('-', ''), "hex").decode('utf-8')


def agg_stats(pbp, by_team=True):

    list_of_teams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET',
                     'GB', 'HOU', 'IND', 'JAX', 'KC', 'LAC', 'LA', 'LV', 'MIA', 'MIN', 'NE', 'NO',
                     'NYG', 'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS']

    #####  https://github.com/nflverse/nflfastR/blob/master/R/aggregate_game_stats.R

    ## filter to regular season games
    ## TODO: function argument to allow for postseason play

    pbp_df = pbp[pbp['season_type'] == "REG"]

    ####### PASSING STATS

    ## from pbp_df take only passing plays (filter out PENALTY, PAT2's)
    pass_pbp_df = pbp_df[(pbp_df['play_type_nfl'] == 'PASS') | (pbp_df['play_type_nfl'] == 'SACK')].copy()

    # Calculate additional stats from pbp data

    # sack fumbles (QB specific stat)
    sack_fumbles = pass_pbp_df.apply(
        lambda row: sack_fumble_calculator(row['sack'], row['fumble_lost']), axis=1).copy()
    
    # yards lost on a sack
    sack_yards_lost = pass_pbp_df.apply(
        lambda row: calc_sack_yards(row['sack'], row['yards_gained']), axis=1).copy()

    pass_pbp_df['sack_fumbles_lost'] = sack_fumbles
    pass_pbp_df['sack_yards'] = sack_yards_lost
  
    ## TODO: function argument to allow for grouping by player
    ## if by_team = False: .groupby(player_id)
    ## will require a player id -> name reindex

    passing_stats_to_aggregate = ['passing_yards', 'air_yards', 'pass_touchdown', 'interception', 'complete_pass', 'incomplete_pass', 'pass_attempt', 'epa',
                                'qb_epa', 'comp_air_epa', 'comp_yac_epa', 'air_epa', 'yac_epa', 'first_down_pass', 'sack', 'sack_fumbles_lost', 'sack_yards']

    # create passing stats df, aggregating some columns + calculating new ones 
    pass_stats_df = pass_pbp_df.groupby(['posteam']).agg(stat_agg_func(passing_stats_to_aggregate))

    pass_stats_df.rename(columns={'sack': 'sacks_taken', 'pass_attempt': 'drop_backs', 'complete_pass': 'completions',
                                  'incomplete_pass': 'incompletions', 'first_down_pass': 'passing_first_downs', 'pass_touchdown': 'passing_tds'},
                                  inplace=True)
    
    pass_stats_df['pass_attempts'] = pass_stats_df.drop_backs - pass_stats_df.sacks_taken
    pass_stats_df['net_passing_yards'] = pass_stats_df.passing_yards + pass_stats_df.sack_yards

    # net yards per passing play
    pass_stats_df['net_yards_pp'] = pass_stats_df.net_passing_yards / pass_stats_df.drop_backs

    ####### RUSHING STATS

    # rush df 1: primary rusher

    # from pbp_df take only rushing plays:

    rush_pbp_df = pbp_df[(pbp_df['play_type_nfl'] == 'RUSH')]

    ### TODO: a better way to aggregate >1 stats into list/tuple/dictionary
    ##  ex : {'left':.33,'middle':.33,'right':.33}

    ## run direction for % splits
    rush_left = rush_pbp_df.apply(
            lambda row: if_run_left(row['run_location']), axis=1).copy()
    rush_middle = rush_pbp_df.apply(
            lambda row: if_run_middle(row['run_location']), axis=1).copy()
    rush_right = rush_pbp_df.apply(
            lambda row: if_run_right(row['run_location']), axis=1).copy()

    rush_pbp_df['rush_left'] = rush_left
    rush_pbp_df['rush_middle'] = rush_middle
    rush_pbp_df['rush_right'] = rush_right

    ## run gaps for % splits
    rush_end = rush_pbp_df.apply(
        lambda row: if_run_end(row['run_gap']), axis=1).copy()
    rush_guard = rush_pbp_df.apply(
        lambda row: if_run_guard(row['run_gap']), axis=1).copy()
    rush_tackle = rush_pbp_df.apply(
        lambda row: if_run_tackle(row['run_gap']), axis=1).copy()

    rush_pbp_df['run_end'] = rush_end
    rush_pbp_df['run_guard'] = rush_guard
    rush_pbp_df['run_tackle'] = rush_tackle


    ## list of pbp stats to sum
    rushing_stats_to_aggregate = ['rushing_yards', 'rush_attempt', 'rush_touchdown', 'fumble',
    'fumble_lost', 'first_down_rush', 'epa', 'rush_left', 'rush_middle', 'rush_right', 'run_end', 'run_guard', 'run_tackle']

    rush_stats_df = rush_pbp_df.groupby(['posteam']).agg(stat_agg_func(rushing_stats_to_aggregate))

    rush_stats_df.rename(columns={'rush_attempt': 'carries', 'rush_touchdown': 'rushing_tds', 'fumble': 'fumbles', 
        'fumble_lost': 'fumbles_lost', 'first_down_rush': 'rushing_first_downs', 'epa': 'rushing_epa'}, inplace=True)   

    # TODO: laterals (lol)

    ####### RECIVING STATS

    # receiving df 1: primary reciver

    # from pbp_df take only passing plays:

    receiving_pbp_df = pbp_df[(pbp_df['play_type_nfl'] == 'PASS')]

    receiving_stats_to_aggregate = ['receiving_yards', 'complete_pass', 'pass_touchdown', 'fumble', 'fumble_lost',
                                    'air_yards', 'yards_after_catch', 'first_down_pass', 'epa']

    receiving_stats_df = receiving_pbp_df.groupby(['posteam']).agg(stat_agg_func(receiving_stats_to_aggregate))

    receiving_stats_df.rename(columns={'complete_pass': 'receptions', 'pass_touchdown': 'receving_td', 'fumble_lost': 'fumbles_lost',
                                        'first_down_pass': 'reciving_first_down', 'epa': 'receiving_epa'}, inplace=True)

    ####### SPECIAL TEAMS STATS
    ## TODO

    ####### TWO POINT CONVERSIONS
    

    two_point_pbp_df = pbp_df[(pbp_df['two_point_attempt'] == 1)]

    two_point_rush_attempt = two_point_pbp_df.apply(
        lambda row: if_two_point_run(row['rusher_player_id']), axis=1).copy()
    two_point_pass_attempt = two_point_pbp_df.apply(
        lambda row: if_two_point_pass(row['passer_player_id']), axis=1).copy()
    two_point_success = two_point_pbp_df.apply(
        lambda row: if_two_point_success(row['two_point_conv_result']), axis=1).copy()

    two_point_pbp_df['two_point_rush_attempt'] = two_point_rush_attempt
    two_point_pbp_df['two_point_pass_attempt'] = two_point_pass_attempt
    two_point_pbp_df['two_point_success'] = two_point_success

    two_point_rush_conv = two_point_pbp_df.apply(
        lambda row: if_two_point_rush_conv(row['two_point_success'], row['two_point_rush_attempt']), axis=1).copy()

    two_point_pass_conv = two_point_pbp_df.apply(
        lambda row: if_two_point_pass_conv(row['two_point_success'], row['two_point_pass_attempt']), axis=1).copy()

    two_point_pbp_df['two_point_rush_conv'] = two_point_rush_conv
    two_point_pbp_df['two_point_pass_conv'] = two_point_pass_conv

    two_point_stats_to_aggregate = ['two_point_attempt', 'two_point_rush_attempt', 'two_point_pass_attempt', 'two_point_success', 'two_point_rush_conv', 'two_point_pass_conv']

    two_point_stats_df = two_point_pbp_df.groupby(['posteam']).agg(stat_agg_func(two_point_stats_to_aggregate))


    two_point_stats_df['two_point_conv_rate'] = two_point_stats_df.two_point_success / two_point_stats_df.two_point_attempt

    ####### MERGE STAT DFs
    ## TODO

    return pass_stats_df, rush_stats_df, receiving_stats_df, two_point_stats_df # now returning 4 df's

####### HELPER FUNCTIONS
# functions in this section are applied to df's to help calculate stats

## binary counters for two point plays
# if two point rush
def if_two_point_run(runner_id):
    if (runner_id == ''):
        return 0
    else:
        return 1
# if two point pass
def if_two_point_pass(passer_id):
    if (passer_id == ''):
        return 0
    else:
        return 1
# if two point success
def if_two_point_success(play_result):
    if(play_result == 'failure'):
        return 0
    else:
        return 1
# if two point rush success
def if_two_point_rush_conv(play_result, rush_status):
    if((play_result == 1) & (rush_status == 1)):
        return 1
    else: 
        return 0
# if two point pass success
def if_two_point_pass_conv(play_result, pass_status):
    if((play_result == 1) & (pass_status == 1)):
        return 1
    else: 
        return 0

# helper function to calculate if there was a sack + fumble on pbp data
def sack_fumble_calculator(sack, fumble):
    sack_fumble = 0
    if ((sack == 1) & (fumble == 1)):
        sack_fumble = 1
    return sack_fumble

# helper function to calc QB net yards if there was a sack on pbp data
def calc_sack_yards(sack, yards):
    if (sack == 1):
        return yards

# helper function to output list/array for rush breakdowns
# def rush_breakdown(location, gap):
#     run_location = 

# add binary columns for run direction + gap
## TODO: There has to be a better way to do this
def if_run_left(run_location):
    if (run_location == "left"):
        return 1
    else:
        return 0

def if_run_middle(run_location):
    if (run_location == "middle"):
        return 1
    else:
        return 0

def if_run_right(run_location):
    if (run_location == "right"):
        return 1
    else:
        return 0

def if_run_end(run_location):
    if (run_location == "end"):
        return 1
    else:
        return 0

def if_run_guard(run_location):
    if (run_location == "guard"):
        return 1
    else:
        return 0

def if_run_tackle(run_location):
    if (run_location == "tackle"):
        return 1
    else:
        return 0

# this function takes a list of stats to be summed & returns a dict that can be read by pd.groupby.agg()
# useful for counting stats (yards, epa, and binary play events (TDs, Fumbles, Sacks))
def stat_agg_func(stats_to_aggregate):
    agg_dict = {stats_to_aggregate[i]: 'sum' for i in range(0, len(stats_to_aggregate))}
    return agg_dict
