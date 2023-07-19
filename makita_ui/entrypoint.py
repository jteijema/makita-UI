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

    def _show_add_script_window(self, output_dir):
        # Get the list of available scripts
        available_scripts = [
            p.stem[7:] for p in Path(TEMPLATES_FP).glob("script_*.template")
    ]
        self.file_handler = FileHandler()
        self.file_handler.overwrite_all = True

        add_script_layout = [
            [sg.Text("Select Scripts:")],
            [sg.Listbox(values=available_scripts, size=(30, 6), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
            [sg.Button("Back"), sg.Button("Create")]
        ] 
        window = sg.Window("Add Script", add_script_layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Back":
                break
            elif event == "Create":
                print("Selected scripts: ", values[0])
                selected_scripts = values[0]
                for script in selected_scripts:
                    new_script = self.file_handler.render_file_from_template(
                        script, "script")

                    # export script
                    export_fp = Path(output_dir, script)
                    self.file_handler.add_file(new_script, export_fp)
                sg.popup(f"Created {self.file_handler.total_files} files!\n\n{',  '.join([s for s in selected_scripts])}")
                self.file_handler.total_files = 0

        window.close()

def run_makita_ui():
    interface = MakitaUI()
    interface.execute()

if __name__ == "__main__":
    interface = MakitaUI()
    interface.execute()
