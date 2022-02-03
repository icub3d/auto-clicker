import tkinter
import time
import datetime
import random
import threading

import pyautogui
import pynput


class Timer:
    def __init__(self, scale, button, forever):
        self.running = False
        self.clicks = 0
        self.scale = scale
        self.button = button
        self.forever = forever
        self.start = time.time()

    def run(self):
        self.running = True
        countdown = 5
        while self.running and countdown > 0:
            yield {
                "countdown": countdown,
                "clicks": self.clicks,
                "next": "",
                "duration": "",
            }
            time.sleep(1)
            countdown -= 1

        while self.running and (self.forever or time.time() - self.start < self.scale * 60):
            if self.button == "LEFT_MOUSE":
                pyautogui.click()
            elif self.button == "RIGHT_MOUSE":
                pyautogui.click(button='right')
            else:
                pyautogui.press(self.button)

            self.clicks += 1
            when = 0.6 + random.uniform(0.0, 0.2)
            yield {
                "countdown": countdown,
                "clicks": self.clicks,
                "next": "{:0.3f}".format(when),
                "duration": datetime.timedelta(seconds=time.time()-self.start),
            }
            time.sleep(when)


class AutoClicker:
    def __init__(self):
        self.root = tkinter.Tk()
        self.scale = tkinter.IntVar()
        self.time = tkinter.StringVar()

        hotkey = pynput.keyboard.HotKey(
            pynput.keyboard.HotKey.parse('<ctrl>+<alt>+h'),
            self.pause)

        self.l = pynput.keyboard.Listener(
            on_release=self.for_canonical(hotkey.release),
            on_press=self.for_canonical(hotkey.press),
        )
        self.l.start()

    def for_canonical(self, f):
        return lambda k: f(self.l.canonical(k))

    def ui(self):
        self.root.title("Auto Clicker")
        self.scale.set(5)

        self.b = tkinter.Button(self.root, text="Start", command=self.start)
        self.b.grid(row=0, column=0)

        self.p = tkinter.Button(self.root, text="Pause", command=self.pause)
        self.p.grid(row=0, column=1)

        self.time.set("Click start to begin!")
        l = tkinter.Label(self.root, textvariable=self.time)
        l.grid(row=1, column=0, columnspan=2)

        self.key = tkinter.StringVar()
        self.key.set("LEFT_MOUSE")
        k = tkinter.Entry(self.root, textvariable=self.key)
        k.grid(row=3, column=0, columnspan=2)

        self.forever = tkinter.IntVar()
        check = tkinter.Checkbutton(self.root, text='Forever', variable=self.forever,
                                    onvalue=1, offvalue=0, command=self.check_forever)
        check.grid(row=4, column=0, columnspan=2)

        self.s = tkinter.Scale(self.root, from_=1, to=60, variable=self.scale,
                               orient=tkinter.HORIZONTAL)
        self.s.grid(row=5, column=0, columnspan=2)

        self.root.mainloop()

    def check_forever(self):
        print(f"Checking forever {self.forever}")
        if self.forever.get() == 1:
            self.s.grid_forget()
        else:
            self.s.grid(row=6, column=0, columnspan=2)

    def pause(self):
        self.go = False
        self.p.configure(text="Unpause", command=self.unpause)

    def unpause(self):
        self.go = True
        self.p.configure(text="Pause", command=self.pause)
        threading.Thread(target=self.clicker).start()

    def stop(self):
        self.go = False
        self.time.set("Click start to begin!")
        self.b.configure(text="Start", command=self.start)

    def start(self):
        self.b.configure(text="Stop", command=self.stop)
        self.go = True
        self.t = Timer(self.scale.get(), self.key.get(),
                       self.forever.get() == 1)
        threading.Thread(target=self.clicker).start()

    def keys(self, key):
        if key == pynput.keyboard.Key.esc and self.go:
            self.pause()

    def clicker(self):
        for msg in self.t.run():
            if msg["countdown"] > 0:
                self.time.set("starting in {}".format(msg["countdown"]))
            else:
                self.time.set("clicks: {} (next: {}) (duration: {})".
                              format(msg["clicks"], msg["next"], msg["duration"]))

            if not self.go:
                return
        self.stop()


def main():
    ac = AutoClicker()
    ac.ui()


if __name__ == "__main__":
    random.seed()
    main()
