import random

from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from util.database import DataBase

fig, axs = plt.subplots()

db = DataBase()
jupyter_experience = []
jupyter_experience_type_1 = []
jupyter_experience_type_2 = []
count_1 = 0
count_2 = 0

for experience in db.query_by_sql("select experience "
                                  "from clone_jupyter_snippet_commit "
                                  "where jupyter_id in "
                                  "(select jupyter_code_snippet_id "
                                  "from clone_pair "
                                  "where direction = 1 and clone_type = 1) and authors_count > 10"):
    jupyter_experience_type_1.append(["Type 1 clone", experience[0]])
jupyter_experience_type_1 = random.sample(jupyter_experience_type_1, 100)

for experience in jupyter_experience_type_1:
    if experience[1] < 0.1:
        count_1 += 1

for experience in db.query_by_sql("select experience "
                                  "from clone_jupyter_snippet_commit "
                                  "where jupyter_id in "
                                  "(select jupyter_code_snippet_id "
                                  "from clone_pair "
                                  "where direction = 1 and clone_type = 2) and authors_count > 10"):
    jupyter_experience_type_2.append(["Type 2,3 clone", experience[0]])
jupyter_experience_type_2 = random.sample(jupyter_experience_type_2, 100)

for experience in jupyter_experience_type_2:
    if experience[1] < 0.1:
        count_2 += 1

print(count_1, count_2)

jupyter_experience.extend(jupyter_experience_type_1)
jupyter_experience.extend(jupyter_experience_type_2)

sns.set_theme(style="whitegrid")
jupyter_df = pd.DataFrame(data=jupyter_experience, columns=["Clone Type", "Developer experience"])

g1 = sns.violinplot(y="Developer experience", x="Clone Type", width=0.6, data=jupyter_df, inner='point', cut=0)
g1.set(xlabel=None)

plt.show()
plt.savefig('devexperience.eps', format='eps')
