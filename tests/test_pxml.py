import xlrd

from main import *


TEST_FILE =  xlrd.open_workbook(filename='KV_test_2023 xml.xls')


def test_make_argument():
	raw_xml = {'key':'ALPHA', 'key2':'BETA'}
	assert type(make_argument(raw_xml)) == type({})
	assert make_argument(raw_xml) == {'@key':'ALPHA', '@key2':'BETA'}


def test_multiple_rows():
	sh = TEST_FILE.sheet_by_index(1)
	assert type(multiple_rows(TEST_FILE, sh)) == type(list())
	assert multiple_rows(TEST_FILE,sh) == [{'Odb': 'SK4020174642', 'F': 44986.0, 'Den': '2023-03-01', 'Z': 100.0, 'D': 20.0, 'S': 20.0, 'KOpr': ''}, {'Odb': 'SK4020174642', 'F': 44987.0, 'Den': '2023-03-01', 'Z': 200.0, 'D': 40.0, 'S': 20.0, 'KOpr': ''}]


def test_single_row():
	pass


def test_teardown():
	text = '<xml>\n<atribut alpha=432, beta=543></atribut>\n</xml>'
	assert prepare_final_string(text) == '<atribut alpha=432, beta=543 />\n'

def test_get_rid_id_xml():
	text = '<?xml version="1.0" encoding="utf-8"?>\n<Identifikacia>'
	assert type(get_rid_id_xml(text)) == type(str())
	assert get_rid_id_xml(text) == '<Identifikacia>'
	assert get_rid_id_xml('<?xml version="1.0" encoding="utf-8"?>\n') == ''