# Local Vault

Local Vault is a local, offline password manager built with Python. Your data stays on your computer—there’s no cloud storage, account system, or syncing with external servers. Saved passwords are encrypted, and access to the vault is protected by a salted and hashed master password.

## Features

- Works completely offline
- Encrypts saved passwords using Fernet
- Protects the master password with salting and hashing
- Add, view, copy, and delete saved passwords
- Copy passwords to your clipboard without displaying them
- Switch between dark and light mode

## Running the App

Install the required packages:

```bash
pip install customtkinter cryptography
```

Then start the application:

```bash
python gui.py
```

When you open Local Vault for the first time, you’ll be asked to create a master password. On future launches, you’ll use that password to unlock your vault.

## Project Files

- `gui.py` — Handles the application interface
- `vault.py` — Manages encryption, storage, and vault operations
- `key.key` — The encryption key created by the application
- `master.hash` — The hashed master password
- `vault.json` — Stores the encrypted password data

The last three files are generated automatically and are excluded from Git because they contain your actual key and vault data.

## Important Note

Local Vault began as a personal project for learning more about encryption, password storage, and GUI development. It uses real encryption and does not store the master password in plain text, but it has not been professionally audited or extensively tested.

It works well as an offline learning project and may be suitable for basic personal use, but you should avoid relying on it for your most important accounts until it has gone through more testing and security review.