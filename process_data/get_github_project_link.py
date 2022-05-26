from openpyxl import Workbook
import re
from util.database import DataBase

db = DataBase()
jupyter_data = []
ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
book_name_xls = 'jupyter_code_snippet_github_project_0{}.xlsx'
value_title = ["id", "code", "github_project_path"]

for _ in db.query_by_sql("select id, code,jupyter_path from jupyter.jupyter_code_snippet"):
    data = [_[0], _[1]]
    github_project_link = "https://github.com/" + _[2].split("\\")[0].replace("_", "/", 1)
    data.append(github_project_link)
    jupyter_data.append(data)



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
        data = [ILLEGAL_CHARACTERS_RE.sub(r'', str(row[0])),
                ILLEGAL_CHARACTERS_RE.sub(r'', str(row[1]).replace("\n", "")),
                ILLEGAL_CHARACTERS_RE.sub(r'', str(row[2]))]
        worksheet.append(data)
    workbook.save(filename=save_file)
    file_count += 1
