from py_pdf_parser.visualise.main import PDFVisualiser
from py_pdf_parser.loaders import load_file
from py_pdf_parser.components import PDFDocument
from typing import Optional
import tkinter as tk

#bug import
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from enum import IntEnum
from typing import Dict, Optional, List

#confirmation
from py_pdf_parser.visualise.background import get_pdf_background
from py_pdf_parser.visualise.main import _ElementRectangle
from py_pdf_parser.visualise.main import CustomToolbar
from py_pdf_parser.filtering import ElementList

#refactoring
from custom_visualiser_confirmatiom import Custom_Visualiser_Confirmation

STYLES_Confirm = {
    "title": {"color": "#38cc25", "linewidth": 1, "alpha": 0.7},
    "ignored": {"color": "#d41919", "linewidth": 1, "alpha": 0.5},
    "ingredients": {"color": "#2533cc", "linewidth": 1, "alpha": 0.5},
    "step": {"color": "#13d0ed", "linewidth": 1, "alpha": 0.5},
    "note": {"color": "#a010de", "linewidth": 1, "alpha": 0.5},
}

class MouseButton(IntEnum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    BACK = 8
    FORWARD = 9

class CustomVisualiser(PDFVisualiser, Custom_Visualiser_Confirmation):
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
            self.__info_fig, self.__info_text = self.__read_config_window()

            self.title = []
            self.ignore = []
            self.note = []
            self.steps = []
            self.ingredient = []
            self.tags = []
            self.__selected_element = None
    '''
    def divide_fonts(self, Result_dict):
        by_font = {}
        for key in Result_dict.keys():
            by_font[key] = Result_dict[key]['font']
        print(by_font)
        return by_font
    '''
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

    def __make_interface(self):
        title_button = tk.Button(self.read_window, width=15, text="Title", command=self.__write_title_element)
        ingredients_button = tk.Button(self.read_window, text="Ingredients", command=self.__write_ingredients_element)
        step_button = tk.Button(self.read_window, text="Steps", command=self.__write_steps_element)
        note_button = tk.Button(self.read_window, text="Note", command=self.__write_note_element)
        ignore_button = tk.Button(self.read_window, text="Ignore", command=self.__write_ignore_element)
        done_button = tk.Button(self.read_window, text="Done", command=self.__done_conf)
        #tags will be in separete window

        title_button.pack()
        ingredients_button.pack()
        step_button.pack()
        note_button.pack()
        ignore_button.pack()
        done_button.pack()

    def __done_conf(self):
        print('Done')
        self.Result = {
            'title': self.title,
            'ingredients': self.ingredient,
            'step': self.steps,
            'note': self.note,
            'ignored': self.ignore,
        } 
        print(self.Result)
        self.root.destroy()
        return self.Result

    def __write_title_element(self):
        if self.__selected_element is not None:
            self.title.append(self.__selected_element)
            self.__selected_element = None

    def __write_ingredients_element(self):
        if self.__selected_element is not None:
            self.ingredient.append(self.__selected_element)
            self.__selected_element = None

    def __write_steps_element(self):
        if self.__selected_element is not None:
            self.steps.append(self.__selected_element)
            self.__selected_element = None

    def __write_note_element(self):
        if self.__selected_element is not None:
            self.note.append(self.__selected_element)
            self.__selected_element = None

    def __write_ignore_element(self):
        if self.__selected_element is not None:
            self.ignore.append(self.__selected_element)
            self.__selected_element = None

    def __read_config_window(self):
        self.read_window = tk.Toplevel(self.root)
        self.read_window.geometry(f'{int(self.__screen_width*0.98)}x{int(self.__screen_height*0.65)}+{self.__screen_width*2}+0')
        #read_window.grab_set()

        info_fig = Figure()
        canvas = FigureCanvasTkAgg(info_fig, self.read_window)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.__make_interface()
        self.canvas.mpl_connect("button_press_event", self.__on_mouse_click)

        info_text = info_fig.text(
            0.01,
            0.5,
            "",
            horizontalalignment="left",
            verticalalignment="center",
        )
        return info_fig, info_text

    def __on_mouse_click(self, event: "MouseEvent"):
        print("click")
        if event.button == MouseButton.MIDDLE:
            self.__clear_clicked_elements()
            return
        for rect in self.__ax.patches:
            if not rect.contains(event)[0]:
                continue
            # rect is the rectangle we clicked on!
            self.__clicked_elements[event.button] = rect.element
            self.__selected_element = rect.element
            print(rect.element)
            self.__update_text()
            return

    def __clear_clicked_elements(self):
        self.__clicked_elements = {}
        self.__update_text()

    def _get_element_info(self, element: Optional["PDFElement"]) -> List[str]:
        if not element:
            return ["Click an element to see details"]
        return [
                f"Text: {element.text(stripped=False)}",
                f"Font: {element.font}",
                f"Tags: {element.tags}",
                f"Bounding box: {element.bounding_box}",
                f"Width: {element.bounding_box.width}",
                f"Height: {element.bounding_box.height}",
            ]    

    def __update_text(self):
        self.__info_text.set_text(self.__get_clicked_element_info(self.__clicked_elements))
        self.__info_fig.canvas.draw()

    def __get_clicked_element_info(self, clicked_elements: Dict[MouseButton, "PDFElement"]) -> str:
        left_element = clicked_elements.get(MouseButton.LEFT)
        output = []
        output.append("Clicked element:")
        output.append("---------------------")
        output += self._get_element_info(left_element)
        output.append("")
        return "\n".join(output)

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