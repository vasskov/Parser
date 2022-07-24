from py_pdf_parser import loaders

#my scripts imports
from filtering import Filtering
from book_config_handler import Book_Config_Handler
from make_recipe_ import MakeRecipe

import tkinter as tk

#logging
import sys
import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logging.basicConfig(filename="error.log", level=logging.ERROR)
logger.addHandler(handler)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


root = tk.Tk()
root.title('Application')
root.geometry('550x250')


def load_book():
    filetypes = (
        ('text files', '*.pdf'),
        ('All files', '*.*')
    )
    filename = tk.filedialog.askopenfilename(
        title='Open a file',
        initialdir='/Books',
        filetypes=filetypes
    )
    print(filename)

    book_name = filename.split("/")[-1]
    print(book_name)
    return book_name
    
def main():
    sys.excepthook = handle_exception
    tk_main_window()
    root.mainloop()
    print('end')

def procces_book(book_name):
    print('loading....')
    document = loaders.load_file('Book/'+book_name)
    pdf_elements = document.elements

    book_handler = Book_Config_Handler(document,book_name)
    Book_Configuration = book_handler.book_config

    filtering_class = Filtering(pdf_elements, Book_Configuration)
    filtered_book_list = filtering_class.Result_Recipes_List
    
    make_recipe = MakeRecipe(book_name, Book_Configuration, filtered_book_list)

def book_manage():
    print("book_managing")
    book_name = load_book()
    root.destroy()
    procces_book(book_name)

def update_app():
    print("Updating")

def tk_main_window():
    select_file_button = tk.Button(root, text="Select Book", command=book_manage)
    update_app_button = tk.Button(root, text="Update program", command=update_app)

    select_file_button.pack()
    update_app_button.pack()

if __name__ == '__main__':
    main()