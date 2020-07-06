from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QTime
from pypresence import Presence
import time, datetime

class PomoTimer:

    def __init__(self, times, label, tray, rpc, subject):
        self.subject = subject
        self.tray = tray
        self.label = label
        self.main_time = times[0]
        self.time = QTime(0,self.main_time,0)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timerEvent)
        self.rep = 0
        self.RPC = rpc
        self.short_break = self.Interval_timer(times[1], self.label, self.tray, self, self.RPC, self.subject)
        self.long_break = self.Interval_timer(times[2], self.label, self.tray, self, self.RPC, self.subject)
        self.round = 1

    class Interval_timer:
        def __init__(self, main_time, label, tray, outer_class, rpc, subject):
            self.outer_class = outer_class
            self.tray = tray
            self.label = label
            self.main_time = main_time
            self.time = QTime(0,main_time,0)
            self.RPC = rpc
            self.subject = subject

        def timerEvent(self):
            self.time = self.time.addSecs(-1)
            self.label.setText(self.time.toString("mm:ss"))
            if self.time.secsTo(QTime(0,0,0)) == 0:

                print("Break timer stopped")
                self.tray.showMessage("Tomatime","Break time's up", self.tray.icon(), 4000)
                
                self.clearTimer()
                self.outer_class.timer.timeout.disconnect(self.timerEvent)
                self.outer_class.timer.timeout.connect(self.outer_class.timerEvent)
                print("Returning to focus timer")
                self.outer_class.round += 1
                self.outer_class.updateDiscord("Studying")

            return print(self.time.toString("mm:ss"), "   Break timer")

        def startTimer(self):
            print("Starting secondary timer")
            self.outer_class.timer.timeout.connect(self.timerEvent)
            self.outer_class.updateDiscord("Taking a break")

        def clearTimer(self):
            print("Clearing break timer")
            self.time = QTime(0,self.main_time,0)
            self.label.setText(self.time.toString("mm:ss"))

    def timerEvent(self):
        self.time = self.time.addSecs(-1)
        self.label.setText(self.time.toString("mm:ss"))
        if self.time.secsTo(QTime(0,0,0)) == 0:
            self.rep += 1           

            self.timer.timeout.disconnect(self.timerEvent)
            self.clearTimer()

            print("Focus time's up")
            self.tray.showMessage("Tomatime","Focus time's up", self.tray.icon(), 4000)
            if self.rep ==3:
                self.rep = 0
                
                self.long_break.startTimer()
                return print("Starting long break timer")
                
            else:
                
                self.short_break.startTimer()
                return print("Starting short break timer")

        return print(self.time.toString("mm:ss"), ("   Focus Timer Ticking"))

    def startTimer(self):
        self.timer.start()
        print(self.timer.interval())
        self.updateDiscord("Studying")

    def clearTimer(self):
        self.time = QTime(0, self.main_time, 0)

    def pauseTimer(self):
        self.timer.stop()
        try:
            self.RPC.update(state=f"Studying - Round {self.round}", details="Paused", large_image="fsidfsd")
        except:
            print("No Discord app running")

    def resetTimer(self):
        self.pauseTimer()
        self.short_break.clearTimer()
        self.long_break.clearTimer()
        self.clearTimer()
        self.label.setText(str(self.main_time)+":00")
        try:
            self.timer.timeout.disconnect(self.short_break.timerEvent)
        except:
            pass

        try:
            self.timer.timeout.disconnect(self.long_break.timerEvent)
        except:
            pass
        try:
            self.timer.timeout.disconnect(self.timerEvent)
        except:
            pass
        self.timer.timeout.connect(self.timerEvent)

    def epochTime(self, mins, second):
        orig = datetime.datetime.fromtimestamp(time.time())
        new = orig + datetime.timedelta(minutes=mins, seconds=second)
        return time.mktime(new.timetuple())

    def updateDiscord(self, info):
            try:
                self.RPC.update(state=f"Studying {self.subject} - Round {self.round}", details=info, large_image="fsidfsd", end=self.epochTime(self.time.minute(), self.time.second()))
            except:
                print("No Discord app running")