from py_pdf_parser.filtering import ElementList
from py_pdf_parser.visualise import visualise
from BookConfigaration import BookConfig

class Filtering():
    def __init__(self, pdf_elememts, book_config):
        self.book_config = book_config
        self.pdf_elements = pdf_elememts
        self.title_fonts = self.find_title(self.book_config.title)
        self.Result_Recipes_List = self.get_recipe_list(self.pdf_elements)

    def find_title(self, Filt_by:list):
        List = self.pdf_elements.filter_by_fonts(*Filt_by)
        return List

    def make_recipe_between(self, start, end):
        List = self.pdf_elements.between(start, end, inclusive=True)
        List = List.remove_element(end)
        return List

    def filter_ignored_fonts(self, List):
        for i in List:
            if i.font in self.book_config.ignore:
                List = List.remove_element(i)
        return List

    def filter_recipes_maneger(self, List):
        List = self.filter_ignored_fonts(List)
        return List

    def get_recipe_list(self, pdf_elements):
        Res_List = []
        start_recipe = None
        end_recipe = None
        fonts = self.title_fonts
        for item in pdf_elements:
            if item in fonts:
                if start_recipe is None:
                    start_recipe = item
                else:
                    end_recipe = item
                    List = self.make_recipe_between(start_recipe,end_recipe)
                    List = self.filter_recipes_maneger(List)
                    Res_List.append(List)
                    start_recipe = end_recipe
        return Res_List

    def page_based_recipe_book():
        #olny 1 recipe per page
        pass


if __name__ == '__main__':
    pass