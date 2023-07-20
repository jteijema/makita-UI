import os
import PySimpleGUI as sg
from pathlib import Path

from asreviewcontrib.makita.config import TEMPLATES_FP
from makita_ui import layout

sg.theme('LightBlue2')


class MakitaUI:
    def __init__(self):
        self.layout = layout._main_layout()

    def execute(self):
        window = sg.Window("Makita UI", self.layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "-EXIT-":
                break
            elif event == "-TEMPLATE-":
                self._show_template_window()
            elif event == "-ADD-SCRIPT-":
                self._show_add_script_window()

        window.close()

    def _show_template_window(self):
        '''Show the template window.'''

        # Import and create template object
        print("Importing template object, this may take some time...""")
        from asreviewcontrib.makita.entrypoint import MakitaEntryPoint
        template = MakitaEntryPoint()

        # Define templates
        templates = [
            p.stem[9:-4] for p in Path(TEMPLATES_FP).glob("template_*.txt.template")
        ]
        
        # Create the layout
        data_dir = os.path.join(os.getcwd(), "data")
        window = sg.Window("Template", layout._template_layout(templates, data_dir))

        # Event loop
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Back":
                break
            elif event == "-OPEN-WORK-FOLDER-":
                os.startfile(os.getcwd())
            elif event == "-GENERATE-TEMPLATE-":
                # check if a template is selected
                if values["-TEMPLATE-"] == "":
                    sg.popup("No template selected, please select a template.")
                    continue

                # check if data folder exists
                if not os.path.exists(data_dir):
                    sg.popup("Data folder does not exist, please create a data folder.")
                    continue

                # check if data folder has csv, xslx or txt files
                if not any(f.endswith((".csv", ".xlsx", ".ris")) for f in os.listdir(data_dir)):
                    sg.popup("Data folder does not contain data.")
                    continue

                # check if working directory is empty
                if len(os.listdir(os.getcwd())) != 1:
                    sg.popup("Working directory is not empty.\nOverwriting files requires console interaction.")

                args = [
                        values["-TEMPLATE-"],
                        "-s", data_dir,
                        "-o", str(values['template_output_dir']),
                        "--init_seed", str(values['init_seed']),
                        "--model_seed", str(values['model_seed']),
                    ]

                if values["-TEMPLATE-"] == templates[1]:
                    extra_args = [
                        "--n_runs", str(values['n_runs'])
                    ]
                elif values["-TEMPLATE-"] == templates[2]:
                    extra_args = [
                        "--classifiers"] + str(values['classifiers']).split() + [
                        "--feature_extractors"] + str(values['feature_extractors']).split()
                elif values["-TEMPLATE-"] == templates[0]:
                    extra_args = [
                        "--n_priors", str(values['n_priors'])
                    ]

                args.extend(extra_args)
                template._template(args, None)
                sg.popup_scrolled(f"Succes!\n\nTemplate generated for:\n\n{args}", size=(50, 8))

            elif event == "-TEMPLATE-":
                # basic template
                if values["-TEMPLATE-"] == templates[1]:
                    layout._basic_parameters(window)
                # multiple_models template
                elif values["-TEMPLATE-"] == templates[2]:
                    layout._arfi_parameters(window)
                # arfi template
                elif values["-TEMPLATE-"] == templates[0]:
                    layout._mm_parameters(window)

            elif event == "-CREATE-DATA-FOLDER-":
                os.makedirs(data_dir, exist_ok=True)
                sg.popup(f"Data directory created at {data_dir}")
            elif event == "-OPEN-DATA-FOLDER-":
                os.startfile(data_dir)

        window.close()



    def _show_add_script_window(self):
        '''Show the add script window.'''

        # Import and create file handler
        from asreviewcontrib.makita.utils import FileHandler
        self.file_handler = FileHandler()
        self.file_handler.overwrite_all = True

        # Get the list of available scripts
        available_scripts = [
            p.stem[7:] for p in Path(TEMPLATES_FP).glob("script_*.template")
        ]

        # Create the layout
        window = sg.Window("Add Script", layout._script_layout(available_scripts) )

        # Event loop
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Back":
                break
            elif event == "-OVERWRITE-":
                self.file_handler.overwrite_all = values["-OVERWRITE-"]
                if not values["-OVERWRITE-"]:
                    sg.popup(f"Overwrite setting: {values['-OVERWRITE-']}\nConsole interaction will be required for overwriting existing files.")
            elif event == "Create":
                selected_scripts = values["-SCRIPTS-"]
                for script in selected_scripts:
                    new_script = self.file_handler.render_file_from_template(
                        script, "script")

                    # export script
                    export_fp = Path(values["-OUTPUT-DIR-"], script)
                    self.file_handler.add_file(new_script, export_fp)
                sg.popup(f"Created {self.file_handler.total_files} files!\n\n{',  '.join([s for s in selected_scripts])}")
                self.file_handler.total_files = 0
        window.close()


def run_makita_ui():
    '''Run the Makita UI.'''
    interface = MakitaUI()
    interface.execute()

if __name__ == "__main__":
    run_makita_ui()
