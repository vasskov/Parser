from recipe import Recipe

class Recipe_Handler:
    def __init__(self,book_config,  book_name, pdf_item_list):
        self.book_name = book_name
        self.book_config = book_config
        self.__pdf_item_list = pdf_item_list
        self.manege_recipe_text(self.__pdf_item_list)

    def manege_recipe_text(self, list):
        title = self.__set_title()
        
        note = self.__set_item(self.book_config.note)
        
        ingredients = self.__set_item(self.book_config.ingredient)
        steps = self.__set_item(self.book_config.steps)

        tags = self.__set_tags()
        recipe_text = self.__set_recipe_text()

        self.recipe = Recipe(self.book_name,title,recipe_text,note,steps,ingredients,tags)

    def get_recipe(self):
        return self.recipe

    def __set_title(self):
        title_list = self.__set_item(self.book_config.title)
        return title_list[0]

    def __set_recipe_text(self):
        return list(map(lambda item: item.text(), self.__pdf_item_list))

    def __set_item(self, item):
        text_list = []
        if not item.font:
            return []
        for element in self.__pdf_item_list:
            if element.font in item.font:
                text_list.append(element.text())
                self.__pdf_item_list = self.__pdf_item_list.remove_element(element)
        return text_list

    def __set_tags(self):
        return ['tags place holder']