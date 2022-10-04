import numpy as np
from util.database import DataBase

db = DataBase()

violation_count = []
# for count in db.query_by_sql("select count(*), jupyter_id "
#                              "from pylint_violation "
#                              "where jupyter_id is not null group by jupyter_id"):
#     violation_count.append(count[0])
#
# violation_count.extend([0] * 33933)

# for count in db.query_by_sql("select count(*) "
#                              "from style_violation "
#                              "where jupyter_id is not null group by jupyter_id"):
#     violation_count.append(count[0])
#
# violation_count.extend([0] * 2240)

# for count in db.query_by_sql("select count(*) "
#                              "from bandit_violation "
#                              "where jupyter_id is not null group by jupyter_id"):
#     violation_count.append(count[0])
#
# violation_count.extend([0] * 188312)

for count in db.query_by_sql("select count(*) "
                             "from performance_violation "
                             "where jupyter_id is not null group by jupyter_id"):
    violation_count.append(count[0])

violation_count.extend([0] * 191066)

print("mean:", np.mean(violation_count))
print("median:", np.quantile(violation_count, 0.5))
print("max:", np.max(violation_count))
print("min:", np.min(violation_count))
