#import tkinter as tk1   # python3
import Tkinter as tk   # python
from Tkinter import *
import live_withfunct as lv
import ttk, time, datetime
import sqlite3
import tkMessageBox
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import serial
import time
import readline
import re, sys
import csv
from sklearn import preprocessing, cross_validation, neighbors, svm
import time
from scipy.signal import butter, lfilter
import requests
import tkFileDialog
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import subprocess
import os
import xlwt
import glob

column_no = 0


wb = xlwt.Workbook()
ws1 = wb.add_sheet("DATA", cell_overwrite_ok = True)
ws2 = wb.add_sheet("RRI", cell_overwrite_ok = True)
ws3 = wb.add_sheet("FEATURES", cell_overwrite_ok = True)
ws4 = wb.add_sheet("Sensor Data", cell_overwrite_ok = True)



TITLE_FONT = ("Helvetica", 10)
style.use("ggplot")
f = Figure(figsize = (5,5), dpi = 20)
a = f.add_subplot(111)



    
def animations(i):
    u_cols = ['heart']
    files = pd.read_csv("/home/pi/Desktop/new GUI1/data.csv", names = u_cols)
    files[files>1000] = 300
    cal_mean = int (files["heart"].mean())
    files[files<=100] = cal_mean
    files = files.fillna(cal_mean)
    files = files[5:1112].reset_index(drop=True)
    filtered = lv.butter_lowpass_filter(files.heart, 2.5, 100.0, 5)
    a.clear()
    a.plot(filtered, alpha=0.5, color='blue')
    

class Samplegui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)       
        

        self.frames = {}
        for F in (Mainform, Firstform, Secondform, Thirdform, Fourthform, Fifthform):
            form_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[form_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Mainform")

    def show_frame(self, form_name):
        '''Show a frame for the given page name'''
        frame = self.frames[form_name]
        frame.tkraise()


class Mainform(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        FONT = ("Helvetica", 12, "bold")
        label = tk.Label(self, text="RR-Interval Measurement for HRV Analysis          ", font=FONT)
        label.grid(row=1, column=2)
        labe2 = tk.Label(self, text="Instructions:                                                          ", font=TITLE_FONT, anchor = W)
        labe2.grid(row=3, column=2)

        labe3 = tk.Label(self, text="1:Pleasse clean your hands...!                                   ", font=TITLE_FONT)        
        labe3.grid(row=4, column=2)

        labe4 = tk.Label(self, text="2:Oils or sweat on skin cause noise..!                      ", font=TITLE_FONT)
        labe4.grid(row=5, column=2)
        

        button1 = tk.Button(self, text="New",
                            command=lambda: controller.show_frame("Firstform"))
        button2 = tk.Button(self, text="Start",
                            command=lambda: controller.show_frame("Secondform"))
        button1.grid(row=3, column=1,  padx=1, pady=1, ipadx=3, ipady=3)
        button2.grid(row=4, column=1,  padx=1, pady=1, ipadx=3, ipady=3)
        
        button3 = tk.Button(self, text="View",
                            command=lambda: controller.show_frame("Thirdform"))
        button4 = tk.Button(self, text="Help",
                            command=lambda: controller.show_frame("Fifthform"))
        button3.grid(row=5, column=1,  padx=1, pady=1, ipadx=3, ipady=3)
        button4.grid(row=6, column=1,  padx=1, pady=1, ipadx=3, ipady=3)




class Firstform(tk.Frame):
##    user_id = ""
##    name = ""
##    gender = ""
##    age = ""
##    date = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Add New Record", font=TITLE_FONT)                         
        label.grid(row=0, column=1)

        # create string variable----------------------------------------------------------
        self.user_id = tk.StringVar()
        self.name = tk.StringVar()
        self.gender = tk.StringVar()
        self.age = tk.StringVar()
        self.date = tk.StringVar()

        label1 = tk.Label(self, text=" ID ").grid(row=1)

        
##        number = ('1','2')
##        box = ttk.Combobox(self, values = number, postcommand = state = 'readonly', width = 19)
##        box.current(1)
##        box.set('')
##        box.grid(row=1,column=1)
        

        
        label2 = tk.Label(self, text=" Name").grid(row=2)
        label3 = tk.Label(self, text="Gender").grid(row=3)
        gender = ('Male','Female')
        box1 = ttk.Combobox(self, values = gender, state = 'readonly', textvariable = self.gender)
        box1.current(1)
        box1.set('')
        box1.grid(row=3,column=1)
        box1.delete(0, END)


        
        label4 = tk.Label(self, text="Age").grid(row=6)
##        age_group = ('20-25', '25-30', '30-35', '35-40')
##        box2 = ttk.Combobox(self, values = age_group, state = 'readonly')
##        box2.current(1)
##        box2.set('')
##        box2.grid(row=6,column=1)




        label5 = tk.Label(self, text= "Date").grid(row=7)
        
        self.e1 = tk.Entry(self, textvariable = self.user_id)
        conn = sqlite3.connect('hrv.db')
        c = conn.cursor()
        c.execute('SELECT MAX(user_id) FROM userinfo')
        self.data = c.fetchone()
        value = 1
        self.data = int(self.data[0] + value)
        self.e1.insert(0,self.data)
        conn.commit()
        c.close()
        conn.close()
        
        
        
        
        #self.e1.configure(state='readonly')



        
        self.e2 = tk.Entry(self, textvariable = self.name)
        self.e3 = tk.Entry(self, textvariable = self.age)
        e4 = tk.Entry(self, textvariable = self.date)
        
        unix = time.time()
        self.datetime = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        e4.insert(0, self.datetime)
        e4.configure(state='readonly')
        
        
        
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=6, column=1)
        e4.grid(row=7, column=1)
        
        button1 = tk.Button(self, text="Save",
                           command=self.save_detail)
        button1.grid(row=8, column=1, padx=1, pady=1, ipadx=10, sticky=tk.W)

        button2 = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("Mainform"))
        
