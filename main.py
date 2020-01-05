from tkinter import (Tk, Frame)
from modules import admin, user
from modules.pages import MainPage

LARGE_FONT = ("Verdana", 12)

class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.geometry("720x400")
        self.title("Fraud detection System")
        self.frames = {}
        self.pages = [
            MainPage,
            admin.MainView, admin.LoginView, admin.RegisterView,
            user.UserLogin, user.UserRegister, user.UserHome]

        for F in self.pages:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == '__main__':
    app = Application()
    app.mainloop()
