def write_log(log):
    with open("log.txt", "a+") as f:
        f.write(str(log) + "\n")
