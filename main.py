import os
import django
import tkinter as tk
from tkinter import *
from tkinter import ttk
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mogli.settings')
django.setup()
from mogli.models import Admin as AdminModel
from mogli.models import Product
from mogli.models import TransactionHistory

session = []

LARGE_FONT = ("Verdana", 12)


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.geometry("720x300")
        self.title("Fraud detection System")
        self.frames = {}

        for F in (MainPage, Admin, AdminRegister, AdminPage):
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

class MenuBar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def show(self):
        menubar = Menu(self)
        mainmenu = Menu(menubar, tearoff=0)
        productmenu = Menu(menubar, tearoff=0)
        historymenu = Menu(menubar, tearoff=0)

        productmenu.add_command(label="Add products", command=self.create_product)
        productmenu.add_command(label="View products", command=self.view_products)

        historymenu.add_command(label="View transaction history", 
            command=self.view_transaction_history)

        mainmenu.add_command(label="Logout", command=self.do_nothing)

        menubar.add_cascade(label="Main", menu=mainmenu)
        menubar.add_cascade(label="Products", menu=productmenu)
        menubar.add_cascade(label="History", menu=historymenu)

        Label(self, text="Hello").pack()

        self.controller.config(menu=menubar)

    def do_nothing(self):
        create_product_screen = tk.Toplevel(self.controller)
        create_product_screen.title("New Product")
        create_product_screen.geometry("300x250")
        button = Button(create_product_screen, text="Hello, world!")
        button.pack()

    def view_transaction_history(self):
        width, height = (1000, 256)

        window = tk.Toplevel(self.controller)
        window.title("Transaction history")
        window.geometry(f"{width}x{height}")

        cols = ('Username', 'Email', 'Product Name', 'Cost', 'IP Address')

        listBox = ttk.Treeview(window, columns=cols, show='headings')

        for col in cols:
            listBox.heading(col, text=col)
        listBox.grid(row=2, column=5, columnspan=2)

        for product in TransactionHistory.objects.all():
            listBox.insert("", "end", values=(
                product.id_product, product.product_name,
                str(product.cost), product.image
            ))

    def view_products(self):
        width, height = (810, 350)

        window = tk.Toplevel(self.controller)
        window.title("Products")
        window.geometry(f"{width}x{height}")

        cols = ('Product ID', 'Product', 'Cost', 'IMAGE')

        listBox = ttk.Treeview(window, columns=cols, show='headings')

        for col in cols:
            listBox.heading(col, text=col)
        listBox.grid(row=2, column=5, columnspan=2)

        for product in Product.objects.all():
            listBox.insert("", "end", values=(
                product.id_product, product.product_name,
                str(product.cost), product.image
            ))

    def create_product(self):
        width, height = (310, 250)

        window = tk.Toplevel(self.controller)
        window.title("Create New Product")
        window.geometry(f"{width}x{height}")

        self.product_id = StringVar()
        self.product_name = StringVar()
        self.cost = StringVar()
        self.image = StringVar()

        id_label = Label(window, text="Product ID: ")
        id_label.grid(row=2, column=0)

        self.id_entry = Entry(window, textvariable=self.product_id)
        self.id_entry.grid(row=2, column=1, pady=10)

        name_label = Label(window, text="Name: ")
        name_label.grid(row=5, column=0, pady=10)

        self.name_entry = Entry(window)
        self.name_entry.grid(row=5, column=1, pady=10)

        cost_label = Label(window, text="Cost: ")
        cost_label.grid(row=7, column=0, pady=10)

        self.cost_entry = Entry(window)
        self.cost_entry.grid(row=7, column=1, pady=10)

        image_label = Label(window, text="Image: ")
        image_label.grid(row=9, column=0, pady=10)

        self.image_entry = Entry(window)
        self.image_entry.grid(row=9, column=1, pady=10)

        create_button = Button(window, text="Create", command=self.save_product)
        create_button.grid(row=12, column=1, pady=20)

        self.info_label = Label(window, text="")
        self.info_label.grid(row=13, column=1, pady=5)

    def save_product(self):
        _id = self.id_entry.get()
        name = self.name_entry.get()
        cost = self.cost_entry.get()
        image = self.image_entry.get()

        if _id and name and cost and image:
            product = Product(
                id_product=_id, product_name=name,
                cost=float(cost), image=image
            )
            product.save()
            self.id_entry.delete(0, END)
            self.name_entry.delete(0, END)
            self.cost_entry.delete(0, END)
            self.image_entry.delete(0, END)

            print(f"Product {name} registered correctly")
        else:
            print("Empty inputs")

class AdminPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = Label(self, text="", font=LARGE_FONT)
        title.pack(padx=10, pady=10)

class Admin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = Label(self, text="Login Admin", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        self.username = StringVar()
        self.password = StringVar()
        self.controller = controller
        self.menuBar = MenuBar(parent, controller)

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
        self.controller = controller

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username:
            try:
                admin = AdminModel.objects.get(username=username)
                if admin.password == password:
                    print("Login")
                    self.menuBar.show()
                    self.controller.show_frame(AdminPage)
                    session.append((username, 1))
                else:
                    print("Password incorrect")

            except Exception as e:
                print(f"Admin doesn't exist: {e}")
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
