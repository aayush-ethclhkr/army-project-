import re

def check_password_strength(password):
    # Define the criteria for password strength
    criteria = [
        (len(password) >= 8, "Password should be at least 8 characters long."),
        (re.search(r"[A-Z]", password), "Password should contain at least one uppercase letter."),
        (re.search(r"[a-z]", password), "Password should contain at least one lowercase letter."),
        (re.search(r"\d", password), "Password should contain at least one digit."),
        (re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Password should contain at least one special character."),
    ]
    
    # Check the criteria
    errors = [error for valid, error in criteria if not valid]
    
    if not errors:
        return "Strong password!"
    else:
        return f"Weak password. Issues:\n" + "\n".join(errors)

# Test the function
if __name__ == "__main__":
    user_password = input("Enter a password to check its strength: ")
    result = check_password_strength(user_password)
    print(result)
