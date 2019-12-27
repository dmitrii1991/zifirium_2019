import sys
import threading

import tkinter
import tkinter.scrolledtext
import tkinter.ttk
import tkinter.messagebox

from main import get_result, Work


class StdoutRedirector(object):

    def __init__(self, text_area, obj_self):
        self.text_area = text_area
        self.obj_self = obj_self

    def write(self, str):
        self.text_area.insert(tkinter.END, str)
        self.text_area.see(tkinter.END)
        self.obj_self.update_idletasks()


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
        self.btnGo["command"] = threading.Thread(target=self.work.first, kwargs={'progress': self.pgb_value}).start
        self.btnGo.grid(row=0, column=0)

        self.btnStop = tkinter.ttk.Button(self, width=20, text="Cтоп")
        self.btnStop["command"] = sys.exit
        self.btnStop.state(["disabled"])  # нужна доработка
        self.btnStop.grid(row=1, column=0)

        self.info = tkinter.Text(self, wrap='word')
        self.info.configure(font='TkFixedFont')
        self.info.grid(row=0, column=1, rowspan=3, sticky='w, n, e, s')
        sys.stdout = StdoutRedirector(self.info, self)

        self.pgb = tkinter.ttk.Progressbar(self, maximum=100, variable=self.pgb_value)
        self.pgb.grid(row=4, column=1, sticky='w, e')

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
