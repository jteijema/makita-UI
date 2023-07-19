import PySimpleGUI as sg

class MakitaUI:
    def __init__(self):
        # Initialization code here
        from asreviewcontrib.makita.entrypoint import MakitaEntryPoint

    def execute(self):
        """Run the makita UI."""
        layout = [
            [sg.Button("Click Me")],
            [sg.Text("Hello, GUI!", key="-OUTPUT-")]
        ]

        window = sg.Window("My GUI", layout)

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