try:
    from tkinter import *
    from tkinter import ttk
except ImportError:
    from Tkinter import *
    import ttk

import encode
import json
import pyperclip


NORM_FONT = ("Helvetica", 10)
LARGE_FONT = ("Verdana", 13)


class ListWindow(Toplevel):
    def __init__(self, *args):
        Toplevel.__init__(self, *args)
        self.title("List Database")

        self.frame = getTreeFrame(self, bd=3)
        self.frame.pack()


class getTreeFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.addLists()

    def addLists(self, *arg):
        dataList = self.getData()
        headings = ["Service", "Username"]

        if dataList:
            # Adding the Treeview
            Label(self, text="Double Click to copy password",
                  bd=2, font=LARGE_FONT).pack(side="top")

            # Scroll bar
            scroll_bar = ttk.Scrollbar(self, orient=VERTICAL, takefocus=True)

            # Creates a Treeview widget with specified columns and headings.
            self.tree = ttk.Treeview(self, columns=headings, show="headings")
            scroll_bar.config(command=self.tree.yview)
            # Configures the Treeview to use the scrollbar.
            self.tree.configure(yscroll=scroll_bar.set)

            scroll_bar.pack(side=RIGHT, fill=Y)
            self.tree.pack(side=LEFT, fill='both', expand=1)

            # Adding headings to the columns and sets commands for sorting
            for heading in headings:
                self.tree.heading(
                    heading, text=heading)
                self.tree.column(heading, width=200)

            for data in dataList:
                self.tree.insert("", "end", values=data)

            self.tree.bind("<Double-1>", self.OnDoubleClick)

        else:
            self.errorMsg()

    def getData(self, *arg):
        fileName = ".data"
        self.data = None

        try:
            with open(fileName, "r") as outfile:
                self.data = outfile.read()
        except IOError:
            return ""

        # If there is no data in file
        if not self.data:
            return ""

        self.data = json.loads(self.data)  # JSON-formatted string to dict
        dataList = []
        for service, detail in self.data.items():
            if detail[0]:
                usr = detail[0]
            else:
                usr = "NO ENTRY"
            dataList.append((service, usr))

        return dataList

    def errorMsg(self, *args):
        msg = "*No saved data*"
        label = Label(self, text=msg, font=NORM_FONT, bd=3, width=30)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(self, text="Okay", command=self.master.destroy)
        B1.pack(pady=10)

    def OnDoubleClick(self, event):
        item = self.tree.focus()

        # Copies password to clipboard
        service = self.tree.item(item, "values")[0]
        var = self.data[service][1]
        var = encode.decode(var)
        pyperclip.copy(var)

    # for search
    def updateList(self, regStr, *args):
        for x in self.tree.get_children(''):
            self.tree.delete(x)
        for data in self.getData():
            if re.search(regStr, data[0]) or re.search(regStr, data[1]):
                self.tree.insert("", "end", values=data)
