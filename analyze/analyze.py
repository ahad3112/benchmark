import os
import glob
import re
import settings
from utilities.display import Display


class PerformanceData:
    # TODO : add nnode to the PerformanceData
    def __init__(self, *, np, ompthreads, nspday, hrpns):
        self.np = np
        self.ompthreads = ompthreads
        self.nspday = nspday
        self.hrpns = hrpns

    def __str__(self):
        return '{np:>5}{ompthreads:>5}{nspday:>8}{hrpns:>8}'.format(np=self.np,
                                                                    ompthreads=self.ompthreads,
                                                                    nspday=self.nspday,
                                                                    hrpns=self.hrpns)


class Analyze:
    _performance_data = []
    _options = ['plot', 'csv', 'raw']

    def __init__(self, *, args):
        self.args = args
        self.__generate_performance_data()

        for p_data in self._performance_data:
            print(p_data)

    def raw(self):
        # Print Raw data
        pass

    def csv(self):
        # Generate csv file
        pass

    def plot(self):
        # Plot data
        pass

    def __generate_performance_data(self):
        hostname = os.popen('echo $HOSTNAME').read()
        self.cluster = hostname if hostname in settings.CLUSTERS else 'UNKNOWN CLUSTER'
        Display.title(
            title='Analyzing for {0}'.format(self.cluster)
        )

        for directory in self.args.directories:
            dir_abspath = os.path.abspath(directory)
            log_files = []
            if self.args.recursive:
                for (dirname, dirshere, fileshere) in os.walk(dir_abspath):
                    log_files.extend(glob.glob(os.path.join(dirname, '*.log')))
            else:
                log_files = [log_file for log_file in os.listdir(dir_abspath)]

            for log_file in log_files:
                self.__add_performance_data(log_file=log_file)

    def __add_performance_data(self, *, log_file):
        topology = os.popen('cat {log_file} | grep -i ^Using'.format(log_file=log_file)).read()
        np = eval(re.search(r'Using ([0-9]) MPI processe?', topology).group(1))
        ompthreads = eval(re.search(r'Using ([0-9]) OpenMP thread?', topology).group(1))

        performance = os.popen('cat {log_file} | grep -i ^performance'.format(log_file=log_file)).read().split()

        (nspday, hrpns) = map(eval, (performance[1].strip(), performance[2].strip()))

        self._performance_data.append(PerformanceData(np=np,
                                                      ompthreads=ompthreads,
                                                      nspday=nspday, hrpns=hrpns))
