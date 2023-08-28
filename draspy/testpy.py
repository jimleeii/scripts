import os
import optrd

o = optrd.options(version='10.0.0.10', help='This is a test', parameters={'-i': '--install', '-u': '--uninstall'})
print(optrd.read(o))