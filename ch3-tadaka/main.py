#!/usr/bin/env python
# -*- coding: utf-8 -*-
import t_vagrant
import yaml
import seqMatcher as sM
import speech_recognition as sr


deamon = 1
box_list_name = ['centos-7.2']
while deamon == 1:
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=3) 
        print("Listning:")
        audio = r.listen(source)
        instruction = ''
        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            #instruction = r.recognize_google(audio)
            #instruction = raw_input("Instruction:")
            instruction = r.recognize_sphinx(audio,"en-US")

            print "Instruction Given: %s" % instruction
        except sr.UnknownValueError:
            print("Speech Recognition service could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))

        avail_method = ['deploy','status','delete','destroy']

        clean_instruction = sM.t_search(avail_method,instruction.lower())

        print clean_instruction

        
        if "deploy" in clean_instruction:
            if len(box_list_name) == 0:
                box_list_name = t_vagrant.vm_box_list()
                print box_list_name
            else:
                print "Deploying..."
                t_vagrant.vm_deploy()
        elif "status" in clean_instruction:
             t_vagrant.vm_status()
        elif any(word in clean_instruction for word in ["delete","destroy"]):
             t_vagrant.vm_destroy()
        elif "shutdown" in clean_instruction:
             deamon = 0
