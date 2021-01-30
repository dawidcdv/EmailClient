import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from src.gui.View import View


class EmailClient(View.Controller):

    def __init__(self,login, password, host="imap.gmail.com", port=993):
        self.login = login
        self.password = password
        self.host = host
        self.port = port

    def load(self, size = 3, offset =0):
        def clean(text):
            # Przygotowanie tekstu do tworzenia nowego folderu
            return "".join(c if c.isalnum() else "_" for c in text)

        imap = imaplib.IMAP4_SSL(self.host)
        # Uwierzytelnianie
        imap.login(self.login, self.password)

        status, messages = imap.select("INBOX")
        # Calkowita liczba maili
        messages = int(messages[0])
        # W przypadku jesli offset jest wiekszy od liczby maili koncze prace
        if offset > messages:
            return

        #Wyliczam zakresy id maili do pobrania
        startMailId = messages - offset
        endMailId = messages - offset - size

        #Pobieram maile w petli
        for id in range(startMailId, endMailId, -1):
            #Pobieram mail po id
            res, msg = imap.fetch(str(id), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    #Parsuje maila
                    msg = email.message_from_bytes(response[1])
                    #Dekoduje tytyul maila
                    # Jesli jest zapisany w bajtach to dekoduje do stringa
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)
                    #Robie to samo dla nadawcy
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)

                    # Tworze odpowiedni folder dla maila jesli nie istnieje
                    folder_name = clean(subject) + str(id)
                    if not os.path.isdir(folder_name):
                        os.mkdir(folder_name)

                    if msg.is_multipart():
                        #Iteruje po czesciach maila
                        for part in msg.walk():
                            # Pobieram content_type w celu sprawdzenia jakiego typu jest mail
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                #Pobieram tresc maila
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                logMsg = From + "\n" + subject + "\n" + body + "\n\n\n"
                                filepath = os.path.join(folder_name, "log.txt")
                                with open(filepath, "a",encoding='utf-8') as f:
                                    print(logMsg,file=f)
                            # Obsluga załacznika
                            elif "attachment" in content_disposition:
                                filename = part.get_filename()
                                if filename:
                                    filepath = os.path.join(folder_name, filename)
                                    #Zapisuje zalacznik
                                    open(filepath, "wb").write(part.get_payload(decode=True))
                    else:
                        #pobieram content_type  i tresc analogicznie jak wyzej, jesli mail nie ma zalacznikow itp.
                        content_type = msg.get_content_type()
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            filepath = os.path.join(folder_name,"log.txt" )
                            logMsg = From + "\n" + subject + "\n" + body+ "\n\n\n"
                            open(filepath, "a").write(logMsg)
                     #Zapisuje plik html w odpowiednim folderze dla danego maila i otwieram go w przegladarce
                    if content_type == "text/html":
                        filename = "index.html"
                        filepath = os.path.join(folder_name, filename)
                        with open(filepath, "w", encoding='utf-8') as f:
                            print(body, file=f)
                        webbrowser.open(filepath)

        #Zamykam polaczenie i sie wylogowuje
        imap.close()
        imap.logout()