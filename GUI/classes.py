import sqlalchemy
from sqlalchemy import insert

class Game:
    def __init__(self, Connection):
        self.engine = sqlalchemy.create_engine(Connection)
        self.metadata = sqlalchemy.MetaData()
        self.metadata.reflect(self.engine)
        self.connection = self.engine.connect()
        self.game = self.metadata.tables['game']
        self.userGame = self.metadata.tables['user_game']
    def GetGameByID(self, id):
        query = self.game.select().where(self.game.c['GameID']==id)

        result = self.connection.execute(query).fetchall()

        return result
    def GetAllGames(self):
        query = self.game.select()

        result = self.connection.execute(query).fetchall()

        return result
    def GetGameUser(self, UserID):
        Games = []
        query = self.userGame.select().where(self.userGame.c['UserID']==UserID)

        games = self.connection.execute(query).fetchall()

        for game in games:
            query = self.game.select().where(self.game.c['GameID']==game[0])
            result = self.connection.execute(query).fetchall()
            Games.append(result[0])

        return Games
    def addGame(self, GameID, GameName, ScoreID):
        query = self.game.insert().values(GameID=GameID, GameName=GameName, ScoreID=ScoreID)
        result = self.connection.execute(query)
        
        self.connection.commit()

        return result