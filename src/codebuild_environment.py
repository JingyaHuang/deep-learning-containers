import os
import re


class GitHubRepositoryURLNotFound(Exception):
    pass


def get_codebuild_build_arn():
    """
    Get env variable CODEBUILD_BUILD_ARN

    :return: value or empty string if not set
    """
    return os.getenv("CODEBUILD_BUILD_ARN", "")


def get_github_repo_url():
    """
    Get env variable CODEBUILD_SOURCE_REPO_URL

    :return: value or empty string if not set
    """
    # Example: "https://github.com/aws/deep-learning-containers.git"
    return os.getenv("CODEBUILD_SOURCE_REPO_URL")


def get_user_and_repo_name():
    """
    Get GitHub Repository information for cloned repository

    :return: tuple (str, str) providing GitHub user id and repository name
    """
    repo_url = get_github_repo_url()
    if not repo_url:
        raise GitHubRepositoryURLNotFound("Environment did not contain GitHub Repository URL")
    _, user, repo_name = repo_url.rstrip(".git").rsplit("/", 2)
    return user, repo_name


def get_codebuild_project_name():
    """
    Get env variable CODEBUILD_SOURCE_REPO_URL

    :return: value, or "local_test" if not set
    """
    # Default value for codebuild project name is "local_test" when run outside CodeBuild
    return os.getenv("CODEBUILD_BUILD_ID", "local_test").split(":")[0]


def get_codebuild_project_id():
    """
    Get env variable CODEBUILD_SOURCE_REPO_URL

    :return: value, or "0" if not set
    """
    return os.getenv("CODEBUILD_BUILD_ID", "0").split(":")[-1]


def get_cloned_folder_path():
    """
    Extract the root folder path for the repository.

    :return: str
    """
    root_dir_pattern = re.compile(r"^(\S+deep-learning-containers)")
    pwd = os.getcwd()
    codebuild_src_dir_env = os.getenv("CODEBUILD_SRC_DIR")

    # Ensure we are inside some directory called "deep-learning-containers
    try:
        if not codebuild_src_dir_env:
            codebuild_src_dir_env = root_dir_pattern.match(pwd).group(1)
    except AttributeError as e:
        raise RuntimeError(
            f"Unable to find DLC root directory in path {pwd}, and no CODEBUILD_SRC_DIR set"
        ) from e

    return codebuild_src_dir_env


def get_codepipeline_url(pipeline_name):
    """
    Construct CodePipeline URL from pipeline name

    :param pipeline_name: name of CodePipeline
    :type pipeline_name: str

    :return: str
    """
    region = os.getenv("AWS_REGION")
    return f"https://{region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline_name}/view?region={region}"


def get_cloudwatch_url(project):
    """
    Construct CloudWatch URL from project ID

    :param codebuild_project_id: ID of CodeBuild project
    :type codebuild_project_id: str

    :return: str
    """
    region = os.getenv("AWS_REGION")
    logpath = os.getenv("CODEBUILD_LOG_PATH")

    return f"https://{region}.console.aws.amazon.com/cloudwatch/home?region={region}#logEventViewer:group=/aws/codebuild/{project};stream={logpath}"
