from ComandHandler import ComandHandler

if __name__ == "__main__":
    handler = ComandHandler()
    while True:
        print("Введите команду:")
        command = input()
        handler.handle(command)