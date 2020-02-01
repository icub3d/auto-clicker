import pyautogui
import tkinter
import time
import random
import threading

class AutoClicker:
    def __init__(self):
        self.root = tkinter.Tk()
        self.msgTemplate = "Hello! This will simulate clicking the left mouse button. Once you click start, it will count down for 5 seconds and then click the left mouse button for {} minute."
        self.msg = tkinter.StringVar()
        self.scale = tkinter.IntVar()
        self.time = tkinter.StringVar()
        self.go = False
        
    def scale_changed(self, to):
        self.msg.set(self.msgTemplate.format(self.scale.get()))

    def ui(self):
        self.root.title("Auto Clicker")
        self.root.geometry("500x160")
        self.scale.set(5)
        self.scale_changed(5)
        m = tkinter.Message(self.root, width=500,
                            textvariable=self.msg)
        m.pack()


        s = tkinter.Scale(self.root, from_=1, to=10, variable=self.scale,
                          orient=tkinter.HORIZONTAL, length=500,
                          command=self.scale_changed)
        s.pack()
    

        self.b = tkinter.Button(self.root, text="Start", command=self.start)
        self.b.pack()

        self.time.set("Click start to begin!")
        l = tkinter.Label(self.root, width=500, textvariable=self.time)
        l.pack()

        self.root.mainloop()

    def stop(self):
        self.go = False
        
        
    def start(self):
        self.b.configure(text="Stop", command=self.stop)
        self.go = True
        threading.Thread(target=self.clicker).start()

    def clicker(self):
        countdown = 5
        clicks = 0

        while self.go and countdown > 0:
            self.time.set("starting in {}".format(countdown))
            time.sleep(1)
            countdown -= 1
            
        start = time.time()
        while self.go and time.time() - start < self.scale.get() * 60:
            pyautogui.click()
            clicks += 1
            when = 0.5 + random.uniform(0.0, 0.2)
            self.time.set("clicks: {} (next: {})".format(clicks, when))
            time.sleep(when)
        self.time.set("Click start to begin!")
        self.b.configure(text="Start", command=self.start)

def main():
    ac = AutoClicker()
    ac.ui()
    
if __name__ == "__main__":
    random.seed()
    main()
