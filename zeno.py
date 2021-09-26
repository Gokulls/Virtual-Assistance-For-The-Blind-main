import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import sys
import smtplib
from requests import get
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from zenoUi import Ui_MainWindow



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice',voices[0].id)


def speak(audio):
    engine.say(audio) 
    engine.runAndWait()


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('rs2626670@gmail.com', 'ritika@123')
    server.sendmail('jadhavakha19ce@student.mes.ac.in', to, content)
    server.close()


def wishme():
    hour = int(datetime.datetime.now().hour)    
    if hour>=0 and hour<12:
        speak("Good Morning")

    elif hour>=12 and hour<18:
        speak("Good Afternoon")

    else:
        speak("Good Evening")

    speak("I am zenos sir. Please tell me how can i help you")

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()


    def takeCommand(self):
        #It takes microphone input from the user and returns string output

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source,timeout=1,phrase_time_limit=5)

        try:
            print("Recognizing...")    
            query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
            print(f"User said: {query}\n")  #User query will be printed.

        except Exception as e:
            
            speak("Say that again please...")   #Say that again will be printed in case of improper voice 
            print("Say that again please...\n")
            return "None" #None string will be returned
        query = query.lower()
        return query


    def TaskExecution(self):
        wishme()
        while True:
                self.query = self.takeCommand().lower() #Converting user query into lower case

                # Logic for executing tasks based on query
                if 'wikipedia' in self.query:  #if wikipedia found in the query then this block will be executed
                    speak('Searching Wikipedia...')
                    self.query = self.query.replace("wikipedia", "")
                    results = wikipedia.summary(self.query, sentences=1) 
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)

                elif 'open youtube' in self.query:
                    webbrowser.open("youtube.com")    

                elif 'open google' in self.query:
                    speak("Sir, what should i search on google")
                    cm = self.takeCommand().lower()
                    webbrowser.open(f"{cm}")

                elif 'open stackoverflow' in self.query:
                    webbrowser.open("www.stackoverflow.com")

                elif 'play music' in self.query:
                    music_dir = 'C:\\Users\\srona\\Music'
                    songs = os.listdir(music_dir)
                    print(songs)    
                    os.startfile(os.path.join(music_dir, songs[0]))

                elif 'the time' in self.query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")    
                    speak(f"Sir, the time is {strTime}")

                elif 'open code' in self.query:
                    codePath = "C:\\Program Files (x86)\\Geany\\bin\\geany.exe"
                    os.startfile(codePath)

                elif 'open command prompt' in self.query:
                    os.system("start cmd")
                
                elif 'email to akshay' in self.query:
                    try:
                        speak("What should I say?")
                        content = self.takeCommand()
                        to = "jadhavakha19ce@student.mes.ac.in"    
                        sendEmail(to, content)
                        speak("Email has been sent!")
                    except Exception as e:
                        print(e)
                        speak("Sorry my friend ronak bro. I am not able to send this email")    

                elif 'ip address' in self.query:   
                    ip = get('https://api.ipify.org').text              
                    speak(f"your IP address is {ip}")

                elif 'no thanks' in self.query:
                    speak("thanks for using me sir,have a good day")
                    sys.exit() 

                speak("sir, do you have any other work")
                print("sir, do you have any other work")    


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("aed11d6975231b91c8e992c02b8376da.gif")    
        self.ui.zenoUi.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("T8bahf.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer =QTimer(self)
        timer.timeout.connect(self.showTime)

        startExecution.start()

    def showTime(self):
        current_time = QTimer.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)



app = QApplication(sys.argv)
zeno = Main()
zeno.show()
exit(app.exec_())