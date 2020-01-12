import sys
import threading

import concurrent.futures as cf

import tkinter
import tkinter.scrolledtext
import tkinter.ttk
import tkinter.messagebox

from main import Work


class StdoutRedirector(object):
    def __init__(self, text_area, obj_self):
        self.text_area = text_area
        self.obj_self = obj_self

    def write(self, str):
        self.text_area.insert(tkinter.END, str)
        self.text_area.see(tkinter.END)
        self.obj_self.update_idletasks()

    # def flush(self):
    #     pass


class Application(tkinter.ttk.Frame):
    def __init__(self, work=None, master=None):
        super().__init__(master)
        self.work = work
        self.grid(sticky="w, n, e, s", padx=4, pady=4)
        self.create_widgets()
        self.master.title("Test")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        orig_stdout = sys.stdout


    def create_widgets(self):
        self.master.option_add('*tearOff', 'FALSE')
        self.pgb_value = tkinter.IntVar()

        self.btnGo = tkinter.ttk.Button(self, width=20, text="Запуск")
        self.btnGo["command"] =lambda: threading.Thread(target=self.work.first, kwargs={'progress': self.pgb_value, 'running': True}).start()
        self.btnGo.grid(row=0, column=0)

        self.btnStop = tkinter.ttk.Button(self, width=20, text="Cтоп")
        self.btnStop["command"] = self.work.terminate
        self.btnStop.grid(row=1, column=0)

        self.btnExit = tkinter.ttk.Button(self, width=20, text="Выход")
        self.btnExit["command"] = sys.exit
        self.btnExit.state(["disabled"])  # нужна доработка
        self.btnExit.grid(row=2, column=0)

        self.info = tkinter.Text(self, wrap='word')
        self.info.configure(font='TkFixedFont')
        self.info.grid(row=0, column=1, rowspan=3, sticky='w, n, e, s')
        sys.stdout = StdoutRedirector(self.info, self)

        self.pgb = tkinter.ttk.Progressbar(self, maximum=100, variable=self.pgb_value)
        self.pgb.grid(row=4, column=1, sticky='w, e')

        sgp = tkinter.ttk.Sizegrip(self)
        sgp.grid(row=4, column=2, sticky="e, s")

        self.grid_rowconfigure(0, pad=5)
        self.grid_rowconfigure(1, pad=5)
        self.grid_rowconfigure(2, pad=5, weight=1)
        self.grid_rowconfigure(3, pad=5)
        self.grid_columnconfigure(0, pad=5, minsize=20)
        self.grid_columnconfigure(1, weight=1, pad=5)





work = Work()
root = tkinter.Tk()
app = Application(work=work, master=root)
root.mainloop()

from threading import Thread
import time

class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(5)

c = CountdownTask()
t = Thread(target=c.run, args=(10,))
t.start()
...
c.terminate()   # Сигнал завершения
t.join()        # Ждать реального завершения (если необходимо)


# todo Иногда вы можете встретить определение потоков через наследование от класса Thread
class CountdownThread(Thread):
    def __init__(self, n):
        super().__init__()
        self.n = 0

    def run(self):
        while self.n > 0:
            print('T-minus', self.n)
            self.n -= 1
            time.sleep(5)

c = CountdownThread(5)
c.start()
