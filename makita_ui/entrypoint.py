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
            [sg.Text("Welcome to Makita UI!", font=("Arial", 14, "bold"))],
            [sg.Text("This interface allows you to generate templates and scripts for the ASReview Makita extension.")],
            [sg.Text("Select an option below to get started:")],
            [sg.Button("Template", key="-TEMPLATE-")],
            [sg.Button("Add Script", key="-ADD-SCRIPT-")],
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
                self._show_add_script_window()

        window.close()

    def _create_template_layout(self, templates, dataFolderString):
        return [
            [sg.Text("Work Folder", font=("Arial", 14, "bold"))],
            [sg.Text(f"Current working directory: \n {os.getcwd()}")],
            [sg.Button("Open work Folder", key="-OPEN-WORK-FOLDER-")],
            [sg.Text("\nTemplate", font=("Arial", 14, "bold"))],
            [sg.Text("Select a template to generate:")],
            [sg.Text('Template\t\t'), sg.Combo(templates, size=(43, 1), key="-TEMPLATE-", enable_events=True)],
            [sg.Text('output_dir\t'), sg.InputText(key='template_output_dir', default_text='output')],
            [sg.Text('init_seed\t\t'), sg.InputText(key='init_seed', default_text='400')],
            [sg.Text('model_seed\t'), sg.InputText(key='model_seed', default_text='250')],
            [sg.Text('n_runs\t\t', visible=False, key='n_runs_text'), sg.InputText(key='n_runs', default_text='1', visible=False)],
            [sg.Text('n_priors\t\t', visible=False, key='n_priors_text'), sg.InputText(key='n_priors', default_text='1', visible=False)],
            [sg.Text('classifiers\t', visible=False, key='classifiers_text'), sg.InputText(key='classifiers', default_text='logistic nb rf svm', visible=False)],
            [sg.Text('feature_extractors\t', visible=False, key='feature_extractors_text'), sg.InputText(key='feature_extractors', default_text='doc2vec sbert tfidf', visible=False)],
            [sg.Button("Generate Template", key="-GENERATE-TEMPLATE-")],
            [sg.Text("\nData Folder", font=("Arial", 14, "bold"))],
            [dataFolderString],
            [sg.Button("Open Data Folder", key="-OPEN-DATA-FOLDER-")],
            [sg.Button("Back", button_color=("white", sg.theme_background_color()), pad=((0, 0), (10, 0)))],
        ]

    def _show_template_window(self):
        from asreviewcontrib.makita.entrypoint import MakitaEntryPoint
        # Define your templates
        templates = [
            p.stem[9:-4] for p in Path(TEMPLATES_FP).glob("template_*.txt.template")
        ]
        
        data_dir = os.path.join(os.getcwd(), "data")
        if os.path.exists(data_dir):
            # load all the files in the data folder
            data_files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
            dataFolderString = sg.Text(f"Files in data folder:\n{', '.join(data_files)}")
        else:
            dataFolderString = sg.Button("Create Data Folder", key="-CREATE-DATA-FOLDER-")

        template_layout = self._create_template_layout(templates, dataFolderString)

        window = sg.Window("Template", template_layout)

        def _create_data_dir():
            os.makedirs(data_dir, exist_ok=True)
            sg.popup(f"Data directory created at {data_dir}")

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Back":
                break
            elif event == "-OPEN-WORK-FOLDER-":
                os.startfile(os.getcwd())
            elif event == "-GENERATE-TEMPLATE-":
                # check if data folder exists
                if not os.path.exists(data_dir):
                    sg.popup("Data folder does not exist, please create a data folder.")
                    continue
                # check if data folder is empty
                if len(os.listdir(data_dir)) == 0:
                    sg.popup("Data folder is empty, please add data to the data folder.")
                    continue
                # check if working directory is empty
                if len(os.listdir(os.getcwd())) != 1:
                    sg.popup("Working directory is not empty.\nOverwriting files requires console interaction.")

                template = MakitaEntryPoint()

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
                        "--classifiers", str(values['classifiers']).split(" "),
                        "--feature_extractors", str(values['feature_extractors']).split(" "),
                    ]
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
                    window["n_runs_text"].update(visible=True)
                    window["n_runs"].update(visible=True)
                    window["n_priors_text"].update(visible=False)
                    window["n_priors"].update(visible=False)
                    window["classifiers_text"].update(visible=False)
                    window["classifiers"].update(visible=False)
                    window["feature_extractors_text"].update(visible=False)
                    window["feature_extractors"].update(visible=False)
                # multiple_models template
                elif values["-TEMPLATE-"] == templates[2]:
                    window["classifiers_text"].update(visible=True)
                    window["classifiers"].update(visible=True)
                    window["feature_extractors_text"].update(visible=True)
                    window["feature_extractors"].update(visible=True)
                    window["n_priors_text"].update(visible=False)
                    window["n_priors"].update(visible=False)
                    window["n_runs_text"].update(visible=False)
                    window["n_runs"].update(visible=False)
                # arfi template
                elif values["-TEMPLATE-"] == templates[0]:
                    window["n_priors_text"].update(visible=True)
                    window["n_priors"].update(visible=True)
                    window["n_runs_text"].update(visible=False)
                    window["n_runs"].update(visible=False)
                    window["classifiers_text"].update(visible=False)
                    window["classifiers"].update(visible=False)
                    window["feature_extractors_text"].update(visible=False)
                    window["feature_extractors"].update(visible=False)

            elif event == "-CREATE-DATA-FOLDER-":
                _create_data_dir()
            elif event == "-OPEN-DATA-FOLDER-":
                os.startfile(data_dir)

        window.close()

    def _create_script_layout(self, available_scripts):
        return [
            [sg.Text("Add Script", font=("Arial", 14, "bold"))],
            [sg.Text("Select Scripts:")],
            [sg.Listbox(values=available_scripts, key="-SCRIPTS-", size=(30, 6), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
            [sg.Text("Scripts will be generated in the output directory.")],
            [sg.Text("Output", font=("Arial", 14, "bold"))],
            [sg.Text("Output Directory: ")],
            [sg.Input(default_text=os.getcwd(), key="-OUTPUT-DIR-"), sg.FolderBrowse(target="-OUTPUT-DIR-")],
            [sg.Checkbox("Allow Overwrites", key="-OVERWRITE-", default=True, enable_events=True)],
            [sg.Button("Back", button_color=("white", sg.theme_background_color())), sg.Button("Create")]
        ]

    def _show_add_script_window(self):
        # Get the list of available scripts
        available_scripts = [
            p.stem[7:] for p in Path(TEMPLATES_FP).glob("script_*.template")
        ]
        self.file_handler = FileHandler()
        self.file_handler.overwrite_all = True

        add_script_layout = self._create_script_layout(available_scripts) 
        window = sg.Window("Add Script", add_script_layout)

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
    interface = MakitaUI()
    interface.execute()

if __name__ == "__main__":
    interface = MakitaUI()
    interface.execute()
