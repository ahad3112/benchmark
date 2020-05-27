'''
Author :
    * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com>
Usage:
    $ python3 benchmark.py -h/--help
'''

import sys
try:
    from core.arguments import Argument
except ImportError:
    import sys
    sys.path.append('..')
    from core.arguments import Argument

import settings


class PerformanceAnalyzeCLI:
    '''
    This module will submit job to the queue system
    '''

    # mutually exclusive group option is for possible extension
    mutually_exclusive_groups_name = []
    mutually_exclusive_groups = {}

    args = {
        Argument(
            name=('-dt', '--dir-tag'),
            help=f'directory: where to look for LOG FILES. ' +
            'DIRECTORIES can be provided using ABSOLUTE PATH or RELATIVE to the CURRENT WORKING DIRECTORY. ' +
            '( default : {settings.DEFAULT_WORKDIR} ). Tag: will be used as hue during plot.',
            metavar='directory:tag',
            nargs='+',
            default=[settings.DEFAULT_WORKDIR, ]
        ),
        Argument(
            name=('-r', '--recursive'),
            help=f'RECURSIVE looking for LOG FILES ' +
            'within the DIRECTORY/DIRECTORIES provided for option -d/--directories. ',
            action='store_true',
            default=False
        ),
        Argument(
            name=('-s', '--suffix'),
            help=f'SUFFIX to be considered as LOG FILE to be ANALYZED. ( default : {settings.DEFAULT_ANALYZE_FILE_SUFFIX} ).',
            default=settings.DEFAULT_ANALYZE_FILE_SUFFIX
        ),
        Argument(
            name=('--view',),
            help='VIEW performance data.',
            action='store_true',
            default=False
        ),
        Argument(
            name=('--plot',),
            help='PLOT performance data.',
            action='store_true',
            default=False
        ),
        Argument(
            name=('--csv',),
            help='WRITE performance data to CSV file.',
            action='store_true',
            default=False
        ),
        Argument(
            name=('-f', '--file',),
            help='FILE name where CSV data will be written. ' +
            'If ABSOLUTE PATH is not given, CURRENT WORKING DIRECTORY will be APPENDED.',
            type=str,
        ),
    }

    def __init__(self, *, subparsers):
        self.parser = subparsers.add_parser(
            'analyze',
            help='ANALYZE the performance of the FINISHED JOBS for the CLUSTER where the SCRIPT is being RUN.'
        )

        self.__add_mutually_exclusive_groups()
        self.__add_arguments()

    def __add_arguments(self):
        for arg in self.args:
            if arg.action in ['store_true', 'store_false']:
                self.parser.add_argument(
                    *arg.name,
                    help=arg.help,
                    action=arg.action,
                    required=arg.required,
                    default=arg.default,
                )
            else:
                self.parser.add_argument(
                    *arg.name,
                    help=arg.help,
                    choices=arg.choices,
                    action=arg.action,
                    type=arg.type,
                    nargs=arg.nargs,
                    required=arg.required,
                    metavar=arg.metavar,
                    default=arg.default,
                )

    def __add_mutually_exclusive_groups(self):
        for group_name in self.mutually_exclusive_groups_name:
            self.mutually_exclusive_groups[group_name] = self.parser.add_mutually_exclusive_group()
            print('Group : {0} has been added to {1}'.format(group_name, self.__class__.__name__))
