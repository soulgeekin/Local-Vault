import customtkinter as ctk
from vault import load_vault, add_password, get_password, save_vault
from vault import is_first_launch, check_master_password, create_master_password

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x300")
app.title("Local Vault")


def open_vault_window():
    app.withdraw()
    vault_win = ctk.CTkToplevel()
    vault_win.geometry("500x550")
    vault_win.title("Local Vault — Unlocked")

    top_bar = ctk.CTkFrame(vault_win, fg_color="transparent")
    top_bar.pack(pady=10, fill="x", padx=15)

    title = ctk.CTkLabel(top_bar, text="Your Vault", font=("Arial", 18, "bold"))
    title.pack(side="left")

    def toggle_theme():
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if current == "Dark" else "dark")

    theme_button = ctk.CTkButton(top_bar, text="Theme", width=60, command=toggle_theme)
    theme_button.pack(side="right")

    site_list_frame = ctk.CTkScrollableFrame(vault_win, height=250)
    site_list_frame.pack(pady=10, padx=15, fill="both", expand=True)

    def copy_to_clipboard(text):
        vault_win.clipboard_clear()
        vault_win.clipboard_append(text)

    def delete_site(site):
        data = load_vault()
        if site in data:
            del data[site]
            save_vault(data)
        refresh_site_list()

    def refresh_site_list():
        for widget in site_list_frame.winfo_children():
            widget.destroy()

        data = load_vault()
        if not data:
            empty_label = ctk.CTkLabel(site_list_frame, text="No saved passwords yet.")
            empty_label.pack(pady=10)
            return

        for site in data.keys():
            row = ctk.CTkFrame(site_list_frame)
            row.pack(pady=5, fill="x")

            site_label = ctk.CTkLabel(row, text=site, width=120, anchor="w")
            site_label.pack(side="left", padx=10)

            pw_label = ctk.CTkLabel(row, text="********", width=100)
            pw_label.pack(side="left", padx=5)

            def make_reveal(s=site, lbl=pw_label):
                def reveal():
                    if lbl.cget("text") == "********":
                        real_pw = get_password(s)
                        lbl.configure(text=real_pw)
                    else:
                        lbl.configure(text="********")
                return reveal

            reveal_btn = ctk.CTkButton(row, text="Show", width=50, command=make_reveal())
            reveal_btn.pack(side="left", padx=3)

            def make_copy(s=site):
                def copy():
                    real_pw = get_password(s)
                    copy_to_clipboard(real_pw)
                return copy

            copy_btn = ctk.CTkButton(row, text="Copy", width=50, command=make_copy())
            copy_btn.pack(side="left", padx=3)

            def make_delete(s=site):
                def delete():
                    delete_site(s)
                return delete

            delete_btn = ctk.CTkButton(row, text="Delete", width=60, fg_color="darkred",
                                        hover_color="red", command=make_delete())
            delete_btn.pack(side="left", padx=3)

    refresh_site_list()

    add_frame = ctk.CTkFrame(vault_win)
    add_frame.pack(pady=10, padx=15, fill="x")

    new_site_entry = ctk.CTkEntry(add_frame, placeholder_text="Site name")
    new_site_entry.pack(pady=5, padx=10, fill="x")

    new_pass_entry = ctk.CTkEntry(add_frame, placeholder_text="Password", show="*")
    new_pass_entry.pack(pady=5, padx=10, fill="x")

    def save_new_entry():
        site = new_site_entry.get()
        pw = new_pass_entry.get()
        if site and pw:
            add_password(site, pw)
            new_site_entry.delete(0, "end")
            new_pass_entry.delete(0, "end")
            refresh_site_list()

    save_button = ctk.CTkButton(add_frame, text="Add Password", command=save_new_entry)
    save_button.pack(pady=10)


def show_login_screen():
    title_label = ctk.CTkLabel(app, text="Local Vault", font=("Arial", 24, "bold"))
    title_label.pack(pady=(30, 10))

    sub_label = ctk.CTkLabel(app, text="Enter master password")
    sub_label.pack(pady=(0, 10))

    password_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=220)
    password_entry.pack(pady=10)

    status_label = ctk.CTkLabel(app, text="")

    def check_password():
        tried_pass = password_entry.get()
        if check_master_password(tried_pass):
            status_label.configure(text="Unlocked!", text_color="green")
            open_vault_window()
        else:
            status_label.configure(text="Wrong Password", text_color="red")

    unlock_btn = ctk.CTkButton(app, text="Unlock", command=check_password, width=220)
    unlock_btn.pack(pady=10)

    status_label.pack(pady=10)


if is_first_launch():
    # create a master password (only shown the very first time) 

    title_label = ctk.CTkLabel(app, text="Local Vault", font=("Arial", 24, "bold"))
    title_label.pack(pady=(30, 10))

    sub_label = ctk.CTkLabel(app, text="Create your master password")
    sub_label.pack(pady=(0, 10))

    new_master_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=220)
    new_master_entry.pack(pady=5)

    confirm_entry = ctk.CTkEntry(app, placeholder_text="Confirm password", show="*", width=220)
    confirm_entry.pack(pady=5)

    setup_status_label = ctk.CTkLabel(app, text="")
    setup_status_label.pack(pady=10)

    def save_master_pass():
        pw1 = new_master_entry.get()
        pw2 = confirm_entry.get()
        if pw1 == "" or pw2 == "":
            setup_status_label.configure(text="Fields can't be empty.", text_color="red")
        elif pw1 != pw2:
            setup_status_label.configure(text="Passwords don't match.", text_color="red")
        else:
            create_master_password(pw1)
            for widget in app.winfo_children():
                widget.destroy()
            show_login_screen()

    confirm_btn = ctk.CTkButton(app, text="Create Password", width=220, command=save_master_pass)
    confirm_btn.pack(pady=10)

else:
    # normal login (shown every time after the first)
    show_login_screen()

app.mainloop()