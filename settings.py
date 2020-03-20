import os
import sys

# Encoding
ENCODING = 'utf-8'

# Home Dorectory
HOME_DIRECTORY = os.path.abspath(sys.path[0])
TEMPLATE_DIRECTORY = os.path.join(HOME_DIRECTORY, 'templates')

# List of Cluster
CLUSTERS = ['Tegner', 'Beskow', ]


# Default values

DEFAULT_SCRIPT_SUFFIX = '.sh'
DEFAULT_SCRIPT_NAME = 'run_test{0}'.format(DEFAULT_SCRIPT_SUFFIX)

DEFAULT_WORKDIR = os.getcwd()

DEFAULT_JOB_NAME = 'jobs'
DEFAULT_MIN_NODES = 1
DEFAULT_MAX_NODES = 1
DEFAULT_MIN_NTASKS_PER_NODE = 1
DEFAULT_MAX_NTASKS_PER_NODE = 3

DEFAULT_WALL_TIME = '01:00:00'

DEFAULT_OUTPUT_FILE_NAME = 'output_file.o'
DEFAULT_ERROR_FILE_NAME = 'error_file.e'


DEFAULT_ARGS = {
    '$gres$': ['# Not Provided'],
    '$modules$': ['# Not Provided'],
    '$envs$': ['# Not Provided'],
    '$memories$': ['# Not Provided'],
    '$simg$': '',
}
