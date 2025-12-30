
class Recipe:

    def __init__(self, dico):
        self.id = dico["id"]
        self.diet = dico["diet"]
        self.course = dico["course"]
        self.cuisine = dico["cuisine"]
        self.rating = dico["rating"]
        self.description = dico["description"]
        self.recipe_title = dico["recipe_title"]
        self.vote_count = dico["vote_count"]
        self.url = dico["url"]
        self.tags = dico["tags"]
        self.category = dico["category"]
        self.author = dico["author"]
        self.instructions = dico["instructions"]
        self.ingredients = dico["ingredients"]
        self.prep_time = dico["prep_time"]
        self.cook_time = dico["cook_time"]
        self.record_health = dico["record_health"]

        # recipe_title, url, record_health, vote_count, rating, description, cuisine, course, diet, prep_time, cook_time, ingredients, instructions, author, tags, category

    def getAverageRating(self):
        return self.rating / self.vote_count

