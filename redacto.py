import os
import sys
import json
import argparse

import cv2


def redact_bounded_areas(ARGS):
	'''
	redact text from jpg image based on bounding areas listed in json 
	-- list of files containing lists of dicts containing bounding areas
	   (returned from AWS Textract)
	'''
	print (ARGS.dir)
	print (os.path.sep)
	print(ARGS.bounding)
	bounding = json.load(open('{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.bounding),'r'))
	for f_name, bounding_list in bounding.items():
		print (f_name)
		img = cv2.imread('{}{}{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.in_f, os.path.sep, f_name))
		dim = img.shape
		for area in bounding_list:
			box = area['Polygon']
			left = (box[0]['X'] + box[3]['X'])/2
			right =(box[1]['X'] + box[2]['X'])/2
			height =(box[0]['Y'] + box[2]['Y'])/2
			cv2.line(img,(int(left*dim[1]),int(height*dim[0])),(int(right*dim[1]),int(height*dim[0])),(0,0,0),25)

		cv2.imwrite('{}{}{}{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.out_f, len(bounding_list), os.path.sep, f_name), img)

def parse_arguments(parser):
    parser.add_argument('--dir', type=str, help='base directory',
            default='C:/Users/esilgard/Fred Hutchinson Cancer Research Center/Karlsen, Christine A - Flow Sorts, Binders 1 - 20/Binder 21')
    parser.add_argument('--bounding', type=str, help='name of bounding file - defaults to bounding_areas.json',
            default='bounding_areas.json')
    parser.add_argument('--in_f', type=str, help='input folder containing images (defaults to JPG)',
            default='JPG')
    parser.add_argument('--out_f', type=str, help='output folder *basename* for redacted images (defaults to Redacted \
    	- expects multiple folders for number of redacted areas found (for QA purposes))',
            default='Redacted')
   
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ARGS = parse_arguments(PARSER)
    redact_bounded_areas(ARGS)