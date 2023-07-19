import os
import PySimpleGUI as sg
from pathlib import Path

from asreviewcontrib.makita.config import TEMPLATES_FP
from asreviewcontrib.makita.utils import FileHandler


class MakitaUI:
    def __init__(self):
        self.layout = self._create_layout()

    def _create_layout(self):
        return [
            [sg.Button("Template", key="-TEMPLATE-")],
            [sg.Button("Add Script", key="-ADD-SCRIPT-")],
            [sg.Text("Output Directory: "), sg.Input(default_text=os.getcwd(), key="-OUTPUT-DIR-"), sg.FolderBrowse(target="-OUTPUT-DIR-")],
            [sg.Button("Exit", button_color=("white", sg.theme_background_color()), key="-EXIT-", pad=((0, 0), (10, 0)))]
        ]

    def execute(self):
        window = sg.Window("Makita UI", self.layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "-EXIT-"):
                break
            elif event == "-TEMPLATE-":
                self._show_template_window()
            elif event == "-ADD-SCRIPT-":
                self._show_add_script_window(values["-OUTPUT-DIR-"])

        window.close()

    def _show_template_window(self):
        template_layout = [
            # Add template specific elements here
            [sg.Text("Template Window")],
            [sg.Button("Back")]
        ]
        window = sg.Window("Template", template_layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Back":
                break

        window.close()


        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == "Click Me":
                window["-OUTPUT-"].update("Button Clicked!")

        window.close()

def run_makita_ui():
    interface = MakitaUI()
    interface.execute()

if __name__ == "__main__":
    run_makita_ui()