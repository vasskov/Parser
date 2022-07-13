import json
from py_pdf_parser.visualise import visualise
from threading import Thread
from Custom_Visualiser import CustomVisualiser#,custom_visualise, close_window, custom_class

from py_pdf_parser.components import PDFDocument
from typing import Dict, Optional, List


'''
- make config
- option to choose
- seve config to json
- volidate gui visualse
- conflict resolution list
'''

class BookConfig():
    def __init__(self, document, gui=True):
        self.document = document
        self.pdf_elements = self.document.elements
        self.fonts = self.document.fonts
        self.fonts = list(self.fonts)
        self.fonts.sort()

        self.title = []
        self.ignore = []
        # make: note, steps, ingredient, tags
        self.note = []
        self.steps = []
        self.ingredient = []
        self.tags = []

        if gui:
            self.run_config_gui()
        else:
            self.run_config_cli()
        

    def run_config_gui(self):
        self.custom_visualise(self.document,config_window=True,show_info=False)
        #Complite list
        self.gui_Result = self.__result_config_procesed(self.custom_class.Result)
        self.title = list(map(self.__get_font, self.custom_class.Result['title']))
        self.ignore = list(map(self.__get_font, self.custom_class.Result['ignored']))
        self.note = self.custom_class.Result['note']
        self.steps = self.custom_class.Result['step']
        self.ingredient = self.custom_class.Result['ingredients']
        
        self.validation_config(self.custom_class.Result)
        #self.validation_config(self.gui_Result)

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

    def custom_visualise(
        self,
        document: PDFDocument,
        **kwargs
        
    ):
        self.custom_class = CustomVisualiser(document = document,**kwargs)# config_window=config_window)
        self.custom_class.root.mainloop()

    def make_config_cli(self):
        for i in range(len(self.fonts)):
            print(i,' ', self.fonts[i])
        self.title = self.make_item_cli('Enter title')
        self.ignore = self.make_item_cli('Enter ignore')
        #add make item to note, ...
        self.close_window()
    
    def close_window(self):
        self.custom_class.root.destroy()

    def conflict_less():
        
        pass
    def common_member(a, b):
        result = []
        for x in list1:
            for y in list2:
                if x == y:
                    result.append(x)
        if result.__len__() == 0: return None
        else: return result

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

    def toJSON(self, dict_config):
        return json.dumps(dict_config, indent = 4)

    def validation_config(self,rec_dict):
        self.custom_visualise(self.document,confirmation=rec_dict)
        '''
        book_cong = BookConfig()
        filtered = Filtering(document.elements, book_cong)
        for List in filtered.Result_Recipes_List:
            for p in List:
                print(p)
            #visualise(document,show_info=True, elements=List)
        print(len(filtered.Result_Recipes_List))
        '''
        pass

if __name__ == '__main__':
    from py_pdf_parser.loaders import load_file 
    document = load_file("Recipe-Book.pdf")
    book_config = BookConfig(document)
    #custom_visualise(document, )