import tkinter as tk
import time
import math 
from typing import Callable
import datetime



class Watch(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watch")
        # self.geometry("400x400")
        
        #display params  : 
        self.w,self.h = 300,300 #width , height
        self.x0,self.y0 = self.w//2,self.h//2 #center cords 
        self.r = 100  #circle radius 
        
        # mechanical params : 
        self.current_time = datetime.datetime.now() # time.strftime("%H:%M:%S")
        self.isTimeEditable = False         
        self.mode_clicks = 0 # ->  # Track # times  mode button was clicked 
                # 0 ->  self.isTimeEditable = false  => increase_action = None 
                # 1 -> increase_action = AddOneHour
                # 2 -> increase_action = AddOneMinute
        self.increase_action = None  #describe the action of the increase button : None,AddOneHour,AddOneMinute
        
        
        self.create_watch_interface()        
        self.create_buttons()
    
        self.refresh_increase_action()
        
        self.refresh_time()
    
    
    def refresh_time(self):
        """display the current time , advance time by 1s and then call itself """
        
        # get the current time str : 
        current_time_str = self.current_time.strftime("%H:%M:%S")
        # update the time text @watch : 
        self.watch.itemconfig(self.time_text, text=current_time_str.split(":")[0] + ":" + current_time_str.split(":")[1])
        self.watch.itemconfig(self.time_seconds, text=current_time_str.split(":")[2])
        
        # advance time by 1 second : 
        self.current_time = self.current_time + datetime.timedelta(seconds=1)       
        # call itself again after 1 second 
        self.after(1000, self.refresh_time)
    
    
    
    def refresh_increase_action(self):
        actionsList =  ['None','AddOneHour','AddOneMinute']        
        self.increase_action = actionsList[self.mode_clicks]
        print(f'increase action = {self.increase_action}')        

    
    def create_watch_interface(self):
        
        self.geometry(str(self.w)+"x"+str(self.h))        
        self.watch = tk.Canvas(self, bg="white", width=self.w, height=self.h)
        
        # init shapes :       
        self.watch_circle = self.watch.create_oval( self.x0- self.r, self.y0- self.r,self.x0+ self.r, self.y0+ self.r, fill="blue", width=2)
        self.watch.pack()
        
        self.time_bg = self.watch.create_rectangle(self.x0//2, self.y0 *3/4, self.x0*3/2, self.y0 *5/4, fill="white", width=2)    
        self.time_text = self.watch.create_text(self.x0*0.9, self.y0*0.95, text="00:00", font=("Arial", 20), fill="black")
        self.time_seconds = self.watch.create_text(self.x0*1.2, self.y0*1.05, text="13", font=("Arial", 15), fill="black")
        
        
        self.origin = self.watch.create_text(self.x0, self.y0, text="X", font=("Arial", 30), fill="Red",tags='origin')
    
    
    
    def create_buttons(self) :      
        
        self.mode_button = self.create_button("Mode",45,self.mode_button_callback)
        self.increase_button = self.create_button("Increase",-45,self.increase_button_callback)
        self.light_button = self.create_button("Light",-135,self.light_button_callback)
        
    
    
    def create_button(self,btn_txt:str,angle_degree:float, callback: Callable[[], None] = None)-> tk.Button:
        """Creates a button on the watch interface with the specified btn_txt
        angle_degree -> the angle (in degrees) between the center of the widget and the desired location of the butto.
        """
        
        # btn params 
        angle = angle_degree * math.pi/180         
        btn_width,btn_height  = 50,25
        
        
        # compute relx,rely to adjust the boarder between the cicrle and the button 
        if abs(angle_degree)>90 : 
            relx = -btn_width/self.w
        else : 
            relx = 0
                 
        if angle_degree > 0 : 
            rely = -btn_height/ self.h
        else : 
            rely = 0
        
        #create the button ; 
        btn = tk.Button(self.watch, text=btn_txt, bg="lightblue", font=("Arial",9),command=callback) 
        btn.place(x=self.x0 + self.r *math.cos(angle), y=self.y0-self.r * math.sin(angle),
                  width=50, height=25,relx=relx,rely=rely)
        
        return btn 
    
    
    ## Callbacks : 
    
    def light_button_callback(self):       
        # get original color 
        original_color = self.watch.itemcget(self.time_bg, "fill") 
        # turn ther screen "on" ( changing its color to green)
        self.watch.itemconfig(self.time_bg, fill="green")
        # schedule  color change back to the original after  2s
        self.after(2000, lambda: self.watch.itemconfig(self.time_bg, fill=original_color))
    
    def increase_button_callback(self): 
        if not self.isTimeEditable :                    
            pass
        
        if self.increase_action == 'AddOneHour' :
            self.current_time = self.current_time + datetime.timedelta(hours=1)   
            pass 
        
        if self.increase_action == 'AddOneMinute' :
            self.current_time = self.current_time + datetime.timedelta(minutes=1)
        
    def mode_button_callback(self):
        self.mode_clicks = (self.mode_clicks+1) % 3 
        self.isTimeEditable = not self.mode_clicks == 0  
        self.refresh_increase_action()
        
               
            
   


if __name__ == "__main__":
    app = Watch()
    app.mainloop()