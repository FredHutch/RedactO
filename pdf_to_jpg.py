import os
import sys
import argparse

from pdf2image import convert_from_path

def convert_pdf_to_jpgs(ARGS):
    '''
    convert PDFs (potentially w/multiple pages)
    into individual JPG images (one image file per page)
    '''
    for f in os.listdir('{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.in_f)):
        f_name = f.split('.')[0]
        print ('processing {}'.format(f))
        pages = convert_from_path('{}{}{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.in_f, os.path.sep, f))
        print ('{} individual pages'.format(len(pages)))
        p = 1
        for page in pages:
            page.save('{}{}{}{}{}{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.out_f, os.path.sep, f_name, '_', p, '.jpg'), 'JPEG')
            p += 1

def parse_arguments(parser):
    parser.add_argument('--dir', type=str, help='base directory',
            default='C:/Users/esilgard/Fred Hutchinson Cancer Research Center/Sanchez, Carissa A - sort samples')
    parser.add_argument('--in_f', type=str, help='input folder within directory (defaults to PDF)',
            default='PDF')
    parser.add_argument('--out_f', type=str, help='output folder within direcotry (defaults to JPG)',
            default='JPG')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ARGS = parse_arguments(PARSER)
    convert_pdf_to_jpgs(ARGS)
