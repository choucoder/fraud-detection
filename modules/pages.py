from tkinter import (Frame, Label, Button, Toplevel)

LARGE_FONT = ("Verdana", 12)

class PopUp(Toplevel):

    def __init__(self, message, width=400, height=200):
        super().__init__()
        self.title("Message")
        self.geometry(f"{width}x{height}")
        self.attributes("-topmost", True)

        space = Label(self, text='', height='5')
        space.pack()

        label = Label(self, text=message)
        label.pack()

        self.lift()

class MainPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)

        from .admin import LoginView
        from .user import UserLogin
        
        label = Label(self, text="Level access", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = Button(self, text="User", height="2", width="30",
            command=lambda: controller.show_frame(UserLogin))
        button.pack(padx=5, pady=5)

        button2 = Button(self, text="Admin", height="2", width="30",
            command=lambda: controller.show_frame(LoginView))
        button2.pack(padx=5, pady=5)