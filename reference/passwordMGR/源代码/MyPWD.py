import sqlite3
import tkinter
from itertools import cycle
from tkinter.ttk import Combobox
from tkinter.messagebox import showinfo, showerror, askyesno


class DatabaseAccess:
    @staticmethod
    def doSql(sql):
        with sqlite3.connect('MyPWD.sqlite3') as conn:
            conn.execute(sql)
            conn.commit()

    @staticmethod
    def getData(sql):
        with sqlite3.connect('MyPWD.sqlite3') as conn:
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()


root = tkinter.Tk()
root.geometry('350x250+400+300')
root.resizable(False, False)
root.title('(C)2022彭_Yu')
lbKey = tkinter.Label(root, text='密码数据库密钥：')
lbKey.place(x=10, y=10, width=100, height=20)
key = tkinter.StringVar(root, '')
entryKey = tkinter.Entry(root, textvariable=key, show='*')
entryKey.place(x=120, y=10, width=200, height=20)
lbPlatform = tkinter.Label(root, text='平台  名称：')
lbPlatform.place(x=10, y=40, width=100, height=20)
platformName = tkinter.StringVar(root, '')
entryPlatform = tkinter.Entry(root, textvariable=platformName)
entryPlatform.place(x=120, y=40, width=200, height=20)
lbPassword = tkinter.Label(root, text='设置  密码：')
lbPassword.place(x=10, y=70, width=100, height=20)
password = tkinter.StringVar(root, '')
entryPassword = tkinter.Entry(root, textvariable=password)
entryPassword.place(x=120, y=70, width=200, height=20)


def add_modify():
    if not (key.get() and platformName.get() and password.get()):
        showerror('出错',
                  '请同时输入密码数据库密钥、平台名称、密码.\n注意：密钥不要随意更改.')
        return
    if key.get().isdigit():
        showerror('密钥安全性出错', '为了您的密钥安全，不能使用纯数字作为密钥')
        return
    if sum(map(lambda x,y: x==y, password.get(), key.get())) > 0:
        showerror('密钥安全性出错', '密码不合适，为了您的密钥安全，密码和密钥不能有对应位置相同的字符')
        return
    pwd = ''.join(map(lambda x,y: chr(ord(x)^ord(y)), password.get(), cycle(key.get())))
    sql = 'SELECT * FROM passwords WHERE platform="'+platformName.get()+'"'
    if len(DatabaseAccess.getData(sql)) == 1:
        sql = 'UPDATE passwords SET pwd="'+pwd+'" WHERE platform="'+platformName.get()+'"'
        DatabaseAccess.doSql(sql)
        showinfo('恭喜请求执行成功', '修改密码成功')
    else:
        sql = 'INSERT INTO passwords(platform,pwd) VALUES("'+platformName.get()+'","'+pwd+'")'
        DatabaseAccess.doSql(sql)
        bindPlatformNames()
        showinfo('恭喜请求执行成功', '增加密码成功')


btnAddModify = tkinter.Button(root,
                              text='增加或修改密码',
                              bg='cyan',
                              fg='black',
                              command=add_modify)
btnAddModify.place(x=20, y=100, width=300, height=20)
lbChoosePlatform = tkinter.Label(root, text='请选择平台：')
lbChoosePlatform.place(x=10, y=130, width=100, height=20)


def bindPlatformNames():
    sql = 'SELECT platform FROM passwords'
    data = DatabaseAccess.getData(sql)
    data = [item[0] for item in data]
    comboPlatform['values'] = data


comboPlatform = Combobox(root)
bindPlatformNames()
comboPlatform.place(x=120, y=130, width=200, height=20)

lbResult = tkinter.Label(root, text='查询  结果：')
lbResult.place(x=10, y=160, width=100, height=20)
result = tkinter.StringVar(root, '')
entryResult = tkinter.Entry(root, textvariable=result)
entryResult['state'] = 'disabled'
entryResult.place(x=120, y=160, width=200,height=20)


def getPassword():
    if not comboPlatform.get().strip():
        showerror('出错', '还没选择平台名称')
        return
    if not key.get():
        showerror('出错', '请输入密钥')
        return
    sql = 'SELECT pwd FROM passwords WHERE platform="'+comboPlatform.get()+'"'
    pwd = DatabaseAccess.getData(sql)[0][0]
    pwd = ''.join(map(lambda x,y: chr(ord(x)^ord(y)), pwd, cycle(key.get())))
    result.set(pwd)


btnGetResult = tkinter.Button(root,
                              text='查询密码',
                              bg='cyan',
                              fg='black',
                              command=getPassword)
btnGetResult.place(x=20, y=190, width=149, height=20)


def deletePassword():
    if not comboPlatform.get().strip():
        showerror('出错', '您还没选择平台名称')
        return
    if not askyesno('请确认您的请求', '确定要删除吗？删除后不可恢复！'):
        return
    sql = 'DELETE FROM passwords WHERE platform="'+comboPlatform.get()+'"'
    DatabaseAccess.doSql(sql)
    showinfo('恭喜操作成功完成', '密码删除成功')
    bindPlatformNames()


btnDelete = tkinter.Button(root, text='删除密码',
                           bg='red', fg='yellow',
                           command=deletePassword)
btnDelete.place(x=179, y=190, width=140, height=20)
root.mainloop()
