import datetime as dt
from dataclasses import dataclass
# from asyncio import tasks
# from email import message
from threading import Thread
import sqlite3
from time import sleep
from tkinter.ttk import Combobox
from tkinter.ttk import Separator
import pandas as pd
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import askquestion
import os
# from sqlalchemy import true
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from pyparsing import col

# datapath = 'cd C:\Users\Alandalus\python\projects\ToD2\data'

def save_task(e0,e1=Entry()):

    global no_tasks,ab,sb,tasks,checkboxs,bools,namtask,slb,hb,change,descr,important,urgent,boolsimp,boolsurg

    change = True

    ab.grid_forget()
    sb.grid_forget()
    
    namtask.append(e0.get())
    descr.append(e1.get())
    bools.append(BooleanVar())

    e0.destroy()
    e1.destroy()

    for i in range(len(bools)):
        tasks[namtask[i]]=bools[i].get()

    if kind == 'normal':

        ab = Button(normal,text='Add',command=add_task)

        checkboxs.append(Checkbutton(normal, text=namtask[-1], variable=bools[-1], onvalue=True, offvalue=False))

        for nocheckbox in range(len(checkboxs)):
            checkboxs[nocheckbox].grid(row=nocheckbox+1,column=0,columnspan=2, padx=10,pady=10)

        ab.grid(row=no_tasks+1,column=0,pady=12)
        slb.grid(row=no_tasks+2,column=0,pady=9)
        hb.grid(row=no_tasks+2,column=2,pady=9)

    elif kind == 'professional':

            ab = Button(professional,text='Add',command=add_task)

            checkboxs.append(Checkbutton(professional, text=namtask[-1], variable=bools[-1], onvalue=True, offvalue=False))

            for nocheckbox in range(len(checkboxs)):

                Label(professional,text=descr[nocheckbox],font='Times 9').grid(row=nocheckbox+1,column=3,padx=12)
                checkboxs[nocheckbox].grid(row=nocheckbox+1,column=0,columnspan=2, padx=10,pady=10)

            ab.grid(row=no_tasks+1,column=0,pady=12)
            slb.grid(row=no_tasks+2,column=0,pady=9)
            hb.grid(row=no_tasks+2,column=3,pady=9)

    elif kind == 'Advanced':

            ab = Button(Advanced,text='Add',command=add_task)

            boolsimp.append(BooleanVar())
            boolsurg.append(BooleanVar())

            checkboxs.append(Checkbutton(Advanced, text=namtask[-1], variable=bools[-1], onvalue=True, offvalue=False))
            important.append(Checkbutton(Advanced, text='Important', variable=boolsimp[-1], onvalue=True, offvalue=False))
            urgent.append(Checkbutton(Advanced, text='urgent', variable=boolsurg[-1], onvalue=True, offvalue=False))

            for nocheckbox in range(len(checkboxs)):

                checkboxs[nocheckbox].grid(row=nocheckbox+1,column=0,columnspan=2, padx=10,pady=10)
                important[nocheckbox].grid(row=nocheckbox+1,column=4,columnspan=2, padx=10,pady=10)
                urgent[nocheckbox].grid(row=nocheckbox+1,column=6,columnspan=2, padx=10,pady=10)

                Label(Advanced,text=descr[nocheckbox],font='Times 9').grid(row=nocheckbox+1,column=2,padx=12,columnspan=2)

            ab.grid(row=no_tasks+1,column=0,pady=12)
            slb.grid(row=no_tasks+2,column=0,pady=9)
            hb.grid(row=no_tasks+2,column=3,pady=9)

    _update()

def _update():

    global bools,tasks,namtask,completed,date,textdate,entereddate

    for i in range(len(bools)):

        tasks[namtask[i]]=bools[i].get()

    if all(tasks.values()):
            completed = True

    else:
            completed = False

    try:
        textdate = entereddate.get()
        date = textdate

    except:
        date = textdate
    
