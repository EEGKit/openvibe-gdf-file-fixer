import PyInstaller.__main__
import os

if __name__ == "__main__":

    app_name = "OpenViBE GDF File Fixer"
    name_option = "-n {}".format(app_name)

    script = "../src/main.py"

    PyInstaller.__main__.run([
        script,
        name_option,
        '--noconsole',
        '-y'
    ])

