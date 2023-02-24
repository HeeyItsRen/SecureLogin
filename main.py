import customtkinter
import socket
import tkinter
import sqlite3
import hashlib

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999)) 
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")
count = 0

def register_handler():
    root.withdraw()
    global pop
    pop = customtkinter.CTkToplevel()
    pop.geometry("500x350")
    rframe = customtkinter.CTkFrame(master=pop)
    rframe.pack(padx=60, pady=20, fill="both", expand=True)
    
    label = customtkinter.CTkLabel(master=rframe, text="Register New Account", font=("Roboto", 24))
    label.pack(padx=10, pady=12)

    regUsername = customtkinter.CTkEntry(master=rframe, placeholder_text="Username")
    regUsername.pack(padx=10, pady=12)

    regPassword = customtkinter.CTkEntry(master=rframe, placeholder_text="Password", show="*")
    regPassword.pack(padx=10, pady=12)

    button2 = customtkinter.CTkButton(master=rframe, text="Register", command= lambda: register(regUsername.get(), regPassword.get()))
    button2.pack(padx=20, pady=20)
    
    pop.protocol("WM_DELETE_WINDOW", exit_pop)
    def register(username, password):
        global count
        msg = ""
        if username and password is not None:
            client.send("Register".encode())
            print(client.recv(1024).decode()) # Requesting username
            client.send(username.encode())
            print(client.recv(1024).decode()) # username received requesting password
            client.send(password.encode())
            print(client.recv(1024).decode()) # password received
            msg = client.recv(1024).decode()
        else:
            tkinter.messagebox.showinfo("Hospital System v1.0", "Username and Password are Required!")
            
        if msg != "":    
            if msg == "Registration Successful":
                regiSuccessLabel = customtkinter.CTkLabel(master=frame, text="Registration Sucessful", font=("Roboto", 24))
                regiSuccessLabel.pack(padx=10, pady=12)
                tkinter.messagebox.showinfo("Hospital System v1.0", "Registration Sucessful")
                root.deiconify()
                pop.withdraw()
                count = 0
            elif count < 1:
                button2 = customtkinter.CTkButton(master=rframe, text="Login?", command=lambda:[root.deiconify(), pop.withdraw()])
                button2.pack()
                dupeUsernameLabel = customtkinter.CTkLabel(master=rframe, text="Username already exists!", font=("Roboto", 24))
                dupeUsernameLabel.pack(padx=10, pady=12)
                count += 1
            
            
def login(username, password):
    msg = ""
    if username and password is not None:
        client.send("Login".encode())
        print(client.recv(1024))
        client.send((username).encode())
        print(client.recv(1024))
        client.send((password).encode())
        msg = client.recv(1024).decode()
    else:
        tkinter.messagebox.showinfo("Hospital System v1.0", "Username and Password are Required!")
    
    if msg != "":    
        if msg == "Login Successful":
            root.destroy()
            hp = customtkinter.CTk()
            hp.geometry("1280x720")
            hp.title('Hospital System v1.0')
            l1=customtkinter.CTkLabel(master=hp, text="Home Page",font=('Century Gothic',60))
            l1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            hp.mainloop()
        else:
            tkinter.messagebox.showinfo("Hospital System v1.0", "Username or Password is Incorrect!")
        
def exit_pop():
    pop.destroy()
    
def exit_app():
    root.destroy()
        
def main():
    global frame
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(padx=60, pady=20, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="Login System v1.0", font=("Roboto", 24))
    label.pack(padx=10, pady=12)

    entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
    entry1.pack(padx=10, pady=12)

    entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
    entry2.pack(padx=10, pady=12)

    button = customtkinter.CTkButton(master=frame, text="Login", command= lambda: login(entry1.get(), entry2.get()))
    button.pack(padx=10, pady=12)
    button2 = customtkinter.CTkButton(master=frame, text="Register", command=register_handler)
    button2.pack(padx=10, pady=12)

    checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember me")
    checkbox.pack(padx=10, pady=12)

    root.protocol("WM_DELETE_WINDOW", exit_app)
    root.mainloop()
    
if __name__ == "__main__":
    main()