def add_task():

    global no_tasks,normal,sb,professional,Advanced

    no_tasks+=1

    if kind == 'normal':

        e = Entry(normal, width=25, borderwidth=5)
        e.grid(row=no_tasks,column=1,columnspan=2, padx=10,pady=10)

        sb = Button(normal,text='Save',command=lambda:save_task(e))
        sb.grid(row=no_tasks,column=0,pady=12)

    elif kind == 'professional':

        e1 = Entry(professional, width=20, borderwidth=5)
        e1.grid(row=no_tasks,column=1,columnspan=2, padx=10,pady=10)

        e2 = Entry(professional, width=20, borderwidth=5)
        e2.grid(row=no_tasks,column=3,columnspan=2, padx=10,pady=10)

        sb = Button(professional,text='Save',command=lambda:save_task(e1,e2))
        sb.grid(row=no_tasks,column=0,pady=12)

    elif kind == 'Advanced' :

        e1 = Entry(Advanced, width=20, borderwidth=5)
        e1.grid(row=no_tasks,column=1,columnspan=2, padx=10,pady=10)

        e2 = Entry(Advanced, width=20, borderwidth=5)
        e2.grid(row=no_tasks,column=3,columnspan=2, padx=10,pady=10)

        sb = Button(Advanced,text='Save',command=lambda:save_task(e1,e2))
        sb.grid(row=no_tasks,column=0,pady=12)

    _update()

def saveTDL():

    _update()

    global tasks,kind,completed,date,issaved,change

    if change:

        ctdl.execute(f'SELECT date FROM to_do_dates')
        dates_in = ctdl.fetchall()

        for d in dates_in:
            if date in d:

                issaved = True

        if issaved:

            ctdl.execute(f'DELETE FROM to_do_tasks WHERE date = "{textdate}"')
            ctdl.execute(f'DELETE FROM to_do_dates WHERE date = "{textdate}"')

            issaved = False

            saveTDL()

        else:

            if kind == 'normal':
                for task in tasks:

                    ctdl.execute(f'INSERT INTO to_do_tasks(task,done,date,kind) VALUES("{task}","{tasks[task]}","{textdate}","{kind}")') 

                ctdl.execute(f"INSERT INTO to_do_dates(date,completed) VALUES('{textdate}','{completed}')")

            elif kind == 'professional':
                for task in tasks:

                    ctdl.execute(f'INSERT INTO to_do_tasks(task,done,date,kind,time) VALUES("{task}","{tasks[task]}","{textdate}","{kind}","{descr[list(tasks.keys()).index(task)]}")') 

                ctdl.execute(f'INSERT INTO to_do_dates(date,completed) VALUES("{textdate}","{completed}")')

            elif kind == 'Advanced':
                for task in tasks:

                    i = list(tasks.keys()).index(task)

                    ctdl.execute(f'INSERT INTO to_do_tasks(task,done,date,kind,time,important,urgent) VALUES("{task}","{tasks[task]}","{textdate}","{kind}","{descr[i]}","{boolsimp[i].get()}","{boolsurg[i].get()}")')

                ctdl.execute(f"INSERT INTO to_do_dates(date,completed) VALUES('{textdate}','{completed}')")


            issaved = True

        conn_tdl.commit()

    else:
        showinfo('NO DATA TO SAVE!',"You didn't give any data yet!")

def NTDL(root):

    global no_tasks,normal,tasks,checkboxs,bools,namtask,kind,entereddate,textdate,ab,slb,hb

    kind = 'normal'
    namtask=[]
    checkboxs=[]
    bools=[]
    tasks={}
    no_tasks=0

    root.destroy()
    
    normal = Tk()
    normal.title('Normal to do list')
    normal.iconbitmap('clipboard.ico')

    Label(normal,text='Date or Title',font='Times 9').grid(row=0,column=0,padx=12)

    entereddate = Entry(normal, width=25, borderwidth=5)
    entereddate.grid(row=0,column=1,columnspan=2, padx=20,pady=10)

    ab=Button(normal,text='Add',command=add_task)
    ab.grid(row=no_tasks+1,column=0,pady=12)

    slb = Button(normal,text='Save list',command=saveTDL)
    slb.grid(row=no_tasks+2,column=0,pady=9)

    hb = Button(normal,text='Home',command=lambda:tdl_back(normal))
    hb.grid(row=no_tasks+2,column=2,pady=9)

    normal.mainloop()

