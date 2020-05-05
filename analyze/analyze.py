import os
import settings
from utilities.display import Display


class PerformanceData:
    def __init__(self, *, nnode, np, nthreads, nspday, hrpns):
        self.nnode = nnode
        self.np = np
        self.nthreads = nthreads
        self.nspday = nspday
        self.hrpns = hrpns

class Analyze:
    _performance_data = []
    def __init__(self, *, args):
        self.args = args
        self.__generate_performance_data()

    def __generate_performance_data(self):
        hostname = os.popen('echo $HOSTNAME').read()
        for cluster in settings.CLUSTERS:
            if cluster.lower() in hostname:
                Display.title(
                    title='Analyzing for {0}'.format(cluster)
                )
                #  setting the cluster
                self.cluster = cluster

                for directory in self.args.directories:
                    dir_abspath = os.path.abspath(directory)
                    if self.args.recursive:
                        self.__collect_data_recursively(directory=dir_abspath)
                    else:
                        fileshere = os.listdir(dir_abspath)
                        for log in fileshere:
                            if file.endswith(self.args.suffix):
                                self.__add_data(log=log)
                break


    def __collect_data_recursively(self, *, directory):
        for (dirname, dirshere, fileshere) in os.walk(directory):
            if os.path.split(dirname)[1] == self.cluster:
                for (subdirname, subdirshere, subfileshere) in os.walk(dirname):
                    for log in subfileshere:
                        if log.endswith(self.args.suffix):
                            self.__add_data(log=log)

    def __add_data(self, *, log):
        pipe = os.popen('cat {log} | grep -i Using'.format(log=log))
        print(pipe.read())

