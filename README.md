# Makita UI

Makita UI is a user-friendly interface for the Makita library. It provides a GUI that makes it easier for you to select templates, add scripts, and generate new ones based on your preferences.
Features

- Selection of templates for different use-cases.
- Customizable parameters based on the selected template.
- Ability to create a data folder directly from the interface.
- Option to add and generate scripts from a list of available ones.

## Requirements

- Python 3.7+
- PySimpleGUI
- Makita library

## Usage

To use Makita UI, simply install directly from the repository:

```sh
pip install https://github.com/jteijema/makita-UI/archive/master.zip
```

Then run the following command in your makita folder:

```sh
makita-ui
```

### The main window 

![image](https://github.com/jteijema/makita-UI/assets/28191416/6b606e69-e5c6-48d6-b7ba-b5bad41e4626)

The main window will provide you with the following options:

- Template: Clicking this button opens a window where you can select a template from a dropdown menu, specify parameters according to the chosen template, and generate a new template with these settings.
- Add Script: This button opens a window that lists available scripts. You can select multiple scripts and create them all at once.

### Template Window

![image](https://github.com/jteijema/makita-UI/assets/28191416/ebdbae78-48e4-4d03-9642-8bcd159f2c36)

The template window provides various options, which dynamically adjust based on the selected template:
#### Work Folder

- Displays the current working directory.
- Open Work Folder: Opens the work folder in your file explorer.

#### Template

- Template: Select the desired template from the dropdown menu.
- Parameters: Input fields for parameters adjust according to the selected template. This includes output_dir, init_seed, model_seed, n_runs, n_priors, classifiers, and feature_extractors. Not all parameters are applicable to each template, non-applicable ones remain hidden.
- Generate Template: Generates the selected template with the specified parameters.

#### Data Folder

- Create Data Folder: This button creates a data folder in the output directory, only available if no data folder is currently present.
- Open Data Folder: Opens the data folder in your file explorer.

### Add Script Window

![image](https://github.com/jteijema/makita-UI/assets/28191416/5409ca20-b88c-4f02-8bf9-e6427208421f)

The "Add Script" window allows you to manage and generate scripts.
#### Add Script

- Select Scripts: Choose from a list of available scripts presented in a multi-select list box. You can select multiple scripts at once.
- Note: Scripts will be generated in the output directory.

#### Output

- Output Directory: This is the directory where all generated templates and scripts will be saved. You can either manually input the directory path or click the "Browse" button to select it.
- Allow Overwrites: A checkbox option that when selected, allows generated scripts to overwrite existing scripts in the output directory if they have the same name.


# License

Makita UI is released under the MIT License.

# Acknowledgements

Thanks to the Makita team for their work on the library that this UI was built on.

# Contribute

Your contributions are always welcome! Please feel free to submit a pull request.
