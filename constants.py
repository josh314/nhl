"""
Constants for use in this package
"""

################### Player id ################################

# A placeholder value indicating no player, e.g. to indicate
# pulled goalie
NOPLAYER = 'xxxxxxxNA'

########################### GCODE ##############################

# Each game of a season is assigned a unique 'gcode' number. The
# regular season games are between 20000 & 30000 and playoff games
# are over 30000

SEASON_START = 20000
PLAYOFFS_START = 30000
 
#################################################################

######################## Player columns #########################

# Use these arrays to grab all the columns for the home or away
# team in the WOI event data. They include include spots for a 6th
# attacker if the goalie is pulled. Note that at least one of the
# columns in each array will be NaN for every event because of this.


HOME_PLAYERS = ['h1','h2','h3','h4','h5','h6','home.G']
AWAY_PLAYERS = ['a1','a2','a3','a4','a5','a6','away.G']

# Same as above but without the goalies. 
HOME_SKATERS = ['h1','h2','h3','h4','h5','h6']
AWAY_SKATERS = ['a1','a2','a3','a4','a5','a6']
