from util.database import DataBase

db = DataBase()
count = 0
vote_count = 0
for so_id, vote in db.query_by_sql("select distinct so_code_snippet_id, vote "
                                   "from clone_pair as cp, clone_so_snippet_info as cs "
                                   "where cp.so_code_snippet_id = cs.so_id and clone_type = 1 and is_accepted = 1 and type = 2;"):
    count += 1
    vote_count += vote

print(count)
print(vote_count)
print(vote_count / count)