##        button2 = tk.Button(self, text="Back",
##                            command=self.quit())
        
        button2.grid(row=8, column=1, padx=1, pady=1, ipadx=10, sticky=tk.E+tk.E)

        button3 = tk.Button(self, text="KeyBoard",
                           command=self.callback)
        button3.grid(row=2, column=2, padx=1, pady=1, ipadx=10, sticky=tk.E+tk.E)



    def callback(self):
        p = subprocess.Popen(['matchbox-keyboard'])
        


    def save_detail(self):
            dbid = self.user_id.get()
            dbname = self.name.get()
            dbgender = self.gender.get()
            dbage = self.age.get()
            dbdate = self.date.get()
            conn = sqlite3.connect('hrv.db')
            c = conn.cursor()
            c.execute("INSERT INTO userinfo VALUES (?, ?, ?, ?, ?)", (dbid, dbname, dbgender, dbage, dbdate))
            conn.commit()
            c.close()
            conn.close()
            inpute = self.user_id.get()
            

##            filename = str("/home/pi/Desktop/new GUI1/database/" + inpute + ".csv")
##            textfile = open(filename, "w+")
##            textfile.write(dbid + "\n")
##            textfile.write(dbname + "\n")
##            textfile.write(dbgender + "\n")
##            textfile.write(dbage + "\n")
##            textfile.write(dbdate + "\n")
##            textfile.close()
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)           

            
            
            conn = sqlite3.connect('hrv.db')
            c = conn.cursor()
            c.execute('SELECT MAX(user_id) FROM userinfo')
            self.data = c.fetchone()
            value = 1
            self.data = int(self.data[0] + value)
            self.e1.insert(0,self.data)
            conn.commit()
            c.close()
            conn.close()
            tkMessageBox.showinfo("Message", "Data is saved!")

        

    
            
        
        
       


