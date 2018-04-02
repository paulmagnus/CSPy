def main():
    while True:
        number = input("enter a positive number: ")
        if number <= 0:
            raise ValueError("that's not a positive number, dipshit")
            
main()
