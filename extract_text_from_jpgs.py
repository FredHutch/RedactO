import json
import sys
import os
import re
import argparse

import boto3


def parse_arguments(parser):
    parser.add_argument('--dir', type=str, help='base directory',
            default='C:/Users/esilgard/Fred Hutchinson Cancer Research Center/Karlsen, Christine A - Flow Sorts, Binders 1 - 20/Binder 21')
    parser.add_argument('--config', type=str, help='name of config file containing aws account info - defaults to config.json',
            default='config.json')
    parser.add_argument('--in_f', type=str, help='input folder containing images (defaults to JPG)',
            default='JPG')
    parser.add_argument('--out_f', type=str, help='output folder for text files (defaults to TXT)',
            default='TXT')
    parser.add_argument('--bounding', type=str, help='name of output bounding file - defaults to bounding_areas.json',
            default='bounding_areas_v2.json')
   
    args = parser.parse_args()
    return args

def get_aws_client(ARGS):
    '''
    aws account details stored separately in config file 
    '''
    config = json.load(open(ARGS.config,'r'))
    session = boto3.Session(profile_name=config['profile_name'])
    client = session.client(
             service_name='textract',
             region_name= 'us-west-1',
             endpoint_url='https://textract.us-west-1.amazonaws.com',
    )

    return client

def textract_detect_text_from_jpg(ARGS):
    client = get_aws_client(ARGS)
    bounding_areas = {}
    # use textract OCR to extract text from jpg images
    for f in os.listdir('{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.in_f)):
        print (f)
        base_name = f.split('.')[0]

        with open('{}{}{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.in_f, os.path.sep, f), 'rb') as file:
            image_test = file.read()
            bytes_test = bytearray(image_test)
        response = client.detect_document_text(Document={'Bytes': bytes_test})
        
        #Get the text blocks
        blocks=response['Blocks']
        text = ''
        bounding_areas[f] = []
        grab_next = False
        last_line = ''
        # print out text, capture bounding box for redaction
        # note this pattern is specific to the Ried lab Sorts documents
        for block in blocks:                   
            if block['BlockType'] == 'LINE':
                text += block['Text'] + '\n'            
                # restrict to capture areas are to the left of the page
                if block['Geometry']['BoundingBox']['Left'] < .3:
                    if grab_next:
                        bounding_areas[f].append(block['Geometry'])               
                        print ('grab next {}'.format(block['Text']))
                        grab_next = False
                    if 'NUMBER' in block['Text'] and \
                        ('SAMPLE' in block['Text'] or 'SAMPLE' in last_line):
                        if re.search('NUMBER[\s]*:[\s]*[A-Z]+', block['Text']):
                            bounding_areas[f].append(block['Geometry']) 
                            print ('grab same {}'.format(block['Text']))
                        else:
                            grab_next = True

                    last_line = block['Text']  
        with open('{}{}{}{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.out_f, os.path.sep, base_name, '.txt'),'w') as out:
            out.write(text)     

    json.dump(bounding_areas,open('{}{}{}'.format(ARGS.dir, os.path.sep, ARGS.bounding),'w'), indent=4, separators=(',', ':'))

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ARGS = parse_arguments(PARSER)
    textract_detect_text_from_jpg(ARGS)  

         
    
    
