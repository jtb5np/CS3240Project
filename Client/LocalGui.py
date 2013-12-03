__author__ = 'Jacob'

from Tkinter import *


class LocalGui():
    def __init__(self, l, f, u, p):
        self.control = ''
        self.other_user = ''
        self.on = True
        self.lch = l
        self.fwr = f
        self.user_id = u
        self.password = p
        self.master = Tk()
        self.master.wm_minsize(280, 180)
        self.master.configure(background="#e5eaff")
        self.label_text = StringVar()
        self.entry_text = ''
        self.label_text.set("Please make a selection.")
        self.l = Label(self.master, textvariable=self.label_text, background="#e5eaff")
        self.e = Entry(self.master)
        self.l.grid(row=0, column=0, sticky=W+E, columnspan=2)
        self.e.grid(row=1, column=0, padx=3)

        self.e.focus_set()

        self.b_enter = Button(self.master, text="Enter", command=self.entertext, fg="#760000", bg="#f1faf1")
        self.b = Button(self.master, text="Change Password", command=self.changepass, fg="#760000", bg="#f1faf1")
        self.b2 = Button(self.master, text="Turn off Synchronization", command=self.signout, fg="#760000", bg="#f1faf1")
        self.b3 = Button(self.master, text="Share Files", command=self.share, fg="#760000", bg="#f1faf1")
        self.b4 = Button(self.master, text="Sign Out and Exit", command=self.finish, fg="#760000", bg="#f1faf1")
        self.b5 = Button(self.master, text="Close GUI (keep sync on)", command=self.finish_without_stopping,
                         fg="#760000", bg="#f1faf1")
        self.b_enter.grid(row=1, column=1, sticky=W, padx=4)
        self.b.grid(row=2, column=0, pady=5)
        self.b2.grid(row=2, column=1, pady=5)
        self.b3.grid(row=3, column=0, pady=5)
        self.b5.grid(row=3, column=1, pady=5)
        self.b4.grid(row=4, column=1, pady=10)

        mainloop()

    def entertext(self):
        if self.control == 'password':
            password = self.e.get()
            if self.lch.change_password(password):
                print "Password changed to: " + password
            else:
                print "ERROR: password unchanged. Please make sure that you are logged in"
            self.control = ''
            self.label_text.set("Please make a selection.")
        elif self.control == 'signout':
            response = self.e.get()
            if response == 'on':
                if self.lch.sign_in(self.user_id, self.password):
                    print 'sign in successful'
                    self.control = ''
                    self.label_text.set("Please make a selection.")
        elif self.control == 'share':
            self.other_user = self.e.get()
            self.label_text.set("Enter the file/folder you want to share.")
            self.control = 'share2'
        elif self.control == 'share2':
            filename = self.e.get()
            if self.lch.share_file(filename, self.other_user):
                print 'File successfully shared.'
            else:
                print 'File share unsuccessful.'
            self.control = ''
            self.label_text.set("Please make a selection.")

    def changepass(self):
        self.label_text.set("Input your new password.")
        self.control = 'password'

    def signout(self):
        if self.lch.sign_out():
            print "Sign out successful"
            self.label_text.set("Enter 'on' to turn synchronization back on.")
            self.control = 'signout'

    def share(self):
        self.label_text.set("Enter the name of the user you're sharing with.")
        self.control = 'share'

    def finish(self):
        if self.lch.sign_out():
            print "User signed out"
            self.exit_client()
            self.master.destroy()
        else:
            print "ERROR: Sign out unsuccessful"

    def finish_without_stopping(self):
        self.on = False
        self.master.destroy()

    def exit_client(self):
        if self.lch is not None:
            self.lch._Thread__stop()
        if self.fwr is not None:
            self.fwr._Thread__stop()
        print "Exited."
        sys.exit(0)