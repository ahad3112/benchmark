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
        for cluster in self.args.clusters:
            getattr(clusters, cluster)(args=self.args)
