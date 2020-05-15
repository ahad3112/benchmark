
'''
Author :
    * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com>
Usage:
    $ python3 benchmark.py -h/--help
'''

import os
try:
    from core.arguments import Argument
except ImportError:
    import sys
    sys.path.append('..')
    from core.arguments import Argument

# appending to sys.path in the previous exception handling make sure that
# the following works even we run this file as the top-level script
import settings
from utilities.display import Display


class ScriptTemplateCLI:
    # mutually exclusive group option is for possible extension
    mutually_exclusive_groups_name = []
    mutually_exclusive_groups = {}

    args = [
        Argument(
            name=('-n', '--name'),
            help=f'NAME of the JOB ( default : "{settings.DEFAULT_JOB_NAME}" ).',
            default=settings.DEFAULT_JOB_NAME
        ),
        Argument(
            name=('-c', '--cluster'),
            help='CLUSTER name for which bechmark will be generated.',
            choices=settings.CLUSTERS,
            required=True
        ),
        Argument(
            name=('-p', '--project'),
            help='PROJECT name for the allocation.',
            required=True
        ),
        Argument(
            name=('-wt', '--wall-time'),
            help=f'TIME (approximate) required for the JOB. Format => <hh:mm:ss> . ( default: {settings.DEFAULT_WALL_TIME} )',
            default=settings.DEFAULT_WALL_TIME
        ),
        Argument(
            name=('--min-nodes',),
            help=f'MINIMUN number of NODES ( default : {settings.DEFAULT_MIN_NODES} ).',
            type=int,
            default=settings.DEFAULT_MIN_NODES
        ),
        Argument(
            name=('--max-nodes',),
            help=f'MAXIMUM number of NODES ( default : {settings.DEFAULT_MAX_NODES} )',
            type=int,
            default=settings.DEFAULT_MAX_NODES
        ),
        Argument(
            name=('--min-ntasks-per-node',),
            help=f'MINIMUN number of TASK per NODE ( default : {settings.DEFAULT_MIN_NTASKS_PER_NODE} ).',
            type=int,
            default=settings.DEFAULT_MIN_NTASKS_PER_NODE
        ),
        Argument(
            name=('--max-ntasks-per-node',),
            help=f'MAXIMUM number of TASKS per NODE ( default : {settings.DEFAULT_MAX_NTASKS_PER_NODE} ).',
            type=int,
            default=settings.DEFAULT_MAX_NTASKS_PER_NODE
        ),
        Argument(
            name=('-g', '--gres',),
            help=f'GENERIC resources ( AVAILABLE: {settings.GENERIC_RESOURCES} ).',
            nargs='+',
            default=settings.DEFAULT_ARGS['$gres$']
        ),
        Argument(
            name=('-mem', '--memories',),
            help=f'MEMORY resources ( AVAILABLE: {settings.MEMORY_RESOURCES} ).',
            nargs='+',
            default=settings.DEFAULT_ARGS['$memories$']
        ),
        Argument(
            name=('-o', '--output-file',),
            help=f'OUTPUT file name ( default : {settings.DEFAULT_OUTPUT_FILE_NAME} ).',
            nargs='?',
            default=settings.DEFAULT_OUTPUT_FILE_NAME,
        ),
        Argument(
            name=('-e', '--error-file',),
            help=f'ERROR file name ( default : {settings.DEFAULT_ERROR_FILE_NAME} ).',
            nargs='?',
            default=settings.DEFAULT_ERROR_FILE_NAME,
        ),
        Argument(
            name=('-mod', '--modules',),
            help='MODULES (space separated) to be loaded.',
            nargs='+',
            default=settings.DEFAULT_ARGS['$modules$']
        ),
        Argument(
            name=('-env', '--envs',),
            help='ENV variables as key=value pair within SINGLE(\'\') or DOUBLE QUOTES(\"\"). '  +
            'Do not put spaces before or after = .' +
            '( EXAMPLE : \'PATH=/usr/local/bin:$PATH\' \"LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH\" ).',
            nargs='+',
            metavar='KEY=VALUE',
            default=settings.DEFAULT_ARGS['$envs$']
        ),
        Argument(
            name=('-exe', '--exe'),
            help='EXECUTABLE to be run. ENCLOSED executable and params within single(\'\') or doube quotes(\"\"). \
            ( EXAMPLE: "gmx_mpi mdrun -s topol.tpr )"',
            nargs='+',
            required=True
        ),
        Argument(
            name=('-wd', '--workdir'),
            help=f'WORKDIR, created benchmark will be stored here. \
            If absolute path is not used, current working directory will be prepended. \
            ( default : {settings.DEFAULT_WORKDIR} )',
            default=settings.DEFAULT_WORKDIR
        ),
        Argument(
            name=('--simg',),
            help='ABSOLUTE path to the SINGULARITY IMAGE.',
            type=str,
            default=settings.DEFAULT_ARGS['$simg$']
        ),
        Argument(
            name=('-th', '--threads'),
            help='Set No. of  THREADS per PROCESS.',
            type=str,
        ),
        Argument(
            name=('-gpu', '--gpu'),
            help='ENABLE GPU acceleration.',
            action='store_true',
            default=False
        ),
        Argument(
            name=('--node', ),
            help='Specify if any EXCLUSIVE node to be used for this JOB.' +
            f' ( AVAILABLE: {settings.NODES} ).',
            type=str,
        ),
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

    @staticmethod
    def validate_args(*, args):
        '''
        This method check whether user provided input is consistent with the chosen Cluster
        '''
        # validate walltime
        if len(args.wall_time.split(':')) == 3:
            if not all([tt.isnumeric() for tt in args.wall_time.split(':')]):
                raise RuntimeError('INPUT ERROR ==> Wrong format for -wt/--walltime. Right format is hh:mm:ss')
        else:
            raise RuntimeError('INPUT ERROR ==> Wrong format for -wt/--walltime. Right format is hh:mm:ss')

        # Generic resources
        for gres in args.gres:
            if gres not in settings.DEFAULT_ARGS['$gres$']:
                if gres not in settings.GENERIC_RESOURCES.get(args.cluster, []):
                    raise RuntimeError(f'INPUT ERROR ==> {gres} not GENERIC resoures for CLUSTER {args.cluster} : ' +
                                       f'(AVAILABLE: {settings.GENERIC_RESOURCES[args.cluster]}).')

        # memory resources
        for memory in args.memories:
            if memory not in settings.DEFAULT_ARGS['$memories$']:
                if memory not in settings.MEMORY_RESOURCES.get(args.cluster, []):
                    raise RuntimeError(f'INPUT ERROR ==> {memory} not MEMORY resoures for CLUSTER {args.cluster} : ' +
                                       f'(AVAILABLE: {settings.MEMORY_RESOURCES[args.cluster]}).')

        # TODO: modules

        # singularity image
        if args.simg:
            if not os.path.exists(args.simg):
                raise RuntimeError(f'INPUT ERROR ==> SINGULARITY IMAGE "{args.simg}" does not exist. ' +
                                   'Please provide valid ABSPATH to a SINGULARITY IMAGE.')
            else:
                # TODO : Check that the file is a singularity image file or not
                if not os.path.isfile(args.simg) or not args.simg.endswith('sif'):
                    raise RuntimeError(f'INPUT ERROR ==> Not a SINGULARITY IMAGE file "{args.simg}". ' +
                                       'Please provide valid ABSPATH to a SINGULARITY IMAGE file.')

        # Exclusive Node
        if args.node:
            if args.node not in settings.NODES.get(args.cluster, []):
                raise RuntimeError(f'INPUT ERROR ==> NODE {args.node} is not available in the CLUSTER {args.cluster} : ' +
                                   f'( Available NODES for {args.cluster} are {settings.NODES.get(args.cluster, [])}).')
