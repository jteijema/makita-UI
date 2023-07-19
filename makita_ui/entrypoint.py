import os
import PySimpleGUI as sg
from pathlib import Path

from asreviewcontrib.makita.config import TEMPLATES_FP
from asreviewcontrib.makita.utils import FileHandler

sg.theme('LightBlue2')


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
                self._show_template_window(values["-OUTPUT-DIR-"])
            elif event == "-ADD-SCRIPT-":
                self._show_add_script_window(values["-OUTPUT-DIR-"])

        window.close()

    def _show_template_window(self, output_dir):
        # Define your templates
        templates = [
            p.stem[9:-4] for p in Path(TEMPLATES_FP).glob("template_*.txt.template")
        ]
        
        data_dir = os.path.join(output_dir, "data")
        if os.path.exists(data_dir):
            dataFolderString = sg.Text(f"Data folder exists at: \n{data_dir}", key="-CREATE-DATA-FOLDER-")
        else:
            dataFolderString = sg.Button("Create Data Folder", key="-CREATE-DATA-FOLDER-")

        template_layout = [
            [sg.Text("--Template--")],
            [sg.Text('Template\t\t'), sg.Combo(templates, size=(20, 1), key="-TEMPLATE-", enable_events=True)],
            [sg.Text('output_dir\t'), sg.InputText(key='template_output_dir', default_text='output')],
            [sg.Text('init_seed\t\t'), sg.InputText(key='init_seed', default_text='400')],
            [sg.Text('model_seed\t'), sg.InputText(key='model_seed', default_text='250')],
            [sg.Text("\t\t", key="-INPUT-FIELD-1-"), sg.InputText(key='field-1')],
            [sg.Button("Generate Template", key="-GENERATE-TEMPLATE-")],
            [sg.Text("\n--Data Folder--")],
            [dataFolderString],
            [sg.Button("Open Data Folder", key="-OPEN-DATA-FOLDER-")],
            [sg.Button("Back", button_color=("white", sg.theme_background_color()), pad=((0, 0), (10, 0)))],
        ]

        window = sg.Window("Template", template_layout)

        def _create_data_dir():
            os.makedirs(data_dir, exist_ok=True)
            sg.popup(f"Data directory created at {data_dir}")

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Back":
                break
            elif event == "-GENERATE-TEMPLATE-":
                from asreviewcontrib.makita.entrypoint import MakitaEntryPoint
                template = MakitaEntryPoint()

                args = [
                        values["-TEMPLATE-"],
                        "-o", str(values['template_output_dir']),
                        "--init_seed", str(values['init_seed']),
                        "--model_seed", str(values['model_seed']),
                    ]

                if values["-TEMPLATE-"] == templates[1]:
                    extra_args = [
                        "--n_runs", str(values['field-1'])
                    ]
                elif values["-TEMPLATE-"] == templates[2]:
                    extra_args = [
                        "--classifiers", str(values['field-1'])
                    ]
                elif values["-TEMPLATE-"] == templates[0]:
                    extra_args = [
                        "--n_priors", str(values['field-1'])
                    ]

                args.extend(extra_args)
                template._template(args, None)
                print(args)
                sg.popup(f"Template generated for {args}")

            elif event == "-TEMPLATE-":
                # basic template
                if values["-TEMPLATE-"] == templates[1]:
                    window["-INPUT-FIELD-1-"].update("n_runs\t\t")
                    window["field-1"].update("1")
                # multiple_models template
                elif values["-TEMPLATE-"] == templates[2]:
                    window["-INPUT-FIELD-1-"].update("classifiers\t")
                    window["field-1"].update("logistic nb rf svm")
                # arfi template
                elif values["-TEMPLATE-"] == templates[0]:
                    window["-INPUT-FIELD-1-"].update("n_priors\t\t")
                    window["field-1"].update("1")

            elif event == "-CREATE-DATA-FOLDER-":
                _create_data_dir()
            elif event == "-OPEN-DATA-FOLDER-":
                os.startfile(data_dir)

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
            [sg.Checkbox("Allow Overwrites", key="-OVERWRITE-", default=True, enable_events=True)],
            [sg.Button("Back", button_color=("white", sg.theme_background_color())), sg.Button("Create")]
        ] 
        window = sg.Window("Add Script", add_script_layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Back":
                break
            elif event == "-OVERWRITE-":
                self.file_handler.overwrite_all = values["-OVERWRITE-"]
                if not values["-OVERWRITE-"]:
                    sg.popup(f"Overwrite setting: {values['-OVERWRITE-']}\nConsole interaction will be required for each file.")
            elif event == "Create":
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
