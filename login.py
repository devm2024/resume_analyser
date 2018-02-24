from tkinter import *

def login():
    master = Tk()
    Label(master, text="Username").grid(row=0)
    Label(master, text="Password").grid(row=1)

    user = Entry(master)
    password = Entry(master, show="*")

    user.grid(row=0, column=1)
    password.grid(row=1, column=1)

    Button(master, text='Login', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
    master.bind('<Return>', lambda x: master.quit())

    mainloop()

    u, p = user.get(), password.get()
    master.destroy();
    return u, p

if __name__ == '__main__':
    print(login())
