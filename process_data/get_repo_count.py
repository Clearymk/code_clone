from util.database import DataBase

db = DataBase()

cur = db.mysql.cursor()
cur.execute("select jupyter_path from jupyter.jupyter_code_snippet where id")
repo = set()
for _ in cur.fetchall():
    # print(_[0].split("\\")[0])
    repo.add(_[0].split("\\")[0])

print(len(repo))
