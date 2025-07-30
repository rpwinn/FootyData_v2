# Match Data Structure Analysis

## Overview
Based on our exploration of the FBR API match endpoints, here's the complete data structure for match data.

## 1. Match Metadata (`/matches` endpoint)

### Fields (13 total):
- `match_id`: str (8-character unique identifier)
- `date`: str (YYYY-MM-DD format)
- `time`: str (HH:MM format)
- `wk`: str (week number)
- `home`: str (home team name)
- `home_team_id`: str (home team ID)
- `away`: str (away team name)
- `away_team_id`: str (away team ID)
- `home_team_score`: int or None (final score)
- `away_team_score`: int or None (final score)
- `venue`: str (stadium name)
- `attendance`: str (attendance figure)
- `referee`: str (referee name)

## 2. Match Stats (`/all-players-match-stats` endpoint)

### Top-level structure:
- `data`: array of player stats (all outfield players)
- `keepers`: array of goalkeeper stats

## 3. Player Metadata (for each player in `data` array)

### Fields (5 total):
- `player_id`: str (unique player identifier)
- `player_name`: str (player full name)
- `player_country_code`: str (3-letter country code)
- `player_number`: str (jersey number)
- `age`: str (player age)

## 4. Player Stats Categories (5 categories)

### 4.1 Summary Stats (26 fields):
- `positions`: str or array (player positions)
- `min`: str (minutes played)
- `gls`: int (goals scored)
- `sh`: int (shots)
- `sot`: int (shots on target)
- `xg`: float (expected goals)
- `non_pen_xg`: float (non-penalty expected goals)
- `ast`: int (assists)
- `xag`: float (expected assists)
- `pass_cmp`: int (passes completed)
- `pass_att`: int (passes attempted)
- `pct_pass_cmp`: float (pass completion percentage)
- `pass_prog`: int (progressive passes)
- `sca`: int (shot-creating actions)
- `gca`: int (goal-creating actions)
- `touches`: int (total touches)
- `carries`: int (carries)
- `carries_prog`: int (progressive carries)
- `take_on_att`: int (take-on attempts)
- `take_on_suc`: int (successful take-ons)
- `tkl`: int (tackles)
- `int`: int (interceptions)
- `blocks`: int (blocks)
- `yellow_cards`: int (yellow cards)
- `red_cards`: int (red cards)
- `pk_made`: int (penalties made)
- `pk_att`: int (penalty attempts)

### 4.2 Passing Stats (16 fields):
- `pass_ttl_dist`: int (total pass distance)
- `pass_prog_ttl_dist`: int (progressive pass distance)
- `pass_cmp_s`: int (short passes completed)
- `pass_att_s`: int (short passes attempted)
- `pct_pass_cmp_s`: float (short pass completion %)
- `pass_cmp_m`: int (medium passes completed)
- `pass_att_m`: int (medium passes attempted)
- `pct_pass_cmp_m`: float (medium pass completion %)
- `pass_cmp_l`: int (long passes completed)
- `pass_att_l`: int (long passes attempted)
- `pct_pass_cmp_l`: float (long pass completion %)
- `xa`: float (expected assists)
- `key_passes`: int (key passes)
- `pass_fthird`: int (passes into final third)
- `pass_opp_box`: int (passes into opposition box)
- `cross_opp_box`: int (crosses into opposition box)

### 4.3 Passing Types (13 fields):
- `pass_live`: int (live ball passes)
- `pass_dead`: int (dead ball passes)
- `pass_fk`: int (free kick passes)
- `through_balls`: int (through balls)
- `switches`: int (switches)
- `crosses`: int (crosses)
- `pass_offside`: int (offside passes)
- `pass_blocked`: int (blocked passes)
- `throw_ins`: int (throw-ins)
- `ck`: int (corner kicks)
- `ck_in_swinger`: int (in-swinging corners)
- `ck_out_swinger`: int (out-swinging corners)
- `ck_straight`: int (straight corners)

