from util.database import DataBase

if __name__ == "__main__":
    clone_db = DataBase()
    answer_count = 0
    question_count = 0
    answer_vote_count = 0
    question_vote_count = 0
    accepted_count = 0

    for so_code_snippet_id in clone_db.query_by_sql("select distinct so_code_snippet_id "
                                                    "from clone_pair "
                                                    "where direction = 1"):
        so_type = clone_db.query_by_sql("select distinct id, clone_type "
                                        "from jupyter.so_code_snippet "
                                        "where id = {}".format(so_code_snippet_id[0]))
        so_info = clone_db.query_by_sql("select distinct so_id, vote "
                                        "from clone_so_snippet_info "
                                        "where so_id = {}".format(so_code_snippet_id[0]))
        if so_type[0][1] == 1:
            question_vote_count += so_info[0][1]
            question_count += 1
        elif so_type[0][1] == 2:
            answer_vote_count += so_info[0][1]
            answer_count += 1
        else:
            print(so_type, so_info)
            print("------")
    print(question_count, question_vote_count)
    print(answer_count, answer_vote_count)
    # for so_code_snippet_info in clone_db.query_by_sql("select distinct so_id, vote, is_accepted "
    #                                                   "from clone_so_snippet_info "
    #                                                   "where so_id in "
    #                                                   "(select distinct so_code_snippet_id "
    #                                                   "from clone_pair "
    #                                                   "where direction = 1);"):
    #     count += 1
    #     vote_count += so_code_snippet_info[1]
    #     accepted_count += so_code_snippet_info[2]
    #
    # print(count)
    # print("vote count:", vote_count)
    # print("accepted count:", accepted_count)
