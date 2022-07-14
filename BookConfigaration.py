import json
#from py_pdf_parser.visualise import visualise
#from threading import Thread
from Custom_Visualiser import CustomVisualiser#,custom_visualise, close_window, custom_class

from py_pdf_parser.components import PDFDocument
from typing import Dict, Optional, List

from dataclasses import dataclass
'''
- make config
- option to choose
- seve config to json
- volidate gui visualse
- conflict resolution list
'''
@dataclass
class PDF_Item_ids():
    font = []
    box = []

class Book_Config():
    def __init__(self):
        self.title = PDF_Item_ids()
        self.ignore = PDF_Item_ids()
        # make: note, steps, ingredient, tags
        self.note = PDF_Item_ids()
        self.steps = PDF_Item_ids()
        self.ingredient = PDF_Item_ids()
        self.tags = PDF_Item_ids()

    def toJSON(self, dict_config):
        return json.dumps(dict_config, indent = 4)
    
    def get_key(self):
        return vars(self).keys()



if __name__ == '__main__':
    book_config = Book_Config()
    book_config.steps.box.append(5)
    print(book_config.get_key())
    #custom_visualise(document, )
    for atrib in book_config.get_key():
        getattr(book_config, atrib, font.append(5))
    #for atrib in book_config.get_key():
        print(book_config.atrib.font)