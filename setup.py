import PyInstaller.__main__
import os

# Ensure the paths are correct
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'main.pyw',
    '--onefile',
    '--add-data=requirements.txt:.',
    '--add-data=main.pyw:.',
    f'--add-data={os.path.join(current_dir, "main.spec")}:.',
    f'--add-data={os.path.join(current_dir, "Config_Creator.py")}:.',
    f'--add-data={os.path.join(current_dir, "cookie_creator.ico")}:.',
    '--icon=cookie_creator.ico',
    '--name=CashOutCookieCreator',
    '--specpath=.',
])