#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Background image is designed by Starline
#(https://www.freepik.com/free-vector/abstract-geometric-hexagonal-medical_2870384.htm)
import kivy
import keras

from kivy.config import Config

Config.set('graphics', 'resizable', False)

kivy.require('1.10.1') #current kivy version

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.factory import Factory

import os
import json
import subprocess
import shlex
import string
import csv
import pandas as pd
import numpy
import pickle

from keras.models import model_from_json

import txtfileprocessing as txtp

# A part of code is from https://stackoverflow.com/questions/40090453/font-color-of-filechooser

Builder.load_string("""
#:import utils kivy.utils

[FileListEntry@FloatLayout+TreeViewNode]:
    locked: False
    entries: []
    path: ctx.path
    # FIXME: is_selected is actually a read_only treeview property. In this
    # case, however, we're doing this because treeview only has single-selection
    # hardcoded in it. The fix to this would be to update treeview to allow
    # multiple selection.
    is_selected: self.path in ctx.controller().selection

    orientation: 'horizontal'
    size_hint_y: None
    height: '48dp' if dp(1) > 1 else '24dp'
    # Don't allow expansion of the ../ node
    is_leaf: not ctx.isdir or ctx.name.endswith('..' + ctx.sep) or self.locked
    on_touch_down: self.collide_point(*args[1].pos) and ctx.controller().entry_touched(self, args[1])
    on_touch_up: self.collide_point(*args[1].pos) and ctx.controller().entry_released(self, args[1])
    BoxLayout:
        pos: root.pos
        size_hint_x: None
        width: root.width - dp(10)
        Label:
            # --------------
            # CHANGE FONT COLOR
            # --------------
            color: 0, .3, .4, .85
            id: filename
            text_size: self.width, None
            halign: 'left'
            shorten: True
            text: ctx.name
        Label:
            # --------------
            # CHANGE FONT COLOR
            # --------------
            color: 0, .3, .4, .85
            text_size: self.width, None
            size_hint_x: None
            halign: 'right'
            text: '{}'.format(ctx.get_nice_size())



<MyScreen>:
    canvas.before:
        Color:
            rgb: utils.get_color_from_hex('#B9D7D9')
        Rectangle:
            pos: self.pos
            size: self.size
            source: '15002_50.jpg'
    id: my_screen
    FloatLayout:
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'

            Image:
                source: 'white.jpeg'
                size_hint_x: None
                size_hint_y: None
                height: dp(850)
                width: dp(750)
                opacity: 0.4
        AnchorLayout:
            pos: 0,10
            anchor_x: 'center'
            anchor_y: 'bottom'
            Button:
                background_normal: ''
                background_color: 73/255, 55/255, 54/255, 1
                canvas.before:
                    Color:
                        rgb: utils.get_color_from_hex('#493736')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                text: "Upload"
                color: 185/255,215/255,217/255
                font_size: '20sp'
                size: 300,75
                size_hint: None, None
                on_press: my_screen.open(filechooser.path, filechooser.selection)
                
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'
            FileChooserListView:
                background_normal: ''
                background_color: 1,1,1,1
                canvas.before:
                    Color:
                        rgb: utils.get_color_from_hex('#EB9F9F')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                id: filechooser
                size: 700,400
                size_hint: None, None
                color: 1,0,1,1
                canvas.before:
                    Color:
                        rgba: 1,1,1, 1
                on_selection: my_screen.selected(filechooser.selection)

        AnchorLayout:
            pos: -200,235
            anchor_x: 'left'
            anchor_y: 'top'
            Label:
                font_size: '30sp'
                text: 'Select File to Evaluate'
                font_name: 'Roboto'
                color: 42/255,40/255,41/255

            
<ShowResultsScreen>:
    id: show_results
    on_pre_enter: show_results.setFunctions()
    canvas.before:
        Color:
            rgb: utils.get_color_from_hex('#B9D7D9')
        Rectangle:
            pos: self.pos
            size: self.size
            source: '15002_50.jpg'
    FloatLayout:
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'

            Image:
                source: 'white.jpeg'
                size_hint_x: None
                size_hint_y: None
                height: dp(850)
                width: dp(750)
                opacity: 0.3
        
        AnchorLayout:
            pos: -230,235
            anchor_x: 'left'
            anchor_y: 'top'
            Label:
                font_size: '30sp'
                text: "Result"
                color: 42/255,40/255,41/255
        
        AnchorLayout:
            pos: 65,-100
            anchor_x: 'center'
            anchor_y: 'top'
            Label:
                id: resultlbl
                color: 42/255,40/255,41/255, 1
                font_size: '20sp'
                size: 400,200
                size_hint: None, None
                text: ''
                text_size: 650, None

        AnchorLayout:
            pos: 65,0
            anchor_x: 'center'
            anchor_y: 'center'
            Label:
                id: functionslbl
                color: 123/255,59/255,59/255, 1
                font_size: '15sp'
                size: 400,200
                size_hint: None, None
                text: 'placeholder ' * 100
                text_size: 650, None

        AnchorLayout:
            pos: 0,10
            anchor_x: 'center'
            anchor_y: 'bottom'
            Button:
                background_normal: ''
                background_color: 73/255,55/255,54/255
                canvas.before:
                    Color:
                        rgb: utils.get_color_from_hex('#493736')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                size: 300,75
                size_hint: None, None
                text: 'Back'
                color: 185/255,215/255,217/255
                font_size: '20sp'
                on_press: root.manager.current = 'main'
                
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'

            Image:
                source: 'frame.png'
                size_hint_x: None
                size_hint_y: None
                height: dp(400)
                width: dp(700)
                opacity: 0.6


<MyPopup@Popup>:
    title:'Invalid File Selected'
    size: 400,400
    size_hint: None,None
    auto_dismiss: False
    background: 'popup.PNG'
    BoxLayout:
        orientation: 'vertical'
        size: 400,400
        size_hint: None,None
        Label:
            font_size: '20sp'
            text: 'Please select an object (.o) file.'
        AnchorLayout:
            pos: 0,10
            anchor_x: 'center'
            Button:
                background_normal: ''
                background_color: 73/255,55/255,54/255
                canvas.before:
                    Color:
                        rgb: utils.get_color_from_hex('#668284')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                size: 300,75
                size_hint: None, None
                text: 'Close'
                on_release: root.dismiss()
""")

