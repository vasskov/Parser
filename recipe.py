import json
import time
from hashlib import md5
from BookConfigaration import Book_Config
from dataclasses import dataclass

@dataclass
class Recipe():
    def __init__(self, book_name,title,recipe_text,note,steps,ingredients,tags):
        self.version = 0.1
        self.source = book_name
        named_tuple = time.localtime()
        self.creation_time = time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
        self.title = title
        self.recipe_text = recipe_text
        self.note = note
        self.steps = steps
        self.ingredients = ingredients
        self.tags = tags
        self.recipe_hash = self.hashing()

    def __str__(self):
        text = str(self.__dict__)
        replace_list = [('{',''),("'",''),('}',''),(',','\n'),('version: ', '\nRecipe\nversion: ')]
        for key, valt in replace_list:
            text = text.replace(key, valt)
        text_en = text.encode("ascii", "ignore")
        text = text_en.decode()
        return text

    def hashing(self):
        text = self.__str__()
        return md5(text.encode()).hexdigest()

    def toJSON(self, human_read=True):
        #return json.dumps({"try":"recipe"})
        return json.dumps(self, default=lambda o: o.__dict__, indent=4 if human_read else None)
        #return json.dumps(self, default=lambda o: o.__dict__)
        #return json.dumps(self.__str__())

if __name__ == '__main__':
    pass