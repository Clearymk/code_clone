def write_log(log_info, log_path="log.txt"):
    with open(log_path, "a+") as f:
        f.write(str(log_info) + "\n")
