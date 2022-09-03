import os
import socket as sock
import threading as th
import tkinter as tk
from time import sleep, strftime

import config_screen as conf

class App:
    def __init__(self):
        # Create system files and registre process
        start_time = strftime("%H_%M_%S")
        conf.init_default("client", start_time)
        # conf.registre_pid("client") => Main process can die by itself

        # Init the graphic user interface (GUI)
        self.app = tk.Tk()
        def refresh_title(start_time):
            start_time = start_time.replace("_", ":")
            conf.registre_pid("client")
            while True:
                self.app.title("Screener : client-gui | Start at {0} | {1}".format(start_time, strftime("%H:%M:%S")))
                sleep(1)
        thread = th.Thread(target=refresh_title, args=[start_time])
        thread.start()
        self.app.minsize(width=600, height=600)
        self.app.geometry("600x600+100+100")
        self.widgets = [] # (widget, x%, y%, width%, height%, font)

        # Variables for socket
        self.client_socket = None

        # Variables for the menu
        self.label_for_ip_and_port = tk.StringVar()
        self.label_for_ip_and_port.set("Please enter the address of the conncetion : ")
        self.ip = tk.StringVar(); self.port = tk.StringVar()
        ip, port = conf.datas["client"]["address"]
        self.ip.set(ip); self.port.set(str(port))

        # Variables for the terminal
        self.contain_of_text_widget = ""
        self.contain_of_entry_for_text_widget = tk.StringVar()
        self.label_for_lighting_button = tk.StringVar()
        self.label_for_lighting_button.set("white")
        self.terminal_need_break = False

        self.menu()

    def run(self):
        self.app.mainloop()
        if self.client_socket != None:
            self.client_socket.close()
        conf.kill_pids("client")

    def update(self):
        # Update informations about sizes
        self.app.update_idletasks() # Update tkinter informations
        self.wScreen = self.app.winfo_screenwidth()
        self.hScreen = self.app.winfo_screenheight()
        self.wWindow = self.app.winfo_width()
        self.hWindow = self.app.winfo_height()

    def clear(self):
        # Destroy all current widgets
        for each in self.widgets:
            each[0].destroy()
        l = self.widgets
        self.widgets = []
        del l

    def create_widget(self, widget, x, y, width, height):
        # Auto-create the widget and append it in the cache
        new_widget = (widget, x, y, width, height)
        self.widgets.append(new_widget)
        return new_widget

    def configure_window(self, background=None):
        theme = self.label_for_lighting_button.get()
        if background != None:
            self.app.configure(background=background)
        else:
            if theme == "black":
                self.app.configure(background="black")
            else:
                self.app.configure(background="white")

    def configure_widget(self, widget, foreground=None, background=None, activeforeground=None, activebackground=None, font=None):
        # Easily configuration
        wid = widget[0]
        theme = self.label_for_lighting_button.get()
        ####
        if foreground != None:
            wid.configure(foreground=foreground)
        else:
            if theme == "black":
                wid.configure(foreground="white")
            else:
                wid.configure(foreground="black")
        ####
        if background != None:
            wid.configure(background=background)
        else:
            if theme == "black":
                wid.configure(background="black")
            else:
                wid.configure(background="white")
        ####
        if type(wid) in (tk.Label, tk.Button):
            if activeforeground != None:
                wid.configure(activeforeground=activeforeground)
            else:
                if theme == "black":
                    wid.configure(activeforeground="black")
                else:
                    wid.configure(activeforeground="white")
            ####
            if activebackground != None:
                wid.configure(activebackground=activebackground)
            else:
                if theme == "black":
                    wid.configure(activebackground="white")
                else:
                    wid.configure(activebackground="black")
            ####
        ####
        if font != None:
            wid.configure(font=font)

    def place_widget(self, widget):
        # Place the widget according to the sizes of the window, it respects pourcentage dimensions
        wid = widget[0]
        wid.place(x=(widget[1] * self.wWindow), y=(widget[2] * self.hWindow), width=(widget[3] * self.wWindow), height=(widget[4] * self.hWindow))

    def place_all_widgets(self):
        # Auto-place all widgets
        self.update()
        for each in self.widgets:
            self.place_widget(each)

    def init_connection(self):
        try:
            self.client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            self.client_socket.connect((self.ip.get(), int(self.port.get())))
        except ConnectionRefusedError:
            self.label_for_ip_and_port.set("Connection refused, ip or port isn't valid....")
            return
        self.terminal()

    ########################################################################################

    def menu(self):
        self.clear()
        self.update()
        font = ("arial", 12)
        self.configure_window()

        self.configure_widget(self.create_widget(tk.Label(self.app, textvariable=self.label_for_ip_and_port), 0.1, 0.1, 0.8, 0.05), foreground="red", font=font)

        self.configure_widget(self.create_widget(tk.Label(self.app, text="Ip :"), 0.3, 0.3, 0.4, 0.05), foreground="red", font=font)
        self.configure_widget(self.create_widget(tk.Entry(self.app, textvariable=self.ip), 0.3, 0.4, 0.4, 0.05), font=font)

        self.configure_widget(self.create_widget(tk.Label(self.app, text="Port : "), 0.3, 0.5, 0.4, 0.05), foreground="red", font=font)
        self.configure_widget(self.create_widget(tk.Entry(self.app, textvariable=self.port), 0.3, 0.6, 0.4, 0.05), font=font)

        self.configure_widget(self.create_widget(tk.Button(self.app, text="Submit", command=lambda: self.init_connection()), 0.3, 0.7, 0.4, 0.1), font=font)

        self.place_all_widgets()

        self.app.bind("<Configure>", lambda event: self.place_all_widgets())

    ########################################################################################

    def terminal(self):
        def refresh_panel():
            conf.registre_pid("client")
            file = conf.get_address("screener", "output_txt_file")
            while True:
                message = self.client_socket.recv(1024).decode()
                while self.terminal_need_break:
                    pass
                self.text_widget.insert(tk.END, message)
                self.contain_of_text_widget += message
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
        self.configure_window()

        self.text_widget = tk.Text(self.app)
        self.configure_widget(self.create_widget(self.text_widget, 0, 0, 1, 0.8), font=font)
        self.text_widget.insert("0.0", self.contain_of_text_widget)

        if not self.terminal_need_break:
            thread = th.Thread(target=refresh_panel)
            thread.start()

        #### Four small buttons

        def clear_text_widget():
            self.contain_of_text_widget = ""
            self.text_widget.delete("0.0", tk.END)

        self.configure_widget(self.create_widget(tk.Button(self.app, text="Clear", command=lambda: clear_text_widget()), 0, 0.8, 0.25, 0.05), font=font)

        def reverse_theme():
            if self.label_for_lighting_button.get() == "black":
                self.label_for_lighting_button.set("white")
            else:
                self.label_for_lighting_button.set("black")
            self.terminal_need_break = True
            self.terminal()

        self.configure_widget(self.create_widget(tk.Button(self.app, text=self.label_for_lighting_button.get(), command=lambda: reverse_theme()), 0.25, 0.8, 0.25, 0.05), font=font)

        ####

        self.configure_widget(self.create_widget(tk.Entry(self.app, textvariable=self.contain_of_entry_for_text_widget), 0, 0.85, 1, 0.05), font=font)

        self.configure_widget(self.create_widget(tk.Button(self.app, text="Send", command=lambda: complet_panel()), 0, 0.9, 1, 0.1), font=font)
        self.app.bind("<Return>", lambda event: complet_panel())

        self.place_all_widgets()

        self.app.bind("<Configure>", lambda event: self.place_all_widgets())

        self.terminal_need_break = False

if __name__ == "__main__":
    app = App()
    app.run()
