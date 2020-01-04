import os
import django
import tkinter as tk
from tkinter import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mogli.settings')
django.setup()
from mogli.models import Admin as AdminModel

session = []

LARGE_FONT = ("Verdana", 12)

class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.geometry("1300x400")
        self.title("Fraud detection System")
        self.frames = {}

        for F in (MainPage, Admin, AdminRegister, AdminWindow):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Level access", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="User", height="2", width="30",
            command=lambda: controller.show_frame(PageOne))
        button.pack(padx=5, pady=5)

        button2 = tk.Button(self, text="Admin", height="2", width="30",
            command=lambda: controller.show_frame(Admin))
        button2.pack(padx=5, pady=5)

class AdminWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = Tk()

        menubar = Menu(self.controller)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.do_nothing)
        filemenu.add_command(label="Open", command=self.do_nothing)
        filemenu.add_command(label="Save", command=self.do_nothing)
        filemenu.add_command(label="Save as", command=self.do_nothing)
        filemenu.add_command(label="Close", command=self.do_nothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.do_nothing)
        menubar.add_cascade(label="File", menu=filemenu)

        self.controller.config(menu=menubar)
        Label(self, text="Hola login").pack()

    def do_nothing(self):
        test = TopLevel(self.controller)
        button = Button(test, text="Hello, world!")
        button.pack()

class Admin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = Label(self, text="Login Admin", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        self.username = StringVar()
        self.password = StringVar()
        self.controller = controller

        username_label = Label(self, text="Username *", width="20")
        username_label.pack()

        self.username_entry = Entry(self, textvariable=self.username,
            width="20")
        self.username_entry.pack()

        password_label = Label(self, text="Password *", width="20")
        password_label.pack()

        self.password_entry = Entry(self, textvariable=self.password, 
            show="*", width="20")
        self.password_entry.pack()

        self.info_label = Label(self, text="")
        self.info_label.pack()

        login_btn = Button(self, text="Login", height="1", width="17", 
            command=self.login)
        login_btn.pack()


        mainPage_btn = Button(self, text="Back to Home",
            command=lambda: controller.show_frame(MainPage))
        mainPage_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        register_btn = Button(self, text="Register",
            command=lambda: controller.show_frame(AdminRegister))
        register_btn.pack(side=tk.RIGHT)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username:
            try:
                admin = AdminModel.objects.get(username=username)
                if admin.password == password:
                    print("Login")
                    session.append((username, 1))
                    self.controller.show_frame(AdminWindow)
                else:
                    print("Password incorrect")

            except mogli.models.DoesNotExist as e:
                print("Admin doesn't exist")
        else:
            print(f"Field username empty")

        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        print(f"Login: {username} - {password}")

class AdminRegister(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = Label(self, text="Register Admin", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        username = StringVar()
        password = StringVar()

        username_label = Label(self, text="Username *", width="30")
        username_label.pack()

        self.username_entry = Entry(self, textvariable=username)
        self.username_entry.pack()

        password_label = Label(self, text="Password *", width="30")
        password_label.pack()

        self.password_entry = Entry(self, textvariable=password, show="*")
        self.password_entry.pack()

        Label(self, text="").pack()

        login_btn = Button(self, text="Sign in", height="1", width="17", 
            command=self.register)
        login_btn.pack()

        register_btn = Button(self, text="Back to Login",
            command=lambda: controller.show_frame(Admin))
        register_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            try:
                admin = AdminModel(username=username, password=password)
                admin.save()
                self.username_entry.delete(0, END)
                self.password_entry.delete(0, END)
            except Exception as e:
                print(f"{username} is already exist: {e}")
        else:
            print("Empty fields*")

        print(f"{username} - {password}")

if __name__ == '__main__':
    app = Application()
    app.mainloop()