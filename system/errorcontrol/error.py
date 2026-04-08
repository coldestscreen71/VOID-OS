def er(msg, context=None):
    RED = "\033[31m"
    RESET = "\033[0m"

    if context:
        print(f"{RED}[ERROR] {msg}{RESET}: {context}")
    else:
        print(f"{RED}[ERROR] {msg}{RESET}")