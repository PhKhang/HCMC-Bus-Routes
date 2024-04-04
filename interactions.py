def intro():
    print("Called as a module")
    
print(__name__)
if __name__ == "__main__":
    intro()
    print("No problem found because this line is executed successfully")