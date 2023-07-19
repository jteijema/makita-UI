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

To use Makita UI, simply clone the repository, navigate to the root directory, and run main.py:

```sh
git clone https://github.com/jteijema/makita_ui.git
cd makita_ui
pip install .
```

Then run the following command:

```sh
makita-ui
```

### The main window 

![image](https://github.com/jteijema/makita-UI/assets/28191416/20d49393-d5eb-4b77-a512-cc48bf7b5fb0)

The main window will provide you with the following options:

- Template: Clicking this button opens a window where you can select a template from a dropdown menu, specify parameters according to the chosen template, and generate a new template with these settings.
- Add Script: This button opens a window that lists available scripts. You can select multiple scripts and create them all at once.
- Output Directory: This is where all generated templates and scripts will be saved. You can type the directory manually or click the "Browse" button to select it.

### Template Window

![image](https://github.com/jteijema/makita-UI/assets/28191416/c562208d-a126-4aa3-b19f-f5b74f2a9bd7)

The template window has several options that are dynamically adjusted based on the selected template:

`--Template--`
- Template: Select the desired template from the dropdown menu.
- Parameters: Input fields for parameters will adjust according to the selected template.
- Generate Template: Generates the selected template with specified parameters.

`--Data Folder--`
- Create Data Folder: This button will create a data folder in the output directory.
- Open Data Folder: Opens the data folder in your file explorer.

### Add Script Window

![image](https://github.com/jteijema/makita-UI/assets/28191416/09593eff-5931-4957-b25f-d8fafdda10bf)

The "Add Script" window displays a list of available scripts. You can select multiple scripts from the list and click "Create" to generate all selected scripts at once.
Contribute

Your contributions are always welcome! Please feel free to submit a pull request.

# License

Makita UI is released under the MIT License.

# Acknowledgements

Thanks to the Makita team for their work on the library that this UI was built on.
