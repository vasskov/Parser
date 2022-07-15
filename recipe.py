import json
import time
from hashlib import md5
from BookConfigaration import Book_Config

class Recipe():
    def __init__(self,book_config,  book_name, pdf_item_list):

        self.version = 0.1
        self.book_config = book_config
        self.source = book_name
        #self.__pdf_item_list = pdf_item_list
        named_tuple = time.localtime()
        self.creation_time = time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
        self.manege_recipe_text(pdf_item_list, book_config)
        self.recipe_hash = self.hashing()
        print(self.__dict__)
        
    def manege_recipe_text(self, list, book_config):
        self.title = self.__set_title(list)
        self.recipe_text = self.__set_recipe_text(list)
        self.note = self.__set_note(list, book_config)
        self.steps = self.__set_steps(list)
        self.ingredients = self.__set_ingredients(list)
        self.tags = self.__set_tags(list)

    def __pdfelements__to__text(self, item):
        st = ""
        for i in item:
            st += i.text()
        return st

    def __set_title(self, list):
        return list[0].text()

    def __set_recipe_text(self,list):
        return self.__pdfelements__to__text(list[1::])

    def __set_note(self,list, book_config):
        return ["note"]
        if not self.book_config.note.font:
            return
        for element in self.__pdf_item_list:
            print(element.font)
            print(self.book_config.note.font)
            if element.font in self.book_config.note.font:
                print(True)
                note.append(element.text())
                self.__pdf_item_list.remove_element(element)
        return note

    def __set_steps(self, list):
        return ['steps place holder']

    def __set_ingredients(self, list):
        return ['ingredients place holder']

    def __set_tags(self, list):
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
        #return json.dumps({"try":"recipe"})
        return json.dumps(self, default=lambda o: o.__dict__, indent=4 if human_read else None)
        #return json.dumps(self, default=lambda o: o.__dict__)
        #return json.dumps(self.__str__())

if __name__ == '__main__':
    pass