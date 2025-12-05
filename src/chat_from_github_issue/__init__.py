# Based on https://pygithub.readthedocs.io/en/v2.8.1/introduction.html
from github import Github
from github import Auth as GithubAuth
from ollama import chat
from ollama import ChatResponse

from os import environ
from pprint import pprint

def chat_message_of_(comment):
    # comment.body: str
    # comment.author_association = OWNER
    #                            | ...
    #                            | NONE (for github-action bot account
    #                                    when tested from Github Enterprise
    # comment.reactions: dict
    # ^ Can be used to make a recap on close (persistent memory)
    role = 'user' if comment.author_association != 'NONE' else 'assistant'
    return { 'role': role, 'content': comment.body }
# def/ END

def make_response_for_(messages):
    if 'CI' in environ:
        sample = """Hello! I'm Alex, your friendly AI assistant here to help you with whatever you need! 😊"""
        return sample
    # if/ END

    # References
    # - https://apidog.com/blog/how-to-use-ollama/ 
    args = {}

    args['model'] = 'qwen3:1.7b' # To run LLM onNVIDIA GeForce GTX 1650 (4GB VRAM)
    args['messages'] = messages
    args['options'] = { 'num_ctx': 8 * 1024 } # Q. How to adjust this number?

    response: ChatResponse = chat(**args)

    return response.message.content
# def/ END

def main() -> None:
    # NOTE Caller SHOULD set 'GITHUB_TOKEN' before (even for Github Actions)
    auth = GithubAuth.Token(environ['GITHUB_TOKEN'])
    g = Github(auth=auth)

    param = {}

    param['src_issue_number'] = '13'

    repository: str = 'parjong/prototype'
    src_issue_number: int = 13

    repo = g.get_repo(repository)
    issue = repo.get_issue(number=src_issue_number)

    messages = []

    # System Prompt
    messages += [ { 'role': 'system', 'content': 'You are alex, a kind assistant' } ]

    # Chat History
    # Q. How to treat the main description? 
    #
    # - As system prompt?
    # - As chat history?
    messages += [ { 'role': 'user', 'content': issue.body } ]
    messages += [ chat_message_of_(comment) for comment in issue.get_comments() ]

    print('Messages:')
    pprint(messages)

    response = make_response_for_(messages)

    print('Response:')
    print(response)

    if 'DST_ISSUE_NUMBER' in environ:
        dst_issue_number = int(environ['DST_ISSUE_NUMBER'])
        issue = repo.get_issue(number=dst_issue_number)
        issue.create_comment(response)

    # NOTE Possible to remove How to remove
    #
    # Variable     | How?
    # ---          | ---
    # repository   | Use 'GITHUB_REPOSITORY' environment variable
    # issue_number | Use action event context
    #              | (e.g. github.context.issue.number for 'issue_comment' trigger)
    #
    # From [1]

    # NOTE. System Design Pros/Cons
    #
    # - Pros: Minimal infrastructure
    # - Cons: Redundant re-computation (cannot reuse the KV from existing turns)
# def/ END

# References
#
# [1] https://docs.github.com/en/actions/reference/workflowsu-and-actions/variables
# [2] https://pygithub.readthedocs.io/en/v2.8.1/examples.html