class Secondform(tk.Frame):
    global rr_interval
    

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
##        label = tk.Label(self, text="Start Data Acquization", font=TITLE_FONT)
##        label.grid(row=0, column=2, pady=10)
##        button1 = tk.Button(self, text="Read",
##                           command=self.read_data)
##        button1.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5)
##        button2 = tk.Button(self, text="Result",
##                           command=lambda: controller.show_frame("Fourthform"))
##        button2.grid(row=3, column=1, padx=5, pady=5, ipadx=3, ipady=3)
##        
##        button3 = tk.Button(self, text="Back",
##                            command=lambda: controller.show_frame("Mainform"))
##        button3.grid(row=5, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        
##        u_cols = ['heart']
##        files = pd.read_csv("/home/pi/Desktop/new GUI1/data.csv", names = u_cols)
##        files[files>1000] = 300
##        cal_mean = int (files["heart"].mean())
##        files[files<=100] = cal_mean
##        files = files.fillna(cal_mean)
##        files = files[5:1112].reset_index(drop=True)    
##            
##        filtered = lv.butter_lowpass_filter(files.heart, 2.5, 100.0, 5)
##        a.plot(filtered, alpha=0.5, color='blue')
        
        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=tk.BOTH, expand = True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=tk.BOTH, expand = True)

               
        button1 = tk.Button(self, text="Read",
                            command=self.read_data)
        button1.pack(side = LEFT)
        button2 = tk.Button(self, text="Result",
                            command=lambda: controller.show_frame("Fourthform"))
        button2.pack(side = LEFT)
        
        button3 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame("Mainform"))
        button3.pack(side = LEFT)     



        


    def read_data(self):
           
            
            lv.readdata()
            tkMessageBox.showinfo("Message", "Data Acquization is done..")



    
    





        
