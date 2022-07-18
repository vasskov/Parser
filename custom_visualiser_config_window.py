import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict, Optional, List
from enum import IntEnum

class MouseButton(IntEnum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    BACK = 8
    FORWARD = 9

class Custom_Visualiser_Config_Window:
    def read_config_window(self):
        self.__screen_width = int(self.root.winfo_screenwidth() / 2)
        self.__screen_height = self.root.winfo_screenheight()
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

    def __on_mouse_click(self, event: "MouseEvent"):
        print("click")
        if event.button == MouseButton.MIDDLE:
            self.__clear_clicked_elements()
            return
        for rect in self._Custom_Visualiser__ax.patches:
            if not rect.contains(event)[0]:
                continue
            # rect is the rectangle we clicked on!
            self._Custom_Visualiser__clicked_elements[event.button] = rect.element
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
        self._Custom_Visualiser__info_text.set_text(
            self.__get_clicked_element_info(self._Custom_Visualiser__clicked_elements)
            )
        self._Custom_Visualiser__info_fig.canvas.draw()

    def __get_clicked_element_info(self, clicked_elements: Dict[MouseButton, "PDFElement"]) -> str:
        left_element = clicked_elements.get(MouseButton.LEFT)
        output = []
        output.append("Clicked element:")
        output.append("---------------------")
        output += self._get_element_info(left_element)
        output.append("")
        return "\n".join(output)