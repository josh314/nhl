# NHL 
Code for analyzing NHL data. Most of the data used can be obtained from [WAR-On-Ice](war-on-ice.com) which scrapes the NHL's play-by-play stats. More on the data below.

## WAR-On-Ice Data

Links to the WAR-On-Ice (WOI) data can be found [here](http://war-on-ice.com/data/links.txt). As of this time, the data doesn't have the greatest documentation (it has been released publicly only recently). You can keep up with the state of the documentation and look at any old discussion of the data at [the blog](http://blog.war-on-ice.com/) over at WAR-On-Ice (you might start with [this post](http://blog.war-on-ice.com/sharing-is-caring/)). 

The rawest form of the WOI data is the play-by-play data. This is scraped by WOI from the NHL's own post-game play-by-play breakdowns (here's [an example](http://www.nhl.com/scores/htmlreports/20112012/PL030146.HTM)). The results of the scraping are stored in the files with names like `nhlscrapr-20xx20yy.RData`. This serializes an R data frame with the full play-by-play data table for the 20xx-20yy season. The same table is stored in CSV form as `playbyplay-20xx20yy.csv` in the archive `waronice-20xx20yy.zip`. This table is a little opaque on its own, but luckily WOI provides [a legend](https://docs.google.com/spreadsheets/d/152qlz8NFffmUvCQqPUtTuf52psCAsAGlypMqhpzR7PM/edit#gid=0).

Also in the archives are CSV files containing data derived/built from the play-by-play. 

Also among the WOI data files are some CSV files containing off-ice statistics (team colors and rosters) and a game-by-game summary (`games.csv`).

#### Note on Team Abbreviations

**TL;DR** I don't like some of the team abbreviations that WOI uses (the ones that have a period) so there will be some transforming of those names (explicitly or implicitly) in the code. Specificly, I will change them to what I consider the standard name as used by the NHL and national broadcasters, as follows

+ L.A -> LAK
+ N.J -> NJD
+ S.J -> SJS
+ T.B -> TBL

**Rant:** In my experience (or my imagination?), there is a standard set of abbreviations for the team names, namely the three letter codes that the NHL and national broadcasters use in their boxscores and scoreboxes, respectively. These are (including the moved teams)

+ ANA -        Anaheim Ducks
+ ARI -      Arizona Coyotes
+ ATL -    Atlanta Thrashers
+ BOS -        Boston Bruins
+ BUF -       Buffalo Sabres
+ CAR -  Carolina Hurricanes
+ CBJ - Columbus Blue Jackets
+ CGY -       Calgary Flames
+ CHI -   Chicago Blackhawks
+ COL -   Colorado Avalanche
+ DAL -        Dallas Stars
+ DET -    Detroit Red Wings
+ EDM -      Edmonton Oilers
+ FLA -     Florida Panthers
+ LAK -    Los Angeles Kings
+ MIN -       Minnesota Wild
+ MTL -  Montreal Canadiens
+ NJD -   New Jersey Devils
+ NSH - Nashville Predators
+ NYI -  New York Islanders
+ NYR -    New York Rangers
+ OTT -     Ottawa Senators
+ PHI - Philadelphia Flyers
+ PHX - Phoenix Coyotes
+ PIT - Pittsburgh Penguins
+ SJS -     San Jose Sharks
+ STL -     St. Louis Blues
+ TBL - Tampa Bay Lightning
+ TOR - Toronto Maple Leafs
+ VAN -   Vancouver Canucks
+ WSH - Washington Capitals
+ WPG -       Winnipeg Jets

WAR-On-Ice departs from some of these abbreviations for the teams whose homes have compound names 

+ L.A -    Los Angeles Kings
+ N.J -   New Jersey Devils
+ S.J -     San Jose Sharks
+ T.B - Tampa Bay Lightning

This bothers me mostly for aesthetic reasons, but using the three letter abbreviations also makes things a bit simpler when it comes to regular expressions and reading from CSV. 

So I'll be using the three letter abbreviations in most of the code in this repo. There will either be explicit transformation code or it will be implicit that transformed data is being used (in many cases, it probably won't matter).

