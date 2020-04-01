try:
    from core.arguments import Argument
except ImportError:
    import sys
    sys.path.append('..')
    from core.arguments import Argument

# appending to sys.path in the previous exception handling make sure that
# the following works even we run this file as the top-level script
import settings


class ScriptTemplateCLI:
    # mutually exclusive group option is for possible extension
    mutually_exclusive_groups_name = []
    mutually_exclusive_groups = {}

    args = [
        Argument(
            name=('-n', '--name'),
            help='Name of the job. Given name will be suffixed with _nnode_ntask. \
            Default is "{0}".'.format(settings.DEFAULT_JOB_NAME),
            default=settings.DEFAULT_JOB_NAME
        ),
        Argument(
            name=('-c', '--clusters'),
            help='Clusters name separated by white space',
            choices=settings.CLUSTERS,
            nargs='+',
            required=True
        ),
        Argument(
            name=('-p', '--project'),
            help='Project name to be charged for the allocation',
            required=True
        ),
        Argument(
            name=('-wt', '--wall-time'),
            help='Approximate time <hh:mm:ss> required for the job. Default is "{0}"'.format(settings.DEFAULT_WALL_TIME),
            default=settings.DEFAULT_WALL_TIME
        ),
        Argument(
            name=('--min-nodes',),
            help='Min number of nodes. Default is "{0}"'.format(settings.DEFAULT_MIN_NODES),
            type=int,
            default=settings.DEFAULT_MIN_NODES
        ),
        Argument(
            name=('--max-nodes',),
            help='Max number of nodes. Default is "{0}"'.format(settings.DEFAULT_MAX_NODES),
            type=int,
            default=settings.DEFAULT_MAX_NODES
        ),
        Argument(
            name=('--min-ntasks-per-node',),
            help='Max number of nodes. Default is "{0}"'.format(settings.DEFAULT_MIN_NTASKS_PER_NODE),
            type=int,
            default=settings.DEFAULT_MIN_NTASKS_PER_NODE
        ),
        Argument(
            name=('--max-ntasks-per-node',),
            help='Max number of nodes. Default is "{0}"'.format(settings.DEFAULT_MAX_NTASKS_PER_NODE),
            type=int,
            default=settings.DEFAULT_MAX_NTASKS_PER_NODE
        ),
        Argument(
            name=('-g', '--gres',),
            help='Generic resources',
            nargs='+',
            default=settings.DEFAULT_ARGS['$gres$']
        ),
        Argument(
            name=('-mem', '--memories',),
            help='Specify Memory resources',
            nargs='+',
            default=settings.DEFAULT_ARGS['$memories$']
        ),
        Argument(
            name=('-o', '--output-file',),
            help='Output file name. Default is "{0}"'.format(settings.DEFAULT_OUTPUT_FILE_NAME),
            nargs='?',
            default=settings.DEFAULT_OUTPUT_FILE_NAME,
        ),
        Argument(
            name=('-e', '--error-file',),
            help='Error file name. Default is "{0}"'.format(settings.DEFAULT_ERROR_FILE_NAME),
            nargs='?',
            default=settings.DEFAULT_ERROR_FILE_NAME,
        ),
        Argument(
            name=('-mod', '--modules',),
            help='List of modules to be loaded.',
            nargs='+',
            default=settings.DEFAULT_ARGS['$modules$']
        ),
        Argument(
            name=('-env', '--envs',),
            help='List of Environment variables as key=value pair within single or double quote. Do not put spaces before or after =.\
            KEY/VALUE with space should be enclosed by single or double quote.',
            nargs='+',
            metavar='KEY=VALUE',
            default=settings.DEFAULT_ARGS['$envs$']
        ),
        Argument(
            name=('-exe', '--exe'),
            help='exe to be run. To avoid some strange behaviour, Enclosed executable and param by single or doube quote. \
            example: "gmx_mmpi mdrun -s topol.tpr"',
            nargs='+',
            required=True
        ),
        Argument(
            name=('-wd', '--workdir'),
            help='Default workdir is the directory from where you execute the tool. \
            If absolute path is not used for any file, it will be considered to be relative to this directory.\
            For this run working directory is: {0}'.format(settings.DEFAULT_WORKDIR),
            default=settings.DEFAULT_WORKDIR
        ),
        Argument(
            name=('-s', '--simg'),
            help='Absolute path of the singularity image where to run executable.',
            type=str,
            default=settings.DEFAULT_ARGS['$simg$']
        ),
        Argument(
            name=('-th', '--threads'),
            help='No of threads per process.',
            type=str,
        ),
        Argument(
            name=('-gpu', '--gpu'),
            help='Enables GPU acceleration',
            action='store_true',
            default=False
        )
    ]

    def __init__(self, *, subparsers):
        self.parser = subparsers.add_parser(
            'create',
            help='Create job scripts'
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
