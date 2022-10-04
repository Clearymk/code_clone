from util.database import DataBase

db = DataBase()

# performance_violations = {'W0104'}
performance_violations = {'E0401', 'E0601', 'E0603', 'E0611', 'E1101', 'E1102', 'E1133', 'W0012', 'W0401', 'W0611',
                          'W0614'}
# insert data
for performance_violation in performance_violations:
    for data in db.query_by_sql("select id,so_id, jupyter_id, type, message_id, message, symbol "
                                "from pylint_violation "
                                "where message_id = \'{}\'".format(performance_violation)):
        db.insert_irrelevant_violation(data[1:])
        db.delete_pylint_violation_by_id(data[0])
