import json
from dataclasses import dataclass
'''
- seve config to json
'''
@dataclass
class PDF_Item_ids():
    font = []
    box = []

    def toJSON(self):
        return json.dumps(self, indent = 4)

class Book_Config():
    def __init__(self):
        self.book_name = ''
        self.title = PDF_Item_ids()
        self.ignore = PDF_Item_ids()
        # make: note, steps, ingredient, tags
        self.note = PDF_Item_ids()
        self.steps = PDF_Item_ids()
        self.ingredient = PDF_Item_ids()
        self.tags = PDF_Item_ids()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent = 4)
    
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