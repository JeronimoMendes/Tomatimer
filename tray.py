from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QMenu
from PyQt5.QtGui import QIcon

from timer import PomoTimer
from pypresence import Presence

class System_tray():
    def __init__(self, tray, app, times, subject, pref_win):
        self.times = times
        self.main_time = times[0]
        self.app = app
        self.tray = tray
        self.subject = subject
        self.pref_win = pref_win
        self.label = QAction(str(self.main_time)+":00")
        
        try:
            self.RPC = Presence("729011176477818890")  # Initialize the Presence client
            self.RPC.connect() # Start the handshake loop
        except:
            print("You don't have a discord app open")

    def setupUi(self):
        # Create Menu
        self.menu = QMenu()
        self.tray.setContextMenu(self.menu)

        self.tray.setIcon(QIcon("material/images/tomato.png"))
        self.tray.setVisible(True)

        # Create and add Menu Actions
        self.preferences_btt = QAction("Preferences")
        self.preferences_btt.triggered.connect(self.preferences)

        self.quit = QAction("Quit")
        self.quit.triggered.connect(self.app.quit)

        self.start_btt = QAction("Start")
        self.start_btt.triggered.connect(self.start)

        self.pause_btt = QAction("Pause")
        self.pause_btt.triggered.connect(self.pause)
        self.pause_btt.setVisible(False)

        self.reset_btt = QAction("Reset")
        self.reset_btt.triggered.connect(self.reset)
        self.reset_btt.setVisible(False)

        self.menu.addAction(self.label)
        self.menu.addSeparator()
        self.menu.addActions([self.start_btt, self.pause_btt, self.reset_btt, self.preferences_btt, self.quit])

        self.menu.addMenu

    def start(self):
        print("Start")
        self.timer_main.startTimer()

        self.start_btt.setVisible(False)
        self.pause_btt.setVisible(True)
        self.reset_btt.setVisible(True)

    def pause(self):
        print("Pause")
        self.timer_main.pauseTimer()

        self.start_btt.setVisible(True)
        self.pause_btt.setVisible(False)

    def preferences(self):
        print("Preferences")
        self.pref_win.show()

    def reset(self):
        self.timer_main.resetTimer()

        self.pause_btt.setVisible(False)
        self.start_btt.setVisible(True)
        self.reset_btt.setVisible(False)

    def createTimer(self):
        # Creates a timer
        self.timer_main = PomoTimer(self.times, self.label, self.tray, self.RPC, self.subject)