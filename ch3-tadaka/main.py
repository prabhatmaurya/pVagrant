#!/usr/bin/env python
# -*- coding: utf-8 -*-
import t_vagrant
import yaml
import seqMatcher as sM
import speech_recognition as sr
import warnings
import voice as v
import os
import requests

warnings.warn("deprecated", DeprecationWarning)
deamon = 1
box_list_name = ['centos-7.2']
while deamon == 1:
    # Record Audio
    r = sr.Recognizer()
    r.energy_threshold = 500
    with sr.Microphone() as source:
        print("Listning:")
        audio = r.listen(source)
        instruction = ''
        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            #instruction = r.recognize_google(audio)
            # instruction = raw_input("Instruction:")
            instruction = r.recognize_sphinx(audio,"en-in")

            print "Instruction Given: %s" % instruction
        except sr.UnknownValueError:
            print("Speech Recognition service could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))

        avail_method = ['deploy',
                        'status',
                        'delete',
                        'destroy',
                        'shutdown',
                        'list',
                        'machine',
                        'box',
                        'vm',
                        'docker',
                        'phpmyfaq']

        #clean_instruction = sM.t_search(avail_method,instruction.lower())
        clean_instruction = instruction.lower()

        print clean_instruction

        if "vm" in clean_instruction:
            if "deploy" in clean_instruction:
                if len(box_list_name) == 0:
                    box_list_name = t_vagrant.vm_box_list()
                    print box_list_name
                else:
                    v.speak("Deploying...")
                    t_vagrant.vm_deploy()
            elif "status" in clean_instruction:
                 msg = t_vagrant.vm_status()
                 for i in msg:
                     v.speak("Status of machine %s is %s" % (i.name, i.state ))
            elif any(word in clean_instruction for word in ["delete","destroy"]):
                 t_vagrant.vm_destroy()
            elif "list" in clean_instruction:
                if "machine" in clean_instruction:
                    msg  = t_vagrant.vm_machine_list()
                    if len(msg) > 0:
                        v.speak("Total %s machines available. List of machines are" % len(msg))
                        for i in msg:
                            v.speak(i)
                elif "box" in clean_instruction:
                    msg = t_vagrant.vm_box_list()
                    if len(msg) > 0:
                        v.speak("Total %s box's available, The list of boxes are" % len(msg))
                        for i in msg:
                            v.speak(i)
        elif "faq" in clean_instruction:
            if "deploy" in clean_instruction:
                v.speak("Starting phpmyfaq")
                os.system("cd /Users/prabhat.maurya/Documents/GIT/plabs/phpmyfaq/; docker-compose up -d; &> /dev/null")
            elif any(word in clean_instruction for word in ["delete","destroy"]):
                v.speak("Stopping phpmyfaq")
                os.system("cd /Users/prabhat.maurya/Documents/GIT/plabs/phpmyfaq/; docker-compose stop; &> /dev/null")
            elif "status" in clean_instruction:
                try:
                    r  = requests.get("http://127.0.0.1:8080/")
                    status = '%s' % r.status_code
                except Exception as e:
                    print(e)
                    status = 503
                if status == "200":
                    v.speak("phpmyfaq is running")
                else:
                    v.speak("phpmyfaq is not running")
            else:
                v.speak("Sorry, I did not understand what to do")

        elif "shutdown" in clean_instruction:
             deamon = 0
