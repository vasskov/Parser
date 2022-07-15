from recipe import Recipe
import json
import os

#Upload result to google drive
class MakeRecipe():
    Recipe_List = []
    def __init__(self, book_name, book_config, filtered_List):
        self.book_name = book_name
        self.book_config = book_config
        self.List = filtered_List
        self.make_recipe(filtered_List)

        self.path = "Result/"
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.make_result()
  

    def make_recipe(self, List):
        for items in List:
            recipe = Recipe(self.book_config,self.book_name, items)
            self.Recipe_List.append(recipe)
        return self.Recipe_List

    #def toText(self, item):
    #    #from pdf_elem to text
    #    st = ""
    #    for i in item:
    #        st += i.text()
    #    return st

    def write2file(self, path, info:str):
        with open(path, "w") as f:
            f.write(info)

    def make_result_json(self):
        all_json = '['
        json_line = "\n,"
        cur_path = self.path + self.Recipe_List[-1].source
        if not os.path.exists(cur_path):
            os.mkdir(cur_path)
        if not os.path.exists(cur_path + "/JSON"):
            os.mkdir(cur_path + "/JSON")
        for recipe in self.Recipe_List:
            if all_json != '[':
                all_json = all_json + json_line + recipe.toJSON()
            else:
                all_json = all_json + "\n" + recipe.toJSON()
            
            self.write2file(cur_path + "/JSON/" + recipe.title + ".json", recipe.toJSON())
        all_json += "]"
        self.write2file(cur_path + "/" + recipe.source + ".json", all_json)

    def make_result_txt(self):
        text_line = "\n\n"
        cur_path = self.path + self.Recipe_List[0].source
        if not os.path.exists(cur_path):
            os.mkdir(cur_path)
        if not os.path.exists(cur_path + "/TXT"):
            os.mkdir(cur_path + "/TXT")
        all_text = ""
        for recipe in self.Recipe_List:
            all_text = all_text + text_line + str(recipe)
            self.write2file(cur_path + "/TXT/" + recipe.title + ".txt", str(recipe))
        self.write2file(cur_path + "/"+ recipe.source + ".txt", all_text)

    def make_result(self):
        self.make_result_json()
        self.make_result_txt()

if __name__ == '__main__':
    #make = MakeRecipe("Recipe-Book", MainList)
    pass