import os
import urllib.request
import tkinter as tk
from tkinter import *
from tkinter import ttk

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mogli.settings')
django.setup()

from .pages import MainPage

from mogli.models import User as UserModel, Product, TransactionHistory


session = []
session2 = {}
LARGE_FONT = ("Verdana", 12)

def getipaddress():
    try:
        ip_address = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    except:
        import socket
        ip_address = socket.gethostbyname(socket.gethostname())
    return ip_address

# Base Login
class Login(Frame):

    def __init__(self, parent, controller, kind, model, register_view, return_view):
        tk.Frame.__init__(self, parent)
        
        
        self.username = StringVar()
        self.password = StringVar()
        self.controller = controller
        self.kind = kind
        self.model = model
        self.register_view = register_view
        self.return_view = return_view

        label = Label(self, text=f"Login {self.kind}", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
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

        self.menu_bar = MenuBar(parent, controller)

        mainPage_btn = Button(self, text="Back to Home",
            command=lambda: controller.show_frame(MainPage))
        mainPage_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        register_btn = Button(self, text="Register",
            command=lambda: controller.show_frame(self.register_view))
        register_btn.pack(side=tk.RIGHT)
        self.controller = controller

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username:
            try:
                target = self.model.objects.get(username=username)
                if target.password == password:
                    print("Login")
                    
                    self.menu_bar.show()
                    self.controller.show_frame(self.return_view)
                    session.append((username, target.email_id, 1))
                    session2['user'] = target
                else:
                    print("Password incorrect")

            except Exception as e:
                print(f"Admin doesn't exist: {e}")
        else:
            print(f"Field username empty")

        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        print(f"Login: {username} - {password}")


class PopUp(tk.Toplevel):

    def __init__(self, message):
        width, height = (400, 200)
        super().__init__()
        self.title("Message")
        self.geometry(f"{width}x{height}")
        self.attributes("-topmost", True)

        space = Label(self, text='', height='5')
        space.pack()

        label = Label(self, text=message)
        label.pack()

        self.lift()



# The Menubar
class MenuBar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def show(self):
        menubar = Menu(self)
        mainmenu = Menu(menubar, tearoff=0)
        productmenu = Menu(menubar, tearoff=0)
        historymenu = Menu(menubar, tearoff=0)

        productmenu.add_command(label="View products", command=self.view_products)

        historymenu.add_command(label="View transaction history", 
            command=self.view_transaction_history)

        mainmenu.add_command(label="Logout", command=self.do_nothing)

        menubar.add_cascade(label="Products", menu=productmenu)
        menubar.add_cascade(label="History", menu=historymenu)

        # Label(self, text="Hello").pack()

        self.controller.config(menu=menubar)

    def do_nothing(self):
        create_product_screen = tk.Toplevel(self.controller)
        create_product_screen.title("New Product")
        create_product_screen.geometry("300x250")
        button = Button(create_product_screen, text="Hello, world!")
        button.pack()

    def view_transaction_history(self):
        width, height = (1200, 256)

        window = tk.Toplevel(self.controller)
        window.title("Transaction history")
        window.geometry(f"{width}x{height}")

        cols = ('Username', 'Email', 'Product Name', 'Cost', 'IP Address', 'DATE')

        listBox = ttk.Treeview(window, columns=cols, show='headings')

        for col in cols:
            listBox.heading(col, text=col)
        listBox.grid(row=2, column=5, columnspan=2)

        for history in TransactionHistory.objects.filter(user=session2['user']):
            listBox.insert("", "end", values=(
                history.user.username, history.user.email_id,
                history.product.product_name, history.cost,
                history.ip_address, history.created_at
            ))

    def view_products(self):

        width, height = (810, 300)

        window = tk.Toplevel(self.controller)
        window.title("Products")
        window.geometry(f"{width}x{height}")

        cols = ('Product ID', 'Product', 'Cost', 'IMAGE')

        self.listBox = ttk.Treeview(window, columns=cols, show='headings')
        self.listBox.bind('<ButtonRelease-1>', self.selectItem)

        for col in cols:
            self.listBox.heading(col, text=col)
        self.listBox.grid(row=2, column=5, columnspan=2)

        for product in Product.objects.all():
            self.listBox.insert("", "end", values=(
                product.id_product, product.product_name,
                str(product.cost), product.image
            ))
    
    def selectItem(self, a):

        selected = self.listBox.focus()
        item = self.listBox.item(selected)
        print(item)
        self.buy_product(item)

    def buy_product(self, item):

        width, height = (610, 450)

        buywin = tk.Toplevel()
        buywin.title("Buy product")
        buywin.geometry(f"{width}x{height}")
        buywin.attributes("-topmost", True)

        product_id = item['values'][0]
        product_name = item['values'][1]
        product_price = item['values'][2]
        product_image = item['values'][3]
        self.product_id = product_id

        wintitle_label = Label(buywin, text="Buy product", font=LARGE_FONT, bg='gray', width='70', height='2')
        wintitle_label.pack()

        separator1 = Label(buywin, text='', height='2')
        separator1.pack()

        product_id_label = Label(buywin, text=f'Product ID: {product_id}')
        product_id_label.pack()

        product_name_label = Label(buywin, text=f'Product name: {product_name}')
        product_name_label.pack()

        product_price_label = Label(buywin, text=f'Product price: {product_price}')
        product_price_label.pack()

        product_image_label = Label(buywin, text=f'Product image: {product_image}')
        product_image_label.pack()

        separator2 = Label(buywin, text='', height='2')
        separator2.pack()

        credit_card_label = Label(buywin, text="Credit card number *", width="20")
        credit_card_label.pack()

        self.credit_card = StringVar()
        self.credit_card_entry = Entry(buywin, textvariable=self.credit_card,
            width="20")
        self.credit_card_entry.pack()

        separator3 = Label(buywin, text='', height='5')
        separator3.pack()

        buy_button = Button(buywin, text="Buy", command=self.finish_buying)
        buy_button.pack()

        buywin.lift()

    def finish_buying(self):

        product_id = self.product_id
        product = Product.objects.get(id_product=product_id)
        user = session2['user']
        credit_card = self.credit_card_entry.get()
        ip_address = getipaddress()

        print(f"{user} buy product with id {product} using credit card {credit_card}")

        transaction = TransactionHistory(
            product=product,
            cost=product.cost,
            ip_address=ip_address,
            user=user
        )

        try:
            transaction.save()
            PopUp("Transaction completed correctly.")
        except Exception:
            PopUp("Transaction failed. Verify your data and try again.")

        

# User views
class UserLogin(Login):

    def __init__(self, parent, controller):

        super().__init__(parent, controller, "User", UserModel, UserRegister, UserHome)

class UserRegister(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Register User", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        username = StringVar()
        password = StringVar()
        phone = StringVar()
        email = StringVar()
        amount_limit = StringVar()
        ip_address = StringVar()

        # Username
        username_label = Label(self, text="Username *", width="30")
        username_label.pack()

        self.username_entry = Entry(self, textvariable=username)
        self.username_entry.pack()

        # Password
        password_label = Label(self, text="Password *", width="30")
        password_label.pack()

        self.password_entry = Entry(self, textvariable=password, show="*")
        self.password_entry.pack()

        # Phone number
        phone_label = Label(self, text="Phone *", width="30")
        phone_label.pack()

        self.phone_entry = Entry(self, textvariable=phone)
        self.phone_entry.pack()

        # Email
        email_label = Label(self, text="Email *", width="30")
        email_label.pack()

        self.email_entry = Entry(self, textvariable=email)
        self.email_entry.pack()

        # Amount limit
        amount_limit_label = Label(self, text="Amount limit *", width="30")
        amount_limit_label.pack()

        self.amount_limit_entry = Entry(self, textvariable=amount_limit)
        self.amount_limit_entry.pack()
        
        Label(self, text="").pack()

        login_btn = Button(self, text="Sign in", height="1", width="17", 
            command=self.register)
        login_btn.pack()

        register_btn = Button(self, text="Back to Login",
            command=lambda: controller.show_frame(UserLogin))
        register_btn.pack(side=RIGHT, padx=5, pady=5)
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        amount_limit = self.amount_limit_entry.get()
        ip_address = getipaddress()

        if username and password and phone and email and amount_limit and ip_address:
            try:
                user = UserModel(
                    username=username,
                    password=password,
                    phone_number=phone,
                    email_id=email,
                    amount_limit=amount_limit,
                    ip_address=ip_address)
                user.save()

                self.username_entry.delete(0, END)
                self.password_entry.delete(0, END)
                self.phone_entry.delete(0, END)
                self.email_entry.delete(0, END)
                self.amount_limit_entry.delete(0, END)
                self.ip_address_entry.delete(0, END)

            except Exception as e:
                print("Some fields could't be totally validated or...")
                print(f"{username} already exist: {e}")
        else:
            print("Empty fields*")

        print(f"{username} - {password}")


class UserHome(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = Label(self, text="Welcome User!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.menu_bar = MenuBar(parent, controller)

