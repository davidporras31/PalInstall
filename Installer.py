import os
from PyQt5.QtWidgets import QApplication, QDialog
from enum import Enum
import Archiver
import Dialog

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
    


    length =  len([name for name in os.listdir(collection_path) if os.path.isfile(os.path.join(collection_path, name))])
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
    
    if not validateGamePath(game_path):
        return
    print("Starting purge")
    
    # Purge UE4SS mods
    ue4ss_mods_path = os.path.join(game_path, UE4SS_Mod_path)
    #purgePath(ue4ss_mods_path)
    ui.progress_bar.setValue(50)
    # Purge PAKS mods
    paks_mods_path = os.path.join(game_path, PAKS_Mod_path)
    purgePath(paks_mods_path)
    ui.progress_bar.setValue(100)
    
    print("Purge complete.")

def purgePath(path):
    if not os.path.isdir(path):
        print("Invalid path.")
        return
    print("purgeing path:", path)
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".dll") or file.endswith(".ini") or file.endswith(".pak"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

class InstallType(Enum):
    UE4SS = 1
    PAKS = 2
    UNKNOWN = 3

def determineInstallType(archive : Archiver.Archiver) -> InstallType:
    paks_num = 0
    ue4ss_num = 0

    for file in archive.namelist():
        if file.endswith(".pak"):
            paks_num += 1
        elif (file.endswith(".dll") or file.endswith(".ini")):
                ue4ss_num += 1
    return InstallType.PAKS if paks_num > ue4ss_num \
        else InstallType.UE4SS if ue4ss_num > paks_num \
        else InstallType.UNKNOWN

def installFile(file_path, game_path):
    print(f"Installing {os.path.basename(file_path)}...")
    ##try:
    archive = Archiver.makeArchive(file_path)
    itype = determineInstallType(archive)
    if itype == InstallType.UNKNOWN:
        print(f"Unknown install type for {file_path}. Skipping.")
        return False
    elif itype == InstallType.UE4SS:
        print("Detected UE4SS mod.")
        return True
    elif itype == InstallType.PAKS:
        print("Detected PAKS mod.")
        names:list = []
        for file in archive.namelist():
            if file.endswith(".pak"):
                names.append(file)
        if len(names) > 1:
            dialog = Dialog.NameSelectionDialog("Multiple paks found","Select all paks to install:",names)
            if dialog.exec_() == QDialog.Accepted:
                names = dialog.selected
            else:
                print("Installation cancelled by user.")
                return False
        print(f"Extracting ...")
        for name in names:
            Archiver.makeArchive(file_path).extract(name, os.path.join(game_path, PAKS_Mod_path))
            if "/" in name:
                os.rename(os.path.join(game_path, PAKS_Mod_path, name), os.path.join(game_path, PAKS_Mod_path, name.rsplit("/")[1]))
    return True
    #except Exception as e:
     #   print(f"Error installing {file_path}: {e}")
      #  return False