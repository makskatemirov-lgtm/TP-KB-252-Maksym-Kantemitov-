# List [Item1, Item2, Item3]
# Item {"name":"Jon", "phone":"0631234567"}

# already sorted list
list = [
    {"name": "Bob", "phone": "0631234567",
        "email": "bob@gmail.com", "group": "kb-242"},
    {"name": "Emma", "phone": "0631234567",
        "email": "emma@gmail.com", "group": "kb-242"},
    {"name": "Jon",  "phone": "0631234567",
        "email": "jon@gmail.com", "group": "kb-242"},
    {"name": "Zak",  "phone": "0631234567",
        "email": "zak@gmail.com", "group": "kb-242"}
]


def printAllList():
    for elem in list:
        strForPrint = "Student name is " + \
            elem["name"] + ",  Phone is " + elem["phone"] + \
            ",  Email is " + elem["email"] + ",  Group is " + elem["group"]
        print(strForPrint)


def addNewElement():
    name = input("Pease enter student name: ")
    phone = input("Please enter student phone: ")
    email = input("Please enter student email: ")
    group = input("Please enter student group: ")

    newItem = {"name": name, "phone": phone, "email": email, "group": group}
    # find insert position
    insertPosition = 0
    for item in list:
        if name > item["name"]:
            insertPosition += 1
        else:
            break
    list.insert(insertPosition, newItem)
    print("New element has been added")
    return


def deleteElement():
    name = input("Please enter name to be delated: ")
    deletePosition = -1
    for item in list:
        if name == item["name"]:
            deletePosition = list.index(item)
            break
    if deletePosition == -1:
        print("Element was not found")
    else:
        print("Dele position " + str(deletePosition))
        # list.pop(deletePosition)
        del list[deletePosition]
    return

# ---------------------------------------------------


def updateElement():
    name = input("Please enter name to be updated data: ")
    for i, item in enumerate(list):
        if item["name"] == name:
            upname = input("Enter new name: ")
            upphone = input("Enter new phone: ")
            upemail = input("Enter new email: ")
            upgroup = input("Enter new group: ")

            updateItem = {"name": upname, "phone": upphone,
                          "email": upemail, "group": upgroup}
            del list[i]

            insertPosition = 0
            for n in list:
                if upname > n["name"]:
                    insertPosition += 1
                else:
                    break
            list.insert(insertPosition, updateItem)
            print("Element update")
            return

    print("Element was not found")
    return

# ---------------------------------------------------


def main():
    while True:
        chouse = input(
            "Please specify the action [ C create, U update, D delete, P print,  X exit ] ")
        match chouse:
            case "C" | "c":
                print("New element will be created:")
                addNewElement()
                printAllList()
            case "U" | "u":
                print("Existing element will be updated")
                updateElement()
            case "D" | "d":
                print("Element will be deleted")
                deleteElement()
            case "P" | "p":
                print("List will be printed")
                printAllList()
            case "X" | "x":
                print("Exit()")
                break
            case _:
                print("Wrong chouse")


main()