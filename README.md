# Minsweeper_AI

This project is intended to explore how data collection and inference can inform future action and future data
collection. This is a situation frequently confronted by artificial intelligence agents operating in the world - based on
current information, they must decide how to act, balancing both achieving a goal and collecting new information.

The environment should take a dimension d and a number of mines n and generate a random d × d boards
containing n mines. The agent will not have direct access to this location information, but will know the size of
the board. Note: It may be useful to have a version of the agent that allows for manual input, that can accept
clues and feed you directions as you play an actual game of minesweeper in a separate window.
* In every round, the agent should assess its knowledge base, and decide what cell in the environment to query.
* In responding to a query, the environment should specify whether or not there was a mine there, and if not,
how many surrounding cells have mines.
* The agent should take this clue, add it to its knowledge base, and perform any relevant inference or deductions
to learn more about the environment. If the agent is able to determine that a cell has a mine, it should flag or
mark it, and never query that cell. If the agent can determine a cell is safe, it’s reasonable to query that cell
in the next round. A correctly operating agent should not flag a cell as mined when it in fact does
not have a mine!
* Traditionally, the game ends whenever the agent queries a cell with a mine in it - a final score being assessed
in terms of number of mines safely identified.
* However, extend your agent in the following way: if it queries a mine cell, the mine goes off, but the
agent can continue, using the fact that a mine was discovered there to update its knowledge base (but not
receiving a clue about surrounding cells). In this way the game can continue until the entire board is revealed
- a final score being assessed in terms of number of mines safely identified out of the total number of mines.

## A Youtube video to show the working of Basic Agent vs AI Agents

[![IMAGE ALT TEXT HERE](https://i9.ytimg.com/vi/CgeuywBUGns/mq2.jpg?sqp=CKSpoYQG&rs=AOn4CLBGXb_W3G0ZcxkiSOKor6aKTwq44Q)](https://youtu.be/CgeuywBUGns)