def tdl_back(root):

    global issaved,change

    if change:
        if issaved:

            root.destroy()

            home()

        else:

            saved = askquestion('Save?','Do you wanna save your progress?')

            if saved == 'yes':

                try:
                    saveTDL()
                except:
                    saveTDLdraft()

                tdl_back(root)

            else:

                root.destroy()

                home()
    else:

        try:
            saveTDLdraft()
        except:
            pass

        gohome(root)

def saveTDLdraft():

    _update()

    global issaved,draft_tasks,namtask

    issaved = True
    completed = True

    for i in range(len(draft_tasks.task)):
        namtask.append(draft_tasks.task.iloc[i])

    if draft_kind in ['normal','professional']:

        for i in range(len(bools)):
            ctdl.execute(f'UPDATE to_do_tasks SET done = "{bools[i].get()}" WHERE task = "{draft_tasks.task.iloc[i]}" AND date = "{date}"')
    
    elif draft_kind == 'Advanced':

            for i in range(len(bools)):
                print(bools[i].get())
                ctdl.execute(f'UPDATE to_do_tasks SET done = "{bools[i].get()}" WHERE task = "{draft_tasks.task.iloc[i]}" AND date = "{date}"')
                ctdl.execute(f'UPDATE to_do_tasks SET important = "{boolsimp[i].get()}" WHERE task = "{draft_tasks.task.iloc[i]}" AND date = "{date}"')
                ctdl.execute(f'UPDATE to_do_tasks SET urgent = "{boolsurg[i].get()}" WHERE task = "{draft_tasks.task.iloc[i]}" AND date = "{date}"')                

    for bool in bools:
        if bool.get() == False:
            completed = False
        

    ctdl.execute(f'UPDATE to_do_dates SET completed = "{completed}" WHERE date = "{date}"')

    conn_tdl.commit()

