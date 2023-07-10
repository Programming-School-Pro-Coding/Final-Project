import sqlalchemy
import sqlalchemy

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

class user:
    def __init__(self,db_url):
        self.engine = sqlalchemy.create_engine(db_url)
        self.meta= sqlalchemy.MetaData()
        self.meta.reflect(self.engine)
        self.connection= self.engine.connect()

    def login(self,username,password):
        query= self.meta.tables["user"].select().where(self.meta.tables["user"].c['userName']==username , self.meta.tables["user"].c['pass']==password)
        result= self.connection.execute(query).fetchall()
        if (not result):
            return False
        else:
            return result
    def getAllUsers(self):
        query= self.meta.tables["user"].select()
        result= self.connection.execute(query).fetchall()
        return result
    def getUserById(self,id):
        query= self.meta.tables["user"].select().where(self.meta.tables["user"].c['userID']==id)
        user= self.connection.execute(query).fetchall()
        return user
    def filterUser(self,filter=[]):
        query= self.meta.tables["user"].select().where(*filter)
        user= self.connection.execute(query).fetchall()
        return user
    def register(self,userID, username, password, ScoreID):
        query= self.meta.tables["user"].insert().values(userName=username,password=password,ScoreID=ScoreID,userID=userID)
        done=self.connection.execute(query)
        self.connection.commit()
        if(done):
            print("User created")
            return True
        else:
            print("User not created")
            return False
        
    def deleteUser(self,id):
        query= self.meta.tables["user"].delete().where(self.meta.tables["user"].c['userID']==id)
        done=self.connection.execute(query)
        self.connection.commit()
        if(done):
            print("User deleted")
            return True
        else:
            print("Can't delete The User.")
            return False


class score:
    def __init__(self,db_url):
        self.engine = sqlalchemy.create_engine(db_url)
        self.meta= sqlalchemy.MetaData()
        self.meta.reflect(self.engine)
        self.connection= self.engine.connect()
        self.score = self.meta.tables['score']
        self.user = self.meta.tables['user']
    def getScoreUser(self, UserID):
        query1 = self.user.select().where(self.user.c['userID']==UserID)

        user = self.connection.execute(query1).fetchall()

        ScoreID = user[0][3]

        query2 = self.score.select().where(self.score.c['ScoreID']==ScoreID)

        score = self.connection.execute(query2).fetchall()


        return {
            'ScoreID': score[0][0],
            'UserID': user[0][0]
        }
    def resetScore(self, ScoreID):
        query1 = self.score.select().where(self.user.c['ScoreID']==ScoreID)
        
        score = self.connection.execute(query1).fetchall()

        query2 = self.score.update().where(self.user.c['ScoreID']==score[0][0]).values(ScoreNum=0)

        updatedScore = self.connection.execute(query2)

        self.connection.commit()

        return True