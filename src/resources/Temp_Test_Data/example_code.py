def test_connection(username, password):
    try:
        # Replace with your actual Oracle DB connection details
        dsn = "your_host:your_port/your_service_name"
        connection = oracledb.connect(user=username, password=password, dsn=dsn)
        connection.close()
        messagebox.showinfo("Connection Test", "Connection successful!")
        return True
    except oracledb.Error as error:
        messagebox.showerror("Connection Test", f"Connection failed: {error}")
        return False

def show_login_window():
    def on_submit():
        nonlocal username, password
        username = entry_username.get()
        password = entry_password.get()
        if test_connection(username, password):
            login_window.destroy()

    def on_test_connection():
        username = entry_username.get()
        password = entry_password.get()
        test_connection(username, password)

    login_window = ctk.CTk()
    login_window.title("Login")
    login_window.geometry("400x300")

    ctk.CTkLabel(login_window, text="Login", font=("Arial", 24)).pack(pady=20)

    ctk.CTkLabel(login_window, text="Username").pack(pady=5)
    entry_username = ctk.CTkEntry(login_window)
    entry_username.pack(pady=5)

    ctk.CTkLabel(login_window, text="Password").pack(pady=5)
    entry_password = ctk.CTkEntry(login_window, show="*")
    entry_password.pack(pady=5)

    ctk.CTkButton(login_window, text="Test Connection", command=on_test_connection).pack(pady=5)
    ctk.CTkButton(login_window, text="Submit", command=on_submit).pack(pady=20)

    username = None
    password = None
    login_window.mainloop()

    return username, password