# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 01:27:40 2020

@author: Asaf Stern
"""


import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import datetime as dt
import os

############################## colors ##############################
main_color = "lightblue3"  #frame color
button_color = "lightblue2"  #buttons color
#tabs_colors =  ["lightyellow","lightblue","pink","salmon","indianred","maroon","azure2"]
tabs_colors =  ["grey"+str(i) for i in range(99,42,-5)]
#print(tabs_colors)
                 #amount of tabs as amount of colors
####################################################################

#class Button:
#    def __init__(self,main, text, mainColor, enterColor,hight = 2, width = 50, fontsize = 12):
#        self._label = tk.Label(main , text = text ,font = ("Ariel",fontsize),height = hight , width = width , bg = mainColor)
#        self._label.grid(row = 0, column = 0)
#        self._label.bind("<Enter>" , lambda event: self._label.configure(bg = enterColor))
#        self._label.bind("<Leave>" , lambda event: self._label.configure(bg = mainColor))
        
class Button:
    def __init__(self,main, text, mainColor, enterColor, hight = 2, width = 50, fontsize = 12):
        self.inFlag = True
        self.root = main
        self.font =  fontsize
        self._label = tk.Label(main , text = text ,font = ("Ariel",fontsize),height = hight , width = width , bg = mainColor)
        self.mainColor = mainColor
        self.after = 9
        self._label.grid(row = 0, column = 0)
        self._label.bind("<Enter>", lambda event: self.fadein(event,10))
        self._label.bind("<Leave>", self.leave)
    
    def fadein(self,event,i):
        if i >= 100:
            self.inFlag = True
            return
        if self.inFlag:
            self._label.configure(bg = f'gray{100-i}', fg = f'grey{i}',font = ("Ariel", self.font-1, "bold"))
            self.root.after(self.after, lambda event: self.fadein(event,i+2), event)
        else:
            self._label.configure(bg = self.mainColor, fg = "black", font = ("Ariel",self.font))           

        
    def setF(self,event):
        self._label.configure(bg = self.mainColor, fg = "black", font = ("Ariel",self.font))
        self.inFlag = True
        
    def leave(self,event):
        self.inFlag = False
        self.root.after(self.after+1, self.setF ,event)
        
        
class Tab():
    def __init__(self,root, text, i, color):
        self.i = i
        self.color = color
        self.root = root
        self.text = text
        self.frame = tk.Frame(root.tab_frames,bg = main_color)
        self.frame.configure(highlightbackground = main_color, highlightthickness = 2)
        self.l = tk.Label(self.frame, text = "    "+text+"    ", bg = color, font = ("Ariel",12))
        self.l.pack(padx = 0)
        self.bind()
        self.DClickLST = tk.Frame(self.root.tab_frames)
        self.double_click_flag = False
        
    def reduceGrid(self):
        self.i += -1
        self.frame.grid_forget()
        self.frame.grid(row = 0 ,column = self.i)
        
        
    def mouse_click(self,event):
        '''  delay mouse action to allow for double click to occur
        '''
        self.root.root.after(200, self.mouse_action, event)

    def double_click(self,event):
        '''  set the double click status flag
        '''
#        global double_click_flag
        self.double_click_flag = True

    def mouse_action(self,event):
#        global double_click_flag
        if self.double_click_flag:
#            print('double mouse click event')
            self.dclick(None)
            self.double_click_flag = False
        else:
            self.root.tabPress(self.i)
#            print('single mouse click event')
        
        
    def dclick(self, event):
#        print(1)
        self.frame.grid_forget()
#        print(2)
        self.DClickLST.grid(row = 0 , column = self.i)
#        print(3)
        l1 = tk.Label(self.DClickLST, text = " / delete tab", bg = self.color)
        l1.grid(row = 0, column = 1)
        l1.bind("<Button-1>", lambda event: self.root.delete_tab(self.i))
        l1.bind("<Enter>" , lambda event: l1.configure(bg= "lightgrey", fg = "white"))
        l1.bind("<Leave>", lambda event: l1.configure(bg= self.color, fg = "black"))
        self.var = tk.StringVar(value = self.text)
#        print(4)
        def ent_press(event = None, sv = None):
#            print(9)
            self.l["text"] = "    "+self.var.get()+"    "
            self.text = self.var.get()
            self.root.tabs[self.i][0] = self.text
            self.DClickLST.grid_forget()
            self.frame.grid(row = 0, column = self.i)
#            print(10)
            self.root.adjustTabs()
#        print(5)
#        self.var.trace("w", lambda name, index, mode, sv = self.var: ent_press(sv))
#        print(6)
        E1 = tk.Entry(self.DClickLST, textvariable = self.var, width = 12, bg = self.color)
#        print(7)
        E1.grid(row = 0 , column = 0)
        E1.bind("<Return>", ent_press)
#        E1.bind("<FocusOut>", ent_press)
#        print(8)
        
        
        
    def bind(self):
        self.frame.grid(row = 0, column = self.i)
        self.l.bind("<Enter>" , lambda event: self.l.configure(bg= "lightgrey", fg = "white"))
        self.l.bind("<Leave>", lambda event: self.l.configure(bg= self.color, fg = "black"))
        self.l.bind("<Double-Button-1>",  self.double_click)
        self.l.bind("<Button-1>",  self.mouse_click)
        
        
        
class main():
    def __init__(self):
        self.main = tk.Tk(className = " Self Task Maneger")
        self.main["background"] = main_color
        self.root = tk.Frame(self.main, bg = main_color)
        self.root.pack(pady = 15)
        self.tab_frames = tk.Frame(self.root, bg = main_color)
        self.tab_frames.grid(row = 0, column = 1)
        self.frames = tk.Frame(self.root)
        self.frames.grid(row = 1, column = 1)
        self.leftFrame = tk.Frame(self.root)
        self.leftFrame.grid(row = 1, column = 0)
        self.rightFrame= tk.Frame(self.root)
        self.rightFrame.grid(row = 1, column = 2)
        self.newVar = tk.StringVar(value = "new tab")
        self.PFrame = tk.Frame(self.tab_frames, bg = main_color)
        tk.Label(self.PFrame,text = "   ", bg = main_color).grid(row = 1, column = 0)
        tk.Label(self.PFrame,text = "   ", bg = main_color).grid(row = 1, column = 3)
        self.newTab = tk.Entry(self.PFrame, textvariable = self.newVar, width = 11, relief = "flat", bg= main_color)
        self.newTabP = tk.Label(self.PFrame, text = " + ", bg = main_color)
        
        
        ############################################################3
        self.tabs = []
        self.headtabs = []
        self.curr = 0  #index of curr open tab
        self.file = "tasksTXT.txt"
        self.colors = tabs_colors
        self.loadFrames()
        self.leftVis = True
        self.rightVis = False
        
        
        
    def loadFrames(self):
        try:
            file = open(self.file,"r")
        except:
            file = open(self.file,"w")
            file.write("example tab%&(")
            file.close()
            file = open(self.file,"r")
        tmp = file.read().split("^*)")   # shift 6 8 0  splitting between tabs
        for tab in tmp:
            self.tabs.append(tab.split("%&(")) #shift 5 7 9 splitting between tab name and tasks
        for i in range(len(self.tabs)):
            if len(self.tabs[i]) != 2:
                self.tabs.pop(i)
                break
            self.headtabs.append( None )#creating a pointer
            framePoint = Queue(self.colors[i], self)
            framePoint.createQueue(self.tabs[i][1])
            self.tabs[i][1] = framePoint
            if i == 0:
                framePoint.pack()
                
            self.headtabs[i] = Tab(self, self.tabs[i][0], i, self.colors[i])
        
        #######################################
        #   creating the +tab
            
        self.PFrame.grid(row = 0, column = len(self.tabs))
        self.newTab.grid(row = 1, column = 2)
        self.newTabP.grid(row = 1, column = 1)
        self.adjustTabs()
        self.newTabP.bind("<Enter>" , lambda event: self.newTabP.configure(bg= "lightgrey", fg = "white"))
        self.newTabP.bind("<Leave>", lambda event: self.newTabP.configure(bg= main_color, fg = "black"))
        self.newTabP.bind("<Button-1>", self.create_new_tab)
        self.tabPress(0)


    def tabPress(self, i):
        if len(self.headtabs)==0:
            return
        self.headtabs[self.curr].frame.configure(highlightbackground = main_color)
        self.tabs[self.curr][1].unpack()
        self.curr = i
        self.headtabs[i].frame.configure(highlightbackground = self.headtabs[i].color)
        self.tabs[i][1].pack()
        
    def adjustTabs(self):
        if len(self.headtabs)==0:
            return
        eachlen = int((77/(len(self.headtabs)*1.6))*0.8)  #76, 68, 60, 51-44, 44-35,
        if len(self.headtabs) > 8:
            eachlen = int((77/(len(self.headtabs)*1.6))*0.8) -1
#        eachlen = 40 - (len(self.headtabs)^2)
#        print(f' eachlen = {eachlen}')
        for tab in self.headtabs:
            if len(tab.text) < eachlen:
                spaces = " "*((eachlen-len(tab.text))//2)
                tab.l["text"] = spaces + tab.text + spaces
            else:
                tab.l["text"] = tab.text[:eachlen]
        
        
    def create_new_tab(self, event):
        if len(self.tabs) == len(self.colors):
            self.newVar.set("no room")
            return
        self.tabs.append( [self.newVar.get() , ""] )
        self.newVar.set("new tab")
        framePoint = Queue(self.colors[len(self.tabs)-1], self)
        framePoint.createQueue("")
        self.tabs[-1][1] = framePoint
        self.headtabs.append( Tab(self, self.tabs[-1][0], len(self.tabs)-1 , self.colors[len(self.tabs)-1]))
        self.PFrame.grid_forget()
        self.PFrame.grid(row = 0, column = len(self.tabs)+1)
        self.adjustTabs()
        
        
    def delete_tab(self,i):
        if self.curr == i:
#            self.tabs[self.curr][1].unpack()
            if self.curr == 0:
                self.curr = 1
            else:
                self.curr = 0
        self.headtabs[i].DClickLST.grid_forget()
        self.headtabs.pop(i)
        self.tabs[i][1].unpack()
        self.tabs.pop(i)
        if self.curr > i:
            self.curr += -1
        self.tabs[self.curr][1].pack()
        self.colors.append(self.colors.pop(i))
        for ind in range(i,len(self.headtabs)):
            self.headtabs[ind].reduceGrid()
        self.adjustTabs()
    
    
    def run(self):
        self.main.mainloop()
        ##### ending program ######
        savedText  = ""
        try:
            os.mkdir("backup")
        except:
            pass
        f = open("backup/tmpSave.txt", "w")
        for i in range(len(self.tabs)):
            self.tabs[i][1].end_program()
            savedText += f'{self.tabs[i][0]}%&({self.tabs[i][1].file}'
            if i != len(self.tabs):
                savedText += "^*)"
        try:
            f.write(savedText)
            with open(self.file,"w") as file:
                file.write(savedText)
        except:
            raise Exception("unable to save current file, restoring last version")
        finally:
            f.close()
            


class Queue():
    def __init__(self, color, father):
        self.toDoList = None
        self.DoneList = None
        self.file = None
        self.tk_objects = []
        self.left_visible = True
        self.righ_visible = False
        self.color = color
        self.father = father
        self.root = father.frames
        
        self.main_canvas = tk.Canvas(self.root, height = 450, width = 800, bg = main_color)
#        self.main_canvas.pack()
        self.tk_objects.append(self.main_canvas)

        self.left_arrow = tk.Canvas(self.father.leftFrame,height = 400, width = 2, bg = "lightgrey")
        self.left_arrow.grid(row = 0, column = 0)
        self.tk_objects.append(self.left_arrow)
        
        self.Larrow = Button(self.left_arrow,">",main_color,"lightgrey",22,2)
        self.Larrow._label.bind("<Button-1>", self.press_leftArrow)
#        self.tk_objects.append(self.Larrow)
        
        self.right_arrow = tk.Canvas(self.father.rightFrame,height = 400, width = 2, bg = "lightgrey")
        self.right_arrow.grid(row = 0, column = 1)
        self.tk_objects.append(self.right_arrow)
        
        self.Rarrow = Button(self.right_arrow,"<",main_color,"lightgrey",22,2)
        self.Rarrow._label.bind("<Button-1>", self.press_rightArrow)
#        self.tk_objects.append(self.Rarrow)
        
        self.left = tk.Frame(self.father.leftFrame,height = 400, width = 100, bg = "lightgrey")
        self.left.grid(row = 0,column = 1)
        self.tk_objects.append(self.left)
        
        self.task_canvas = tk.Frame(self.main_canvas , height = 450 , width = 200 , bg = color)
        self.task_canvas.grid(row = 0, column  = 2)
        self.tk_objects.append(self.task_canvas)
        
        self.right = tk.Frame(self.father.rightFrame,height = 400, width = 100, bg = "lightblue")
        self.right.grid(row = 0,column = 0)
        self.tk_objects.append(self.right)
        
        rightHead = tk.Label(self.right, text = "Last Done:",height = 2, width = 40, bg = "lightblue", font = ("Ariel",10))
        rightHead.pack()
        
                
        leftHead = tk.Label(self.left, text = "Next to Do:",height = 2, width = 40, bg = "lightgrey", font = ("Ariel",10))
        leftHead.pack()
        
        self.next5 = tk.Label(self.left,height = 20, width = 40, bg = "lightgrey")
        self.next5.pack()
        
        self.last5 = tk.Label(self.right,height = 20, width = 40, bg = "lightblue")
        self.last5.pack()
        
        self.curHead = tk.Label(self.task_canvas, text = "Current Task:", bg= color , font = ("Ariel",10))
        self.curHead.grid(row = 0, column = 0)
        
        nuller = tk.Label(self.task_canvas,text="",bg = color)
        nuller.grid(row = 1, column = 0)
        
        self.curTask = tk.Label(self.task_canvas, text = "\n\n", bg= color, font = ("Ariel",16))   
        self.curTask.grid(row = 2, column = 0)
        
        nuller = tk.Label(self.task_canvas,text="",bg = color)
        nuller.grid(row = 3, column = 0)
        
        self.done = Button(self.task_canvas ,"Mark as Done",button_color,"lightgrey")
        self.done._label.bind("<Button-1>",self.press_done)
        self.done._label.grid(row = 4, column = 0)
        
#        self.begin_re_insert = Button(self.task_canvas ,"Re-insert task to the head of the queue","greenyellow","lightblue")
        self.begin_re_insert = Button(self.task_canvas ,"\u2baa back to head",button_color,"lightgrey")
        self.begin_re_insert._label.bind("<Button-1>",self.press_reinsert_beginning)
        self.begin_re_insert._label.grid(row = 5, column = 0)
        
#        self.last_re_insert = Button(self.task_canvas ,"Re-insert task to the tail of the queue","greenyellow","lightblue")
        self.last_re_insert = Button(self.task_canvas ,"\u2ba8 back to tail",button_color,"lightgrey")
        self.last_re_insert._label.bind("<Button-1>",self.press_reinsert_end)
        self.last_re_insert._label.grid(row = 6, column = 0)
        
        nuller = tk.Label(self.task_canvas,text = "", bg = color)
        nuller.grid(row = 7, column = 0, pady = 20)
        
        self.adder = ScrolledText(self.task_canvas,height = 4, width = 30, font = ("Ariel", 10), bg = button_color)
        self.adder.insert(tk.INSERT," add task here!")
        self.adder.grid(row = 8,column = 0)
        
        nuller = tk.Label(self.task_canvas,text="",bg = color)
        nuller.grid(row = 9, column = 0)
        
        self.add = Button(self.task_canvas ,"Add Task",button_color,"lightgrey")
        self.add._label.bind("<Button-1>",self.press_add)
        self.add._label.grid(row = 10, column = 0)
    
        
    def extract(self,lst):
        retxt = ""
        for task in lst[:5]:
            retxt += "\n\n\n"+task
        return retxt
    
    def is_visible(self,ob):
        try:
            ob.pack_info()
        except tk.TclError:
        # pack_info raises if pack hasn't been
        # called yet.
            return bool(ob.grid_info())
        # grid_info returns {} if grid hasn't been
        # called yet.
        else:
            return True
        
    
    def press_done(self,event):
        if len(self.toDoList) > 0:
            cur_task = self.toDoList.pop(0)
            self.DoneList.append(cur_task)
        else:
            cur_task = ""
        self.curTask["text"] = cur_task
        self.refrash()
        
        
    def press_leftArrow(self,event):
        if self.is_visible(self.left):
            self.left.grid_remove()
            self.left_visible = False
            self.Larrow._label["text"] = "<"
        else:
            self.left.grid(row = 0,column = 1)
            self.left_visible = True
            self.Larrow._label["text"] = ">"
     
    def press_rightArrow(self, event):
        if self.is_visible(self.right):
            self.right.grid_remove()
            self.righ_visible = False
            self.Rarrow._label["text"] = ">"
        else:
            self.right.grid(row = 0,column = 0)
            self.righ_visible = True
            self.Rarrow._label["text"] = "<"
        
    def press_reinsert_beginning(self,event):
        if len(self.toDoList)>1:
            tmp = self.toDoList.pop(1)
            self.toDoList = [tmp] + self.toDoList[:]
            self.curTask["text"] = tmp
        self.refrash()

       
    def press_reinsert_end(self,event):
        if len(self.toDoList)>1:
            tmp = self.toDoList.pop(0)
            self.toDoList.append(self.curTask["text"])
            self.curTask["text"] = tmp
        self.refrash()
    
    def press_add(self, event):
        curtask = self.adder.get('1.0', 'end-1c')
        if curtask.replace(" ","").replace("\n","") != "":
            self.adder.delete('1.0', 'end-1c')
            self.toDoList.append(curtask)
            self.refrash()
        
        
    def refrash(self):
#        print(self.toDoList, self.DoneList)
        self.next5.config(text = self.extract(self.toDoList[1:6]))
        self.last5.config(text = self.extract(self.DoneList[-5:]))
        if len(self.toDoList)>0:
            self.curTask.configure(text = self.toDoList[0])
        else:
            self.curTask.configure(text = "")
        
        
    def end_program(self):
        re_write = ""
        for task in self.toDoList:
            re_write += task + "#%&"
        for task in self.DoneList:
            if task != "":
                re_write += task + "@$^"
        self.file = re_write.replace("  "," ").replace("@$^@$^","@$^")\
                        .replace("\n\n","\n").replace("#%&#%&","#%&")\
                                .replace("@$^@$^","@$^").replace("\n \n","\n").replace("#%& #%&","#%&")
                                
                                        
    def unpack(self):
        self.main_canvas.pack_forget()
        self.task_canvas.pack_forget()
        self.left.grid_forget()
        self.left_arrow.grid_forget()
        self.right.grid_forget()
        self.right_arrow.grid_forget()
        
    def pack(self):
        self.main_canvas.pack()
        self.task_canvas.pack()
        if self.is_visible(self.left):
            self.Larrow._label["text"] = ">"
        else:
            self.Larrow._label["text"] = "<"
        self.left_arrow.grid(row = 0, column = 0)
        if self.is_visible(self.right):
            self.Rarrow._label["text"] = "<"
        else:
            self.Rarrow._label["text"] = ">"
        self.right_arrow.grid(row = 0, column = 1)
        if self.left.winfo_ismapped():
            self.press_leftArrow(None)
    
    
    def createQueue(self, data_text):
        self.toDoList = data_text.split("#%&")
        self.file = data_text
        tmp = self.toDoList[-1]
        if "@$^" not in self.toDoList[0]:
            self.curTask.config(text = self.toDoList[0])
        self.toDoList = self.toDoList[:-1]
        self.DoneList = tmp.split("@$^")
        self.refrash()
#        self.press_leftArrow(None)
#        self.press_rightArrow(None)
        self.unpack()
        
        
        
if __name__ == '__main__':
    M = main()
    M.run()
        