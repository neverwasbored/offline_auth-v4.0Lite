import time
import tkinter as tk
from tkinter import ttk

import pyotp
import pyperclip

from core.utils import JsonData


class App(tk.Tk):
    def __init__(self, json_data: JsonData):
        super().__init__()
        self.json_data = json_data

        self.title('HHTNQ AUTH')
        self.iconbitmap('img/logo.ico')
        self.minsize(350, 400)
        self.maxsize(350, 400)
        self['background'] = '#333333'
        self.conf = {'padx': 10, 'pady': 10}
        self.bold_font = 'Inter 16'
        self.anchor = 'center'
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.put_frames()

    def put_frames(self):
        self.top_frame = TopFrame(self)
        self.mid_frame = MidFrame(self)
        self.bot_frame = BotFrame(self)

        self.top_frame.grid(row=0, column=0, sticky='nwe', pady=(15, 0))
        self.mid_frame.grid(row=1, column=0, sticky='nswe', pady=50)
        self.bot_frame.grid(row=3, column=0, sticky='swe')


class TopFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.put_widgets()

    def put_widgets(self):
        self.name = ttk.Label(self, text='HHTNQ',
                              background=self.master['background'], foreground='white', font=self.master.bold_font, anchor='center')

        self.name.grid(row=0, column=0, sticky='nwe')


class MidFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = '#444444'
        self.foreground = 'white'
        self.bold_font = 'Inter 12'
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.put_widgets()
        self.current_key = None
        self.after_id = None

    def put_widgets(self):
        self.input_label = ttk.Label(
            self, text='Search by email', font=self.bold_font, background=self['background'], foreground=self.foreground, anchor=self.master.anchor)
        self.input_data = ttk.Entry(
            self, width=30, font='Inter 8', background=self['background'])
        self.input_data.bind(
            '<KeyRelease>', lambda event: self.search(event, self.master.json_data.data, self.input_data.get()))
        self.info_label = ttk.Label(self, text='Write your email', font=self.bold_font,
                                    background=self['background'], foreground=self.foreground, anchor=self.master.anchor)
        self.code_static_label = ttk.Label(
            self, text='Code:', font=self.bold_font, background=self['background'], foreground=self.foreground, anchor=self.master.anchor)
        self.code_dynamic_label = ttk.Label(
            self, text='', font=self.bold_font, background=self['background'], foreground=self.foreground, anchor=self.master.anchor)
        self.remaining_time_label = ttk.Label(
            self, text='', font=self.bold_font, background=self['background'], foreground=self.foreground, anchor=self.master.anchor)
        self.copy_btn = tk.Button(
            self, text='Copy to clipboard', cursor='hand2', command=self.copy, anchor=self.master.anchor)
        self.empty_column = ttk.Label(
            self, anchor=self.master.anchor, background=self['background'])

        self.input_label.grid(
            row=0, column=1, cnf=self.master.conf, sticky='n')
        self.input_data.grid(
            row=1, column=1, cnf=self.master.conf, sticky='n')
        self.empty_column.grid(
            row=1, column=2, cnf=self.master.conf, sticky='ne', padx=(0, 60))
        self.info_label.grid(
            row=2, column=1, cnf=self.master.conf, sticky='n')
        self.code_static_label.grid(
            row=3, column=0, cnf=self.master.conf, sticky='nw')
        self.code_dynamic_label.grid(
            row=3, column=1, cnf=self.master.conf, sticky='n')
        self.remaining_time_label.grid(
            row=3, column=2, cnf=self.master.conf, sticky='ne')
        self.copy_btn.grid(row=4, column=1, cnf=self.master.conf, sticky='n')

    def search(self, event, json_data: list, input_data: str):
        name = None
        key = None

        if input_data == '':
            if self.after_id != None:
                self.after_cancel(self.after_id)
                self.after_id = None
            self.current_key = None
            self.info_label.configure(text='Write your email')
            self.code_dynamic_label.configure(text='')
            self.remaining_time_label.configure(text='')
            return

        for elem in json_data:
            if input_data.lower().strip() in elem['name'].lower().strip()[0: len(input_data)]:
                name = elem['name']
                key = elem['key']
                break

        if name and key:
            self.info_label.configure(text=name)
            if key != self.current_key:
                self.current_key = key
                if self.after_id is not None:
                    self.after_cancel(self.after_id)
                self.update_func()
        else:
            self.current_key = None
            self.info_label.configure(text='Not found')
            self.code_dynamic_label.configure(text='')
            self.remaining_time_label.configure(text='')

    def update_func(self):
        if not self.current_key:
            return
        totp = pyotp.TOTP(self.current_key)
        authy_code = totp.now()
        remaining_time = round(
            totp.interval - (time.time() % totp.interval))
        self.code_dynamic_label.configure(text=authy_code)
        self.remaining_time_label.configure(text=remaining_time)
        self.after_id = self.after(1000, self.update_func)

    def copy(self):
        if self.code_dynamic_label.cget('text') != '':
            pyperclip.copy(self.code_dynamic_label.cget('text'))
            self.copy_btn.configure(
                background='#39ff00', state='disabled')
            self.after(1000, self.restore_button_state)

    def restore_button_state(self):
        self.copy_btn.configure(
            background='white', state='active')


class BotFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.foreground = 'white'
        self.bold_font = 'Inter 10'
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.put_widgets()

    def put_widgets(self):
        self.data_name_label = ttk.Label(
            self, text=self.master.json_data.name, background=self['background'], foreground=self.foreground, font=self.bold_font, anchor=self.master.anchor)
        self.version_label = ttk.Label(
            self, text='version 4.0L', background=self['background'], foreground=self.foreground, font=self.bold_font, anchor=self.master.anchor)

        self.data_name_label.grid(
            row=1, column=0, sticky='sw', cnf=self.master.conf)
        self.version_label.grid(
            row=1, column=2, sticky='se', cnf=self.master.conf)
