#!/usr/bin/env python

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
        title='Available Modules',
        description='Generate Job Script, submit jobss to the Queue System, \
        analyze the results',
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
