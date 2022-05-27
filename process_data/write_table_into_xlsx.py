from openpyxl import Workbook
from util.database import DataBase
import re

ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
book_name_xls = 'so_code_snippet_0{}.xlsx'
value_title = ["id", "hash_value", "code", "so_post_id", "zip_path"]

value = []
db = DataBase()

for _ in db.query_by_sql("select * from jupyter.so_code_snippet"):
    d = list(_)
    value.append(d)


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


count = 1
for _ in chunks(value, 1048574):
    workbook = Workbook()
    save_file = book_name_xls.format(count)
    worksheet = workbook.active
    worksheet.title = "Sheet1"
    worksheet.append(value_title)
    for row in _:
        print(row)
        data = []
        for text in row:
            data.append(ILLEGAL_CHARACTERS_RE.sub(r'', str(text).replace("\n", "")))
        worksheet.append(data)
    workbook.save(filename=save_file)
    count += 1
