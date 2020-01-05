from tkinter import (Frame, Label, Button)

LARGE_FONT = ("Verdana", 12)

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