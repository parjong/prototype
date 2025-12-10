#!/usr/bin/env -S uv run --script

from gql import gql
from gql import Client as GQLClient
from gql.dsl import DSLSchema, DSLQuery, dsl_gql
from gql.transport.requests import RequestsHTTPTransport as GQLTransport

from dataclasses import dataclass
import os
from pprint import pp

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

client = GQLClient(
    transport=GQLTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f"token {GITHUB_TOKEN}"},
    ),
)


class Evaluator:
    def __init__(self, client):
        self._client = client

    def __call__(self, expr):
        return expr.eval(self._client)

@dataclass
class Issue:
    oid : str

class Body:
    def __init__(self, subject: Issue): # Issue,
        self._subject_id = subject.oid
        self._query = gql("""query($subjectId: ID!) {
          node(id: $subjectId) { ... on Issue { body } }
        }""")

    def eval(self, client) -> str:
        result = client.execute(self._query, variable_values={"subjectId": self._subject_id})
        return result["node"]["body"]
def body_of_(subject):
    return Body(subject)

get = Evaluator(client)

oid = "I_kwDOPpIoXc7cXf60" # https://api.github.com/repos/parjong/prototype/issues/13
issue = Issue(oid)

body = get(body_of_(issue))

pp(body)