def get_tdl_draft(number,root):

    global bools,checkboxs,date,draft_tasks,namtask,tasks,textdate,uncompleted,dictdrafts,boolsimp,boolsurg,important,urgent,draft_kind

    in_it = False

    try:
        if int(number) in dictdrafts.values():
            in_it = True

        else:
            showinfo('Not found!',"There're no such a draft matching the number you entered!")

    except:
        showinfo('Not number!',"Please enter a number!")

    
    
    if in_it:

        number = uncompleted[int(number)-1][0]
        bools = []
        boolsurg = []
        boolsimp = []
        checkboxs = []
        important = []
        urgent = []
        namtask = []
        tasks = {}
        textdate = number
        date = number

        ctdl.execute(f'SELECT * FROM to_do_tasks where date = "{number}"')
        draft_tasks = pd.DataFrame(ctdl.fetchall(),columns=['task','done','date','kind',"time",'important','urgent'])
        try:
            draft_kind = draft_tasks.iloc[0,3]
        except:
            showerror("Not found!","the data for this date/title is lost.")
        root.destroy()

        draft_tdl = Tk()
        draft_tdl.title('Uncompleted to do list')
        draft_tdl.iconbitmap('clipboard.ico')

        Label(draft_tdl,text=number,font='Times 12').grid(row=0,column=0,padx=12,columnspan=3)

        s = Button(draft_tdl,text='Save',command=lambda:saveTDLdraft())
        s.grid(row=len(draft_kind)+2,column=0,columnspan=2, padx=10,pady=10)

        hb = Button(draft_tdl,text='Home',command=lambda:tdl_back(draft_tdl))
        hb.grid(row=len(draft_kind)+2,column=3,pady=9,padx=9)

        if draft_kind == 'normal':

            for i in range(len(draft_tasks.task)):

                namtask.append(draft_tasks.task.iloc[i])
                
                bools.append(BooleanVar())

                checkboxs.append(Checkbutton(draft_tdl, text=draft_tasks.task.iloc[i], variable=bools[i], onvalue=True, offvalue=False))
                checkboxs[i].grid(row=i+1,column=0,columnspan=2, padx=10,pady=10)

                if draft_tasks.done.iloc[i]=='True':
                    checkboxs[i].select()

        if draft_kind == 'professional':

            for i in range(len(draft_tasks.task)):

                namtask.append(draft_tasks.task.iloc[i])
                bools.append(BooleanVar())

                checkboxs.append(Checkbutton(draft_tdl, text=draft_tasks.task.iloc[i], variable=bools[i], onvalue=True, offvalue=False))
                checkboxs[i].grid(row=i+1,column=0,columnspan=2, padx=10,pady=10)

                Label(draft_tdl,text=draft_tasks.time.iloc[i]).grid(row=i+1,column=3,columnspan=2, padx=10,pady=10)

                if draft_tasks.done.iloc[i]=='True':
                    checkboxs[i].select()

        if draft_kind == 'Advanced':

            for i in range(len(draft_tasks.task)):

                namtask.append(draft_tasks.task.iloc[i])

                bools.append(BooleanVar())
                boolsimp.append(BooleanVar())
                boolsurg.append(BooleanVar())

                checkboxs.append(Checkbutton(draft_tdl, text=draft_tasks.task.iloc[i], variable=bools[i], onvalue=True, offvalue=False))
                checkboxs[i].grid(row=i+1,column=0,columnspan=2, padx=10,pady=10)

                important.append(Checkbutton(draft_tdl, text='Important', variable=boolsimp[i], onvalue=True, offvalue=False))
                important[i].grid(row=i+1,column=4,columnspan=2, padx=10,pady=10)
                urgent.append(Checkbutton(draft_tdl, text='Urgent', variable=boolsurg[i], onvalue=True, offvalue=False))
                urgent[i].grid(row=i+1,column=6,columnspan=2, padx=10,pady=10)

                Label(draft_tdl,text=draft_tasks.time.iloc[i]).grid(row=i+1,column=2,columnspan=2, padx=10,pady=10)

                if draft_tasks.done.iloc[i]=='True':
                    checkboxs[i].select()
                if draft_tasks.important.iloc[i]=='True':
                    important[i].select()
                if draft_tasks.urgent.iloc[i]=='True':
                    urgent[i].select()
                
        draft_tdl.mainloop()

def tdl_drafts(root):

    global uncompleted,dictdrafts

    dictdrafts = {}

    root.destroy()

    drafts = Tk()
    drafts.title('draft To do lists')
    drafts.iconbitmap('file-download.ico')

    ctdl.execute('SELECT date FROM to_do_dates where completed = "False"')
    uncompleted = ctdl.fetchall()
    
    Label(drafts,text= "Enter number of darft!").pack()
    e = Entry(drafts, width=25, font=('Arial',9))
    e.pack()

    Button(drafts ,text = 'Go',command=lambda:get_tdl_draft(e.get(),drafts)).pack()

    for un in uncompleted:

        Label(drafts,text=f"{str(uncompleted.index(un)+1)}: {un[0]}",font='Times 12').pack()

        dictdrafts[un[0]] = uncompleted.index(un)+1

    Button(drafts ,text = 'Back',command=lambda:TDL(drafts)).pack()

    drafts.mainloop()

def gohome(root):

    root.destroy()

    home()

def PTDL(root):

    global no_tasks,professional,tasks,checkboxs,bools,namtask,kind,entereddate,textdate,ab,slb,hb,descr

    kind = 'professional'
    namtask=[]
    descr = []
    checkboxs=[]
    bools=[]
    tasks={}
    no_tasks=0

    root.destroy()
    
    professional = Tk()
    professional.title('Professional to do list')
    professional.iconbitmap('clipboard.ico')

    Label(professional,text='Date or Title',font='Times 9').grid(row=0,column=0,padx=12)
    
    entereddate = Entry(professional, width=40, borderwidth=5)
    entereddate.grid(row=0,column=1,columnspan=3, padx=20,pady=10)

    ab=Button(professional,text='Add',command=add_task)
    ab.grid(row=no_tasks+1,column=0,pady=12)

    slb = Button(professional,text='Save list',command=saveTDL)
    slb.grid(row=no_tasks+2,column=0,pady=9)

    hb = Button(professional,text='Home',command=lambda:tdl_back(professional))
    hb.grid(row=no_tasks+2,column=3,pady=9)

    professional.mainloop()

