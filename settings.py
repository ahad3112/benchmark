import os
import sys

# Encoding
ENCODING = 'utf-8'

# Home Dorectory
HOME_DIRECTORY = os.path.abspath(sys.path[0])
DEFAULT_WORKDIR = os.getcwd()
TEMPLATE_DIRECTORY = os.path.join(HOME_DIRECTORY, 'templates')

# List of Cluster
CLUSTERS = ['Tegner', 'Beskow']

# Generic Resources
GENERIC_RESOURCES = {
    'Tegner': ['gpu:K420:1', 'gpu:K80:1', 'gpu:K80:2'],
    'Beskow': [],
}

MEMORY_RESOURCES = {
    'Tegner': ['1000000', '2000000'],
    'Beskow': [],
}

NODES = {
    'Tegner': ['Haswell', ],
    'Beskow': [],
}


# Default values
DEFAULT_ANALYZE_FILE_SUFFIX = '*.log'
DEFAULT_SCRIPT_SUFFIX = '.sh'
DEFAULT_SCRIPT_NAME = 'run_test{0}'.format(DEFAULT_SCRIPT_SUFFIX)

DEFAULT_JOB_NAME = 'job'
DEFAULT_MIN_NODES = 1
DEFAULT_MAX_NODES = 1
DEFAULT_MIN_NTASKS_PER_NODE = 1
DEFAULT_MAX_NTASKS_PER_NODE = 3
DEFAULT_N_THREADS = 6

DEFAULT_WALL_TIME = '01:00:00'

DEFAULT_OUTPUT_FILE_NAME = 'output_file.o'
DEFAULT_ERROR_FILE_NAME = 'error_file.e'


DEFAULT_ARGS = {
    '$gres$': ['# Not Provided'],
    '$modules$': ['# Not Provided'],
    '$envs$': ['# Not Provided'],
    '$memories$': ['# Not Provided'],
    '$node$': '# Not Provided',
    '$simg$': '',
}

# File backup
DEFAULT_FILE_BACKUP_SUFFIX = '_backup'