class Thirdform(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #---------------------------------create lables---------------------------------------------------------------------------
        label1 = tk.Label(self, text="ID").grid(row=0, column = 1)
        self.user_id = tk.StringVar()
        self.dataentry = tk.StringVar()
        self.e1 = tk.Entry(self, textvariable = self.user_id, width = 5)
        self.e1.grid(row=0, column=2)

        label2 = tk.Label(self, text=" Name").grid(row=1, column = 1)
        label3 = tk.Label(self, text="Gender").grid(row=2, column = 1)
        label3 = tk.Label(self, text="Age").grid(row=3, column = 1)
        label3 = tk.Label(self, text="Date").grid(row=4, column = 1)
        label3 = tk.Label(self, text="HB").grid(row=5, column = 1)
        label3 = tk.Label(self, text="RESULT").grid(row=6, column = 1)
        label3 = tk.Label(self, text="ACCURACY").grid(row=7, column = 1)
        
       




        self.e2 = tk.Entry(self, width = 15)
        self.e3 = tk.Entry(self, width = 15)
        self.e4 = tk.Entry(self, width = 15)        
        self.e5 = tk.Entry(self, width = 15)
        self.e6 = tk.Entry(self, width = 15)
        self.e7 = tk.Entry(self, width = 15)
        self.e8 = tk.Entry(self, width = 15)
        
        self.e2.grid(row=1, column=2)
        self.e3.grid(row=2, column=2)
        self.e4.grid(row=3, column=2)
        self.e5.grid(row=4, column=2)
        self.e6.grid(row=5, column=2)
        self.e7.grid(row=6, column=2)
        self.e8.grid(row=7, column=2)
        




        button1 = tk.Button(self, text="View",
                           command=self.view_data)
        button1.grid(row = 1, column = 0,  padx=0, pady=0, ipadx=0, ipady=0)

        button2 = tk.Button(self, text="Delete",
                            command=self.delete_data)
        button2.grid(row = 2, column = 0,  padx=0, pady=0, ipadx=0, ipady=0)

        button3 = tk.Button(self, text="Send",
                            command=self.send_data)
        button3.grid(row = 3, column = 0,  padx=0, pady=0, ipadx=0, ipady=0)

        button3 = tk.Button(self, text="Clear",
                            command=self.clear)
        button3.grid(row = 4, column = 0,  padx=0, pady=0, ipadx=0, ipady=0)

        button4 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame("Mainform"))
        button4.grid(row = 5, column = 0,  padx=0, pady=0, ipadx=0, ipady=0)


        button5 = tk.Button(self, text="KeyBoard",
                           command=self.callback)
        button5.grid(row=0, column=3, padx=1, pady=1, ipadx=10, sticky=tk.E+tk.E)



    def callback(self):
        p = subprocess.Popen(['matchbox-keyboard'])



  
        




    def view_data(self):
        
        
        try:
            dbid = self.user_id.get()            
            conn = sqlite3.connect('hrv.db')
            c = conn.cursor()
            
            c.execute("SELECT user_id FROM userinfo WHERE user_id=?", (dbid,))
            u_id = c.fetchone()

            if (u_id == None):
                tkMessageBox.showinfo("Message", "Record not found!")
                

            c.execute("SELECT name FROM userinfo WHERE user_id=?", (dbid,))
            name = c.fetchone()

            c.execute("SELECT gender FROM userinfo WHERE user_id=?", (dbid,))
            gender = c.fetchone()

            c.execute("SELECT age  FROM userinfo WHERE user_id=?", (dbid,))
            age = c.fetchone()

            c.execute("SELECT date FROM userinfo WHERE user_id=?", (dbid,))
            date = c.fetchone()

            c.execute("SELECT heartbeat FROM heartinfo WHERE user_id=?", (dbid,))
            hb = c.fetchone()

            c.execute("SELECT prediction FROM heartinfo WHERE user_id=?", (dbid,))
            result = c.fetchone()

            c.execute("SELECT accuracy FROM heartinfo WHERE user_id=?", (dbid,))
            accuracy = c.fetchone()

            self.e2.insert(0, name )
            self.e3.insert(0, gender)
            self.e4.insert(0, age)
            self.e5.insert(0, date)
            self.e6.insert(0, hb)
            self.e7.insert(0, result)
            self.e8.insert(0, accuracy)
            c.close()
            conn.close()



        except IOError :
            tkMessageBox.showinfo("Message", "Record not found!")







    def delete_data(self):
        dbid = self.user_id.get()
        dbid1 = self.user_id.get()
        
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)
        self.e5.delete(0, END)
        self.e6.delete(0, END)
        self.e7.delete(0, END)
        self.e8.delete(0, END)


        
        conn = sqlite3.connect('hrv.db')
        c = conn.cursor()
        c.execute("DELETE FROM userinfo WHERE user_id=?", (dbid,))        
        conn.commit()
        c.close()
        conn.close()
        
        dbid = self.user_id.get()
        conn = sqlite3.connect('hrv.db')
        c = conn.cursor()
        c.execute("DELETE FROM heartinfo WHERE user_id=?", (dbid1,))
        conn.commit()
        c.close()
        conn.close()
        tkMessageBox.showinfo("Message", "record deleted!")



    def send_data(self):
        self.f = tkFileDialog.askopenfile()
        self.f = self.f.read()
        files = []
        files.append(self.f)
        print files

        
        try:

            r = requests.post(url='http://visbamu.in/RRInterval/pythonFile.php', files={'file':self.f})
            tkMessageBox.showinfo("Message", "Data is sent!")
            print r.status_code
            print r.headers
        except IOError :
            tkMessageBox.showinfo("Message", "check internet connection!")

##        colume_no = 0
##        userdataapp = []
##        userdata = [dbid,dbname,dbgender,dbage,dbdate];
##        userdataapp.append(userdata)
##        for row_no, item in enumerate(userdataapp):
##            ws1.write(row_no,colume_no,str(item))
##            wb.save("Satish Suradkar.xls")
##        colume_no=colume_no+1

##        filename = '02.xls'
##        f = open(filename,'rb')
##        try:
##            r = requests.post(url='http://visbamu.in/RRInterval/pythonFile.php', files={'file':f})
##            print r.status_code
##            print r.headers
##
##        except IOError :
##            tkMessageBox.showinfo("Message", "check internet connection!")

        

        



        


    def clear(self):
        self.e1.delete(0, END)                
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)
        self.e5.delete(0, END)
        self.e6.delete(0, END)
        self.e7.delete(0, END)
        self.e8.delete(0, END)
        


       

