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


class JobInspectCLI:
    '''
    This module will submit job to the queue system
    '''

    # mutually exclusive group option is for possible extension
    mutually_exclusive_groups_name = []
    mutually_exclusive_groups = {}

    args = {
        Argument(
            name=('-s', '--status'),
            help='STATUS of the SUBMITTED JOBS to the QUEUE SYSTEM.',
            action='store_true',
            default=True
        ),
        # Argument(
        #     name=('-c', '--cancel'),
        #     help='Cancel job/jobs',
        #     action='store_true',
        #     default=True
        # ),

    }

    def __init__(self, *, subparsers):
        self.parser = subparsers.add_parser(
            'inspect',
            help='INSPECT JOBS submitted to the QUEUE SYSTEM of the CLUSTER where the SCRIPT is being RUN'
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
