import json
import time
from hashlib import md5
from BookConfigaration import BookConfig

class Recipe():
    def __init__(self,book_config,  book, item):
        self.version = 0.1
        self.source = book
        named_tuple = time.localtime()
        self.creation_time = time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
        self.manege_recipe_text(item)
        self.recipe_hash = self.hashing()
        
    def manege_recipe_text(self, list):
        self.title = self.set_title(list)
        self.recipe_text = self.set_recipe_text(list)
        self.note = self.set_note(list)
        self.steps = self.set_steps(list)
        self.ingredients = self.set_ingredients(list)
        self.tags = self.set_tags(list)

    def toText(self, item):
        st = ""
        for i in item:
            st += i.text()
        return st

    def set_title(self, list):
        return list[0].text()

    def set_recipe_text(self,list):
        return self.toText(list[1::])

    def set_note(self,list):
        return ['note place holder']

    def set_steps(self, list):
        return ['steps place holder']

    def set_ingredients(self, list):
        return ['ingredients place holder']

    def set_tags(self, list):
        return ['tags place holder']

    def hashing(self):
        text = self.__str__()
        return md5(text.encode()).hexdigest()

    def __str__(self):
        text = str(self.__dict__)
        replace_list = [('{',''),("'",''),('}',''),(',','\n'),('version: ', '\nRecipe\nversion: ')]
        for key, valt in replace_list:
            text = text.replace(key, valt)
        text_en = text.encode("ascii", "ignore")
        text = text_en.decode()
        return text

    def toJSON(self, human_read=True):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4 if human_read else None)

if __name__ == '__main__':
    pass