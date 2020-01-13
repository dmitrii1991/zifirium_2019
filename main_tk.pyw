import sys
import os
import threading

import tkinter
import tkinter.scrolledtext
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog

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
        self.work = work()
        self.grid(sticky="w, n, e, s", padx=4, pady=4)
        self.create_widgets()
        self.master.title("Реализация")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.path_in_data_a = None
        self.path_in_data_p = None

        orig_stdout = sys.stdout


    def create_widgets(self):
        def run_programm():
            threading.Thread(target=self.work.first, kwargs={'progress': self.pgb_value, 'running': True}).start()
            self.btnExit.state(["disabled"])

        def stop_programm():
            self.work.terminate()
            self.btnExit.state(["!disabled"])

        def get_in_data_a():
            file_name = tkinter.filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),))
            if os.path.basename(file_name) == 'in_data_a.csv':
                self.work.in_data_a = file_name
                self.btn_in_data_a["style"] = 'green.TButton'
                self.btn_in_data_a["text"] = 'найден in_data_a.csv'

        def get_in_data_p():
            file_name = tkinter.filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),))
            if os.path.basename(file_name) == 'in_data_p.csv':
                self.work.in_data_p = file_name
                self.btn_in_data_p["style"] = 'green.TButton'
                self.btn_in_data_a["text"] = 'найден in_data_p.csv'

        self.master.option_add('*tearOff', 'FALSE')
        self.pgb_value = tkinter.IntVar()

        self.btnGo = tkinter.ttk.Button(self, width=20, text="Запуск", command=run_programm)
        self.btnGo.grid(row=0, column=0)

        self.btnStop = tkinter.ttk.Button(self, width=20, text="Cтоп", command=stop_programm)
        self.btnStop.grid(row=1, column=0)

        self.btnExit = tkinter.ttk.Button(self, width=20, text="Выход", command=sys.exit)
        self.btnExit.grid(row=2, column=0)

        self.info = tkinter.Text(self, wrap='word')
        self.info.configure(font='TkFixedFont')
        self.info.grid(row=0, column=1, rowspan=6, sticky='w, n, e, s')

        sys.stdout = StdoutRedirector(self.info, self)


        tkinter.ttk.Style().configure('green.TButton', foreground="green")
        tkinter.ttk.Style().configure('red.TButton', foreground="red")
        if "in_data_a.csv" in os.listdir():
            self.btn_in_data_a = tkinter.ttk.Button(self, width=20, text="найден in_data_a.csv")
            self.btn_in_data_a["style"] = 'green.TButton'
        else:
            self.btn_in_data_a = tkinter.ttk.Button(self, width=20, text="не найден in_data_a.csv")
            self.btn_in_data_a["style"] = 'red.TButton'
        self.btn_in_data_a.grid(row=3, column=0)
        self.btn_in_data_a["command"] = get_in_data_a

        if "in_data_p.csv" in os.listdir():
            self.btn_in_data_p = tkinter.ttk.Button(self, width=20, text="найден in_data_p.csv")
            self.btn_in_data_p["style"] = 'green.TButton'
        else:
            self.btn_in_data_p = tkinter.ttk.Button(self, width=20, text="не найден in_data_p.csv")
            self.btn_in_data_p["style"] = 'red.TButton'
        self.btn_in_data_p.grid(row=4, column=0)
        self.btn_in_data_p["command"] = get_in_data_p

        sgp = tkinter.ttk.Sizegrip(self)
        sgp.grid(row=4, column=2, sticky="e, s")

        self.pgb = tkinter.ttk.Progressbar(self, maximum=100, variable=self.pgb_value)
        self.pgb.grid(row=7, column=1, sticky='w, e')


        self.grid_rowconfigure(0, pad=5)
        self.grid_rowconfigure(1, pad=5)
        self.grid_rowconfigure(2, pad=5)
        self.grid_rowconfigure(3, pad=5)
        self.grid_rowconfigure(4, pad=5)
        self.grid_rowconfigure(5, pad=5, weight=1)

        self.grid_columnconfigure(0, pad=5, minsize=20)
        self.grid_columnconfigure(1, weight=1, pad=5)



root = tkinter.Tk()
app = Application(work=Work, master=root)
root.mainloop()
