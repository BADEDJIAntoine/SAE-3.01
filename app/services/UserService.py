
from app.models.UserDAO import UserSqliteDAO as UserDAO

class UserService():
	"""
	Classe dédiée à la logique des utilisateurs
	"""
	def __init__(self):
		self.udao = UserDAO()

	def getUserByUsername(self, nom_utilisateur):
		res = self.udao.findByUsername(nom_utilisateur)
		# petit ajout : ici in verifie si res est une liste. Si ce n'est pas le cas, nous l'imbriquons dans une liste
		if type(res) is not list: 
			res = [res] 
		return res

	def getUsers(self):
		return self.udao.findAll()
	
	def signin(self, nom_utilisateur, motdepasse):
		return self.udao.createUser(nom_utilisateur, motdepasse)

	def login(self, nom_utilisateur, motdepasse):
		return self.udao.verifyUser(nom_utilisateur, motdepasse)

