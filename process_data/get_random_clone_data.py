from util.database import DataBase
from random import sample

# 需要的数据 code, clone type, so post id, jupyter path type
db = DataBase()
clone_pair_info = []
count = 0
# 得到so_code_snippet_id和jupyter_code_snippet id
for so_id, jupyter_id, clone_type in db.query_by_sql("select so_code_snippet_id, jupyter_code_snippet_id, clone_type "
                                                     "from jupyter.clone_pair "
                                                     "where direction = 1 and clone_type = 1"):
    # 得到so post id合成url, 得到jupyter notebook path合成url, 得到两个代码片段
    so_code, so_post_id = db.query_by_sql("select code, so_post_id "
                                          "from jupyter.so_code_snippet "
                                          "where id = {}".format(so_id))[0]
    so_url = "https://stackoverflow.com/questions/{}".format(so_post_id)
    jupyter_code, jupyter_path = db.query_by_sql("select code, jupyter_path "
                                                 "from jupyter.jupyter_code_snippet "
                                                 "where id = {}".format(jupyter_id))[0]
    github_project, jupyter_file_path = jupyter_path.split("\\", 1)
    github_path = "https://github.com/{}/{}/blob/master/{}".format(github_project.split("_")[0],
                                                                   github_project[github_project.find("_") + 1:],
                                                                   jupyter_file_path.replace(" ", "%20").replace("\\",
                                                                                                                 "/"))
    clone_pair_info.append([so_url, github_path, clone_type, so_code, jupyter_code])
    count += 1
    print(count)

clone_pair_info = sample(clone_pair_info, 2000)
with open("clone_pair_info_1.md", "w", encoding="utf8") as f:
    for _ in clone_pair_info:
        f.write(_[0] + "\n" + _[1] + "\n" + str(_[2]))
        f.write("\n++++++++++++++++\n")
        f.write(_[3])
        f.write("\n++++++++++++++++\n")
        f.write(_[4])
        f.write("\n----------------\n")
