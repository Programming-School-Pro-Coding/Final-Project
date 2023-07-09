import Connection
from classes import Game

GameOne = Game(Connection.DB_URI)

print(GameOne.addGame(1, 'Pubg', 2))