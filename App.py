import threading
from tkinter import *
import tkinter.font as tkFont
from threading import *
import sys
import os

class App() :
    def __init__(self,radar) :
        Thread.__init__(self)
        # root
        self.root = Tk()          
        self.root.title("RADAR")
        
        self.root.iconbitmap(default=self.resource_path("assets\\icon.ico"))

        width=700
        height=600
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        self.root.configure(background='white')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        
        self.r = radar
        if self.r : 
            self.th = threading.Thread(target=self.r.start)
        # labels

        self.bg = PhotoImage(file=self.resource_path("assets\\bg.png"))
        self.background_label = Label(self.root,image=self.bg).place(x=0,y=0,width=350,height=600)

        self.GLabel_131=Label(self.root ,bg="white")
        self.ft = tkFont.Font(family='Times',size=26)
        self.GLabel_131["font"] = self.ft
        self.GLabel_131["fg"] = "#333333"
        self.GLabel_131["justify"] = "center"
        self.GLabel_131["text"] = "The Buisness jet Project"
        self.GLabel_131.place(x=350,y=20,width=350,height=130)

        self.GLabel_318=Label(self.root ,bg="white")
        self.ft = tkFont.Font(family='Times',size=26)
        self.GLabel_318["font"] = self.ft
        self.GLabel_318["fg"] = "#333333"
        self.GLabel_318["justify"] = "center"
        self.GLabel_318["text"] = "Radar"
        self.GLabel_318.place(x=350,y=130,width=350,height=96)

        self.GLabel_231=Label(self.root,bg="white")
        self.ft = tkFont.Font(family='Times',size=10)
        self.GLabel_231["font"] = self.ft
        self.GLabel_231["fg"] = "#333333"
        self.GLabel_231["justify"] = "center"
        self.GLabel_231["text"] = "This work belongs to Yassine AIT MALEK"
        self.GLabel_231.place(x=350,y=530,width=350,height=66)

        self.var = StringVar()
        self.var.set("Ready To Run !!!")
        self.l = Label(self.root, textvariable = self.var ,justify="center" , bg ="white" ).place(x=350,y=430,width=350,height=66)

        # Buttons

        self.start_img_btn= PhotoImage(file=self.resource_path("assets\\Button_start.png"))
        self.stop_img_btn= PhotoImage(file=self.resource_path("assets\\Button_stop.png"))

        self.start_btn= Button(self.root,bg="white",image=self.start_img_btn , command=  self.start_r , borderwidth=0 ).place(x=400,y=250,width=266,height=56) 
        self.stop_btn= Button(self.root,bg="white",image=self.stop_img_btn , command =  self.stop_r, borderwidth=0 ).place(x=400,y=350,width=266,height=56)

        

        self.run()

    def resource_path(self , relative_path):
                # """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
       
    def start_r(self) :
        
        if self.r :
            if self.r.running == False :
        
                self.var.set( "Server Started" )
                try :
                    self.start_btn = Button(self.root,bg="white",image=self.start_img_btn , command=  self.dumb , borderwidth=0 ).place(x=400,y=250,width=266,height=56) 
                    self.th.start()
                except :
                    print("")
            else : 
                self.var.set( "Server is Already Started" )
   
    def dumb(self) :
        if self.r :
            if self.r.running == True :
                self.var.set( "Server is Already Started" )
            else :
                self.var.set( "Server Started" )
                self.th = threading.Thread(target=self.r.start)
                self.th.start()
                self.start_btn = Button(self.root,bg="white",image=self.start_img_btn , command=  self.start_r , borderwidth=0 ).place(x=400,y=250,width=266,height=56) 
            
        
        
    def stop_r(self) :
        if self.r :
        
            if self.r.running == True :
                
                self.var.set( "Server Stopped")
                try : 
                    self.r.stop()
                    self.th.join()
                    self.th = None
                    self.on_close()
                except :
                    print("")
            else : 
                self.var.set( "Server is Already Stopped" )
        
    def run(self) :
        self.root.mainloop()
        
    def on_close(self) :
        if self.r : 
            self.r.stop()
            del self.r
        self.root.destroy()
        sys.exit()
 
    def __del__(self):
        print("App Destroyed")
        
        
def main():
    a = App(None) 
        

if __name__ == "__main__" :
    main()




