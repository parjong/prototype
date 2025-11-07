import ray

ray.init()

@ray.remote
def f(x):
    return x * x

futures = [f.remote(i) for i in range(4)]
print(ray.get(futures)) # [0, 1, 4, 9]

# https://docs.ray.io/en/latest/ray-overview/getting-started.html#libraries-quickstart
