from py_pdf_parser.visualise.main import PDFVisualiser
from py_pdf_parser.loaders import load_file
from py_pdf_parser.components import PDFDocument
from typing import Optional
import tkinter as tk

#bug import
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from enum import IntEnum
from typing import Dict, Optional #,List

#confirmation
from py_pdf_parser.visualise.background import get_pdf_background
from py_pdf_parser.visualise.main import _ElementRectangle
from py_pdf_parser.visualise.main import CustomToolbar
from py_pdf_parser.filtering import ElementList

#refactoring
from custom_visualiser_confirmatiom import Custom_Visualiser_Confirmation
from custom_visualiser_config_window import Custom_Visualiser_Config_Window, MouseButton


STYLES_Confirm = {
    "title": {"color": "#38cc25", "linewidth": 1, "alpha": 0.7},
    "ignored": {"color": "#d41919", "linewidth": 1, "alpha": 0.5},
    "ingredients": {"color": "#2533cc", "linewidth": 1, "alpha": 0.5},
    "step": {"color": "#13d0ed", "linewidth": 1, "alpha": 0.5},
    "note": {"color": "#a010de", "linewidth": 1, "alpha": 0.5},
}


class Custom_Visualiser(
    PDFVisualiser,
    Custom_Visualiser_Confirmation,
    Custom_Visualiser_Config_Window
    ):
    __clicked_elements: Dict[MouseButton, "PDFElement"] = {}
    __info_text: Optional["Text"] = None

    def __init__(self, config_window=False, confirmation=None, **kwargs):
        self.root = tk.Tk()
        self.config_window = config_window
        self.confirmation = confirmation
        super().__init__(root=self.root, width=1000,  **kwargs)
        self.__screen_width = int(self.root.winfo_screenwidth() / 2)
        self.__screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.__screen_width}x{self.__screen_height}+0+0')
        
        self.__ax = self._PDFVisualiser__ax
        self.__fig = self._PDFVisualiser__fig
        if self.confirmation is not None:
            self.confirmation_config()
            
        if self.config_window:
            self.__info_fig, self.__info_text = self.read_config_window()

            self.title = []
            self.ignore = []
            self.note = []
            self.steps = []
            self.ingredient = []
            self.tags = []
            self.__selected_element = None

    def __plot_current_page(self):
        self.__ax.cla()
        # draw PDF image as background
        page = self.document.get_page(self.current_page)
        if self.document._pdf_file_path is not None:
            background = get_pdf_background(
                self.document._pdf_file_path, self.current_page
            )
            self.__ax.imshow(
                background,
                origin="lower",
                extent=[0, page.width, 0, page.height],
                interpolation="kaiser",
            )
        else:
            self.__ax.set_aspect("equal")
            self.__ax.set_xlim([0, page.width])
            self.__ax.set_ylim([0, page.height])

        page = self.document.get_page(self.current_page)
        if self.element_category is not None:
            for key in self.element_category.keys():
                self.__element_style(page.elements & self.element_category[key], STYLES_Confirm[key])

        self._PDFVisualiser__section_visualiser.plot_sections_for_page(page)
        self.__ax.format_coord = self._PDFVisualiser__get_annotations

    def __element_style(self, _elements, style):
        for element in _elements:
            self._PDFVisualiser__plot_element(element, style)

def custom_visualise(
    document: PDFDocument,
    page_number: int = 1,
    elements: Optional["ElementList"] = None,
    show_info: bool = False,
    width: Optional[int] = None,
    height: Optional[int] = None,
):
    global custom_class
    custom_class = CustomVisualiser(document = document)
    custom_class.root.mainloop()

def close_window():
    global custom_class
    custom_class.root.destroy()

if __name__ == '__main__':
    from py_pdf_parser.loaders import load_file 
    document = load_file("Recipe-Book.pdf")
    custom_visualise(document, )