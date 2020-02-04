import os
import sys
import argparse
from dateutil.parser import *
import datetime

import pandas as pd
import numpy as np

def match_sorts(ARGS):
    '''
    match extracted RS numbers and dates to reference sort data
    '''
    extracted = pd.read_csv('{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.data))
    ref = pd.read_excel('{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.ref))

    def get_ret(row):
        # match sort number IFF the date and at least one of the RS numbers matches
        rs_set = row['RAW_RS_NUM'].upper().split(';') + [row['PROCESSED_RS_NUM'].upper()]
        print ('{} - {}'.format(row['SortDate'], rs_set))
        ret = ref.loc[(ref['SortDate'] == row['SortDate']) & \
            ((ref['RSNumDNA'].isin(rs_set)) | (ref['RSNumKi'].isin(rs_set)))]
        if len(set(ret['SortNumSD'])) == 1:
            
            return ret  
    
    extracted.apply(get_ret, axis=1)   
    return extracted


def parse_arguments(parser):
    parser.add_argument('--dir', type=str, help='base directory',
            default='C:/Users/esilgard/Fred Hutchinson Cancer Research Center/Sanchez, Carissa A - SortScanning')
    parser.add_argument('--data', type=str, help='input csv "extracted" data file directory (defaults to extracted_sorts.csv)',
            default='sort samples/extracted_sorts.csv')
    parser.add_argument('--ref', type=str, help='path to csv "reference" file within directory \
            (defaults to "20200129_Reference_Data")',
            default='Reference_Data/20200129_Reference_Data.xlsx')
    parser.add_argument('--out_f', type=str, help='output csv "matched" output sort data (defaults to matched_sorts.csv)',
            default='sort samples/matched_sorts.csv')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ARGS = parse_arguments(PARSER)
    matched_df = match_sorts(ARGS)
    matched_df.to_csv('{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.out_f)
