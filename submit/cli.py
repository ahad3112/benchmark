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


class JobSubmitCLI:
    '''
    This module will submit job to the queue system
    '''

    # mutually exclusive group option is for possible extension
    mutually_exclusive_groups_name = []
    mutually_exclusive_groups = {}

    args = {
        Argument(
            name=('-d', '--directories'),
            help='DIRECTORIES where to look for job script to submit to the QUEUE system. ' +
            'DIRECTORIES can be provided using ABSOLUTE PATH or RELATIVE to the CURRENT WORKING DIRECTORY. ' +
            f'(default : [\'{settings.DEFAULT_WORKDIR}\',] ).',
            nargs='+',
            default=[settings.DEFAULT_WORKDIR, ]
        ),
        Argument(
            name=('-r', '--recursive'),
            help=f'RECURSIVE looking for JOB SCRIPT within the DIRECTORY named as the CLUSTER name ' +
            ' starting at provided value by option -d/--directories.',
            action='store_true',
            default=False
        ),
        Argument(
            name=('-s', '--suffix'),
            help=f'SUFFIX to be considered for job script. ( default : {settings.DEFAULT_SCRIPT_SUFFIX} ).',
            default=settings.DEFAULT_SCRIPT_SUFFIX
        ),
        Argument(
            name=('-o', '--override'),
            help='Providing this flag means, if script folder contain any file or folder except job script, \
            will be removed. If not provided, will ask for permission at program runtime before running each job script.',
            action='store_true',
            default=False
        ),
    }

    def __init__(self, *, subparsers):
        self.parser = subparsers.add_parser(
            'submit',
            help='SUBMIT JOB SCRIPT to the QUEUE SYSTEM of the CLUSTER where the SCRIPT is being RUN.'
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