class Fourthform(tk.Frame):
    
    
    
    

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller



        


        #---------------------------------create lables---------------------------------------------------------------------------
        label2 = tk.Label(self, text="ID").grid(row=0)
        label3 = tk.Label(self, text="INTERVAL").grid(row=1)
        label4 = tk.Label(self, text="FEATURE").grid(row=2)
        label5 = tk.Label(self, text="HB").grid(row=3)
        label6 = tk.Label(self, text="RESULT").grid(row=4)
        label7 = tk.Label(self, text="ACCURACY").grid(row=5)

        #---------------------------Entry widget---------------------------------------------------------

        self.user_id = tk.StringVar()
        self.rrinterval = tk.StringVar()
        self.feature = tk.StringVar()
        self.heartrate = tk.StringVar()
        self.result = tk.StringVar()
        self.accuracy = tk.StringVar()

        self.e1 = tk.Entry(self, textvariable = self.user_id)
        self.e2 = tk.Entry(self, textvariable = self.rrinterval)

        
        
        self.e3 = tk.Entry(self, textvariable = self.feature)
        self.e4 = tk.Entry(self, textvariable = self.heartrate)
        self.e5 = tk.Entry(self, textvariable = self.result)
        self.e6 = tk.Entry(self, textvariable = self.accuracy)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        self.e5.grid(row=4, column=1)
        self.e6.grid(row=5, column=1)


        
        
        

        



        #-------------------------------------Create buton-------------------------------------------------
        button1 = tk.Button(self, text="Show",
                           command=self.heartbeat)
        button1.grid(row=6, column=0, padx=1, pady=1, ipadx=10, sticky=tk.W)
        button2 = tk.Button(self, text="Save",
                           command=self.save_heartinfo)
        button2.grid(row=6, column=1, padx=1, pady=1, ipadx=10, sticky=tk.W)

        button3 = tk.Button(self, text="Clear",
                            command=self.clear)
        button3.grid(row=6, column=1, padx=1, pady=1, ipadx=10, sticky=tk.E+tk.E)

        
        button4 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame("Secondform"))
        button4.grid(row=6, column=2, padx=1, pady=1, ipadx=10, sticky=tk.E+tk.E)




    def heartbeat(self):
               
        u_cols = ['heart']
        files = pd.read_csv("/home/pi/Desktop/new GUI1/data.csv", names = u_cols)
        files[files>1000] = 0
        cal_mean = int (files["heart"].mean())
        files[files<=100] = cal_mean
        #print cal_mean
        files = files.fillna(cal_mean)
        files.to_csv("/home/pi/Desktop/new GUI1/data1.csv")
        files.heart = lv.butter_lowpass_filter(files.heart, 2.5, 100.0, 5)
        files.to_csv("/home/pi/Desktop/new GUI1/sensordata.csv", index=False)
        
        #print files.heart



        #----make database file-----------------------------
        conn = sqlite3.connect('hrv.db')
        c = conn.cursor()
        c.execute('SELECT MAX(user_id) FROM userinfo')
        self.data = c.fetchone()
        #print self.data
        inpute = str(self.data)
        #path = str("/home/pi/Desktop/new GUI1/database/")
        files.to_csv("/home/pi/Desktop/new GUI1/database/"+ inpute + ".csv")