### 4.4 Defense Stats (11 fields):
- `tkl_won`: int (tackles won)
- `tkl_def_third`: int (tackles in defensive third)
- `tkl_mid_third`: int (tackles in middle third)
- `tkl_att_third`: int (tackles in attacking third)
- `tkl_drb`: int (dribbler tackles)
- `tkl_drb_att`: int (dribbler tackle attempts)
- `pct_tkl_drb_suc`: float (dribbler tackle success %)
- `sh_blocked`: int (shots blocked)
- `tkl_plus_int`: int (tackles + interceptions)
- `clearances`: int (clearances)
- `def_error`: int (defensive errors)

### 4.5 Possession Stats (17 fields):
- `touch_def_box`: int (touches in defensive box)
- `touch_def_third`: int (touches in defensive third)
- `touch_mid_third`: int (touches in middle third)
- `touch_fthird`: int (touches in final third)
- `touch_opp_box`: int (touches in opposition box)
- `touch_live`: int (live ball touches)
- `pct_take_on_suc`: float (take-on success %)
- `take_on_tkld`: int (take-ons tackled)
- `pct_take_on_tkld`: float (take-on tackled %)
- `ttl_carries_dist`: int (total carry distance)
- `ttl_carries_prog_dist`: int (progressive carry distance)
- `carries_fthird`: int (carries into final third)
- `carries_opp_box`: int (carries into opposition box)
- `carries_miscontrolled`: int (miscontrolled carries)
- `carries_dispossessed`: int (dispossessed carries)
- `pass_recvd`: int (passes received)
- `pass_prog_rcvd`: int (progressive passes received)

### 4.6 Misc Stats (11 fields):
- `second_yellow_cards`: int (second yellow cards)
- `fls_com`: int (fouls committed)
- `fls_drawn`: int (fouls drawn)
- `offside`: int (offsides)
- `pk_won`: int (penalties won)
- `pk_conceded`: int (penalties conceded)
- `og`: int (own goals)
- `ball_recov`: int (ball recoveries)
- `air_dual_won`: int (aerial duels won)
- `air_dual_lost`: int (aerial duels lost)
- `pct_air_dual_won`: float (aerial duel win %)

## 5. Goalkeeper Stats (separate array)

### Fields (22 total):
- `player_id`: str (goalkeeper ID)
- `player_name`: str (goalkeeper name)
- `player_country_code`: str (country code)
- `gls_ag`: int (goals against)
- `sot_ag`: int (shots on target against)
- `saves`: str (saves made)
- `save_pct`: float (save percentage)
- `psxg`: str (post-shot expected goals)
- `launched_pass_cmp`: int (launched passes completed)
- `launched_pass_att`: int (launched passes attempted)
- `pct_launched_pass_cmp`: float (launched pass completion %)
- `pass_att`: int (total passes attempted)
- `throws_att`: int (throws attempted)
- `pct_passes_launched`: float (passes launched %)
- `avg_pass_len`: float (average pass length)
- `gk_att`: int (goalkeeper actions)
- `pct_gk_launch`: float (goalkeeper launch %)
- `avg_gk_len`: float (average goalkeeper length)
- `crosses_faced`: int (crosses faced)
- `crosses_stopped`: int (crosses stopped)
- `pct_crosses_stopped`: float (crosses stopped %)
- `def_action_outside_box`: int (defensive actions outside box)
- `avg_dist_def_action_outside_box`: float (average distance of defensive actions)

## Data Summary

- **Match metadata**: 13 fields
- **Player metadata**: 5 fields per player
- **Player stats**: 5 categories with 84 total fields
  - Summary: 26 fields
  - Passing: 16 fields
  - Passing Types: 13 fields
  - Defense: 11 fields
  - Possession: 17 fields
  - Misc: 11 fields
- **Goalkeeper stats**: 22 fields per goalkeeper
- **Total unique fields**: ~140+ different data points per match

## Database Design Considerations

1. **Match table**: Store match metadata
2. **Player table**: Store player metadata (linked to matches)
3. **Player stats tables**: Separate tables for each stats category
4. **Goalkeeper stats table**: Separate table for goalkeeper-specific stats
5. **JSON storage**: Consider storing raw API responses for flexibility 