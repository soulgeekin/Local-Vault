# Local Vault

This is a password tool that works on your own machine. There is no user account. There is no cloud. There is no syncing. Your data stays on your computer.

## Features

- Works offline. Nothing is sent out.
- You set a master password the first time you open it.
- After that, you sign in using the same master password each time.
- The master password is salted and hashed. It is not kept in plain text.
- The encryption key is not saved as a file. It is created again each login from your master password. PBKDF2 is used with a high iteration count, so there is no extra key to steal.
- Saved passwords are encrypted with Fernet.
- You can add, open, copy, and remove saved logins.
- A copy button lets you get a password without showing it on the screen.
- There is a dark and light mode switch.

## How to run

Install the needed packages:

```
pip install customtkinter cryptography
```

Then start the app:

```
python gui.py
```

On the first run, you will be asked to set a master password. Next times are simple. You just log in with that same password.

## What files are included

- `gui.py` for the app window and controls
- `vault.py` for the encryption, hashing, and storage parts
- `master.hash` holds the salted and hashed master password. It is made automatically and is ignored by git
- `vault.json` holds the encrypted saved entries. It is made automatically and is ignored by git

## Quick note

This began as a personal project for learning. I wanted to understand password managers by building one. I have not taken it through a full polish pass yet.