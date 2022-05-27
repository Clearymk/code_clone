from openpyxl import Workbook
import re
from util.database import DataBase

db = DataBase()
jupyter_data = set()
ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
book_name_xls = 'jupyter_code_snippet_github_project_0{}.xlsx'
value_title = ["id", "code", "github_project_path"]

for _ in db.query_by_sql("select id, code,jupyter_path from jupyter.jupyter_code_snippet"):
    github_project_link = "https://github.com/" + _[2].split("\\")[0].replace("_", "/", 1)
    jupyter_data.add(github_project_link)

jupyter_data = list(jupyter_data)


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


file_count = 1
for _ in chunks(jupyter_data, 1048575):
    workbook = Workbook()
    save_file = book_name_xls.format(file_count)
    worksheet = workbook.active
    worksheet.title = "Sheet1"
    worksheet.append(value_title)
    for row in _:
        print(row)
        data = [ILLEGAL_CHARACTERS_RE.sub(r'', str(row))]
        worksheet.append(data)
    workbook.save(filename=save_file)
    file_count += 1
