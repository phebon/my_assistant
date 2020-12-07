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
This Script is intended to easily join Zoomcalls and do other stuff in future based on speech recognition.
"""

import speech_recognition as sr
import os

# This is a dummy to later be replaced in the list all_lecs
lec_dummy = "giybf.com/"
ex_dummy = "www.physik.uni-wuerzburg.de/studium/studienorganisation/pruefungstermine/"
""" Those are lists of keywords to check whether you want lecture or exercise."""
exercise = ["exercise", "examples", "tutorium"]
lecture = ["lecture", "lectures", "lesson"]
"""In the following lists, the first entry fenotes the subject. The second is some keywords. The third is the lecture link,
fourth is exercise link."""
statmech = ["Statistical Mechanics",["statistical", "mechanic", "mechanics", "statistic", "statistics"],
lec_dummy,ex_dummy]
fk = ["Festkörperphysik",["solid", "state", "states", "crystall", "solids"],lec_dummy,ex_dummy]
ket = ["Kern und Elementarteilchen",["elementary","particles", "nuclear", "core"],lec_dummy,ex_dummy]
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
""" Um sicherzugehen, werden wir nur, wenn tatsächlich lecture oder exercise gefordert ist, 
	einen Zoom link öffnen."""

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