##        filename = ("/home/pi/Desktop/new GUI1/database/" + inpute + ".csv")
##        textfile = open(filename, "w+")
##        textfile.append(files)
##        textfile.close()

        c.close()
        conn.close()

        #print files


        measures = {}
        heart_rate_window =0.75 #One-sided window size, as proportion of the sampling frequency
        frequency_sam = 100 #The example dataset was recorded at 100Hz
        #w = int(hrw*fs)
        #print w
        mov_avg = pd.rolling_mean(files.heart, window=(heart_rate_window*frequency_sam )) #Calculate moving average
        #mov_avg = pd.Series.rolling(dataset.hart, window=75,center=False).mean()
        #Impute where moving average function returns NaN, which is the beginning of the signal where x hrw
        avg_hr = (np.mean(files.heart))
        mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
        mov_avg = [x*1.2 for x in mov_avg] #For now we raise the average by 20% to prevent the secondary heart contraction from interfering,will do this dynamically
        files['heart_rollingmean'] = mov_avg #Append the moving average to the dataframe
        #print mov_avg
        try:
            #Mark regions of interest
            window = []
            peaklist = []
            listpos = 0 #We use a counter to move over the different data columns
            for datapoint in files.heart:
                rollingmean = files.heart_rollingmean[listpos] #Get local mean

                if (datapoint <= rollingmean) and (len(window) <= 1): #If no detectable R-complex activity -> do nothing
                    listpos += 1

                elif (datapoint > rollingmean): #If signal comes above local mean, mark ROI
                    window.append(datapoint)
                    listpos += 1

                else: #If signal drops below local mean -> determine highest point
                    maximum = max(window)
                    beatposition = listpos - len(window) + (window.index(max(window))) #Notate the position of the point on the X-axis
                    peaklist.append(beatposition) #Add detected peak to list
                    window = [] #Clear marked ROI
                    listpos += 1

            measures['peaklist'] = peaklist
            measures['ybeat'] = [files.heart[x] for x in peaklist]
            #ybeat = [files.heart[x] for x in peaklist] #Get the y-value of all peaks for plotting purposes

        except IOError:
            print "Please dont move hand....data acquzation is not done."
            sys.exit()



        peaklist = measures['peaklist']
        RR_list = []
        cnt = 0
        while (cnt < (len(peaklist)-1)):
            RR_interval = (peaklist[cnt+1] - peaklist[cnt]) #Calculate distance between beats in  samples
            #print RR_interval
            ms_dist = ((RR_interval / frequency_sam) * 1000.0) #Convert sample distances to ms distances
            RR_list.append(ms_dist) #Append to list
            cnt += 1
            measures['RR_list'] = RR_list
        #print ("RR Interval lenght", len(RR_list))
        #print ("rr_list", RR_list)
        #self.bpm = 60000 / np.mean(RR_list) #60000 ms (1 minute) / average R-R interval of signal
        #print "Average Heart Beat is: %.01f" %self.bpm #Round off to 1 decimal and print
        #print self.bpm
        self.heartbeat = len(peaklist)



        self.rr_interval = []
        RR_diff = []
        RR_sqdiff = []
        RR_list = measures['RR_list']
        cnt = 1 #Use counter to iterate over RR_list
        while (cnt < (len(RR_list)-1)): #Keep going as long as there are R-R intervals
            RR_diff.append(abs(RR_list[cnt] - RR_list[cnt+1])) #Calculate absolute difference between successive R-R interval
            RR_sqdiff.append(math.pow(RR_list[cnt] - RR_list[cnt+1], 2)) #Calculate squared difference
            cnt += 1
        #print RR_diff   #, RR_sqdiff
        self.rr_interval.append(RR_list)
        #print (self.rr_interval)
        
        # calculate featurs from RR interval
        
        ibi = np.mean(RR_list) #Take the mean of RR_list to get the mean Inter Beat Interval
        #print "IBI:", ibi
        sdnn = np.std(RR_list) #Take standard deviation of all R-R intervals
        #print "SDNN:", sdnn
        sdsd = np.std(RR_diff) #Take standard deviation of the differences between all subsequent R-R intervals
        #print "SDSD:", sdsd
        rmssd = np.sqrt(np.mean(RR_sqdiff)) #Take root of the mean of the list of squared differences
        #print "RMSSD:", rmssd
        RR_list = pd.DataFrame({'RR_interval':RR_list})
        #print RR_list
        self.features = []
        self.features.append(ibi)
        self.features.append(sdnn)
        self.features.append(sdsd)
        self.features.append(rmssd)
        #print type(self.features)
        features1 = pd.DataFrame({'features':self.features})
        #print features1
        features1.to_csv('/home/pi/Desktop/new GUI1/features.csv', index = False)
        
        try:
            df = pd.read_csv('/home/pi/Desktop/new GUI1/knn1.csv')
            X = np.array(df.drop(['class'], 1))
            y = np.array(df['class'])
            X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.2)
            clf = neighbors.KNeighborsClassifier()
            clf.fit(X_train, y_train)
            self.accuracy = clf.score(X_test, y_test)
            self.accuracy = self.accuracy*100
            self.accuracy = self.accuracy
            #print ('Accuracy of classification: ', self.accuracy)
            #features = [0,0, 0, 0]
            example_measures = np.array(self.features)
            example_measures = example_measures.reshape(1, -1)
            self.prediction = clf.predict(example_measures)

        except IOError:
            print('file is not found or features are not found')





        
        


