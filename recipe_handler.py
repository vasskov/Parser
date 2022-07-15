from recipe import Recipe

class Recipe_Handler:
    def __init__(self,book_config,  book_name, pdf_item_list):
        self.book_name = book_name
        self.book_config = book_config
        self.__pdf_item_list = pdf_item_list
        self.manege_recipe_text(self.__pdf_item_list)

    def manege_recipe_text(self, list):
        title = self.__set_title(list)
        recipe_text = self.__set_recipe_text(list)
        note = self.__set_note(list)
        steps = self.__set_steps(list)
        ingredients = self.__set_ingredients(list)
        tags = self.__set_tags(list)
        self.recipe = Recipe(self.book_name,title,recipe_text,note,steps,ingredients,tags)

    def get_recipe(self):
        return self.recipe

    def __pdfelements__to__text(self, item):
        st = ""
        for i in item:
            st += i.text()
        return st

    def __set_title(self, list):
        return list[0].text()

    def __set_recipe_text(self,list):
        return self.__pdfelements__to__text(list[1::])

    def __set_note(self,list):
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