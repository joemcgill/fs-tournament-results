#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM games")
    db.commit()
    db.close


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.commit()
    db.close


def newTournament():
    deleteMatches()
    deletePlayers()
    print "Player and Match data has been reset."


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) AS num FROM players")
    count = c.fetchone()[0]
    db.close

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    query = "INSERT INTO players (name) VALUES (%s);"
    args = (name,)
    c.execute(query, args)
    db.commit()
    db.close


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM standings ORDER BY wins DESC;")
    standings = c.fetchall()
    db.close()

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    query = "INSERT INTO games (winner, loser) VALUES (%s, %s);"
    args = (winner, loser,)
    c.execute(query, args)
    db.commit()
    db.close()


def assignBye():
    """Returns a player who is being assigned a bye.

    Assign a bye to the next player who has yet to receive one.

    Returns:
        A single tuple, containing (id, name) of the player who is being
        assigned a bye in this round.
    """
    db = connect()
    c = db.cursor()

    # Query for a player who has yet to receive a bye
    query = "SELECT id, name FROM byes WHERE bye_count = 0 LIMIT 1;"
    c.execute(query)
    player = c.fetchone()
    db.close()

    return player


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Set up our variables for pairs, player getting a bye, and the bye pairing
    pairs = []
    byePlayer = False
    byePair = False

    # Use the playerStandings function to get our standings, because DRY.
    standings = playerStandings()
    num_players = len(standings)

    # If we have an odd number of players, we have to assign a bye
    if 0 != num_players % 2:
        byePlayer = assignBye()

    # Loop through every other player in the standings and pair them with
    # the next adjacent player, handle byes when we encounter them.
    i = 0
    while i < num_players:
        # If we have a bye and it's been assigned to one of the next two
        # players in the standings, then pair the bye accordingly.
        if byePlayer and (byePlayer[0] == standings[i][0] or
           byePlayer[0] == standings[i+1][0]):

            # If the first player in the loop has a bye, create the bye pairing
            # and pair the next two players in the standings
            if byePlayer[0] == standings[i][0]:
                # Our bye pairing
                byePair = (
                    standings[i][0],
                    standings[i][1],
                    '',
                    "bye"
                )

                # Skip ahead one since we've only paired one and start over.
                i += 1
                continue

            # If the second player in the loop has a bye, pair the first and
            # third players and create the bye pair with the second player.
            elif byePlayer[0] == standings[i+1][0]:
                # Our next pair
                pair = (
                    standings[i][0],
                    standings[i][1],
                    standings[i+2][0],
                    standings[i+2][1]
                )

                # Our bye pairing
                byePair = (
                    standings[i+1][0],
                    standings[i+1][1],
                    '',
                    "bye"
                )

                # Skip ahead three since we've paired three players
                i += 3

        # If we don't have a bye or it's not being paired during this iteration
        # just pair the next two players and move along.
        else:
            pair = (
                standings[i][0],
                standings[i][1],
                standings[i+1][0],
                standings[i+1][1]
            )

            # skip ahead two since we've paired two players
            i += 2

        # Append the main pair
        pairs.append(pair)

    # After the loop runs, append the bye pair if one exists
    if byePair:
        pairs.append(byePair)

    # Convert the pairs array to a tuple as the requirements suggest.
    tuple(pairs)
    return pairs
