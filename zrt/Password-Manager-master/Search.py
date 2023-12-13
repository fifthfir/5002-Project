try:
    from tkinter import *
    from tkinter import ttk
except ImportError:
    from Tkinter import *
    import ttk
import List
import re

BUTTON_FONT = ("Sans-Serif", 10, "bold")


class SearchWindow(Toplevel):
    def __init__(self, *args):
        Toplevel.__init__(self, *args)

        self.title("Search")

        self.frame = Frame(self, padx=2, pady=2, bd=3)
        self.frame.pack()

        self.to_search = StringVar()
        self.to_search.trace('w', self.onUpdate)
        search_win = ttk.Entry(self.frame, textvariable=self.to_search)
        search_win.grid(row=0, columnspan=2)
        search_win.focus_set()

        sty = ttk.Style()
        sty.configure("Submit.TButton", font=BUTTON_FONT, sticky="e")

        search_btn = ttk.Button(self.frame, text="Search",
                                style="Submit.TButton",
                                command=lambda:  self.onUpdate())
        search_btn.grid(row=0, column=3, sticky="e")

        self.tree = List.getTreeFrame(self, bd=3)
        self.tree.pack()

    def onUpdate(self, *args):
        # *args = [name, index, mode]
        content = self.to_search.get()
        search_re = re.compile(content, re.IGNORECASE)
        self.tree.updateList(search_re)
        return True
