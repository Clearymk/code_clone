import os
import re
from util.code_trimmer import CodeTrimmer
from util.database import DataBase
import hashlib

if __name__ == "__main__":
    db = DataBase()
    path = "C:\\so_01"
    so_snippet_paths = []

    for root, dirs, files in os.walk(path):
        dirs[:] = [os.path.join(root, d) for d in dirs]
        files = [fi for fi in files if re.match(r"\d+.txt", fi)]
        files = [os.path.join(root, f) for f in files]
        if len(files) > 0:
            so_snippet_paths.extend(files)

    for so_snippet_path in so_snippet_paths:
        try:
            code = ""
            if int(so_snippet_path.split("\\")[-2]) < 41069487:
                continue

            with open(so_snippet_path, encoding="utf8") as f:
                for line in f.readlines():
                    code += line

            trimmed_code = CodeTrimmer(code).trim()

            if trimmed_code == "":
                continue
            hash_value = hashlib.md5(trimmed_code.encode("utf-8")).hexdigest()
            db.insert_so_code_snippet(hash_value, code, so_snippet_path.split(os.path.sep)[-2])
        except Exception as e:
            print(e)

    db.mysql.commit()
