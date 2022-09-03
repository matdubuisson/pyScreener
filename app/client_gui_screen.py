import os
import socket as sock
import threading as th
import tkinter as tk
from time import sleep, strftime

import config_screen as conf

class App:
    def __init__(self):
        conf.init_default("client", strftime("%H_%M_%S"))
        conf.registre_pid("client")

        self.init_connection()

        self.app = tk.Tk()
        self.app.title("Screener : client-gui")
        self.app.minsize(width=600, height=600)
        self.app.geometry("600x600+100+100")
        self.widgets = [] # (widget, x%, y%, width%, height%, font)

        self.ip = tk.StringVar()
        self.port = tk.StringVar()

        self.terminal()

    def init_connection(self):
        self.client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.client_socket.connect(conf.datas["client"]["address"])

    def update(self):
        self.app.update_idletasks()
        self.wScreen = self.app.winfo_screenwidth()
        self.hScreen = self.app.winfo_screenheight()
        self.wWindow = self.app.winfo_width()
        self.hWindow = self.app.winfo_height()

    def clear(self):
        for each in self.widgets:
            each[0].destroy()
        l = self.widgets
        self.widgets = []
        del l

    def create_widget(self, widget, x, y, width, height):
        new_widget = (widget, x, y, width, height)
        self.widgets.append(new_widget)
        return new_widget

    def configure_widget(self, widget, foreground=None, background=None, activeforeground=None, activebackground=None, font=None):
        wid = widget[0]
        if foreground != None:
            wid.configure(foreground=foreground)
        if background != None:
            wid.configure(background=background)
        if activeforeground != None:
            wid.configure(activeforeground=activeforeground)
        if activebackground != None:
            wid.configure(activebackground=activebackground)
        if font != None:
            wid.configure(font=font)

    def place_widget(self, widget):
        wid = widget[0]
        # print(self.wWindow, self.hWindow)
        # print((widget[1] * self.wWindow), (widget[2] * self.hWindow), (widget[3] * self.wWindow), (widget[4] * self.hWindow))
        wid.place(x=(widget[1] * self.wWindow), y=(widget[2] * self.hWindow), width=(widget[3] * self.wWindow), height=(widget[4] * self.hWindow))

    def place_all_widgets(self):
        self.update()
        for each in self.widgets:
            self.place_widget(each)

    def terminal(self):
        def refresh_panel(text_widget):
            conf.registre_pid("client")
            file = conf.get_address("screener", "output_txt_file")
            while True:
                message = self.client_socket.recv(1024).decode()
                text_widget.insert(tk.END, message)
                if message == "":
                    # Re-attempt to connect, if no possibilities, it disconnect with the server
                    failure = conf.mark_failure(failure, conf.datas["client"]["address"], "client_sending")
                    if failure == -1:
                        break
                else:
                    failure = 0

        def complet_panel():
            message = self.contain_of_entry_for_text_widget.get()
            try:
                self.client_socket.send(message.encode())
                failure = 0
                self.contain_of_entry_for_text_widget.set("")
            except:
                # Re-attempt to connect, if no possibilities, it disconnect with the user
                failure = conf.mark_failure(failure, conf.datas["client"]["address"], "client_sending")
                if failure == -1:
                    return


        self.clear()
        self.update()
        font = ("arial", 12)

        text_widget = tk.Text(self.app)
        self.configure_widget(self.create_widget(text_widget, 0, 0, 1, 0.8), font=font)
        thread = th.Thread(target=refresh_panel, args=[text_widget])
        thread.start()

        self.contain_of_entry_for_text_widget = tk.StringVar()
        self.configure_widget(self.create_widget(tk.Entry(self.app, textvariable=self.contain_of_entry_for_text_widget), 0, 0.825, 1, 0.05), font=font)

        self.configure_widget(self.create_widget(tk.Button(self.app, text="Send", command=lambda: complet_panel()), 0, 0.9, 1, 0.1), font=font)
        self.app.bind("<Return>", lambda event: complet_panel())

        self.place_all_widgets()

        self.app.bind("<Configure>", lambda event: self.place_all_widgets())

    def menu(self):
        self.clear()
        self.update()

        font = ("arial", 12)

        ip = tk.StringVar()
        port = tk.StringVar()

        self.configure_widget(self.create_widget(tk.Label(self.app, text="Please enter the address of the conncetion : "), 0.1, 0.1, 0.8, 0.05), foreground="red", font=font)

        self.configure_widget(self.create_widget(tk.Label(self.app, text="Ip :"), 0.3, 0.3, 0.4, 0.05), foreground="red", font=font)
        self.configure_widget(self.create_widget(tk.Entry(self.app), 0.3, 0.4, 0.4, 0.05), font=font)

        self.configure_widget(self.create_widget(tk.Label(self.app, text="Port : "), 0.3, 0.5, 0.4, 0.05), foreground="red", font=font)
        self.configure_widget(self.create_widget(tk.Entry(self.app), 0.3, 0.6, 0.4, 0.05), font=font)

        self.configure_widget(self.create_widget(tk.Button(self.app, text="Submit"), 0.3, 0.7, 0.4, 0.1), font=font)

        self.place_all_widgets()

        self.app.bind("<Configure>", lambda event: self.place_all_widgets())

    def run(self):
        self.app.mainloop()
        conf.kill_pids("client")

if __name__ == "__main__":
    app = App()
    app.run()
