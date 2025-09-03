K = []

def testcase(cls):
    print(f'{__name__}: {cls}')
    K.append(cls)

@testcase
class A:
  def __init__(self):
    print('A is initialized')

  pass
