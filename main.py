#!/usr/bin/env python
import sys
from tkinter import *
from tkinter import messagebox
import webbrowser
from make_list import make_list, NoDefinition
from quizlet import post_to_quizlet, oauth, get_quizlet_bearer_token

class QuizletWorder:
    def __init__(self):
        self.word_count = 10
        self.word_entry = []

        self.root = Tk()
        self.root_height = self.word_count*27+120

        self.clist = None
        self.new_term = None

        self.title_var = StringVar()
        self.term_count_var = StringVar()

    def on_submit(self):
        uri = None
        code_var = StringVar()

        wordlist = []
        for entry in self.word_entry:
            wordlist.append(entry[1].get())

        try:
            proc_wordlist = make_list(wordlist)
        except Exception as e:
            print(e)
            return

        auth_window = Toplevel(self.root)
        auth_window.wm_title('Auth')

        def on_ok():
            code = code_var.get()
            token = get_quizlet_bearer_token(code, uri)

            post_res = post_to_quizlet(self.title_var.get(), proc_wordlist[0], proc_wordlist[1], token)
            set_url = post_res['url']

            messagebox.showinfo(title="Success!", message=f"The Quizlet set has been made! {set_url}")
            webbrowser.open(set_url)
            sys.exit()

        def on_proceed():
            uri = oauth()

            label = Label(master=auth_window, text='Enter Auth Code Here:')
            label.grid(row=2, column=0, pady=10)

            code_entry = Entry(master=auth_window, textvariable=code_var)
            code_entry.grid(row=3, column=0)

            ok = Button(master=auth_window, text='OK', command=on_ok)
            ok.grid(row=4, column=0)

        label = Label(master=auth_window,\
        text='Quizlet will now authorize us to be able\n'+\
            ' to access your account.\n' +\
            'After pressing "Proceed", a browser tab\n'+\
            ' will open; the Quizlet authorization page.'+\
            '\n After authorizing us, you will be\n'+\
            ' redirected to a website giving you a code.'+\
            ' \nYou will need to paste that code into the \n'+\
            'text box below and hit "OK".')
        label.grid(row=0, column=0)

        proceed = Button(master=auth_window, text='Proceed', command=on_proceed)
        proceed.grid(row=1, column=0)

    def term_count(self):
        term_count = Toplevel(self.root)
        term_count.resizable(False, False)
        term_count.geometry("200x100")

        def confirm_term_count():
            self.word_count = int(self.term_count_var.get())
            term_count.destroy()

        term_count_label = Label(term_count, text="Number of Terms:")
        term_count_label.pack()
        term_count_entry = Entry(term_count, textvariable=self.term_count_var)
        term_count_entry.pack()
        term_count_confirm = Button(term_count, text="Confirm", command=confirm_term_count)
        term_count_confirm.pack()

    def add_term(self):
        self.word_count += 1

        text_var = StringVar()
        word_input = Entry(self.root, textvariable=text_var)
        word_input.grid(row=self.word_count+3, column=0, padx=22, pady=3)

        self.word_entry.append((word_input, text_var))
        
        self.clist.grid(row=self.word_count+5, column=0)
        self.new_term.grid(row=self.word_count+6, column=0)

        self.root_height = self.word_count*27+120
        self.root.geometry(f'175x{str(self.root_height)}')
        self.root.update()


    def load_window(self):
        title_label = Label(self.root, text="Title of Set:")
        title_label.grid(row=0, column=0)

        title = Entry(self.root, textvariable=self.title_var)
        title.grid(row=1, column=0)

        terms_label = Label(self.root, text="Terms:")
        terms_label.grid(row=2, column=0)

        for word in range(self.word_count):
            text_var = StringVar()
            word_input = Entry(self.root, textvariable=text_var)

            word_input.grid(row=word+3, column=0, padx=22, pady=3)
            self.word_entry.append((word_input, text_var))

        self.clist = Button(self.root, text='Make Quizlet List!', command=self.on_submit)
        self.clist.grid(row=self.word_count+3, column=0, padx=22, pady=3)

        self.new_term = Button(self.root, text='Add Another Term', command=self.add_term)
        self.new_term.grid(row=self.word_count+4, column=0, padx=22, pady=3)

        self.root.title('QW')
        self.root.geometry(f"175x{str(self.root_height)}")
        self.root.resizable(False, False)

    def run(self):
        self.load_window()
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror(title="Error", message=f"{str(e)}")
            sys.exit()

QW = QuizletWorder()
QW.run()