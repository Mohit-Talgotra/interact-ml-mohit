from code_review.src.chunker2.chunk_extractor import ChunkExtractor2
from code_review.src.code_analyser.code_analyser import CodeAnalyser
from code_review.src.fetcher.git_handler import GitHandler
from code_review.src.fetcher.repository_manager import RepositoryManager


def codeReview(body):
    if body == None or body.repo_links == None:
        return {"message": "Repository links are required", "error": "Bad Request"}

    try:
        return codeReviewer(body.repo_links)

    except Exception as e:
        return {"message": f"Error executing script", "error": str(e)}


def fetch_repository(url: str, base_path: str) -> str:
    git_handler = GitHandler()
    repo_manager = RepositoryManager(git_handler)

    repo_manager.clone_repository(url, base_path)


def codeReviewer(repos):
    cloneRepoPath = "code_review/cloned_repos"

    git_handler = GitHandler()
    repo_manager = RepositoryManager(git_handler)
    chunk_extractor = ChunkExtractor2()
    code_analyser = CodeAnalyser()

    for repo in repos:
        fetch_repository(repo, cloneRepoPath)

    chunk_extractor.processRepos(cloneRepoPath)

    repo_manager.complete_cleanup()

    print("Here")

    # scores = code_analyser.processRepos(cloneRepoPath)

    return []
