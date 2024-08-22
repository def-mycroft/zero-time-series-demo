#!/usr/bin/env python

import os
import argparse
import sys
import json
from os.path import exists, dirname, basename, join, expanduser
from glob import glob
import pandas as pd
import numpy as np


HELP_PARAGRAPHS = {
    'main':'an example cli tool',
    'prep': {
        'main':'setup project for analysis',
        'model-data-pipeline':'download data and prep model input data. Same as -dpm.',
        'download-base-data':'download model input data, raw. ',
        'prep-base-data':'after downloading, apply basic prep steps and archive.',
        'prep-model-data':'setup prediction data.',
    },
    'level2': {
        'main':'level 2',
        'third-thing':'docs for third thing',
        'fourth-thing':'docs for fourth thing',
    },
}


def main():
    parser = argparse.ArgumentParser(description=HELP_PARAGRAPHS['main'])
    subparsers = parser.add_subparsers(dest='command', help='')

    h = HELP_PARAGRAPHS['prep']
    parser_corpus = subparsers.add_parser('prep', help=h['main'])
    parser_corpus.add_argument('--model-data-pipeline', '-l', required=False,
                               action='store_true',
                               help=h['model-data-pipeline'])
    parser_corpus.add_argument('--download-base-data', '-d', required=False,
                               action='store_true',
                               help=h['download-base-data'])
    parser_corpus.add_argument('--prep-base-data', '-p', required=False,
                               action='store_true',
                               help=h['prep-base-data'])
    parser_corpus.add_argument('--prep-model-data', '-m', required=False,
                               action='store_true',
                               help=h['prep-model-data'])

    h = HELP_PARAGRAPHS['level2']
    parser_summ = subparsers.add_parser('level2', help=h['main'])
    parser_summ.add_argument('--third-thing', '-t', required=False,
                             default=False, action='store_true',
                             help=h['third-thing'])
    parser_summ.add_argument('--fourth-thing', '-f', required=False,
                             default=False, action='store_true',
                             help=h['fourth-thing'])
    args = parser.parse_args()

    if args.command == 'prep':
        if args.model_data_pipeline:
            args.download_base_data = True
            args.prep_base_data = True
            args.prep_model_data = True
        if args.download_base_data:
            from zero_ts_demo import retrieve_data as rd
            rd.retrieve_data()
        if args.prep_base_data:
            from zero_ts_demo import prep_data as prd
            prd.prep_write()
        if args.prep_model_data:
            from zero_ts_demo import prep_model_data as pmd
            pmd.prep_write()

    elif args.command == 'level2':
        if args.third_thing:
            print('3rd')
        elif args.fourth_thing:
            print('4th')

if __name__ == '__main__':
    main()