evalResult = ""
evalvulnfuncs = []

def LoadModel():
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
    return loaded_model

def GetFunctions(file,path):
    functions = []
    processArg = "readelf -SW "+file
    args = shlex.split(processArg)
    output = subprocess.Popen(args,stdout=subprocess.PIPE,cwd=path ).communicate()[0]
    out = output.decode('utf-8').split('\n')
    for item in out:
        if(item.startswith(".text.",7)):
            item = item[7:]
            newitem = item[6:item.find(' ')]
            functions.append(newitem)
    return functions
		

def GenerateAssemCodeFiles(functions,file,path):
    fullpath = path+"/"+file[:-2]
    if not(os.path.exists(fullpath)):
        folderprocessArg = "mkdir "+file[:-2]
        folderargs = shlex.split(folderprocessArg)
        try:
            folderout = subprocess.check_output(folderargs,cwd=path)
        except subprocess.CalledProcessError:
            print("error while creating folder")
    filenames = []
    for function in functions:
        processArg = "objdump -M intel -w -d --section=.text."+function+" "+file
        args = shlex.split(processArg)
        try:
            out = subprocess.check_output(args,cwd=path)
            filename = function+".txt"
            filenames.append(filename)
            newpath = path+"/"+file[:-2]
            filename = newpath+"/"+filename
            #original path+ new folder+ new file's name
            outfile = open(filename,'w')
            outfile.write(out.decode("utf-8"))
            outfile.close()
        except subprocess.CalledProcessError:
            print("error while creating .txt file")
    return filenames,newpath

def CreateTxtFile(newpath):
    for path, dirs, files in os.walk(newpath):
        if not("vector.csv" in files):
            for file in files:
                txtp.symbolizeAndVectorize(file,path)

#Function to pad zeroes
def trp(l, n):
    return l[:n] + [0]*(n-len(l))

