import json, sqlite3
from app import app
from app.models.Recipe import Recipe
from app.models.RecipeDAOInterface import RecipeDAOInterface

class RecipeSqliteDAO(RecipeDAOInterface):
	"""
	Recipe data access object dédié à SQLite
	"""

	def __init__(self):
		self.databasename = app.static_folder + '/data/recipes.db'
		
	def _getDbConnection(self):
		""" connection à la base de données. Retourne l'objet connection """
		conn = sqlite3.connect(self.databasename)
		conn.row_factory = sqlite3.Row
		return conn

	def findAll(self):
		""" trouve toutes les recettes """
		conn = self._getDbConnection()
		recipes = conn.execute('SELECT * FROM recipes').fetchall()
		instances = list()
		for recipe in recipes:
			instances.append(Recipe(dict(recipe)))
		conn.close()
		return instances
	
	def findByDietSubword(self, diet_term):
		conn = self._getDbConnection()
		recipes = conn.execute("SELECT * FROM recipes WHERE diet LIKE :pattern ", {"pattern":f"%{diet_term}%"}).fetchall()
		conn.close()
		instances = [Recipe(dict(recipe)) for recipe in recipes]
		return instances

	def findByCourseSubword(self, course_term):
		conn = self._getDbConnection()
		recipes = conn.execute("SELECT * FROM recipes WHERE course LIKE :pattern ", {"pattern":f"%{course_term}%"}).fetchall()
		conn.close()
		instances = [Recipe(dict(recipe)) for recipe in recipes]
		return instances
	
	def getNumberOfElements(self):
		conn = self._getDbConnection()
		num = conn.execute("SELECT COUNT(*) FROM recipes;").fetchone()
		conn.close()
		return num
	
	def getUniqueCuisines(self):
		conn = self._getDbConnection()
		cuisines = conn.execute("SELECT DISTINCT cuisine FROM recipes;").fetchall()
		conn.close()
		return [t["cuisine"] for t in cuisines]
	
	def getUniqueDiets(self):
		conn = self._getDbConnection()
		diets = conn.execute("SELECT DISTINCT diet FROM recipes;").fetchall()
		conn.close()
		return [t["diet"] for t in diets]
	
	def getTags(self):
		conn = self._getDbConnection()
		tags = conn.execute("SELECT DISTINCT tags FROM recipes;").fetchall()
		conn.close()
		return [t["tags"] for t in tags]