def ATDL(root):

    global no_tasks,Advanced,tasks,checkboxs,bools,namtask,kind,entereddate,textdate,ab,slb,hb,descr,important,urgent,boolsimp,boolsurg

    kind = 'Advanced'
    namtask=[]
    descr = []
    important = []
    boolsimp = []
    urgent = []
    boolsurg = []
    checkboxs=[]
    bools=[]
    tasks={}
    no_tasks=0

    root.destroy()
    
    Advanced = Tk()
    Advanced.title('Advanced to do list')
    Advanced.iconbitmap('clipboard.ico')

    Label(Advanced,text='Date or Title',font='Times 9').grid(row=0,column=0,padx=12)
    
    entereddate = Entry(Advanced, width=40, borderwidth=5)
    entereddate.grid(row=0,column=1,columnspan=3, padx=20,pady=10)

    ab=Button(Advanced,text='Add',command=add_task)
    ab.grid(row=no_tasks+1,column=0,pady=12)

    slb = Button(Advanced,text='Save list',command=saveTDL)
    slb.grid(row=no_tasks+2,column=0,pady=9)

    hb = Button(Advanced,text='Home',command=lambda:tdl_back(Advanced))
    hb.grid(row=no_tasks+2,column=3,pady=9)

    Advanced.mainloop()

def TDL(root):

    global issaved

    issaved = False

    root.destroy()

    root2=Tk()
    root2.title('To do list')
    root2.iconbitmap('confused.ico')

    Button(root2,text = 'back',command=lambda:gohome(root2)).grid(row=0,column=0)
    Button(root2,text = 'drafts',command=lambda:tdl_drafts(root2)).grid(row=0,column=3)

    lbl = Label(root2,text='Do you want your to do list to be..',font='Times 12 roman normal')
    lbl.grid(row=1,column=0,columnspan=4)

    Button(root2,text='Normal',padx=100,pady=10,command=lambda:NTDL(root2)).grid(row=2,column=0,columnspan=4)
    Button(root2,text='Professional',padx=88,pady=10,command=lambda:PTDL(root2)).grid(row=3,column=0,columnspan=4)
    Button(root2,text='Advanced',padx=93.5,pady=10,command=lambda:ATDL(root2)).grid(row=4,column=0,columnspan=4)

    root2.mainloop()





@dataclass
class field:
    field_name : str
    tasks_list : list
    levels_list : list
    starts_list : list  
    ends_list : list
    hours_list : list
    tasks_scores : list


def updatescore(lbl, fields, ponuses):

    tasks_number = 0
    tasts_scores_ = 0
    ponuses_scores = 0

    for field in fields:
        for task_score,task_level in zip(field.tasks_scores,field.levels_list):
            tasks_number +=1
            print(tasks_number)
            tasts_scores_ += (int(task_score.get()) + 20/task_level)
            print(tasts_scores_)
    
    for ponus in ponuses.values():

        ponuses_scores += ponus



    try:
        lbl['text'] = str( round((tasts_scores_+ponuses_scores) / tasks_number))
    except:
        lbl['text'] = str(ponuses_scores)


def count_hours(f,l):

    if l >= f : return l-f

    else: return 24 + l - f


def submit_field(tod,button,scores):

    try:
        
        for score in scores :

            updatescore(scorelbl,fields_list,ponuses)

            x = int(score.place_info()['x'])
            y = int(score.place_info()['y'])

            Label(tod,text=score.get(),font='Times 12 roman normal').place(x=x,y=y)

            score.place_forget()

        button.place_forget()

    except: showerror('Lake of data',"Make sure you entered all your data!")


    
        


