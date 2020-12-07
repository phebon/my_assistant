#!usr/bin/python3
"""
Copyright 2020 Moritz Siebert

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
"""
This Script is intended to easily join Zoomcalls and do other stuff in future based on speech recognition. It is designed to be used on 
Debian like operating systems but can be adapted to other OSs by changing the <open_zoom> function.
"""

import speech_recognition as sr
from additional_data import *
import os
#The following variable Definition contain explicit links. They should later be stored in extra files, customizable by the user.
# This is a dummy to later be replaced in the list all_lecs
lec_dummy = "giybf.com/"
ex_dummy = "www.physik.uni-wuerzburg.de/studium/studienorganisation/pruefungstermine/"
""" Those are lists of keywords to check whether you want lecture or exercise."""
exercise = ["exercise", "examples", "tutorium"]
lecture = ["lecture", "lectures", "lesson"]
"""In the following lists, the first entry fenotes the subject. The second is some keywords. The third is the lecture link,
	fourth is exercise link. For testing purposes replace the imported links 
	such as fk_lec_link which are defined in additional_data.py by the dummy links above."""
statmech = ["Statistical Mechanics",["statistical", "mechanic", "mechanics", "statistic", "statistics"],
statmech_lec_link,statmech_ex_link]
fk = ["Festkörperphysik",["solid", "state", "states", "crystall", "solids"],fk_lec_link,fk_ex_link]
ket = ["Kern und Elementarteilchen",["elementary","particles", "nuclear", "core"],ket_lec_link,ket_ex_link]
ap3 = ["Labor und Messtechnik",["measurement","measure", "labview", "lab"],lec_dummy,ex_dummy]
all_lecs = [statmech, fk, ket,ap3]
"""Definiere ein paar nützliche Funktionen:"""
def find_subj(text):
	subject = "No Subject found"
	for uni_module in all_lecs:
		for key_word in uni_module[1]:
			if key_word in text:
				subject = uni_module[0]
	return subject

""" To be sure, we only open zoom, if the request contains keywords for lecture or exercise. 
	Therefore we check what event is requested with the following function."""
def lec_or_exercise(text):
	type_of_event = "unknown"
	for key_word in exercise:
		if key_word in text:
			type_of_event = "exercise"
			break
	for key_word in lecture:
		if key_word in text:
			type_of_event = "lecture"
			break
	return type_of_event

""" This function gets the subject name and event_type ('lecture' or 'exercise') 
	as input strings and then opens the corresponding link in firefox. Maybe I'll change this to open zoom directly later. 
	If you are using Windows you'll have to change this function to your needs."""
def open_zoom(subject, event_type):
	did = False
	for element in all_lecs:
		if subject == element[0]:
			print(f"You want to visit the {subject} {event_type}")
			if event_type=="lecture":
				os.system(f'firefox {element[2]}')
				did = True
			elif event_type == "exercise":
				os.system(f'firefox {element[3]}')
				did = True
			#Place a firefox or zoom call here! 
	if not did: print("nothing matched the subjects looked up by the <open_zoom> function ")



recognizer = sr.Recognizer()
text_of_query = "Hi"
with sr.Microphone() as source:
    noo = True
    print("Listening...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        noo = False
    except sr.UnknownValueError:
        print("Could not understand audio")
    if not noo: 
    	print(query.lower())
    	text = query.lower()

subject_of_request = find_subj(text)
print(subject_of_request)
if subject_of_request != "No Subject found":
	event_type_of_request = lec_or_exercise(text)
	open_zoom(subject_of_request,event_type_of_request)
else:
	print("Apparently I didn't understand.")