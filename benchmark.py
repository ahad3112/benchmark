#!/usr/bin/env python
'''
Author :
    * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com>
Usage:
    $ python3 benchmark.py -h/--help
'''


import argparse
import sys
import os

# projcet internal module
from create.cli import ScriptTemplateCLI
from submit.cli import JobSubmitCLI
from create.create import Create
from submit.submit import Submit
from inspects.cli import JobInspectCLI
from inspects.inspect import Inspect
from analyze.cli import PerformanceAnalyzeCLI
from analyze.analyze import Analyze
import centres.clusters as clusters


def cli():
    parser = argparse.ArgumentParser(
        prog=os.path.splitext(os.path.split(sys.argv[0])[1])[0],
    )

    subparsers = parser.add_subparsers(
        title='AVAILABLE SUB-MODULES',
        description='CREATE JOB SCRIPT, SUBMIT JOBS to the QUEUE SYSTEM, ' +
        'INSPECT submitted JOBS and ANALYZE the PERFORMANCE results.'
    )

    # add parser related to scripts
    ScriptTemplateCLI(subparsers=subparsers)
    JobSubmitCLI(subparsers=subparsers)
    JobInspectCLI(subparsers=subparsers)
    PerformanceAnalyzeCLI(subparsers=subparsers)

    args = parser.parse_args()

    return args


def action(*, args):
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'create':
            # need to check user provided input and give the user feedback if wring input provided
            ScriptTemplateCLI.validate_args(args=args)
            Create(args=args)
        elif sys.argv[1] == 'submit':
            Submit(args=args)
        elif sys.argv[1] == 'inspect':
            Inspect(args=args)
        elif sys.argv[1] == 'analyze':
            Analyze(args=args)


if __name__ == '__main__':
    args = cli()
    action(args=args)
