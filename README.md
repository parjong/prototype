# prototype
For fast prototyping!

```
# GraphRecipe = Callable[GraphBuilder, None]
def recipe(graph: GraphBuilder)
  with graph.tensor() as t_0:
    t_0.name = '...'
    t_0.dtype = 'FLOAT32'
    t_0.shape = [1, 3]

  with graph.tensor() as t_1:
    t_1.name = '...'
    t_1.shape = [2, 3]
    t_1.quant = Q8(scale=1.0, zero_point=128)
    assert t_1.dtype == 'UINT8'

  with graph.tensor() as t_2:
    t_2.name = '...'
    t_2.shape = [2, 3]
    t_2.quant = Q16(scale=1.0)
    assert t_2.dtype == 'INT16'

  with graph.tensor() as t_3:
    t_3.name = '...'
    t_3.shape = [2, 3]
    t_3.quant = CustomQuant([QSymm(scale=1.0)])
    assert t_1.dtype == 'UINT8'

  with graph.operation() as op:
    op.code = 'RELU'
    op.inputs = ['x']
    op.outputs = ['y']

  graph.inputs('ifm')
  graph.outputs('ofm')
```
