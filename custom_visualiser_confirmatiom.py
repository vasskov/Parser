from typing import Dict, Optional, List
from py_pdf_parser.visualise.main import CustomToolbar

class Custom_Visualiser_Confirmation:
    def confirmation_config(self):
        prepared_res = self.__prepare_result_to_plot(self.confirmation)
        self.element_category = self.__element_category(prepared_res)
        #prepared_res = self.divide_fonts(self.confirmation)
        #self.element_category = self.__element_category(prepared_res)
        self._Custom_Visualiser__plot_current_page()
        self.toolbar.destroy()
        self.custom_toolbar = CustomToolbar(
                self.canvas,
                self.root,
                next_page_callback=self.__next_page,
                first_page_callback=self.__first_page,
                previous_page_callback=self.__previous_page,
                last_page_callback=self.__last_page,
        )
    
    def __prepare_result_to_plot(self, Result_dict:Dict):
        prepared_dict = {}
        keys = Result_dict.keys()
        for key in keys:
            print(f'{key}:{Result_dict[key]}')
            if not Result_dict[key]: continue
            prepared_dict[key] = []
            for item in Result_dict[key]:
                prepared_dict[key].append(item.font)
        print(prepared_dict)
        return prepared_dict

    def __element_category(self, prepared_dict):
        _elements = self.document.elements
        keys = prepared_dict.keys()
        elements_category = {}
        for key in keys:
            elements_category[key] = _elements
        for element in _elements:
            elem_font = element.font
            for key in keys:
                if elem_font not in prepared_dict[key]:
                    elements_category[key] = elements_category[key].remove_element(element)
        return elements_category

    def __next_page(self):
        current_page_idx = self.document.page_numbers.index(self.current_page)
        next_page_idx = min(current_page_idx + 1, self.document.number_of_pages)
        next_page = self.document.page_numbers[next_page_idx]
        self.__set_page(next_page)

    def __last_page(self):
        self.__set_page(max(self.document.page_numbers))

    def __first_page(self):
        self.__set_page(min(self.document.page_numbers))

    def __previous_page(self):
        current_page_idx = self.document.page_numbers.index(self.current_page)
        previous_page_idx = max(current_page_idx - 1, 0)
        previous_page = self.document.page_numbers[previous_page_idx]
        self.__set_page(previous_page)

    def __set_page(self, page_number: int):
        if self.current_page != page_number:
            self.current_page = page_number
            self._Custom_Visualiser__plot_current_page()
            self._Custom_Visualiser__fig.canvas.draw()
