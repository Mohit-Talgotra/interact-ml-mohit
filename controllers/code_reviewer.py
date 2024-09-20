from code_review.src.chunker2.chunk_extractor import ChunkExtractor2
from code_review.src.code_analyser.code_analyser import CodeAnalyser
from code_review.src.fetcher.git_handler import GitHandler
from code_review.src.fetcher.repository_manager import RepositoryManager
import concurrent.futures


def review_code(body):
    if body == None or body.repo_links == None:
        return {"message": "Repository links are required", "error": "Bad Request"}

    try:
        repos = body.repo_links

        cloneRepoPath = "code_review/cloned_repos"

        git_handler = GitHandler()
        repo_manager = RepositoryManager(git_handler)
        chunk_extractor = ChunkExtractor2()
        code_analyser = CodeAnalyser()

        def process_single_repo(repo):
            try:
                repo_manager.clone_repository(repo, cloneRepoPath)
            except Exception as e:
                print(f"Error cloning repo {repo}: {e}")
                return None

        # Use ThreadPoolExecutor to parallelize the repository cloning
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks to the executor to run in parallel
            futures = [executor.submit(process_single_repo, repo) for repo in repos]
            concurrent.futures.wait(futures)

        chunk_extractor.processRepos(cloneRepoPath)
        scores = code_analyser.processAllRepos(cloneRepoPath)
        repo_manager.complete_cleanup()

        return scores

    except Exception as e:
        return {"message": f"Error fetching code review", "error": str(e)}