def CreateCsvFile(newpath):
    total = 0
    count = 0
    fixedsize = 200
    with open(newpath+"/"+"vector.txt","r") as filletbread:
        lines = [line.strip() for line in filletbread]
        with open(newpath+"/"+"vector.csv","w") as out_file:
            codewriter = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for line in lines:
                templist = [int(x.strip()) for x in line.split(',')]
                
                #Make the size of templist to be fixedsize
                if (len(templist)<fixedsize):
                    templist = trp(templist,fixedsize)
                elif (len(templist)>fixedsize):
                    templist = templist[:fixedsize]
                
                codewriter.writerow(templist)

def EvalCsv(newpath,functions):
    vulnfuncs = []
    keywordsfile = "keywordsdict.txt"
    kfdread = open(keywordsfile,"r")
    keywords = json.load(kfdread)
    kfdread.close()
    n_labels = len(keywords)+2
    model = LoadModel()
    testset = pd.read_csv(newpath+"/"+"vector.csv",header=None)
    testx = testset.iloc[:, 0:].values
    testx1 = numpy.eye(n_labels)[testx]
    testy = model.predict_classes(testx1)
    probability = model.predict_proba(testx1)
    ysum = 0
    probsum = 0
    count=0
    for i in range(0,len(testy)):
        count+=1
        ysum += testy[i][0].item()
        probsum += probability[i][0].item()
        if(testy[i][0].item() == 1):
            vulnfuncs.append(functions[i])
        print("X=%s, Predicted=%s" % (testx1[i], testy[i]))
        print("Probability=%s"%(probability[i]))
    print("Average: "+str(ysum/count))
    print("Avg Probability: "+str(probsum/count))
    evalvulnfuncs = vulnfuncs
    print(evalvulnfuncs)
    with open('FileForEvaluating', 'wb') as fp:
        pickle.dump(evalvulnfuncs, fp)

def ProcessSelectedFile(filepath):
    pathlist = filepath.split("/")
    file = pathlist[-1]
    pathlist2 = pathlist[1:-1]
    path = '/'.join(pathlist2)
    path = '/'+path
    #print(file)
    #print(path)
    functions = []
    if(file.endswith(".o")):
        #functype = file[:-2]+"_bad"
        #functions.append("main") #To retrieve functype dynamically
        functions = GetFunctions(file,path)
    else:
        Factory.MyPopup().open()
        file = "not selected"
    return functions,file,path

class ShowResultsScreen(Screen):
    print("screen loaded")

    def setFunctions(self):
        print("setFunctions was called")
        with open ('FileForEvaluating', 'rb') as fp:
            itemlist = pickle.load(fp)
        if not itemlist:
            resfunc = "-none-"
            self.ids.resultlbl.text = "This file is not vulnerable to Stack-Based Buffer Overflow."
        else:
            resfunc = "\n".join(itemlist)
            self.ids.resultlbl.text = "This file may be vulnerable to Stack-Based Buffer Overflow."
        resultfunctions = "Functions that may be vulnerable: "+resfunc
        print(resultfunctions)
        self.ids.functionslbl.text = resultfunctions


sm = ScreenManager()
sm.add_widget(ShowResultsScreen(name='results'))

class MyScreen(Screen):
    def open(self, path, filename):
        try:
            filepath = os.path.join(path, filename[0])
            functions,file,path = ProcessSelectedFile(filepath)
            if not(file=="not selected"):
                filenames,newpath = GenerateAssemCodeFiles(functions,file,path)
                CreateTxtFile(newpath)
                CreateCsvFile(newpath)
                EvalCsv(newpath,functions)
                self.parent.current = "results"
        except (IndexError):
            Factory.MyPopup().open()
            filepath = ''
    def selected(self, filename):
        try:
            selected_item = filename[0]
            #print("selected: %s" % filename[0])
        except (IOError, OSError, PermissionError, IndexError):
            selected_item = 'null'

sm.add_widget(MyScreen(name='main'))
sm.current = "main"

class MyApp(App):
    def build(self):
        self.title = 'Program Weakness Evaluator'
        return sm

if __name__ == '__main__':
    MyApp().run()
