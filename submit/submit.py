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


class Submit:
    def __init__(self, *, args):
        self.args = args
        self.__submit()

    def __submit(self):
        hostname = os.popen('echo $HOSTNAME').read()
        # print(hostname)
        # here we will force hostname to have value tegner-login-1.pdc.kth.se
        # hostname = 'tegner-login-1.pdc.kth.se'
        #  Remove it later after testing...
        # hostname = 'tegner'.lower()

        for cluster in settings.CLUSTERS:
            if cluster.lower() in hostname:
                Display.title(
                    title='Submitting Job to {0}'.format(cluster)
                )
                #  setting the cluster
                self.cluster = cluster

                for directory in self.args.directories:
                    dir_abspath = os.path.abspath(directory)
                    if self.args.recursive:
                        Display.info(
                            what='{0} '.format(os.path.abspath(directory)),
                            info=' [ Submitting Recursively ]',
                            fill='-'
                        )
                        self.__recursive_submit(directory=dir_abspath)
                    else:
                        Display.info(
                            what='{0} '.format(dir_abspath),
                            info=' [ No Recursive Submitting]',
                            fill='-'
                        )
                        contents = os.listdir(dir_abspath)
                        for content in contents:
                            if content.endswith(self.args.suffix):
                                getattr(clusters, self.cluster).submit(directory=dir_abspath, job=content)

                break

    def __recursive_submit(self, *, directory):
        for (dirname, dirshere, fileshere) in os.walk(directory):
            if os.path.split(dirname)[1] == self.cluster:
                for (subdirname, subdirshere, subfileshere) in os.walk(dirname):
                    for job in subfileshere:
                        if job.endswith(self.args.suffix):
                            getattr(clusters, self.cluster).submit(directory=subdirname, job=job)
