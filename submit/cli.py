import sys
try:
    from core.arguments import Argument
except ModuleNotFoundError:
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
            help='Directories where to look for job script. Required at least on directory. \
            Directory can be provided using absolute path or relative to current working directory. \
            Default is current working directory. {0}'.format(settings.DEFAULT_WORKDIR),
            nargs='+',
            default=[settings.DEFAULT_WORKDIR, ]
        ),
        Argument(
            name=('-r', '--recursive'),
            help='Will look recursively for directories with the Cluster name and will submit all job.',
            action='store_true',
            default=False
        ),
        Argument(
            name=('-s', '--suffix'),
            help='File having suffix will be considered as job script. Default is {0}'.format(
                settings.DEFAULT_SCRIPT_SUFFIX
            ),
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
            help='Sumit job script to the queue system'
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
