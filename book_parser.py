from py_pdf_parser import loaders
from py_pdf_parser.visualise import visualise

#my scripts imports
from filtering import Filtering
#from BookConfigaration import BookConfig
from Book_Handler import Book_Config_Handler
from make_recipe_ import MakeRecipe

import tkinter as tk
#from tkinter import filedialog as fd

def load_book():
    #load book place holder
    root = tk.Tk()
    root.geometry('550x250')
    filetypes = (
        ('text files', '*.pdf'),
        ('All files', '*.*')
    )
    #while True:
    #    filename = tk.filedialog.askopenfilename()
    #    if'.pdf' in filename: break
    #root.destroy()
    
    #return filename
    return "Recipe-Book.pdf"
    
def main():
    book_name = load_book()
    print('loading....')
    document = loaders.load_file(book_name)
    pdf_elements = document.elements

    #Add validation filtering gui
    book_handler = Book_Config_Handler(document,book_name)
    Book_Configuration = book_handler.book_config


    filtering_class = Filtering(pdf_elements, Book_Configuration)
    filtered_book_list = filtering_class.Result_Recipes_List

    make_recipe = MakeRecipe(book_name, Book_Configuration, filtered_book_list)


    print('_1_2_')

def ignore_try():
        i = 0
        for item in pdf_elem:
            if i % 2 == 0:
                item.ignore()
            i += 1

if __name__ == '__main__':
    main()

#visualise(document,page_number=3, show_info=True, elements=pdf_elem)