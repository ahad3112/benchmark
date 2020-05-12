'''
Author :
    * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com>
Usage:
    $ python3 benchmark.py -h/--help
'''

import os
from subprocess import call, Popen, PIPE

try:
    import centres.clusters as clusters
except ModuleNotFoundError:
    import sys
    sys.path.append('..')
    import centres.clusters as clusters

import settings
from utilities.display import Display


class Inspect:
    def __init__(self, *, args):
        self.args = args
        self.__inspect()

    def __inspect(self):
        hostname = os.popen('echo $HOSTNAME').read()

        # Testing ...
        # hostname = 'tegner'
        for cluster in settings.CLUSTERS:
            if cluster.lower() in hostname:
                Display.title(
                    title='Inspecting Submitted Jobs on {0}'.format(cluster)
                )
                #  setting the cluster
                self.cluster = cluster

                # call inspect method from cluster to inspect the submitted jobs
                getattr(clusters, self.cluster).inspect()

            break
