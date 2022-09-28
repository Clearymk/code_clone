from util.database import DataBase

db = DataBase()
jupyter_data = set()
for _ in db.query_by_sql("select id, jupyter_path "
                         "from jupyter_code_snippet "
                         "where id in "
                         "(select jupyter_code_snippet_id "
                         "from clone_pair "
                         "where direction = 1 or direction = 2)"):
    github_project_link = "https://github.com/" + _[1].split("\\")[0].replace("_", "/", 1)
    jupyter_data.add(github_project_link)

print(len(jupyter_data))
