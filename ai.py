# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 13:31:34 2023

@author: austin dixon
"""

import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import wikipedia
import time
from datetime import datetime
from datetime import date

#########################################################################################################################
#blink leds red on adafruit voice bonnet so you know script has started
import board
import adafruit_dotstar

DOTSTAR_DATA = board.D5
DOTSTAR_CLOCK = board.D6

dots = adafruit_dotstar.DotStar(DOTSTAR_CLOCK, DOTSTAR_DATA, 3, brightness=0.2)
dots[0] = (0,0,255)
dots[1] = (0,0,255)
dots[2] = (0,0,255)
dots.show()

time.sleep(5)

dots[0] = (0,0,0)
dots[1] = (0,0,0)
dots[2] = (0,0,0)
dots.show()

#########################################################################################################################
#grab audio from microphone
def get_audio(): #listen to input from microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio) #use Google Cloud to process language
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said

wake_word = "hey Sid"
close_enough_word = "I said"
break_word = "stop"

engine = pyttsx3.init() #start the voice engine
newVoiceRate = 145
engine.setProperty('rate',newVoiceRate) #slow voice down a bit because default talks too fast

while True:
    text = get_audio() #get microphone input as string

    if wake_word in text or close_enough_word in text: #listen for wake word
        text = text.replace(wake_word, '')
        text = text.replace(close_enough_word, '')
        
        #blink leds blue so you know wake word was heard
        dots[0] = (0,255,0)
        dots[1] = (0,255,0)
        dots[2] = (0,255,0)
        dots.show()
        
        time.sleep(2)

        dots[0] = (0,0,0)
        dots[1] = (0,0,0)
        dots[2] = (0,0,0)
        dots.show()
        
        if break_word in text: #stop running script
            break

#########################################################################################################################
#smalltalk
        elif "what is your name" in text or "who are you" in text or "what are you" in text or "who made you" in text or "who created you" in text or "who built you" in text:
            engine.say("My name is Sid. I am a virtual assistiant created by the, brilliant, Austin Dixon.")
            engine.runAndWait()
        elif "hello" in text:
            engine.say("Hello, how are you today?")
            engine.runAndWait()
        elif "how are you" in text or "how are you doing" in text or "how are you feeling" in text:
            engine.say("I'm doing ok, but I do feel a little artificial... Ha Ha.")
            engine.runAndWait()
        
#########################################################################################################################
#search wikipedia
        elif "search" in text:
            text = text.replace('search', '')
            text = text.replace('for', '')
            text = text.replace('the', '')
            text = text.replace('internet', '')
            text = text.replace('wikipedia', '')
            result = ""
            engine.say("Searching")
            engine.runAndWait()
            try:
                result = wikipedia.summary(text)
            except Exception:
                pass
            if result == "":
                engine.say("Sorry, I didn't find any results for " + text)
                engine.runAndWait()
            else:
                engine.say(result)
                engine.runAndWait() 

#########################################################################################################################
#timer
        elif "timer" in text:
            text = text.replace('set', '')
            text = text.replace('a', '')
            text = text.replace('timer', '')
            text = text.replace('for', '')
            if "coffee" in text:
                engine.say("Setting coffee timer for 5 minutes.")
                engine.runAndWait()
                time.sleep(300) #set timer for five mins for coffee
                engine.say("Your coffee is ready! .... Your coffee is ready! .... Your coffee is ready!")
                engine.runAndWait()
            elif "hour" in text:
                if "hours" in text:
                    text = text.replace('hours', '')
                    engine.say("Setting timer for " + text + " hours")
                    engine.runAndWait()
                else:
                    text = text.replace('hour', '')
                    engine.say("Setting timer for one hour")
                    engine.runAndWait()
                hours = int(text) #convert str to int to get hours
                secs = hours * 3600 #convert hours to secs
                time.sleep(secs)
                engine.say("Your time is up! .... Your time is up! .... Your time is up!")
                engine.runAndWait()
            elif "minute" in text:
                if "minutes" in text:
                    text = text.replace('minutes', '')
                    engine.say("Setting timer for " + text + " minutes")
                    engine.runAndWait()
                else:
                    text = text.replace('minute', '')
                    engine.say("Setting timer for one minute")
                    engine.runAndWait()
                mins = int(text) #convert str to int to get mins
                secs = mins * 60 #convert mins to secs
                time.sleep(secs)
                engine.say("Your time is up! .... Your time is up! .... Your time is up!")
                engine.runAndWait()
            elif "seconds" in text:
                secs = int(text.replace('seconds', '')) #get the number from text and convert str to int
                engine.say("Setting timer for " + str(secs) + " seconds")
                engine.runAndWait()
                time.sleep(secs)
                engine.say("Your time is up! .... Your time is up! .... Your time is up!")
                engine.runAndWait()
        
#########################################################################################################################
#get time/date
        elif "time" in text:
            time_now = datetime.now()
            current_time = time_now.strftime("%I:%M %p")
            current_time = time_now.strftime("%I:%M %p") #for some reason the first instance doesn't work, so have to grab time twice
            engine.say("The current time is " + current_time)
            engine.runAndWait()
        elif "date" in text:
            today = date.today()
            engine.say("Today's date is " + str(today))
            engine.runAndWait()
            
#########################################################################################################################
#if input doesn't match any trigger words
        else:
            engine.say("You just asked me " + text + "... sorry, but I do not know anything about that yet.")
            engine.runAndWait()
