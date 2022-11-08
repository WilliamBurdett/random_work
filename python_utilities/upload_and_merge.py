import os

from dotenv import load_dotenv
from github import Github
from github.Branch import Branch
from github.GithubException import GithubException, UnknownObjectException
from github.Repository import Repository

load_dotenv()


def run_command(command: str) -> str:
    stream = os.popen(command)
    output = stream.read()
    print(output)
    return output


def get_repo() -> Repository:
    access_token = os.environ["GITHUB_ACCESS_TOKEN"]
    repo_name = "WilliamBurdett/my-rogue"
    g = Github(access_token)
    return g.get_repo(repo_name)


def get_target_branch_name():
    output = run_command("git status")
    current_branch_name = output.split(" ")[2].split("\n")[0]
    if current_branch_name == "main":
        return input("Branch is main, enter new branch\n")
    return current_branch_name


def get_target_branch(repo: Repository):
    target_branch_name = get_target_branch_name()
    try:
        return repo.get_branch(target_branch_name)
    except GithubException as ge:
        if ge.status == 404:
            sb = repo.get_branch("main")
            r = repo.create_git_ref(
                ref="refs/heads/" + target_branch_name, sha=sb.commit.sha
            )
            return repo.get_branch(target_branch_name)
        else:
            raise ge


def get_pr(repo: Repository, target_branch: Branch):
    try:
        return repo.create_pull(
            target_branch.name, "Automatic PR", "main", target_branch.name
        )
    except GithubException as ge:
        if ge.status == 422:
            prs = repo.get_pulls(state="open")
            for pr in list(prs):
                return repo.get_pull(pr.number)
        raise ge


def delete_branch(repo: Repository, branch: Branch):
    try:
        ref = repo.get_git_ref(f"heads/{branch.name}")
        ref.delete()
    except UnknownObjectException:
        print("No such branch", branch.name)


def main():
    # access_token = os.environ["GITHUB_ACCESS_TOKEN"]
    # repo_name = "WilliamBurdett/my-rogue"
    run_command(f"git restore --staged .")
    repo = get_repo()
    target_branch = get_target_branch(repo)
    run_command(f"git checkout -b {target_branch.name}")
    run_command(r"yarn prettier --write .")
    run_command(r"git add C:/Users/Agathos/Code/my-rogue/.")
    run_command('git commit -m "Automatically adding files"')
    run_command(f"git push --set-upstream origin {target_branch.name}")
    pr = get_pr(repo, target_branch)
    message = f"Automatically merging {target_branch.name}"
    pr.merge(commit_message=message, commit_title=message, merge_method="squash")
    delete_branch(repo, target_branch)
    run_command("git checkout main")
    run_command("git pull")
    run_command(f"git branch -D {target_branch.name}")


if __name__ == "__main__":
    main()
