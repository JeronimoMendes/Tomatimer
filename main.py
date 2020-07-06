from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMainWindow
from tray import System_tray
from timer import PomoTimer
from pref_win import Ui_pref_win
import json

if __name__ == "__main__":
    # Load settings
    with open ("settings.json", "r") as settings:
        settings = json.load(settings)

    subject = settings["subject"]
    times = [settings["main_time"], settings["short_break"], settings["long_break"]]

    # Create app
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Create Settings window
    pref_win = QMainWindow()
    ui = Ui_pref_win(pref_win)
    ui.setupUi(pref_win)

    # Create System Tray 
    tray = QSystemTrayIcon()
    system_tray = System_tray(tray, app, times, subject, pref_win)
    system_tray.createTimer()
    system_tray.setupUi()

    app.exec_()