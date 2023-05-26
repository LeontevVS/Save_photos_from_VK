from CommandHandler import CommandHandler

if __name__ == "__main__":
    handler = CommandHandler()
    while True:
        print("Введите команду:")
        command = input()
        handler.handle(command)