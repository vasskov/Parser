from py_pdf_parser.visualise import visualise
from threading import Thread
from custom_visualiser import Custom_Visualiser
from py_pdf_parser.components import PDFDocument
from typing import Dict, Optional, List
from book_config import Book_Config

class Book_Config_Handler():
    def __init__(self,document, book_name,gui=True):
        self.document = document
        self.pdf_elements = self.document.elements
        self.fonts = self.document.fonts
        self.fonts = list(self.fonts)
        self.fonts.sort()
        self.book_name = book_name
        self.book_config = Book_Config()
        if gui:
            self.run_config_gui()
        else:
            self.run_config_cli()

    def run_config_gui(self):
        self.custom_visualise(self.document,config_window=True,show_info=False)
        #Complite list
        self.gui_Result = self.__result_config_procesed(self.custom_class.Result)
        self.book_config.title.font = self.__get_config_from_dict(self.__get_font, 'title')
        self.book_config.ignore.font = self.__get_config_from_dict(self.__get_font, 'ignored')
        self.book_config.note.font = self.__get_config_from_dict(self.__get_font, 'note')
        self.book_config.steps.font = self.__get_config_from_dict(self.__get_font, 'step')
        self.book_config.ingredient.font = self.__get_config_from_dict(self.__get_font, 'ingredients')
        self.book_config.book_name = self.book_name

        self.__delete_duplicates_font_ids(self.book_config.ingredient, self.book_config.steps)
        self.__delete_duplicates_font_ids(self.book_config.note, self.book_config.ingredient)
        self.__delete_duplicates_font_ids(self.book_config.note, self.book_config.steps)

        self.validation_config(self.custom_class.Result)
        #self.validation_config(self.gui_Result)
        
        #self.create_json_file()

    def __get_config_from_dict(self,function,key):
        return list(set(map(function, self.custom_class.Result[key])))

    def __result_config_procesed(self, dict_config):
        processed_res_dict = {}
        for key in dict_config.keys():
            font_config = list(set(map(self.__get_font, dict_config[key])))
            bounding_box = list(map(self.__get_position, dict_config[key]))
            processed_res_dict[key] = {'font':font_config,'position':bounding_box}
        return processed_res_dict

    def __get_font(self, pdf_element):
        return pdf_element.font

    def __get_position(self, pdf_element):
        return pdf_element.bounding_box

    def run_config_cli(self):
        #cli
        thread = Thread(target=self.make_config_cli, daemon=True)
        thread.start()
        self.custom_visualise(self.document,show_info=True)

    def validation_config(self,rec_dict):
        self.custom_visualise(self.document,confirmation=rec_dict)

    def custom_visualise(
        self,
        document: PDFDocument,
        **kwargs 
    ):
        self.custom_class = Custom_Visualiser(document = document,**kwargs)
        self.custom_class.root.mainloop()

    def make_config_cli(self):
        for i in range(len(self.fonts)):
            print(i,' ', self.fonts[i])
        self.book_config.title = self.make_item_cli('Enter title')
        self.book_config.ignore = self.make_item_cli('Enter ignore')
        #add make item to note, ...
        self.close_window()
    
    def close_window(self):
        self.custom_class.root.destroy()

    def __delete_duplicates_font_ids(self, list_1, list_2):
        list_1.font, list_2.font = list(set(list_1.font) - set(list_2.font)),list(set(list_2.font) - set(list_1.font))


    def make_item_cli(self,text):
        print('\n',text)
        return self.select_cli()

    def select_cli(self):
        selected = []
        while True:
            font = ""
            font = input("Enter font: ")
            if font == "":
                break
            if font.isnumeric():
                if int(font) > len(self.fonts) -1:
                    continue
                selected.append(self.fonts[int(font)])
            else:
                selected.append(font)
        return selected

    def create_json_file(self):
        json = self.book_config.toJSON()
        print(json)
        path = "Result/" + self.book_config.book_name
        with open(path, "w") as f:
            f.write(json)