def savefield(tod,FieldName,button,tasks,levels,starts,ends):

    global fields_list,first_field

    is_not_empty = True
    
    for i in range(len(tasks)):

        if tasks[i].get() == '' or levels[i].get() == '' or starts[i].get() == '' or ends[i].get() == '': is_not_empty = False
    
    try:

        if is_not_empty:

            tasks_list_ = []
            levels_list_ = []
            starts_list_ = []
            ends_list_ = []
            hours_list_ = []
            scores = []
            scores_values = []

            save_bottun_x_place = int(button.place_info()['x'])
            Label(tod,text='Hours Number',font='Times 12 roman normal').place(x=save_bottun_x_place,y=60)
            Label(tod,text='Task Score',font='Times 12 roman normal').place(x=save_bottun_x_place+150,y=60)


            for i in range(len(tasks)):

                level = int(levels[i].get())
                start = int(starts[i].get())
                end = int(ends[i].get())

                tasks_list_.append(tasks[i].get())
                task_Label = Label(tod,text=tasks[i].get(),font='Times 12 roman normal')
                x = int(tasks[i].place_info()['x'])
                y = int(tasks[i].place_info()['y'])
                tasks[i].place_forget()
                task_Label.place(x=x,y=y)

                levels_list_.append(level)
                level_Label = Label(tod,text=level,font='Times 12 roman normal')
                x = int(levels[i].place_info()['x'])
                y = int(levels[i].place_info()['y'])
                levels[i].place_forget()
                level_Label.place(x=x,y=y)

                starts_list_.append(start)
                start_Label = Label(tod,text=str(start),font='Times 12 roman normal')
                x = int(starts[i].place_info()['x'])
                y = int(starts[i].place_info()['y'])
                starts[i].place_forget()
                start_Label.place(x=x,y=y)

                ends_list_.append(end)
                end_Label = Label(tod,text=str(end),font='Times 12 roman normal')
                x = int(ends[i].place_info()['x'])
                y = int(ends[i].place_info()['y'])
                ends[i].place_forget()
                end_Label.place(x=x,y=y) 

                hours = count_hours(start,end)
                hours_list_.append(hours)
                hours_label = Label(tod,text=str(hours),font='Times 12 roman normal')
                hours_label.place(x=x+100,y=y)
                
                scores_values.append(IntVar())
                scores.append(Combobox(tod,textvariable=scores_values[i]))
                scores[i]['values'] = [x*5 for x in range(41)]
                scores[i]['state'] = 'readonly'
                scores[i].place(x=x+200,y=y)
                
            fields_list.append(field(field_name=FieldName,tasks_list=tasks_list_,levels_list=levels_list_,starts_list=starts_list_,ends_list=ends_list_,hours_list=hours_list_,tasks_scores=scores))

            button.place_forget()

            submit_field_b = Button(tod,text='Submet',padx=18,pady=10,command=lambda : submit_field(tod,submit_field_b,scores))
            submit_field_b.place(x=x+350,y=y)

            addf = Button(tod,text='New Field',padx=18,pady=10,command=lambda : addfield(tod, addf))
            addf.place(x=10,y=y+50)

        else:
            raise ValueError
            
    except: showerror('Lake of data',"Make sure you entered all your data!")
        

