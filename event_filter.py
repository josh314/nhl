"""
Functions for subsetting/filtering the cleaned WAR-On-Ice event data. Unless otherwise noted, maintain the original event order.
"""
import pandas as pd
import numpy as np
import nhl.constants as const

############### By time period ###############################

def by_season(events, season):
    "Returns events from a given season. Season codes take the form '20142015'."
    return events[events['season']==season]

############### By team ######################################

def by_home_team(events,team):
    "Returns events from homes games for `team` (use the standard 3-letter abbreviation for team names.)"
    return events[events['hometeam']==team]

def by_away_team(events,team):
    "Returns events from away games for `team` (use the standard 3-letter abbreviation for team names.)"
    return events[events['awayteam']==team]

def by_team(events,team):
    "Returns events from all games for `team` (use the standard 3-letter abbreviation for team names.)"
    home = by_home_team(events,team)
    away = by_away_team(events,team)
    return home.append(away).sort(axis=0)

def by_event_team(events,team):
    "Returns events where event team is `team` (use the standard 3-letter abbreviation for team names.)"
    return events[events['ev.team']==team]

############### By players ######################################

def by_goalie(events,goalie):
    return events[(events['home.G']==goalie) | (events['away.G']==goalie)]

def by_home_goalie(events,goalie):
    return events[(events['home.G']==goalie)]

def by_away_goalie(events,goalie):
    return events[(events['away.G']==goalie)]

def by_skater(events,player):
    bool_vec = pd.Series(False,index=np.arange(len(events)))
    for position in (const.HOME_SKATERS + const.AWAY_SKATERS):
        bool_vec |= (events[position]==player)
    return events[bool_vec]

def by_home_skater(events,player):
    bool_vec = pd.Series(False,index=np.arange(len(events)))
    for position in const.HOME_SKATERS:
        bool_vec |= (events[position]==player)
    return events[bool_vec]

def by_away_skater(events,player):
    bool_vec = pd.Series(False,index=np.arange(len(events)))
    for position in const.AWAY_SKATERS:
        bool_vec |= (events[position]==player)
    return events[bool_vec]

################### Period/Regulation/OT/Shootout ###########################

def period(events,period):
    "Return events from a given period of play."
    return events[events['period'] == period]

def regulation(events):
    "Return events from regulation time, i.e. periods 1,2,3."
    return events[events['period'] <= 3]

def overtime(events):
    "Return events from overtime, excluding shootouts."
    after_regulation = events[events['period'] > 3]
    return remove_shootouts(after_regulation)

def shootouts(events):
    "Returns only shootout events."
    # Shootouts are period 5 of regular season games.
    return events[(events['period'] == 5)
                    & (events['gcode'] <= const.PLAYOFFS_START)]

def remove_shootouts(events):
    "Removes all shootout events."
    # Shootouts are period 5 of regular season games. 
    return events[(events['period']!=5)
                    | (events['gcode'] > const.PLAYOFFS_START)]

################## Man-advantage status #######################

def even_strength(events):
    "Return even-strength (5v5, 4v4, 3v3) events. "
    return events[events['home.skaters']==events['away.skaters']]

def five_on_five(events):#goalies count!
    return events[(events['home.skaters']==6) & (events['away.skaters']==6)]

def four_on_four(events):#goalies count!
    return events[(events['home.skaters']==5) & (events['away.skaters']==5)]

def man_advantage(events):
    return events[events['home.skaters']!=events['away.skaters']]

def power_play(events,team):
    "Returns any power play events for specified team."
    return events[((events['hometeam']==team)
                  & (events['home.skaters']>events['away.skaters']))
                  | ((events['awayteam']==team)
                  & (events['away.skaters']>events['home.skaters']))]

def penalty_kill(events,team):
    "Returns any penalty_kill events for specified team."
    return events[((events['hometeam']==team)
                  & (events['home.skaters']<events['away.skaters']))
                  | ((events['awayteam']==team)
                  & (events['away.skaters']<events['home.skaters']))]

###################### Season status ##############################

def regular_season(events):
    "Return events from regular season games."
    return events[events['gcode'] <= const.PLAYOFFS_START]

def playoffs(events):
    "Return events from playoff games."
    return events[events['gcode'] > const.PLAYOFFS_START]

#################### Offensive events ##############################

def goals(events):
    return events[events['etype']=='GOAL']

def shots(events):
    return events[(events['etype']=='SHOT') | (events['etype']=='GOAL')]

def shot_attempts(events):
        return events[(events['etype']=='SHOT') | (events['etype']=='GOAL')
                      | (events['etype']=='MISS') | (events['etype']=='BLOCK')]

def game_winning_goals(events):
    "Returns subset of the input events which represent game winning goals. Note that the input must include all non-shootout goals in a game for the output to be reliable."
    goals = remove_shootouts(events[events['etype']=='GOAL'])
    games = goals.groupby('gcode')
    def _find_gwg(game_goals):#Returns empty df if a tie
        def _max_score(team):#team = 'home' or 'away'
            score = game_goals[team+'.score'].max()
            if(game_goals.tail(1)['ev.team'].values[0]==game_goals[team+'team'].values[0]):
                score += 1 #score entries don't include the goal just scored
            return score
        winner, loser = 'home', 'away'
        if _max_score('away') > _max_score('home'):
            winner, loser = 'away', 'home'
        winner_goals = game_goals[game_goals['ev.team'] == game_goals[winner+'team']]
        return winner_goals[winner_goals[winner+'.score'] + 1 > _max_score(loser)].head(1)
    gwg = games.apply(_find_gwg)
    gwg.index=gwg.index.levels[1]#removes the redundant gcode indexing layer
    return gwg

#################### Defensive events ##############################

def blocked_shots(events):
    return events[events['etype']=='BLOCK']

#################### Goalie events ###################################

def saves(events):
    return events[events['etype']=='SHOT']

#################### Other events ###################################

