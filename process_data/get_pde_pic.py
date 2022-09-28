from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from util.database import DataBase

fig, axs = plt.subplots()

db = DataBase()
jupyter_experience = []
for experience in db.query_by_sql("select experience "
                                  "from clone_jupyter_snippet_commit "
                                  "where jupyter_id in "
                                  "(select jupyter_code_snippet_id "
                                  "from clone_pair "
                                  "where direction = 1 and clone_type = 1) limit 500"):
    jupyter_experience.append(["Type 1 clone", experience[0]])

for experience in db.query_by_sql("select experience "
                                  "from clone_jupyter_snippet_commit "
                                  "where jupyter_id in "
                                  "(select jupyter_code_snippet_id "
                                  "from clone_pair "
                                  "where direction = 1 and clone_type = 2) limit 500"):
    jupyter_experience.append(["Type 2,3 clone", experience[0]])
sns.set_theme(style="whitegrid")
jupyter_df = pd.DataFrame(data=jupyter_experience, columns=["Clone Type", "Developer experience"])
# sns.violinplot(y="Developer experience", x="Clone Type", width=0.6, data=jupyter_df, inner="quart", cut=0)
g1 = sns.violinplot(y="Developer experience", x="Clone Type", width=0.6, data=jupyter_df, inner='point', cut=0,
                    zorder=1)
g1.set(xlabel=None)

plt.show()
plt.savefig('devexperience.eps', format='eps')

# plt.violinplot(data=jupyter_df, x="Clone Type", y="Developer experience")
plt.show()