def fieldfunc(tod,button,number,name,lbl1,lbl2):

    global first_field

    lbl1.place_forget()
    lbl2.place_forget()

    lE = []
    liV = []
    lCB = []
    start_hour = []
    end_hour = []
    start_list = []
    end_list = []

    try:
        n = int(number.get())
    
        if name.get() == '':
            raise ValueError('')

    except: showerror('Lake of data',"Make sure you entered all your data!")

    x=int(button.place_info()['x'])
    y=int(button.place_info()['y'])

    fn = Label(tod,text='{} : '.format(name.get()),font='Times 14 roman normal')
    fn.place(x=x,y=y + 50 )

    number.place_forget()
    button.place_forget()
    name.place_forget()

    if first_field :

        Label(tod,text='Task Name',font='Times 12 roman normal').place(x=x+100,y=y)
        Label(tod,text='Importance Level',font='Times 12 roman normal').place(x=x+225,y=y)
        Label(tod,text='Start Time',font='Times 12 roman normal').place(x=x+380,y=y)
        Label(tod,text='End Time',font='Times 12 roman normal').place(x=x+455,y=y)

        first_field = False

    for i in range(n):
        
        _y = y + 50 * (i + 1)

        lE.append(Entry(tod,width=16, borderwidth=5))
        lE[i].place(x=x+100,y=_y)

        liV.append(IntVar())
        start_list.append(IntVar())
        end_list.append(IntVar())
        
        lCB.append(Combobox(tod,textvariable=liV[i]))
        lCB[i]['values'] = [1,2,3,4]
        lCB[i]['state'] = 'readonly'
        lCB[i].place(x=x+225,y=_y)

        start_hour.append(Combobox(tod,textvariable=start_list[i],width=8))
        start_hour[i]['values'] = list(range(1,25))
        start_hour[i]['state'] = 'readonly'
        start_hour[i].place(x=x+380,y=_y)

        end_hour.append(Combobox(tod,textvariable=end_list[i],width=8))
        end_hour[i]['values'] = list(range(1,25))
        end_hour[i]['state'] = 'readonly'
        end_hour[i].place(x=x+455,y=_y)

    sv_fld_btn = Button(tod,text='Save Field',padx=16,pady=4,command=lambda : savefield(tod,fn.cget('text'),sv_fld_btn,lE,lCB,start_hour,end_hour))
    sv_fld_btn.place(x=x+550,y=_y-10)


def addfield(tod,button):

    y=int(button.place_info()['y'])
    x=int(button.place_info()['x'])

    button.place_forget()

    fnlbl = Label(tod,text='Field name : ',font='Times 12 roman normal')
    fnlbl.place(x=x+100,y=y)

    fieldName = Entry(tod,width=10, borderwidth=5)
    fieldName.place(x=x+200,y=y)

    ntlbl = Label(tod,text='Tasks number : ',font='Times 12 roman normal')
    ntlbl.place(x=x+300,y=y)

    tn = IntVar()
    tncb = Combobox(tod,textvariable=tn)
    tncb['values'] = [1,2,3,4,5,6]
    tncb['state'] = 'readonly'
    tncb.place(x=x+400,y=y)

    save = Button(tod,text='Save',padx=18,pady=8,command=lambda : fieldfunc(tod,save,tncb,fieldName,fnlbl,ntlbl))
    save.place(x=x,y=y)

def submit_ponus(tod,name,score,button):

    global ponuses

    score_number = score.get()

    if score_number != '':

        ponuses[name] = int(score_number)

        x = int(score.place_info()['x'])
        y = int(score.place_info()['y'])
        
        Label(tod,text=score_number,font='Times 12 roman normal').place(x=x,y=y)

        x = int(button.place_info()['x'])
        y = int(button.place_info()['y'])

        new_ponus =  Button(tod,text='Add Ponus',padx=14,pady=8,command=lambda : addponus(tod,new_ponus))
        new_ponus.place(x=x,y=y)

        button.place_forget()
        score.place_forget()

    else: showerror('',"Enter score!")

    updatescore(scorelbl,fields_list,ponuses)


def save_ponus(tod,entry,button):

    name = entry.get()

    if name != '' and name not in ponuses.keys():

        bx = int(button.place_info()['x'])
        by = int(button.place_info()['y'])
        ex = int(entry.place_info()['x'])
        ey = int(entry.place_info()['y'])

        Label(tod,text=name,font='Times 12 roman normal').place(x=ex,y=ey)

        ponus_score = Combobox(tod,textvariable=IntVar())
        ponus_score['values'] = [x*5 for x in range(1,25)]
        ponus_score['state'] = 'readonly'
        ponus_score.place(x=bx-75,y=by+12)

        submit_ponus_button = Button(tod,text='Submit',padx=14,pady=8,command=lambda : submit_ponus(tod,name,ponus_score,submit_ponus_button))
        submit_ponus_button.place(x=bx-25,y=by+40)

        entry.place_forget()
        button.place_forget()

    else: showerror('',"Unvalid data!")


