import json
import encode

try:
    from tkinter import *
    from tkinter import ttk
except ImportError:
    from Tkinter import *
    import ttk

LABEL_FONT = ("Monospace", 12)
BUTTON_FONT = ("Sans-Serif", 10, "bold")
INFO_FONT = ("Verdana", 12)


class AddWindow(Toplevel):
    ''' Add Window'''
    def __init__(self, *args):  # A tuple of many arguments
        Toplevel.__init__(self, *args)

        # Add Credentials
        self.title("Add")
        self.setFrames()

    def setFrames(self, **kwargs):
        # a Frame called 'add'
        add = Frame(self, padx=2, pady=2, bd=3)
        add.pack()

        # Three labels
        # Service
        Label(add, text="Service *", width=30, bd=3, font=LABEL_FONT).pack()
        service = ttk.Entry(add)
        service.pack()  # Put the Entry into the add frame

        # Username
        Label(add, text="Username", width=30, bd=3, font=LABEL_FONT).pack()
        username = ttk.Entry(add)
        username.pack()

        # Password
        Label(add, text="Password *", width=30, bd=3, font=LABEL_FONT).pack()
        password = ttk.Entry(add, show="*")
        password.pack()

        # Style of submit button, font and align
        sty = ttk.Style()
        sty.configure("Submit.TButton", font=BUTTON_FONT, sticky="s")

        # label for spacing extra information in red
        info = Label(add, width=30, bd=3, fg="red", font=INFO_FONT)
        info.pack()

        addBtn = ttk.Button(add, text="Add to Manager", style="Submit.TButton",
                            command=lambda: self.addClicked(
                                info=info, username=username,
                                password=password, service=service))

        addBtn.pack()

    def addClicked(self, **kwargs):  # A dict of many arguments
        fileName = ".data"
        data = {}
        # Writing data to a secrete file

        if (kwargs['password'].get() != "" and kwargs['service'].get() != ""):
            details = [kwargs['username'].get(),
                    #  encode.encode(kwargs['password'].get()).decode('utf-8')]
                       encode.encode(kwargs['password'].get())]

            # read present data
            try:
                with open(fileName, "r") as outfile:
                    data = outfile.read()  # in json format
            except IOError:
                # Create file if doesn't exits
                open(fileName, "a").close()

            # load new data
            if data:
                data = json.loads(data)  # from json into dictionary
                data[kwargs['service'].get()] = details
            else:
                data = {}
                data[kwargs['service'].get()] = details

            # Writing back the data
            with open(".data", "w") as outfile:
                outfile.write(json.dumps(data, sort_keys=True, indent=4))
                # from dictionary to json, to write into the file

            # To delete contents of the input Entry
            for input_frame in ('username', 'service', 'password'):
                kwargs[input_frame].delete(0, 'end')

            kwargs['info'].config(text="*Added Successfully*")

        # No input
        else:
            kwargs['info'].config(text="*Please enter Service and Password*")
