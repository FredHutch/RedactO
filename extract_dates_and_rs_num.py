import os
import re
import csv
from dateutil.parser import *
import datetime

base_path = 'C:/Users/esilgard/Fred Hutchinson Cancer Research Center/Karlsen, Christine A - Flow Sorts, Binders 1 - 20/Binder 21'

def get_other_date_format(text):
	raw_date_list = []
	date_list = []
	date = re.findall('(([0-9]{1,2})[//1]([0-9]{1,2})[//1]([0-9]{2,4}))', text, re.MULTILINE)
	for d in date:
		raw_date_list.append(d)
		try:
			date_list.append(parse(d[0]))
		except:
			pass
	return raw_date_list, date_list


def get_new_rs_num_format(text):
	# match text like :    SAMPLE NAME : RS22JUN00.28
	return re.findall('SAMPLE NAME[\s]*:[\s]*(RS([\dBOoS]{1,2})([A-Z0]{3,4})([\d]{2})?[\.][\s]?([\dBOoS]+))', text, re.MULTILINE)


def get_other_rs_num_format(text):
	# match text like :   03/08/2007 ; rs08ma07.010 -ds15c11
	return re.findall('(rs([\dBOoS]{1,2})([a-z]{2})([\dBOoS]{2})[\s]?[\.][\s]?([\dBOoS]+))[\s]*[\-]', text, re.MULTILINE)


def get_new_date_format(text):
	raw_date_list = []
	date_list = []
	date = re.findall('SAMPLE DATE[\s]*:[\s]*(([\dBOoS]{1,2})([A-Z0][a-z10O]{2,3})([\dBOoS]{2,4}))', text, re.MULTILINE)
	for d in date:
		day = d[1].replace('B','8').replace('O','0').replace('o','0').replace('l','1').replace('S','5')
		month = d[2].replace('1','l').replace('0','o')
		year = d[3].replace('B','8').replace('O','0').replace('o','0').replace('l','1').replace('S','5')
		# special case for Nov
		if month[-1] == 'u': 
			month = month.replace('u','v')
		raw_date_list.append(d)
		try:
			date_list.append(parse(day + month + year))
		except:
			## the regex matched but the date is unparsable
			pass

	return raw_date_list, date_list

## loop through text files and extract dates and rs numbers	/
sort_d = {}
for file in os.listdir(base_path + os.path.sep + 'TXT'):
	sort_d[file] = dict.fromkeys(['PROCESSED_DATE','PROCESSED_RS_NUM','DATE_QA','RS_QA','RAW_DATE','RAW_RS_NUM'])
	text = open('{}{}{}{}{}'.format(base_path, os.path.sep,'TXT', os.path.sep, file),'r').read()
	print ('{} {}'.format(file,len(text)))

	##################################### DATES #####################################
	
	raw_date_list, date_list = get_new_date_format(text)
	## check for alternate formats
	if not raw_date_list:
		raw_date_list, date_list = get_other_date_format(text)

	if raw_date_list:
		sort_d[file]['RAW_DATE'] = ';'.join([y[0] for y in raw_date_list])
	if date_list:
		sort_d[file]['PROCESSED_DATE'] = date_list[0].strftime("%m/%d/%Y")
	if len(date_list) > 1 and len(set(date_list)) == 1:
		sort_d[file]['DATE_QA'] = 'DATE MATCH'
	else:		
		sort_d[file]['DATE_QA'] = 'DATE QA SUGGESTED'

	##################################### RS NUMS ###################################
	old_version = False
	rs_nums = get_new_rs_num_format(text)
	if not rs_nums:
		rs_nums = get_other_rs_num_format(text)
		old_version = True
	rs_num_list = []
	rs_parse_date = None
	for r in rs_nums:

		day = r[1].replace('B','8').replace('O','0').replace('o','0').replace('S','5')
		month = r[2].replace('0','O')
		year = ''
		# sometimes year isn't there and this is an empty capture group
		year = r[3]
		# special case for Nov
		if month[-1] == 'U': month = month.replace('U','V')
		specimen_num = r[-1].replace('B','8').replace('O','0').replace('o','0').replace('S','5')
		if old_version:
			month = month.replace('ma','mar').replace('oc','oct').replace('se','sep').replace('no','nov').\
						  replace('ja','jan').replace('de','dec').replace('fe','feb').replace('ap','apr')
		processed_rs = 'RS' + day + month + year
		processed_rs += '.' + specimen_num
		rs_num_list.append(r)
		try:
			rs_parse_date = parse(processed_rs.strip('RS').strip('rs').split('.')[0])
		except:
			rs_parse_date = None
		sort_d[file]['PROCESSED_RS_NUM'] = processed_rs
	if rs_num_list:
		sort_d[file]['RAW_RS_NUM'] = re.sub('[\s]','',';'.join([rs[0] for rs in rs_num_list]))
	
	if rs_parse_date and sort_d[file]['PROCESSED_DATE'] and \
		rs_parse_date.day == parse(sort_d[file]['PROCESSED_DATE']).day and \
		(rs_parse_date.month == parse(sort_d[file]['PROCESSED_DATE']).month or \
		rs_parse_date.year == parse(sort_d[file]['PROCESSED_DATE']).year):
			sort_d[file]['RS_QA'] = 'RS MATCH'
	else:
		sort_d[file]['RS_QA'] = 'RS QA SUGGESTED'




## write to file
headers = ['SORT_IMG'] + sorted(['PROCESSED_DATE','PROCESSED_RS_NUM','DATE_QA',\
		'RS_QA','RAW_DATE','RAW_RS_NUM'])
with open('{}{}{}'.format(base_path, os.path.sep,'extracted_sorts.csv'), 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(headers)
    for key in sort_d:
        csvwriter.writerow(([key] + [sort_d[key][i] for i in headers[1:]]))