def addponus(tod,button):

    y = int(button.place_info()['y'])
    x = int(button.place_info()['x'])

    ponus_name = Entry(tod,width=14, borderwidth=5)
    ponus_name.place(x=980,y=y+10)

    submit_ponus_button = Button(tod,text='Save',padx=14,pady=8,command=lambda : save_ponus(tod, ponus_name,submit_ponus_button))
    submit_ponus_button.place(x=x+25,y=y)

    button.place_forget()
    

def quittod(tod):
    pass


def todfun(root):

    global fields_list,first_field,scorelbl,ponuses,tod

    first_field = True
    fields_list = []
    ponuses = {}

    root.destroy()

    tod = Tk()
    tod.title("ToD")
    tod.iconbitmap('timer.ico')
    tod.geometry("1200x900")

    lbl = Label(tod,text="Score : ",font='Times 16 roman normal')
    lbl.place(x=480, y=0)

    scorelbl = Label(tod,text='0',font='Times 16 roman normal')
    scorelbl.place(x=550, y=0)

    addf = Button(tod,text='New Field',padx=18,pady=10,command=lambda : addfield(tod, addf))
    addf.place(x=10, y=60)
    
    separator = Separator(tod, orient='vertical')
    separator.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)

    ponus_button = Button(tod,text='Add Ponus',padx=14,pady=8,command=lambda : addponus(tod,ponus_button))
    ponus_button.place(x = 1090, y=60)
    
    today = Label(tod,text="{}".format(dt.date.today()),font='Times 16 roman normal')
    today.place(relx = 1.0,rely = 0.0,anchor ='ne')

    Button(tod,text='Quit',padx=18,pady=10,command=lambda : quittod(tod)).place(x=10, y=4)

    updatescore(scorelbl,fields_list,ponuses)


    tod.mainloop()


def home():

    global first_time

    root1 = Tk()
    root1.title('How?')
    root1.iconbitmap('question.ico')

    if first_time:

        t = Thread(target=lambda:sleep(1), daemon=True)
        t.start()

        root1.withdraw()

        loading_screen = Toplevel(root1)
        loading_screen.title('Welcome!')
        loading_screen.iconbitmap('customer.ico')

        loading_label = Label(loading_screen, text="This program was created as an attempt to help ambitious\n friends increase performance and achieve goals.",font='Times 12 roman normal')
        loading_label.grid(pady=40,padx=25)

        while t.is_alive():
            root1.update()

        loading_screen.destroy()

        root1.deiconify()
        root1.focus_force()

    lbl = Label(root1,text='You want a..',font='Times 12')
    lbl.grid(row=0,column=0,columnspan=2,pady=20)

    todolist = Button(root1,text='To do list',padx=20,pady=10,command=lambda:TDL(root1))
    todolist.grid(row=1,column=0)

    tod = Button(root1,text='ToD paper',padx=20,pady=10,command=lambda:todfun(root1))
    tod.grid(row=1,column=1)

    first_time = False

    root1.mainloop()


os.chdir(__file__[:-7]+'\data')

first_time=True
change = False
issaved = False

conn_tdl = sqlite3.connect('to_do_lists.db')
ctdl = conn_tdl.cursor()

ctdl.execute("""
    CREATE TABLE IF NOT EXISTS to_do_tasks(
        task text,
        done text,
        date text,
        kind text,
        time text,
        important text,
        urgent text
    )""")

ctdl.execute("""
    CREATE TABLE IF NOT EXISTS to_do_dates(
        date text,
        completed text,
        FOREIGN KEY (date) REFERENCES to_do_tasks(date))""")

conn_tod = sqlite3.connect('ToD_notebook.db')
ctod = conn_tod.cursor()

conn_tdl.commit()
conn_tod.commit()

home()

