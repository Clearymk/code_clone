import os

path = "../token_clone"
zip_paths = []
for root, dirs, files in os.walk(path):
    dirs[:] = [os.path.join(root, d) for d in dirs]
    files = [fi for fi in files if fi.endswith(".zip")]
    files = [os.path.abspath(os.path.join(root, f)) for f in files]
    if len(files) > 0:
        zip_paths.extend(files)

with open("projects-list.txt", "w", encoding="utf8") as f:
    for zip_path in zip_paths:
        f.write(zip_path + "\n")
