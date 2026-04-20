# Python CLI Password Manager

A lightweight, fully functional Command Line Interface (CLI) Password Manager built entirely with Python's built-in libraries. This tool allows you to securely store, retrieve, and manage your website passwords locally on your machine without relying on external databases or third-party web frameworks.

## Features

- **Master Password Authentication**: Secures your vault with a master password hashed using SHA-256.
- **Local Encrypted Storage**: All your passwords and account data are saved to a local `passwords.json` file. Your saved passwords are automatically encrypted via a custom XOR cipher and Base64 encoded.
- **Hidden Inputs**: Keystrokes for typing sensitive passwords are hidden from the console.
- **Secure Password Generator**: Interactively generate highly customizable, strong random passwords.
- **Search & Filtering**: Easily search through your saved credentials by website name or username.
- **Lockout Mechanism**: Prevents brute-forcing by locking the console after 3 failed login attempts.

## Prerequisites

- **Python 3.x**: Since this script uses only standard libraries (`os`, `json`, `hashlib`, `getpass`, `random`, `string`, `datetime`, `base64`), you do not need to install any external dependencies with `pip`.

## How to Run

1. Open your terminal application (Command Prompt or PowerShell on Windows).
2. Navigate to the project directory:
   ```powershell
   cd "c:\Users\dell\Desktop\password manager"
   ```
3. Run the script:
   ```powershell
   python password_manager.py
   ```

## Usage Guide

1. **First-time Setup**: The first time you launch the program, it will ask you to create and confirm a Master Password. **Do not forget this password**, as it serves as the key to encrypt and decipher your vault.
2. **Main Menu**: Upon successful login, you will be presented with a numbered menu:
   - `[1] Add new password`: Enter a website name and username. You can choose to either type your own password or have the tool generate a safe one for you.
   - `[2] View saved passwords`: Displays a formatted list of all your decrypted accounts.
   - `[3] Search passwords`: Type a keyword to quickly find specific account credentials.
   - `[4] Delete password`: Type the exact name of a saved website to wipe its entry from your vault.
   - `[5] Generate a password`: A standalone utility to generate a secure string based on parameters (length, symbols, numbers, etc.) you define.
   - `[6] Exit`: Securely shuts down the program.

## Security Note

All data is stored directly in `passwords.json` in the same directory as the script. Ensure this folder is kept somewhere safe on your machine.
