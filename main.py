# Online Quiz System (OOP + JSON + Basic Python)
# Refactored to use a list of user and course dictionaries

import json
from datetime import datetime

USERS_FILE = 'users.json'
COURSES_FILE = 'courses.json'

# ---------------------------- Helper Functions ----------------------------
def load_data(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

# ---------------------------- User Class ----------------------------
class User:
    def __init__(self, username, email, password, birth_year, sec_q1, sec_q2):
        self.username = username
        self.email = email
        self.password = password
        self.birth_year = birth_year
        self.sec_q1 = sec_q1
        self.sec_q2 = sec_q2
        self.courses = []
        self.quiz_score = None
    
    def to_dict(self):
        return self.__dict__

# ---------------------------- Sign Up Class ----------------------------
class SignUp:
    def execute(self):
        users = load_data(USERS_FILE)
        username = input("Enter username: ")
        if any(u['username'] == username for u in users):
            print("Username already exists.")
            return

        email = input("Enter email: ")
        if any(u['email'] == email for u in users):
            print("Email already registered.")
            return

        password = input("Enter password: ")
        if not self.is_valid_password(password):
            print("Password must be at least 6 characters long and contain both letters and numbers.")
            return

        birth_year = int(input("Enter birth year: "))
        age = datetime.now().year - birth_year
        if age < 18 or age > 50:
            print("Age not in valid range. Please contact support.")
            return

        q1 = input("Security Question 1 - What was your first teacher's name? ")
        q2 = input("Security Question 2 - What was your first phone model? ")

        user = User(username, email, password, birth_year, q1, q2)
        users.append(user.to_dict())
        save_data(USERS_FILE, users)
        print("Sign up successful.")

    def is_valid_password(self, pw):
        return len(pw) >= 6 and any(c.isdigit() for c in pw) and any(c.isalpha() for c in pw)

# ---------------------------- Login Class ----------------------------
class Login:
    def execute(self):
        users = load_data(USERS_FILE)
        username = input("Enter username: ")
        password = input("Enter password: ")

        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            print("Login successful.")
            return username
        else:
            print("Incorrect credentials.")
            choice = input("Forgot password? (y/n): ")
            if choice == 'y':
                return PasswordRecovery().execute()
            return None

# ---------------------------- Password Recovery Class ----------------------------
class PasswordRecovery:
    def execute(self):
        users = load_data(USERS_FILE)
        username = input("Enter username: ")
        
        user = next((u for u in users if u['username'] == username), None)
        if not user:
            print("User not found.")
            return None

        q1 = input("Answer to security question 1: ")
        q2 = input("Answer to security question 2: ")
        
        if user['sec_q1'] == q1 and user['sec_q2'] == q2:
            new_password = input("Enter new password: ")
            if SignUp().is_valid_password(new_password):
                user['password'] = new_password
                save_data(USERS_FILE, users)
                print("Password updated successfully. Please log in again.")
                return username
            else:
                print("Invalid new password.")
                return None
        else:
            print("Incorrect answers.")
            return None

# ---------------------------- Course Manager Class ----------------------------
class CourseManager:
    def execute(self, username):
        users = load_data(USERS_FILE)
        courses = load_data(COURSES_FILE)

        available_courses = ["Python Basics", "Web Development", "Data Analysis"]
        print("Available courses:")
        for i, course in enumerate(available_courses):
            print(f"{i+1}. {course}")
        
        choice = int(input("Enter course number: ")) - 1  
        selected = available_courses[choice]

        user = next((u for u in users if u['username'] == username), None)
        user['courses'].append(selected)
        
        course_entry = next((c for c in courses if c['name'] == selected), None)
        
        if course_entry:
            course_entry['students'].append(username)
        else:
            courses.append({'name': selected, 'students': [username]})

        save_data(USERS_FILE, users)
        save_data(COURSES_FILE, courses)

        print(f"Successfully enrolled in '{selected}'. Date: {datetime.now().date()}")

# ---------------------------- Quiz Manager Class ----------------------------
class QuizManager:
    def execute(self, username):
        quiz = {
            "1": {"q": "What type of language is Python?", "choices": ["Interpreted", "Compiled", "Machine", "None"], "a": 0},
            "2": {"q": "Which conditional structure exists in Python?", "choices": ["if", "when", "case", "select"], "a": 0},
            "3": {"q": "Which function is used to get input from user?", "choices": ["print", "input", "scan", "read"], "a": 1},
            "4": {"q": "How do we define a list?", "choices": ["()", "{}", "[]", "<>"], "a": 2},
            "5": {"q": "Which is used to store data permanently?", "choices": ["RAM", "Cache", "File", "Clipboard"], "a": 2}
        }

        score = 0
        for key in quiz:
            q = quiz[key]
            print(f"\n{q['q']}")
            for i, c in enumerate(q['choices']):
                print(f"{i+1}. {c}")
            
            ans = int(input("Your answer (number): ")) - 1
            if ans == q['a']:
                score += 1  

        users = load_data(USERS_FILE)
        user = next((u for u in users if u['username'] == username), None)
        user['quiz_score'] = score
        save_data(USERS_FILE, users)
        print(f"Quiz finished. Your score: {score}/5")

# ---------------------------- Main Menu Class ----------------------------
class MainMenu:
    def run(self):
        while True:
            print("\n1. Sign Up\n2. Log In\n3. Exit")
            choice = input("Your choice: ")
            if choice == '1':
                SignUp().execute()
            elif choice == '2':
                user = Login().execute()
                if user:
                    self.user_menu(user)
            elif choice == '3':
                print("Exiting program. Goodbye!")
                break

    def user_menu(self, username):
        while True:
            print("\n1. Enroll in Course\n2. Take Quiz\n3. Log Out")
            option = input("Your choice: ")
            if option == '1':
                CourseManager().execute(username)
            elif option == '2':
                QuizManager().execute(username)
            elif option == '3':
                break

if __name__ == '__main__':
    MainMenu().run()
