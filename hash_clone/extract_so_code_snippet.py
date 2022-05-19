import os
import re
import code_trimmer
import database
import hashlib

if __name__ == "__main__":
    db = database.DataBase()
    path = "E:\\test"
    so_snippet_paths = []

    for root, dirs, files in os.walk(path):
        dirs[:] = [os.path.join(root, d) for d in dirs]
        files = [fi for fi in files if re.match(r"\d+.txt", fi)]
        files = [os.path.join(root, f) for f in files]
        if len(files) > 0:
            so_snippet_paths.extend(files)

    for so_snippet_path in so_snippet_paths:
        code = ""

        with open(so_snippet_path) as f:
            for line in f.readlines():
                code += line

        trimmed_code = code_trimmer.CodeTrimmer(code).trim()
        if trimmed_code == "":
            continue
        hash_value = hashlib.md5(trimmed_code.encode("utf-8")).hexdigest()
        db.insert_so_code_snippet(hash_value, code, so_snippet_path)

    db.mysql.commit()