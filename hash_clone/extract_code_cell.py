from nbformat import read, NO_CONVERT
from util.code_trimmer import CodeTrimmer
from util.database import DataBase
import os
import hashlib


def extract_code_cells(file_path):
    try:
        with open(file_path) as f:
            notebook = read(f, NO_CONVERT)
        cells = notebook['cells']
        codes = [c['source'] for c in cells if c['cell_type'] == 'code']
    except Exception:
        return []

    return flatten(codes)


def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])


if __name__ == "__main__":
    path = "/media/viewv/App/jupyter"
    db = DataBase()
    jupyter_paths = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [os.path.join(root, d) for d in dirs]
        files = [fi for fi in files if fi.endswith(".ipynb")]
        files = [os.path.join(root, f) for f in files]

        if len(files) > 0:
            jupyter_paths.extend(files)

    for jupyter_path in jupyter_paths:
        for cell_code in extract_code_cells(jupyter_path):
            try:
                trimmed_code = CodeTrimmer(cell_code).trim()
                remove_comment_code = CodeTrimmer(cell_code).remove_comments_and_docstrings()

                if trimmed_code == "" or remove_comment_code.count("\n") < 4:
                    continue

                hash_value = hashlib.md5(trimmed_code.encode("utf-8")).hexdigest()
                db.insert_jupyter_code_snippet(hash_value, cell_code, jupyter_path.replace(path, ""))
            except Exception as e:
                print(e)

    db.mysql.commit()
