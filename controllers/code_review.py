import json
#import from submodule
from src.chunker2.chunk_extractor import ChunkExtractor2
from src.code_analyser.code_analyser import CodeAnalyser
from src.fetcher.git_handler import GitHandler
from src.fetcher.repository_manager import RepositoryManager
import logging

def codeReview(body):
    if body == None:
        return {
            "message": "Repository links are required", "error": "Bad Request"
        }

    repos = json.dumps(body['repo_links'])

    try:
        codeReviewer(repos)
        return {
            "message": f"Repository analysis completed successfully.", "error": None
        }
    except Exception as e:
        return {
            "message": f"Error executing script", "error": str(e)
        }

def fetch_repository(url: str, base_path: str) -> str:
    git_handler = GitHandler()
    repo_manager = RepositoryManager(git_handler)
    
    repo_manager.clone_repository(url, base_path)

def codeReviewer(repos):
    logger = logging.getLogger(__name__)
    if repos != []:
        repos = eval(repos)
        print(repos)
    else:
        logger.info("Please provide a repository URL")
        return
    
    cloneRepoPath = "./cloned_repos"

    chunk_extractor = ChunkExtractor2()
    code_analyser = CodeAnalyser()
    git_handler = GitHandler()
    repo_manager = RepositoryManager(git_handler)

    for repo in repos:
        fetch_repository(repo, cloneRepoPath)
    
    repo_manager.complete_cleanup()
    chunk_extractor.processRepos(cloneRepoPath)
    code_analyser.processRepos(cloneRepoPath)