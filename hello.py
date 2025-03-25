# Function that returns a greeting message
def greet(name):
    return f"Hello, {name}!"

# Function that invokes another function
def welcome():
    user_name = input("Enter your name: ")  # Taking user input
    message = greet(user_name)  # Calling the greet function
    print(message)

# Calling the welcome function
welcome()