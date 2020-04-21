import tkinter as tk
from functools import partial

def create_widget():
    master = tk.Tk()
    tk.Label(master,
             text="Enter type of information marked").grid(row=0)

    e = tk.Entry(master)

    e.grid(row=0, column=1)

    tk.Button(master,
              text='Submit', command=partial(show_entry_fields,e)).grid(row=3,
                                                           column=1,
                                                           sticky=tk.W,
                                                           pady=4)

    tk.mainloop()

def show_entry_fields(e):
    print("Label: %s" % (e.get()))
    tk.Tk().quit()
