def menu(name, options):
    print(f"----- {name} -----")

    i = 0
    for opt in options:
        print(f"{i} - {opt}")
        i += 1

    action = None

    while action is None:
        resp = input("Enter the number corresponding to your choice:\n")
        try:
            resp = int(resp)
            action = list(options.values())[resp]
        except:
            action = None

    return action
