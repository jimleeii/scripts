# Helps read inputs from python script.
# Passes in version information and help description for python script usage.
# Passes in input options for python script to read in CLS.
# Returns a dictionary of input options and values.

import getopt, sys
from os import replace

class Parameters:
    def __init__(self, short=None, long=None, variable=None, descrption=None):
        self.short = short
        self.long = long
        self.variable = variable
        self.description = descrption

class Options:
    def __init__(self, version=None, help=None, parameters=None):
        self.version = version
        self.help = help
        self.params = parameters

def read(o=Options()):
    ver = o.version
    hel = o.help

    helpOption = {'-h': '--help'}
    versionOption = {'-v': '--version'}

    options = o.params

    shorts = ''.join(helpOption.keys()) + ''.join(versionOption.keys()) + ':'.join(options.keys()) + ':'
    shorts = shorts.replace('-', '')

    longs = []
    longs.append(helpOption['-h'].replace('--', ''))
    longs.append(versionOption['-v'].replace('--', ''))
    for o in list(options.values()):
        longs.append(o.replace('--', '') + '=')

    try:
        opts, args = getopt.getopt(sys.argv[1:], shorts, longs)
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        for h in hel:
            print(h)
        sys.exit(2)

    helopt = helpOption.popitem()
    veropt = versionOption.popitem()

    for o, a in opts:
        if o in veropt:
            print(ver)
            sys.exit()
        elif o in helopt:
            for h in hel:
                print(h)
            sys.exit()

    output = {}

    while len(options) > 0:
        item = options.popitem()
        for o, a in opts:
            if o in item:
                output.update({o:a})
                break

    return output