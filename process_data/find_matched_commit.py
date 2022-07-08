from github import Github
from nbformat import reads, NO_CONVERT
from util.write_log import write_log
import base64
from util.proxy import init_proxy


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
    experience = 0
    authors = {"NotFound": 0}
    matched_author = None
    commit_count = 0

    if len(commits) == 1:
        matched_commit = commits[0]
        experience = 1
    else:
        matched = False
        for i in range(0, len(commits)):
            if matched:
                break

            commit_count += 1
            author = commits[i].author

            if author:
                if author.url in authors:
                    authors[author.url] += 1
                else:
                    authors[author.url] = 1

            file_names = list(file.filename for file in commits[i].files)
            if target_file in file_names:
                file_content = repo.get_contents(target_file, commits[i].sha)
                file_content = base64.b64decode(file_content.content)

                for code_cell in extract_code_cells(file_content):
                    if code_cell == search_code:
                        matched = True
                        matched_commit = commits[i]
                        matched_author = matched_commit.author

                        if matched_author:
                            experience = authors[matched_author.url] / commit_count
                        else:
                            experience = 0
                            write_log(project + ":" + target_file + ":" + matched_commit.sha + ":" + "author not found")
                        break
    return matched_commit.sha, matched_author, matched_commit.last_modified, round(experience, 4)


if __name__ == "__main__":
    init_proxy()
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
    info = get_matched_commit(search_code, repo_path, file_path)
    print(info)
