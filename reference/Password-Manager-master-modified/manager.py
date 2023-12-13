try:
    from tkinter import *
    from tkinter import ttk
except ImportError:
    from Tkinter import *
    import ttk

import Add
import os
import encode
import List
import Search


LARGE_FONT = ("Verdana", 13)
BUTTON_FONT = ("Sans-Serif", 10, "bold")


class Login(Tk):
    def __init__(self, *args):
        Tk.__init__(self, *args)

        if os.name == 'nt':  # Only Windows can use tk
            Tk.iconbitmap(self, default='icon.ico')

        Tk.wm_title(self, "Password Manager")
        self.state = {
            "text": "*Login to access saved password*", "val": False
        }

        if encode.password:  # Has logged in
            self.addLoginFrame()
        else:
            self.addRegisterFrame()

    def addLoginFrame(self):
        login = Frame(self, padx=2, pady=2, bd=2)
        login.pack()

        login_label = Label(login, text=self.state['text'],
                            bd=10, font=LARGE_FONT, width=30)
        login_label.grid(row=0, columnspan=3)

        entry = ttk.Entry(login, show="*")
        entry.grid(row=1, column=1, pady=3)

        entry.focus_set()

        s = ttk.Style()
        s.configure("Submit.TButton", font=BUTTON_FONT)
        submit_btn = ttk.Button(login, text="Submit", style="Submit.TButton",
                                command=lambda: self.checkPwd(
                                   login, label=login_label, entry=entry,
                                   btn=submit_btn))

        submit_btn.grid(row=2, column=1, pady=3)

    def checkPwd(self, frame, **kwargs):
        # **kwargs: label, entry, submit button
        to_check = kwargs['entry'].get()  # input

        # if passwords match
        # if hashlib.md5(chk.encode("utf8")).hexdigest() == encode.password:
        with open(".pwd", "r") as file:
            stored_encrypted_password = file.read()
        decrypted_password = encode.decode(stored_encrypted_password)

        if to_check == decrypted_password:
            self.state['text'] = "*Logged In*"
            self.state['val'] = True
            kwargs['label'].config(text=self.state['text'])
            kwargs['entry'].config(state=DISABLED)  # cannot use
            kwargs['btn'].config(state=DISABLED)

            # add buttons
            self.addConfigBtn(frame)

        # Passwords don't match
        else:
            kwargs['label'].config(text=self.state['text'] + "\n*Try Again*")

    def addConfigBtn(self, login):
        btn_list = ["Add", "List", "Search"]
        btn_cmd_lst = [lambda: Add.AddWindow(self),
                       lambda: List.ListWindow(self),
                       lambda: Search.SearchWindow(self)]

        frames = []  # Frames array
        imgs = []  # image array
        self.img = []  # don't know how the bug fixed...

        for i in range(3):
            frames.append(
                Frame(login, padx=2, width=50, height=50))
            frames[i].grid(row=3, column=i)

            imgs.append(
                PhotoImage(
                    file=btn_list[i] + ".gif", width=48, height=48))
            self.img.append(imgs[i])

            ttk.Button(frames[i], image=imgs[i], text=btn_list[i], compound="top",
                       style="Submit.TButton",
                       command=btn_cmd_lst[i]).grid(sticky="NWSE")

    def addRegisterFrame(self, *arg):
        register = Frame(self, padx=2, pady=2, bd=2)
        register.pack()

        info = "*Register with a password*\n*To start your manager*"
        register_label = Label(register, text=info,
                              bd=10, font=LARGE_FONT, width=30)
        register_label.grid(row=0, columnspan=3)

        pw = ttk.Entry(register, show="*")
        pw.grid(row=1, column=1, pady=3)
        pw.focus_set()

        pwChk = ttk.Entry(register, show="*")
        pwChk.grid(row=2, column=1, pady=3)
        pwChk.bind('<Return>', lambda _: self.register(register,
                                                       pw, pwChk))

        sty = ttk.Style()
        sty.configure("Submit.TButton", font=BUTTON_FONT)
        submit_btn = ttk.Button(register, text="Register",
                               style="Submit.TButton",
                               command=lambda: self.register(register,
                                                             pw, pwChk))
        submit_btn.grid(row=3, column=1, pady=3)

    def register(self, frame, *pwd):
        # *pwd is a list containing password inputs
        if pwd[0].get() == pwd[1].get():
            # encode.password = hashlib.md5(pwd[0].get().encode()).hexdigest()
            encode.password = encode.encode(pwd[0].get())
            # Saving password for future use.
            open(".pwd", "w").write(encode.password)
            frame.destroy()
            self.addLoginFrame()

        else:
            error = "*Passwords dont match*\n*Try again*"
            error_label = Label(frame, text=error,
                               bd=10, font=("Verdana", 11), fg="red")
            error_label.grid(row=4, column=1, pady=3)

            # Removing entered Passwords
            for word in pwd:
                word.delete(0, 'end')


if __name__ == '__main__':
    new = Login()
    new.mainloop()
