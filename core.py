import numpy as np
import sys
import csv
from dataframe import *
from copy import copy, deepcopy
from obvious import *


class SampleElement(object):
    def __init__(self, name, vals):
        self.name = name
        self.orig_n = len(vals)

        df = Dataframe({'vals': vals, 'idx': np.arange(len(vals))})

        #do some transformations on vals
        df = self.filterStep(df)
        df = self.detrendStep(df)

        #save final df
        self.df = df
        
    @staticmethod
    def filterStep(df):
        mean = np.mean(df.vals)
        std = np.std(df.vals, ddof=1)
        return df[np.abs(df.vals - mean) < 2*std]

    @staticmethod
    def detrendStep(df):
        xs = df.idx - np.mean(df.idx)
        ys = df.vals - np.mean(df.vals)

        reg,_,_,_ = np.linalg.lstsq(xs[:, None], ys )

        res_df = deepcopy(df)
        res_df.vals = res_df.vals - xs * reg[0]
        return res_df

class Sample(object):
    pass


df = Dataframe({'a': np.array([1,2,3])})

with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    lines = []
    for xs in reader:
        lines.append(xs)
    
    (header_idx, header_str), = [(a,b) for a,b in enumerate(lines) if b[0] == 'Int.Nr']
    footer_idx = [a for a,b in enumerate(lines) if b[0] == '***' and a>header_idx][0]

    good_lines = lines[header_idx+1:footer_idx]

    elements = []

    for element_idx, element_id in enumerate(header_str):
        if element_id not in ['Int.Nr','Time','']:
            vals = np.array([float(x[element_idx]) for x in good_lines if x[element_idx] != ''])
            elements.append(SampleElement(element_id, vals))

    ##############################

    final = Dataframe(OrderedDict([
        ('name', np.array([x.name for x in elements])),
        ('mean', np.array([np.mean(x.df.vals) for x in elements])),
        ('2dev', np.array([np.std(x.df.vals, ddof=1) for x in elements])),
        ('n', np.array([len(x.df) for x in elements]))
    ]))

    final_rows = [','.join(k for k,v in final.items())]
    for i in xrange(len(final)):
        final_rows.append(','.join(str(v[i]) for k,v in final.items()))


    with open(sys.argv[2], 'w') as f:
        for x in final_rows:
            print>>f, x
