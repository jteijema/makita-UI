import os
import PySimpleGUI as sg

def _mm_parameters(window):
    window["n_runs"].update(visible=False)
    window["classifiers"].update(visible=False)
    window["feature_extractors"].update(visible=False)
    window["n_priors"].update(visible=True)

def _arfi_parameters(window):
    window["n_priors"].update(visible=False)
    window["n_runs"].update(visible=False)
    window["feature_extractors"].update(visible=True)
    window["classifiers"].update(visible=True)

def _basic_parameters(window):
    window["n_priors"].update(visible=False)
    window["classifiers"].update(visible=False)
    window["feature_extractors"].update(visible=False)
    window["n_runs"].update(visible=True)

def _main_layout():
    return [            
        [sg.Text("Welcome to Makita UI!", font=("Arial", 14, "bold"))],
        [sg.Text("This interface allows you to generate templates and scripts for the ASReview Makita extension.")],
        [sg.Text("Select an option below to get started:")],
        [sg.Button("Template", key="-TEMPLATE-")],
        [sg.Button("Add Script", key="-ADD-SCRIPT-")],
        [sg.Button("Exit", button_color=("white", sg.theme_background_color()), key="-EXIT-", pad=((0, 0), (10, 0)))]
    ]

def _script_layout(available_scripts):
    '''Create the layout for the add script window.'''
    return [
        [sg.Text("Add Script", font=("Arial", 14, "bold"))],
        [sg.Text("Select Scripts:")],
        [sg.Listbox(values=available_scripts, key="-SCRIPTS-", size=(30, 6), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
        [sg.Text("Scripts will be generated in the output directory.")],
        [sg.Text("Output", font=("Arial", 14, "bold"))],
        [sg.Text("Output Directory: ")],
        [sg.Input(default_text=os.getcwd(), key="-OUTPUT-DIR-"), sg.FolderBrowse(target="-OUTPUT-DIR-")],
        [sg.Checkbox("Allow Overwrite", key="-OVERWRITE-", default=True, enable_events=True)],
        [sg.Button("Back", button_color=("white", sg.theme_background_color())), sg.Button("Create")]
    ]

def _template_layout(templates, data_dir):
    if os.path.exists(data_dir):
        # load all the files in the data folder
        data_files = '\n'.join([f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))])
        dataFolderString = sg.Multiline(data_files, size=(61, 4), disabled=True, autoscroll=True)
    else:
        dataFolderString = sg.Button("Create Data Folder", key="-CREATE-DATA-FOLDER-")

    return [
        [sg.Text("Work Folder", font=("Arial", 14, "bold"))],
        [sg.Text(f"Current working directory: \n {os.getcwd()}")],
        [sg.Button("Open work Folder", key="-OPEN-WORK-FOLDER-")],
        [sg.Text("\nTemplate", font=("Arial", 14, "bold"))],
        [sg.Text("Select a template to generate:")],
        [sg.Text('Template\t\t'), sg.Combo(templates, size=43, key="-TEMPLATE-", enable_events=True)],
        [sg.Text('output_dir\t'), sg.InputText(key='template_output_dir', default_text='output')],
        [sg.Text('init_seed\t\t'), sg.InputText(key='init_seed', default_text='400')],
        [sg.Text('model_seed\t'), sg.InputText(key='model_seed', default_text='250')],
        [sg.Text('n_priors\t\t'), sg.InputText(key='n_priors', default_text='1', visible=False)],
        [sg.Text('n_runs\t\t'), sg.InputText(key='n_runs', default_text='1', visible=False)],
        [sg.Text('classifiers\t'), sg.InputText(key='classifiers', default_text='logistic nb rf svm', visible=False)],
        [sg.Text('feature_extractors\t'), sg.InputText(key='feature_extractors', default_text='doc2vec sbert tfidf', visible=False)],
        [sg.Button("Generate Template", key="-GENERATE-TEMPLATE-")],
        [sg.Text("\nData Folder", font=("Arial", 14, "bold"))],
        [dataFolderString],
        [sg.Button("Open Data Folder", key="-OPEN-DATA-FOLDER-")],
        [sg.Button("Back", button_color=("white", sg.theme_background_color()), pad=((0, 0), (10, 0)))],
    ]