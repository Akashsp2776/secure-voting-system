import hashlib
import json
import os
import getpass  # To hide password input

USERS_FILE = 'users.json'
VOTES_FILE = 'votes.json'
CANDIDATES = ['Alice', 'Bob', 'Charlie']

# --- Helper Functions ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_data(file, default):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump(default, f)
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# --- Core Functions ---
def register():
    users = load_data(USERS_FILE, {})
    username = input("Enter new username: ")
    if username in users:
        print("Username already exists.")
        return
    password = getpass.getpass("Enter new password: ")
    users[username] = {
        'password': hash_password(password),
        'voted': False
    }
    save_data(USERS_FILE, users)
    print("Registration successful.\n")

def login():
    users = load_data(USERS_FILE, {})
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    if username in users and users[username]['password'] == hash_password(password):
        print("Login successful.\n")
        if username.lower() == "admin":
            admin_panel()
        else:
            vote_panel(username)
    else:
        print("Invalid credentials.\n")

def vote_panel(username):
    users = load_data(USERS_FILE, {})
    if users[username]['voted']:
        print("You have already voted.\n")
        return
    print("\nCandidates:")
    for i, name in enumerate(CANDIDATES, 1):
        print(f"{i}. {name}")
    try:
        choice = int(input("Enter your choice (1-3): "))
        if choice not in range(1, len(CANDIDATES) + 1):
            print("Invalid choice.\n")
            return
    except ValueError:
        print("Invalid input. Please enter a number.\n")
        return

    votes = load_data(VOTES_FILE, {name: 0 for name in CANDIDATES})
    selected_candidate = CANDIDATES[choice - 1]
    votes[selected_candidate] += 1
    save_data(VOTES_FILE, votes)

    users[username]['voted'] = True
    save_data(USERS_FILE, users)
    print("Vote recorded successfully.\n")

def admin_panel():
    votes = load_data(VOTES_FILE, {name: 0 for name in CANDIDATES})
    print("\n--- Voting Results ---")
    for candidate, count in votes.items():
        print(f"{candidate}: {count} votes")
    print()

# --- Main Menu ---
def main():
    print("==== Secure Voting System ====")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")

# Fixed the error in the condition below
if __name__ == "__main__":
    main()
