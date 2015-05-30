Tournament Results
=======================================================

Submission for Project 2 of Udacity's Full Stack Web Developer Nanodgree program.

## Overview

This project includes a database schema for storing data required to run a simple Swiss pairing tournament, and a Python module for adding players, reporting games played, ranking players, and creating player match ups.

## Requirements

To use this code, you must have [PostgreSQL](http://www.postgresql.org/) and [Python](https://www.python.org/) installed.

## Installation

### 1. Setting up the data structure

After downloading this code to your machine, type the following command in your terminal from the project directory in order to set up the database schema:

*NOTE: This will overwrite any previous database you have on your machine named, "tournament," so run with care.*

```
psql -f tournament.sql
```

### 2. Run the tests

The project comes with a set of tests to make sure everything is working properly. From the project directory type the following command to run the test suite:

```
python tournament_test.py
```

If everything is set up correctly, you should see the following result:

```
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
[(70, 'Bruno Walton', 0L, 0L), (71, "Boots O'Neal", 0L, 0L), (72, 'Cathy Burton', 0L, 0L), (73, 'Diane Grant', 0L, 0L)]
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Success!  All tests pass!
```

## Usage

Run this program from within a python prompt, using the following commands:

```
from tournament import *
```

### Resetting tournament data

To reset tournament data, run:

```
newTournament()
```

### Registering new players

To register new players run `registerPlayer(name)`, replacing the 'name' parameter with the name of the player you are adding.

**Example:** Registering a player named Bob Hope
```
registerPlayer('Bob Hope')
```

### Creating match ups

To create a list of match ups for a round of the tournament, use the `swissPairings()` function, which will return an list of match ups containing each player's unique id and name.

### Reporting matches

To report the results of a match, use `reportMatch(winner, loser)`, where winner and loser are the unique ids of the winner and loser of the match, respectively.

**Example:** Bob, whose ID is 4, beats John, whose ID is 2.
```
reportMatch(4, 2)
```

### Get current standings

To return a list of current standings, based on number of wins, use the `playerStandings()` function.
