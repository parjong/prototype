from abc import ABC
from abc import abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from typing import List

@dataclass(slots=True)
class TensorDescr:
    name: str | None = None


class GraphBuilder(ABC):
    @abstractmethod
    def build_tensor(self, tensor: TensorDescr) -> None:
      pass

    @abstractmethod
    def set_graph_inputs(self, inputs: List[str]) -> None:
        pass

class GraphRecipeContext:
    def __init__(self, *, builder: GraphBuilder):
        self._builder = builder

    @contextmanager
    def tensor(self):
        tensor = TensorDescr()
        yield tensor
        self._builder.build_tensor(tensor)

    def inputs(self, *args):
        self._builder.set_graph_inputs(*args)


# GraphRecipe = Callable[GraphRecipeContext, None]
def sample_recipe(graph: GraphRecipeContext):
    with graph.tensor() as t:
        t.name = "X"
        # @dataclass with "slots=True" prevents bugs like below
        # t.my = 'Y'
    graph.inputs('X')


class MyGraphBuilder(GraphBuilder):
    def __init__(self):
        super().__init__()
        self.tensors = []

    def build_tensor(self, tensor: TensorDescr):
        assert tensor.name is not None
        self.tensors.append(tensor)

    def set_graph_inputs(self, names: List[str]):
        print(names)

def main() -> None:
    builder = MyGraphBuilder()
    context = GraphRecipeContext(builder=builder)
    sample_recipe(context)
    print(builder.tensors)
