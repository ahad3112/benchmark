'''
Author :
    * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com>
Usage:
    $ python3 benchmark.py -h/--help
'''

try:
    import centres.clusters as clusters
except ModuleNotFoundError:
    import sys
    sys.path.append('..')
    import centres.clusters as clusters


class Create:
    def __init__(self, *, args):
        self.args = args
        self.__create_benchmark()

    def __create_benchmark(self):
        getattr(clusters, self.args.cluster)(args=self.args)
