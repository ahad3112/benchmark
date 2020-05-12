# ???????????????????????????????????????????
# Trying setting type=None..will change to str if any problem arised


'''
Author :
    * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com>
Usage:
    $ python3 benchmark.py -h/--help
'''


class Argument:
    def __init__(self, *, name, type=None, help='help',
                 action=None, choices=None, nargs=None,
                 required=False, metavar=None,
                 default=None, group=None):
        self.name = name
        self.type = type
        self.help = help
        self.action = action
        self.choices = choices
        self.nargs = nargs
        self.required = required
        self.metavar = metavar
        self.default = default
        self.group = group
