"""
GitHub Tools — Custom tools for agents to interact with GitHub API.

Provides functions for:
- Reading and creating issues
- Managing labels and project status
- Creating branches, commits, and PRs
- Creating releases
"""

import os
from github import Github, GithubException
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")


def get_repo():
    """Get the GitHub repository object."""
    g = Github(GITHUB_TOKEN)
    return g.get_repo(f"{GITHUB_OWNER}/{GITHUB_REPO}")


# ── Issues ──────────────────────────────────────────

def get_issues_by_label(label: str) -> list[dict]:
    """
    Fetch open issues with a specific label.
    
    Args:
        label: Label name (e.g., 'role:architect')
    
    Returns:
        List of issue dicts with id, number, title, body, labels
    """
    repo = get_repo()
    issues = repo.get_issues(state="open", labels=[label])
    return [
        {
            "number": issue.number,
            "title": issue.title,
            "body": issue.body or "",
            "labels": [l.name for l in issue.labels],
            "url": issue.html_url,
        }
        for issue in issues
    ]


def create_issue(title: str, body: str, labels: list[str]) -> dict:
    """
    Create a new GitHub issue.
    
    Args:
        title: Issue title
        body: Issue body (markdown)
        labels: List of label names
    
    Returns:
        Dict with issue number, title, url
    """
    repo = get_repo()
    issue = repo.create_issue(title=title, body=body, labels=labels)
    return {
        "number": issue.number,
        "title": issue.title,
        "url": issue.html_url,
    }


def add_comment(issue_number: int, body: str) -> dict:
    """
    Add a comment to an existing issue.
    
    Args:
        issue_number: Issue number
        body: Comment body (markdown, can include <!-- agent:... --> markers)
    
    Returns:
        Dict with comment id and url
    """
    repo = get_repo()
    issue = repo.get_issue(issue_number)
    comment = issue.create_comment(body)
    return {"id": comment.id, "url": comment.html_url}


def update_issue_labels(issue_number: int, add_labels: list[str] = None, remove_labels: list[str] = None) -> dict:
    """
    Add or remove labels from an issue.
    
    Args:
        issue_number: Issue number
        add_labels: Labels to add
        remove_labels: Labels to remove
    
    Returns:
        Dict with current labels
    """
    repo = get_repo()
    issue = repo.get_issue(issue_number)
    
    if remove_labels:
        for label_name in remove_labels:
            try:
                issue.remove_from_labels(label_name)
            except GithubException:
                pass
    
    if add_labels:
        for label_name in add_labels:
            issue.add_to_labels(label_name)
    
    return {"labels": [l.name for l in issue.labels]}


def close_issue(issue_number: int) -> dict:
    """Close an issue."""
    repo = get_repo()
    issue = repo.get_issue(issue_number)
    issue.edit(state="closed")
    return {"number": issue_number, "state": "closed"}


# ── Branches & PRs ──────────────────────────────────

def create_branch(branch_name: str, base: str = "main") -> dict:
    """
    Create a new branch from base.
    
    Args:
        branch_name: New branch name (e.g., 'feature/expense-api')
        base: Base branch name (default: 'main')
    
    Returns:
        Dict with branch name and sha
    """
    repo = get_repo()
    base_ref = repo.get_branch(base)
    repo.create_git_ref(
        ref=f"refs/heads/{branch_name}",
        sha=base_ref.commit.sha,
    )
    return {"branch": branch_name, "base": base, "sha": base_ref.commit.sha}


def create_or_update_file(branch: str, path: str, content: str, message: str) -> dict:
    """
    Create or update a file in the repository.
    
    Args:
        branch: Branch name
        path: File path in repo (e.g., 'src/main.py')
        content: File content
        message: Commit message
    
    Returns:
        Dict with path and commit sha
    """
    repo = get_repo()
    try:
        existing = repo.get_contents(path, ref=branch)
        result = repo.update_file(path, message, content, existing.sha, branch=branch)
    except GithubException:
        result = repo.create_file(path, message, content, branch=branch)
    
    return {"path": path, "sha": result["commit"].sha}


def create_pull_request(title: str, body: str, head: str, base: str = "main") -> dict:
    """
    Create a pull request.
    
    Args:
        title: PR title
        body: PR body (markdown)
        head: Source branch
        base: Target branch (default: 'main')
    
    Returns:
        Dict with PR number, title, url
    """
    repo = get_repo()
    pr = repo.create_pull(title=title, body=body, head=head, base=base)
    return {"number": pr.number, "title": pr.title, "url": pr.html_url}


def get_pr_diff(pr_number: int) -> str:
    """
    Get the diff of a pull request.
    
    Args:
        pr_number: PR number
    
    Returns:
        String with the diff content
    """
    repo = get_repo()
    pr = repo.get_pull(pr_number)
    files = pr.get_files()
    diff_parts = []
    for f in files:
        diff_parts.append(f"--- {f.filename}\n{f.patch or '(binary)'}")
    return "\n\n".join(diff_parts)


def merge_pull_request(pr_number: int, commit_message: str = "") -> dict:
    """
    Merge a pull request.
    
    Args:
        pr_number: PR number
        commit_message: Optional merge commit message
    
    Returns:
        Dict with merged status
    """
    repo = get_repo()
    pr = repo.get_pull(pr_number)
    result = pr.merge(commit_message=commit_message or f"Merge PR #{pr_number}: {pr.title}")
    return {"merged": result.merged, "sha": result.sha}


# ── Releases ────────────────────────────────────────

def create_release(tag: str, name: str, body: str) -> dict:
    """
    Create a GitHub release.
    
    Args:
        tag: Tag name (e.g., 'v1.0.0')
        name: Release name
        body: Release notes (markdown)
    
    Returns:
        Dict with tag, name, url
    """
    repo = get_repo()
    release = repo.create_git_release(tag=tag, name=name, message=body)
    return {"tag": tag, "name": name, "url": release.html_url}


# ── File Reading ────────────────────────────────────

def get_file_content(path: str, branch: str = "main") -> str:
    """
    Read a file from the repository.
    
    Args:
        path: File path in repo
        branch: Branch name (default: 'main')
    
    Returns:
        File content as string
    """
    repo = get_repo()
    content = repo.get_contents(path, ref=branch)
    return content.decoded_content.decode("utf-8")
