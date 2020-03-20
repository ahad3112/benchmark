import os
from subprocess import call, Popen, PIPE

try:
    import centres.clusters as clusters
except ModuleNotFoundError:
    import sys
    sys.path.append('..')
    import centres.clusters as clusters

import settings


class Submit:
    def __init__(self, *, args):
        self.args = args
        self.__submit()

    def __submit(self):
        pipe = Popen('echo $HOSTNAME', stdout=PIPE, shell=True)
        hostname = pipe.communicate()[0]
        # here we will force hostname to have value tegner-login-1.pdc.kth.se
        # hostname = b'tegner-login-1.pdc.kth.se'
        for cluster in settings.CLUSTERS:
            if cluster.lower() in hostname.decode('latin-1'):
                #  setting the cluster
                self.cluster = cluster
                print('Submitting Job to cluster : {0}'.format(cluster))
                for directory in self.args.directories:
                    dir_abspath = os.path.abspath(directory)
                    if self.args.recursive:
                        print('Recursively Looking for folder with name {0} inside {1}.'.format(
                            cluster,
                            os.path.abspath(directory))
                        )
                        self.__recursive_submit(directory=dir_abspath)
                    else:
                        print('Looking for folder in cluster {0} inside {1}'.format(
                            self.cluster,
                            dir_abspath)
                        )
                        contents = os.listdir(dir_abspath)
                        print(contents)
                        for content in contents:
                            if content.endswith(settings.DEFAULT_SCRIPT_SUFFIX):
                                getattr(clusters, self.cluster).submit(directory=dir_abspath, job=content)
                                print('sbatch {0}'.format(content))

                break

    def __recursive_submit(self, *, directory):
        for (dirname, dirshere, fileshere) in os.walk(directory):
            if os.path.split(dirname)[1] == self.cluster:
                for (subdirname, subdirshere, subfileshere) in os.walk(dirname):
                    for job in subfileshere:
                        if job.endswith(settings.DEFAULT_SCRIPT_SUFFIX):
                            getattr(clusters, self.cluster).submit(directory=subdirname, job=job)