##
##
##
##        heart_info = []
##        heart_info.append(self.rr_interval)
##        rr_interval1 = pd.DataFrame({'rr_interval':heart_info})
##        rr_interval1.to_csv('/home/pi/Desktop/new GUI/rr_interval.csv', index = False)
##
##        result = []
##        result.append(self.bpm)
##        result.append(self.prediction)
##        result.append(self.accuracy)
##        result = pd.DataFrame({'result':result})
##        result.to_csv('/home/pi/Desktop/new GUI/result.csv', index = False)
##
##
        #-----------------insert values---------------------
        



        #-----------ID generation-----------------------
        conn = sqlite3.connect('hrv.db')
        c = conn.cursor()
        c.execute('SELECT MAX(user_id) FROM userinfo')
        self.data = c.fetchone()
##        value = 1
##        self.data = int(self.data[0] + value)
##        
        self.e1.insert(0,self.data)
        conn.commit()
        c.close()
        conn.close()         

        self.e2.insert(0, self.rr_interval)
        self.e3.insert(0, self.features)
        self.e4.insert(0, self.heartbeat)
        a = 'normal'
        b = 'Tachycardia'
        c = 'Bradycardia'
        prediction1 = self.prediction
        if prediction1 == 1:
            self.e5.insert(0, a)
        elif prediction1 == 2:
            self.e5.insert(0, b)
        else:
            self.e5.insert(0, c)
            

        self.e6.insert(0, self.accuracy)




###-------------store in array-------------------------------------------------------------
##        self.rr_interval = np.array(self.rr_interval)
##        print self.rr_interval.reshape(-1)
##        print np.shape(self.rr_interval)
##        print np.transpose(self.rr_interval)
##        print np.shape(self.rr_interval)
##
##        self.features = np.array(self.features)
##        
##        self.accuracy = np.array(self.accuracy)
        conn = sqlite3.connect('hrv.db')
        c = conn.cursor()

        c.execute('SELECT MAX(user_id) FROM userinfo')
        data = c.fetchone()
        dbid = data

        c.execute("SELECT name FROM userinfo WHERE user_id=?", dbid)
        name = c.fetchone()

        c.execute("SELECT gender FROM userinfo WHERE user_id=?", dbid)
        gender = c.fetchone()

        c.execute("SELECT age  FROM userinfo WHERE user_id=?", dbid)
        age = c.fetchone()
        age =str(age)

        c.execute("SELECT date FROM userinfo WHERE user_id=?", dbid)
        date = c.fetchone()

        c.execute("SELECT heartbeat FROM heartinfo WHERE user_id=?", dbid)
        hb = c.fetchone()
        hb = str(hb)

        c.execute("SELECT prediction FROM heartinfo WHERE user_id=?", dbid)
        result = c.fetchone()

        c.execute("SELECT accuracy FROM heartinfo WHERE user_id=?", dbid)
        accuracy = c.fetchone()
        accuracy = str(accuracy)

        ws1.write(0, 0, "Device_Id")
        ws1.write(1, 0, "Name")
        ws1.write(2, 0, "Gender")
        ws1.write(3, 0, "Age")
        ws1.write(4, 0, "Date")
        ws1.write(5, 0, "Heart Beat")
        ws1.write(6, 0, "Result")
        ws1.write(7, 0, "Accuracy")

        ws1.write(0, 1, "01")
        ws1.write(1, 1, name)
        ws1.write(2, 1, gender)
        ws1.write(3, 1, age)
        ws1.write(4, 1, date)
        ws1.write(5, 1, hb)
        ws1.write(6, 1, result)
        ws1.write(7, 1, accuracy)
