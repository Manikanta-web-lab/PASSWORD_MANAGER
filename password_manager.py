import os
import json
import hashlib
import getpass
import random
import string
import datetime
import base64

DATA_FILE = 'passwords.json'

def hash_password(password: str) -> str:
    """Returns the SHA-256 hash of the given password."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def simple_encrypt(key_hash: str, text: str) -> str:
    """Basic encryption using XOR with the master password hash and base64 encoding."""
    key_bytes = key_hash.encode('utf-8')
    text_bytes = text.encode('utf-8')
    
    # Simple XOR cipher for demonstration purposes
    encrypted_bytes = bytearray()
    for i in range(len(text_bytes)):
        encrypted_bytes.append(text_bytes[i] ^ key_bytes[i % len(key_bytes)])
        
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def simple_decrypt(key_hash: str, encrypted_text: str) -> str:
    """Basic decryption using XOR with the master password hash and base64 decoding."""
    key_bytes = key_hash.encode('utf-8')
    encrypted_bytes = base64.b64decode(encrypted_text.encode('utf-8'))
    
    decrypted_bytes = bytearray()
    for i in range(len(encrypted_bytes)):
        decrypted_bytes.append(encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)])
        
    return decrypted_bytes.decode('utf-8')

def load_data() -> dict:
    """Loads the password data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data: dict):
    """Saves the password data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def setup() -> str:
    """Sets up the master password on first run."""
    print("\n--- Password Manager Setup ---")
    while True:
        master_pw = getpass.getpass("Create a Master Password: ")
        confirm_pw = getpass.getpass("Confirm Master Password: ")
        if master_pw == confirm_pw and len(master_pw) > 0:
            break
        print("Passwords do not match or are empty. Please try again.")
    
    data = {"master_hash": hash_password(master_pw), "accounts": []}
    save_data(data)
    print("Master password set successfully!")
    return data["master_hash"]

def login() -> str:
    """Handles user login with a maximum of 3 attempts."""
    data = load_data()
    stored_hash = data.get("master_hash")
    
    attempts = 3
    while attempts > 0:
        entered_pw = getpass.getpass(f"Enter Master Password ({attempts} attempts left): ")
        entered_hash = hash_password(entered_pw)
        
        if entered_hash == stored_hash:
            print("Login successful!\n")
            return entered_hash
        else:
            attempts -= 1
            print("Incorrect password.")
            
    print("Maximum login attempts reached. Locking out.")
    return ""

def generate_password() -> str:
    """Generates a strong random password based on user preferences."""
    print("\n--- Password Generator ---")
    while True:
        try:
            length = int(input("Enter desired length (e.g., 12): "))
            if length < 4:
                print("Password should be at least 4 characters long.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    use_lower = input("Include lowercase letters? (y/n): ").strip().lower() == 'y'
    use_upper = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
    use_digits = input("Include digits? (y/n): ").strip().lower() == 'y'
    use_special = input("Include special characters? (y/n): ").strip().lower() == 'y'
    
    chars = ""
    if use_lower: chars += string.ascii_lowercase
    if use_upper: chars += string.ascii_uppercase
    if use_digits: chars += string.digits
    if use_special: chars += string.punctuation
    
    if not chars:
        print("No character types selected. Using all types by default.")
        chars = string.ascii_letters + string.digits + string.punctuation
        
    password = ''.join(random.choice(chars) for _ in range(length))
    print(f"Generated Password: {password}")
    return password

def add_password(key_hash: str, data: dict):
    """Adds a new account and encrypts the password."""
    print("\n--- Add New Password ---")
    website = input("Website/App Name: ")
    username = input("Username/Email: ")
    
    choice = input("Do you want to (G)enerate a password or (E)nter one manually? (g/e): ").strip().lower()
    if choice == 'g':
        password = generate_password()
    else:
        password = getpass.getpass("Enter Password: ")
        
    encrypted_pw = simple_encrypt(key_hash, password)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_entry = {
        "website": website,
        "username": username,
        "password": encrypted_pw,
        "timestamp": timestamp
    }
    
    data.setdefault("accounts", []).append(new_entry)
    save_data(data)
    print("Password saved successfully!")

def view_passwords(key_hash: str, data: dict):
    """Displays all saved accounts."""
    print("\n--- Saved Passwords ---")
    accounts = data.get("accounts", [])
    if not accounts:
        print("No passwords saved yet.")
        return
        
    for idx, acc in enumerate(accounts, start=1):
        decrypted_pw = simple_decrypt(key_hash, acc['password'])
        print(f"[{idx}] {acc['website']}")
        print(f"    Username: {acc['username']}")
        print(f"    Password: {decrypted_pw}")
        print(f"    Saved On: {acc['timestamp']}")
        print("-" * 25)

def search_passwords(key_hash: str, data: dict):
    """Searches for a specific account by website or username."""
    print("\n--- Search Passwords ---")
    query = input("Enter website or username to search: ").strip().lower()
    
    accounts = data.get("accounts", [])
    found = False
    
    for acc in accounts:
        if query in acc['website'].lower() or query in acc['username'].lower():
            decrypted_pw = simple_decrypt(key_hash, acc['password'])
            print(f"\nWebsite:  {acc['website']}")
            print(f"Username: {acc['username']}")
            print(f"Password: {decrypted_pw}")
            print(f"Saved On: {acc['timestamp']}")
            found = True
            
    if not found:
        print("No matching accounts found.")

def delete_password(data: dict):
    """Deletes an account by website name."""
    print("\n--- Delete Password ---")
    website_to_delete = input("Enter the website of the account to delete: ").strip()
    
    accounts = data.get("accounts", [])
    initial_count = len(accounts)
    
    data["accounts"] = [acc for acc in accounts if acc['website'].lower() != website_to_delete.lower()]
    
    if len(data["accounts"]) < initial_count:
        save_data(data)
        print(f"Successfully deleted account(s) for '{website_to_delete}'.")
    else:
        print(f"No account found for '{website_to_delete}'.")

def main():
    print("\n==================================")
    print("    Python CLI Password Manager       ")
    print("==================================")
    
    data = load_data()
    
    if not data or "master_hash" not in data:
        key_hash = setup()
        data = load_data()
    else:
        key_hash = login()
        if not key_hash:
            return  # Exit due to lockout
            
    while True:
        print("\n=== Main Menu ===")
        print("1. Add new password")
        print("2. View saved passwords")
        print("3. Search passwords")
        print("4. Delete password")
        print("5. Generate a password (tool)")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            add_password(key_hash, data)
        elif choice == '2':
            view_passwords(key_hash, data)
        elif choice == '3':
            search_passwords(key_hash, data)
        elif choice == '4':
            delete_password(data)
        elif choice == '5':
            generate_password()
        elif choice == '6':
            print("Exiting securely... Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()
