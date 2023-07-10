import Connection
import classes


user = classes.user(Connection.DB_URI)

print(user.deleteUser(3))