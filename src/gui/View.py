from tkinter import Button, messagebox, Entry, Label, Menu, StringVar, Frame, N, W ,S ,E
from abc import ABCMeta, abstractmethod

# Klasa odpowiedzialna za powstawanie widoku / interfejsu graficznego
# W tej klasie znajduje sie wszystkie instrukjce dotyczace rysowania elemntow graficznych
# Klasa do porawnego dzialania potrzebuje KOntrolera, ktory implementuje metode read !
class View:

    class Controller:
        __metaclass__ = ABCMeta
        @abstractmethod
        def load(self): raise NotImplementedError

    def __init__(self, tk, controller: Controller):
        self.__root = tk
        self.__controller = controller
        self.login = StringVar()
        self.password = StringVar()
        self.answer = StringVar()
        self.offset = StringVar()
        self.size = StringVar()
        self.host = StringVar()
        self.port = StringVar()
        self.host.set("imap.gmail.com")
        self.port.set(993)

    #Funkcja odpowiedzialna za tworzenie elementow graficznych
    def render(self):
        mainframe = Frame(self.__root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)

        self.answer = StringVar()

        Label(mainframe, text="Login: ").grid(column=1, row=1, sticky=(E))
        Entry(mainframe, textvariable=self.login).grid(column=2, row=1, sticky=(W, E))

        Label(mainframe, text="Hasło:").grid(column=1, row=2, sticky=E)
        Entry(mainframe, show="*", width=50, textvariable=self.password).grid(column=2, row=2, sticky=(W, E))

        Label(mainframe, text="Liczba maili:").grid(column=1, row=3, sticky=E)
        Entry(mainframe, textvariable=self.size).grid(column=2, row=3, sticky=(W, E))

        Label(mainframe, text="Offset:").grid(column=1, row=4, sticky=E)
        Entry(mainframe, textvariable=self.offset).grid(column=2, row=4, sticky=(W, E))

        Label(mainframe, text="Host:").grid(column=1, row=5, sticky=E)
        Entry(mainframe, textvariable=self.host).grid(column=2, row=5, sticky=(W, E))
        
        Label(mainframe, text="Port:").grid(column=1, row=6, sticky=E)
        Entry(mainframe, textvariable=self.port).grid(column=2, row=6, sticky=(W, E))

        Button(mainframe, text=" Pobierz! ",
               command= lambda  : self.__controller.load())\
            .grid(column=3, row=7, sticky=W)


        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    #FUnckja pozwalajaca na wyswietlenie informacji
    def showInfo(self,info):
        messagebox.showerror(title="Info", message=info)


