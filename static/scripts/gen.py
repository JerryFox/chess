def get_generators():
    # returns list of generators
    # generator with index n generates from generator with index n-1
    g = [([] + [0] for i in range(1))] # initial list

    for i in range(10):
        index = len(g) - 1
        #g += [(x + [x[-1] + 1] for x in g[-1])]
        #g += [(x + [x[-1] + 1] for x in g[len(g) - 1])]
        g += [(x + [x[-1] + 1] for x in g[index])]
        # with any of commented lines generator doesn't work - why???!!!
        # it doesn't matter on logic between generators
        """
        correct behavior:

>>> for i in get_generators()[10]: print(i)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        incorrect behavior:

>>> for i in get_generators()[10]: print(i)
Traceback (most recent call last):
  module <module> line 1
    for i in get_generators()[10]: print(i)
ValueError: generator already executing

        """
    return g

