from src.mail.EmailClient import EmailClient
from src.gui.View import View
import tkinter as tk
# Klasa implementuje kontorler widoku
# Klasa jest rowniez kontorlerem dla naszego widoku
class GuiController(View.Controller):
    APP_NAME = "EmailClient"

    def __init__(self, root=tk.Tk):
        self.__root = root()

    #Metoda uruchamiajaca aplikacje
    def run(self):
        self.__root.title(self.APP_NAME)
        self.__view = View(self.__root, self)
        self.__view.render()
        self.__root.mainloop()

    # Funckja wywolywana przez uzytkownika po klikniecu przycisku "Pobierz"
    def load(self):
        try:
            size = self.__getInt(self.__view.size.get(), 3)
            offset = self.__getInt(self.__view.offset.get())
            port = self.__getInt(self.__view.port.get())
            username = self.__view.login.get()
            password = self.__view.password.get()
            host = self.__view.host.get()

            EmailClient(username, password, host, port)\
                .load(size, offset)

        except Exception as e:
            self.__view.showInfo(e.__str__())

    #Rzutuje string na int, jesli wystapi blad to zwracam wskazana watosc domyslna
    # Nie jest to najlepsze miejsce do tej funckji, lepszy bylby jakis helper itp. !
    def __getInt(self, str : str, default = 0):
        try:
            return int(str)
        except:
            return default









