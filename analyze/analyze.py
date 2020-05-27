'''
Author :
    * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com>
Usage:
    $ python3 benchmark.py -h/--help
'''


import pandas as pd
import numpy as np
import matplotlib

# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns

import os
import glob
import re
import settings
from utilities.display import Display


class PerformanceData:
    # TODO : add nnode to the PerformanceData
    def __init__(self, *, np, ompthreads, nspday, hrpns, tag=''):
        self.np = np
        self.ompthreads = ompthreads
        self.nspday = nspday
        self.hrpns = hrpns
        self.tag = tag

    def __str__(self):
        return '{np:>5}{ompthreads:>5}{nspday:>8}{hrpns:>8}{tag:>8}'.format(np=self.np,
                                                                            ompthreads=self.ompthreads,
                                                                            nspday=self.nspday,
                                                                            tag=self.tag)


class Analyze:
    _performance_data = []
    _options = ['plot', 'csv', 'view']

    def __init__(self, *, args):
        self.args = args
        self.__generate_performance_data()
        for option in self._options:
            if getattr(self.args, option):
                getattr(self, option)()

    def view(self):
        headers = ['np', 'omthreads', 'ns/day', 'hr/ns', 'tag']
        print(f'{headers[0]:>10}\t{headers[1]:>10}\t{headers[2]:>10}\t{headers[3]:>10}\t{headers[4]:>10}')
        for performance_data in self._performance_data:
            print(f'{performance_data.np:>10}\t{performance_data.ompthreads:>10}\t{performance_data.nspday:>10}\t{performance_data.hrpns:>10}\t{performance_data.tag:>10}')

    def csv(self):
        '''
        This method generate csv file
        '''
        file_name = os.path.abspath(self.args.file) if self.args.file else os.path.join(os.getcwd(), f'{self.cluster}.csv')
        self.__dataframe().to_csv(file_name)

        print(f'Performance data is stored in {file_name}')

    def plot(self):
        '''
        Plot Performance data using sns pointplot
        '''
        sns.set(style="darkgrid")
        data = self.__dataframe()
        g = sns.pointplot(kind="line",
                          x="#processors",
                          y="ns/day",
                          hue="legends",
                          # style="container",
                          markers=['o', 'x'],
                          linestyles=['--', '-'],
                          data=data,
                          # palette="Set2",
                          )
        plt.show()

    def __dataframe(self):
        df = pd.DataFrame({
            '#processors': [p_data.np for p_data in self._performance_data],
            '#ompthreads': [p_data.ompthreads for p_data in self._performance_data],
            'ns/day': [p_data.nspday for p_data in self._performance_data],
            'hr/ns': [p_data.hrpns for p_data in self._performance_data],
            'legends': [p_data.tag for p_data in self._performance_data]
        })

        return df

    def __generate_performance_data(self):
        hostname = os.popen('echo $HOSTNAME').read()
        for cluster in settings.CLUSTERS:
            if cluster.lower() in hostname:
                self.cluster = cluster
                break
        else:
            self.cluster = 'UNKNOWN-CLUSTER'

        Display.title(
            title='Analyzing for {0}'.format(self.cluster)
        )

        for dir_tag in self.args.dir_tag:
            dir_abspath, tag = self.__extract_dir_tag(dir_tag=dir_tag)
            log_files = []
            if self.args.recursive:
                for (dirname, dirshere, fileshere) in os.walk(dir_abspath):
                    log_files.extend(glob.glob(os.path.join(dirname, settings.DEFAULT_ANALYZE_FILE_SUFFIX)))
            else:
                log_files = [log_file for log_file in glob.glob(
                    os.path.join(dir_abspath, settings.DEFAULT_ANALYZE_FILE_SUFFIX))
                ]

            for log_file in log_files:
                self.__add_performance_data(log_file=log_file, tag=tag)

    def __extract_dir_tag(self, *, dir_tag):
        if ':' in dir_tag:
            directory, tag = [x.strip() for x in dir_tag.split(':')]
        else:
            directory = dir_tag.strip()
            print(f'No tag given for directory "{directory}" : Using tag=""')
            tag = ''

        dir_abspath = os.path.abspath(directory)
        if not os.path.exists(dir_abspath):
            raise RuntimeError(f'InputError : {dir_abspath} does not exist.')

        return (dir_abspath, tag)

    def __add_performance_data(self, *, log_file, tag):

        topology = os.popen('cat {log_file} | grep -i ^Using'.format(log_file=log_file)).read()
        performance = os.popen('cat {log_file} | grep -i ^performance'.format(log_file=log_file)).read().split()

        np_match = re.search(r'Using ([0-9]+) MPI processe?', topology)
        ompthreads_match = re.search(r'Using ([0-9]+) OpenMP thread?', topology)

        if np_match is not None:
            np = eval(np_match.group(1))
        else:
            print(f'No match found in log file for np : {log_file}. NOT GROMACS LOG FILE.')
            return
        if ompthreads_match is not None:
            ompthreads = eval(ompthreads_match.group(1))
        else:
            print(f'No match found in log file for ompthreads : {log_file}. NOT GROMACS LOG FILE.')
            return

        if len(performance) == 3:
            (nspday, hrpns) = map(eval, (performance[1].strip(), performance[2].strip()))
        else:
            print(f'No match found in log file for performance : {log_file}. NOT GROMACS LOG FILE.')
            return

        self._performance_data.append(PerformanceData(np=np,
                                                      ompthreads=ompthreads, nspday=nspday,
                                                      hrpns=hrpns, tag=tag))
