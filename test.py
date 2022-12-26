def file_r():
    with open("file.txt", "r") as file:
        message = file.read()
    print(message)


print(file_r())
