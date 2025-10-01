import sys
import time
import os
from PyQt5.QtWidgets import QApplication
import zipfile

UE4SS_Mod_path = "Pal/Binaries/Win64/Mods"
PAKS_Mod_path = "Pal/Content/Paks/~mods"

def installCollection(ui):
    game_path = ui.game_file_edit.text()
    collection_path = ui.collection_path_edit.text()

    print("Starting installation to game path:", game_path)

    if not validateGamePath(game_path):
        return

    if not os.path.isdir(collection_path):
        print("Invalid collection path.")
        return
    


    length =  len(os.listdir(collection_path))
    if length == 0:
        print("Collection path is empty.")
        return
    ui.progress_bar.setMaximum(length)
    for file in os.listdir(collection_path):
        if os.path.isfile(os.path.join(collection_path, file)):
            installFile(os.path.join(collection_path, file), game_path)
        ui.progress_bar.setValue(ui.progress_bar.value() + 1)
        QApplication.processEvents()  # Update the UI
    print("Installation complete.")

def validateGamePath(game_path):
    if not os.path.isdir(game_path):
        print("Invalid game path.")
        return False
    if not os.path.isdir(os.path.join(game_path, UE4SS_Mod_path)):
        print(f"Missing {UE4SS_Mod_path} directory.")
        return False
    if not os.path.isdir(os.path.join(game_path, PAKS_Mod_path)):
        print(f"Missing {PAKS_Mod_path} directory.")
        return False 
    return True

def purgeCollection(ui):
    game_path = ui.game_file_edit.text()
    
    if not os.path.isdir(game_path):
        print("Invalid game path.")
        return
    # Simulate purge process
    total_steps = 100
    for step in range(total_steps + 1):
        ui.progress_bar.setValue(step)
        time.sleep(0.01)  # Simulate time-consuming task
        QApplication.processEvents()  # Update the UI
    print("Purge complete.")

def installFile(file_path, game_path):
    print(f"Installing {os.path.basename(file_path)}...")
    try:
        # Simulate file installation
        time.sleep(0.01)  # Simulate time-consuming task
        return True
    except Exception as e:
        print(f"Error installing {file_path}: {e}")
        return False