##
        sdata = []
        sensordata = pd.read_csv('/home/pi/Desktop/new GUI1/sensordata.csv')
        sensordata = sensordata[5:2750]
        print sensordata
        for i in sensordata['heart']:
            sdata.append(i)
        print sdata
        #sensordata1.append(sensordata)



        colume_no = 0
        for row_no, item in enumerate(self.rr_interval):
            ws2.write(row_no,colume_no,str(item))
        for row_no, item in enumerate(self.features):
            ws3.write(row_no,colume_no,str(item))
        for row_no, item in enumerate(sdata):
            ws4.write(row_no,colume_no,str(item))
        wb.save("02.xls")
        colume_no=colume_no+1
        c.close()
        conn.close()
            
            




    def save_heartinfo(self):
        dbid = self.user_id.get()
        dbrrinterval = str(self.rr_interval)
        dbfeatures = str(self.features)
        dbbpm = self.heartrate.get()
        dbprediction = self.result.get()
        dbaccuracy = str(self.accuracy)
        
##        
##        print dbid
##        print dbrrinterval
##        print dbfeatures
##        print dbbpm 
##        print dbprediction
##        print dbaccuracy


        inpute = self.user_id.get()
        filename = str("/home/pi/Desktop/new GUI1/database/" + inpute + ".txt")
        textfile = open(filename, "a+")
##        textfile.close()
##        print textfile
        textfile.write(dbid + "\n")
        textfile.write(dbrrinterval + "\n")
        textfile.write(dbfeatures + "\n")
        textfile.write(dbbpm + "\n")
        textfile.write(dbprediction + "\n")
        textfile.write(dbaccuracy + "\n")
        textfile.close()
        





       

##        save_heartinfo = pd.DataFrame({'user_id':dbid}, {'dbrr_interval':dbrr_interval}, {'dbfeatures':dbfeatures}, {'dbbpm ':dbbpm}, {'dbprediction':dbprediction}, {'dbaccuracy':dbaccuracy})
##        print save_heartinfo



        
        
        conn = sqlite3.connect('hrv.db')
        c = conn.cursor()
        
        c.execute("INSERT INTO heartinfo(user_id, heartbeat, prediction, accuracy) VALUES (?, ?, ?, ?)", (dbid, dbbpm, dbprediction, dbaccuracy))
        conn.commit()

        c.close()
        conn.close()



#------------------------select records from table----------------------------------------
##        
##        conn = sqlite3.connect('heartbeat.db')
##        c = conn.cursor()
##        c.execute("SELECT * FROM heartinfo")
##        data = c.fetchall()
##        print data

    

        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)
        self.e5.delete(0, END)
        self.e6.delete(0, END)
        tkMessageBox.showinfo("Message", "Data is saved!")

    def clear(self):
        
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)
        self.e5.delete(0, END)
        self.e6.delete(0, END)


        

class Fifthform(tk.Frame):  
    

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        
        labe1 = tk.Label(self, text="Help:                                                          ", font=TITLE_FONT)
        labe1.grid(row=3, column=2)

        labe2 = tk.Label(self, text="1:Click on New Button to add new record.                                  ", font=TITLE_FONT)        
        labe2.grid(row=4, column=0)

        labe3 = tk.Label(self, text="2:Click on start button to data aquization.                                ", font=TITLE_FONT)
        labe3.grid(row=5, column=0)

        
        labe4 = tk.Label(self, text="3:Click on View button to data view.                                       ", font=TITLE_FONT)
        labe4.grid(row=6, column=0)

                
        labe4 = tk.Label(self, text="4:Click on Send button to Send data.                                       ", font=TITLE_FONT)
        labe4.grid(row=7, column=0)
        



        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame("Mainform"))
        button1.grid(row=9, column=0, padx=10, pady=10, ipadx=10)
##        
##        button2 = tk.Button(self, text="Back",
##                            command=Frame.destroy)
        
        






if __name__ == "__main__":
    gui = Samplegui()
    gui.title("HRV")
    gui.geometry("300x200")
    #-gui.attributes('-fullscreen', True)
    ani = animation.FuncAnimation(f, animations, interval = 1000)
    #gui.update(tk.Tk)
    gui.mainloop()
