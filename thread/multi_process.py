import multiprocessing
import threading
import time
import tkinter as tk
import psutil


class Window:
    def __init__(self):
        self.win = tk.Tk()
        self.Var_Label = tk.StringVar(self.win, "INIT")
        self.Var_Button = tk.StringVar(self.win, "Start")
        self.ppp = multiprocessing.Pipe()

    def GUI_Design(self):
        tk.Label(self.win, textvariable=self.Var_Label).grid(column=0, row=0)
        tk.Button(self.win, textvariable=self.Var_Button,
                  command=self.multiprocess_run).grid(column=1, row=0)

    def GUI_Flush(self):
        while True:
            data = self.ppp[1].recv()
            self.Var_Label.set(data)

    def run(self):
        self.GUI_Design()
        tr = threading.Thread(target=self.GUI_Flush)
        tr.setDaemon(True)
        tr.start()
        self.win.mainloop()

    def multiprocess_run(self):
        if self.Var_Button.get() == "Start":
            test_run = T_main(self.ppp[0])
            tr = multiprocessing.Process(target=test_run.run)
            tr.daemon = True
            tr.start()
            self.p = psutil.Process(tr.pid)
            self.Var_Button.set("Pause")
        elif self.Var_Button.get() == "Pause":
            self.p.suspend()
            self.Var_Button.set("Resure")
        elif self.Var_Button.get() == "Resure":
            self.p.resume()
            self.Var_Button.set("Pause")


class T_main:
    def __init__(self, pip: multiprocessing.Pipe()[0]):
        self.pip = pip

    def run(self):
        count = 0
        while True:
            self.pip.send(str(count))
            count += 1
            time.sleep(1)


if __name__ == "__main__":
    xe = Window()
    xe.run()
