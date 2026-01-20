from gql import gql
from pprint import pp, pformat

class AddComment:
    """Adds a comment to an Issue or Pull Request

    - https://docs.github.com/en/graphql/reference/mutations#addcomment
    - https://docs.github.com/en/graphql/reference/input-objects#addcommentinput
    """
    QUERY = gql("""
    mutation($subjectId: ID!, $body: String!) {
      addComment(input: { subjectId: $subjectId, body: $body, }) {
        comment { id }
      }
    }
    """)

    def __init__(self, subjectId: str, body: str):
        self._values = { "subjectId": subjectId, "body": body }

    # @mockable(retrun_value="...")
    def execute(self, client):
        pp(f"client.execute({self.QUERY}, variable_values={self._values}")
        # resp["addComment"]["comment"]["id"]
        return "id"


# Use annotation to distinguish (special) methods from plain methos
# - Protocol btw. Path and 
def custom_annotation(key, value):
    """A decorator to add a custom key-value pair as an attribute."""
    def decorator(func):
        if not hasattr(func, '_custom_annotations'):
            func._custom_annotations = {}
        func._custom_annotations[key] = value
        return func
    return decorator


class Path: # NAME is TBD
    def __init__(self, item):
        # TODO Keep 'github' client
        self.items = [ item ]

    def __getattr__(self, name):
        last = self.items[-1]

        attr = getattr(last, name)

        if not callable(attr):
            return attr

        def custom_callable(*args, **kwargs):
            result = attr({ "path": self, "args": args, "kwargs": kwargs })
            self.items.append(result)
            return self

        if hasattr(attr, '_custom_annotations'):
            return custom_callable


        # How to distinguish "object creation" method and "mutation" method?
        # - for "objection creation" method, simply bypass args and kwargs
        # - for "mutation" method, pass "history(?) so far" in addition ot
        def wrapped_callable(*args, **kwargs):
            result = attr(*args, **kwargs)
            self.items.append(result)
            return self

        return wrapped_callable

    def __repr__(self):
        return pformat(self.items)



class IssueComment:
    def __init__(self, *, oid: str):
        self._oid = oid

    def __repr__(self):
        return f"Issue({self._oid})"


class Issue:
    def __init__(self, *, number: int):
        self._number = number

    def __repr__(self):
        return f"Issue({self._number})"

    @custom_annotation("X", 1)
    def addComment(self, ctx):
        print(ctx)
        # TODO Get client from ctx
        client = None
        # TODO Get subjectId from ctx (User / Repository / Number)
        subjectId = "123"
        body = ctx["kwargs"]["body"]
        oid = AddComment(subjectId=subjectId, body=body).execute(client)
        return IssueComment(oid=oid)



class Repository:
    def __init__(self, *, name: str):
        super().__init__()
        self._name = name

    def __repr__(self):
        return f"Repository({self._name})"


    @custom_annotation("X", 1)
    def createIssue(self, args):
        print(args)
        # Need to access all the ancestor for this
        return Issue(number=123)

    @custom_annotation("X", 1)
    def number(self, ctx):
        # Issue, Pull Request, or 
        pass

class User:
    def __init__(self, *, login: str):
        super().__init__()
        self._login = login

    def __repr__(self):
        return f"User({self._login})"

    def repository(self, name: str):
        return Repository(name=name)




def user(login: str):
    return Path(User(login=login))

pp(user("parjong").repository("personal"))
pp(user("parjong").repository("personal").createIssue().addComment(body="Hello?"))

# user("parjong").X("personal")
# AttributeError: 'User' object has no attribute 'X'

# github().user("parjong").repository("personal").discussionCategory("5A/...").addDiscussion(...)
# github().user("parjong").repository("personal").discussionCategoryByID("....").addDiscussion(...)

# comment = github().user("parjong").repository("personal").number(1361).addComment(body="Hello?")
# comment.reply(body="Nice to meet you!")
