from github import Github
from nbformat import reads, NO_CONVERT
from dateutil import parser
import base64


def extract_code_cells(file_content):
    try:
        notebook = reads(file_content, NO_CONVERT)
        cells = notebook['cells']
        codes = [c['source'] for c in cells if c['cell_type'] == 'code']
    except Exception as e:
        print(e)
        return []

    return flatten(codes)


def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])


def get_matched_commit(search_code, project, target_file):
    git = Github("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")
    repo = git.get_repo(project)

    commits = list(repo.get_commits())
    matched_commit = None

    if len(commits) == 1:
        matched_commit = commits[0]
    else:
        matched = False
        for i in range(0, len(commits)):
            if matched:
                break

            file_names = list(file.filename for file in commits[i].files)
            if target_file in file_names:
                file_content = repo.get_contents(target_file, commits[i].sha)
                file_content = base64.b64decode(file_content.content)

                for code_cell in extract_code_cells(file_content):
                    if code_cell == search_code:
                        matched_commit = commits[i]
                        matched = True
                        break
    return matched_commit


if __name__ == "__main__":
    repo_path = "davetang/learning_python"
    file_path = "notebook/functions.ipynb"
    search_code = '''num = list(range(11, 17))

print(num.index(13))
print(num.count(11))

num.append(17)
print(num)

num.remove(13)
print(num)

num.reverse()
print(num)'''
    commit = get_matched_commit(search_code, repo_path, file_path)
    print(commit.author.url)
    print(commit.last_modified)
    print(commit.sha)
