-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop database;
DROP DATABASE tournament;
-- Create database.
CREATE DATABASE tournament;

-- Connect to the DB before creating tables.
\c tournament;

-- Create table for players.
CREATE TABLE players (id serial primary key, name text);

-- Create table for games.
CREATE TABLE games (game_id serial primary key, winner integer, loser integer);

-- Create view to show standings.
-- There are probably many ways to do this, but this seemed the least verbose.
-- I'd love to see other suggestions for how to create this view.
CREATE VIEW standings AS
SELECT players.id, players.name,
	SUM( CASE WHEN games.winner = players.id THEN 1 ELSE 0 END ) AS wins,
	count(games.*) AS games
FROM players LEFT JOIN games
ON players.id = games.winner OR players.id = games.loser
GROUP BY players.id;
