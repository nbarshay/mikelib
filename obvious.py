#ll__  is everything! Be afraid.

import os
import sys
import itertools
from itertools import chain
import argparse
from collections import OrderedDict, defaultdict, namedtuple, deque
from functools import total_ordering, partial
import re
from copy import copy, deepcopy
import types
import math
import operator
import numpy as np
import subprocess
import glob
import shutil
import json
from StringIO import StringIO

def funnel(xs, eq=operator.eq):
    it = iter(xs)
    ret = it.next()
    assert all( eq(x, ret) for x in it)
    return ret

def concat(xs):
    res = []
    for x in xs:
        res.extend(x)
    return res

def singlify(l):
    assert(len(l) == 1)
    return l[0]

def sortUnique(l):
    return sorted(list(set(l)))

#################

def dSet(d, k, v):
    assert k not in d
    d[k] = v

def dUpdate(d, other):
    for k,v in other.iteritems():
        dSet(d, k, v)

def dWith(d, k, v):
    r = copy(d)
    dSet(r, k, v)
    return r

def dMerge(xs, t=dict):
    r = t()
    for x in xs:
        dUpdate(r, x)
    return r

def dCreate(xs, t=dict):
    r = t()
    for k,v in xs:
        dSet(r, k, v)
    return r
