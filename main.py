from openpyxl import load_workbook  # nevie pracovat so starym xls
import xlrd  # toto pracuje so starym xls
import datetime  # na konverziu xls datumov do normalneho formatu
import xmltodict  # na konverziu medzi pythonom a xls stringami
import sys   # na nahravanie suborov do programu ako argumentov
from output.save_tools import SaveTools  # nastroje na manipulaciu so subormi
from mods.identifikacia_mods import identifikacia_mods


def multiple_rows(wb, sh):
	'''
	Function to process multiple rows of data within one sheet.
	param1::: wb - workbook openpyxl. object
	param2::: sh - sheet
	return::: list of rows with data in dictionaries
	'''
	multiple = list()
	for row in range(1, sh.nrows):
		# print('DATA_ROW : ', row, sh[row])
		row_value = get_values_from_row(wb,sh, row)
		multiple.append(row_value)
	return multiple


def process_single_row(wb, sh):
	'''
	Function to process multiple rows of data within one sheet.
	param1::: wb - workbook openpyxl. object
	param2::: sh - sheet
	return::: data in dictoionary

	'''
	# print('DATA_ROW : ', 1, sh[0])
	row_value = get_values_from_row(wb,sh, 0)
	# print(row_value)
	return row_value


def get_values_from_row(wb, sh, row):
	'''
	Function extracts data from given row from given sheet. Automatically reads COLUMNS and makes them to keys in result 
	Dictionary b1
	param1::: wb - workbook from XLS file
	param2::: sh - sheet to extract data from
	param3::: row - specific row containig data
	return::: b1 - dict prepared to XML conversion
	'''
	b1 = dict()
	for rx in range(sh.ncols):
		# print("COLUMN : ", rx)
		# print(rx, type(sh.col(rx)[row]), dir(sh.col(rx)[row]))
		# print(sh.col(rx)[row].ctype)  # zistujeme co sa v bunke nachadza
			

    	# Automaticka konverzia z xlsdate do datumu

		if sh.col(rx)[row].ctype == 3:  # tento kod 3 znamena ze ide o xldate
			#print('POZOR KONVERZIA DATUMU')
			excel_date = sh.col(rx)[1].value
			#print(excel_date)
			python_date = datetime.datetime(*xlrd.xldate_as_tuple(excel_date, 0))
			#print(python_date)
			iso_date = python_date.strftime('%Y-%m-%d')
			b1[sh.col(rx)[0].value] = iso_date
		else:
			# TU SA ODSTRANUJE NS1:
			key_name = sh.col(rx)[0].value
			if key_name[0:4] == 'ns1:':
				key_name = key_name[4:]  # ODSTRANUJE ns1:

		b1[key_name] = sh.col(rx)[row].value  # TU ZAPISUJE HODNOTY
			# b1[sh.col(rx)[0].value] = sh.col(rx)[row].value
	# print('ROW DICT :', b1)
	return b1


def get_transactions(wb, sheet):
	# NAHRAVAM DATA DO SLOVNIKA B1  - VSETKY RIADKY
	b1total = list()
	sh = wb.sheet_by_index(sheet)
	# print("MENO TABULKY: {0} \tPOCET RIADKOV: {1} \tPOCET STLPCOV: {2}".format(sh.name, sh.nrows, sh.ncols))
	# print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
	b1 = dict()

	if sh.nrows > 1:  # detekcia viacerich riadkov v tabulke
		# print('MULTIPLE ROWS DETECTED', sh.nrows)
		multiple_list = multiple_rows(wb, sh)

		for rows in multiple_list:
			#process_row_dict(rows)
			pass

		b1total.append(multiple_list)
	else:  # IN CASE ONLY ONE ROW IN SHEET
		print('SINGLE ROW DETECTED', sh.nrows)
		single_row = process_single_row(wb, sh)
		# process_row_dict(single_row)
		b1total.append(single_row)
	# print(b1total)
	return b1total


def process_row_dict(row_dict):  # vypise postupne vsetky hodnoty a ich kluce pre kontrolu
	b1 = row_dict
	for key in b1.keys():
		print("KLUC: {0} \tHODNOTA:  {1}".format(key, b1[key]))
	
def xml_string_conversion(name, part):
	# print("NAME :", name, "\tPART : ", part, "DLZKA ZAZNAMU", len(part[0]))
	for i in part:
		part = {name:i}
		part_output = xmltodict.unparse(part, pretty=True)
		print(part_output)
	# TU SA SPRAVIA POSLEDNE UPRAVY
	#final_id = identifikacia_mods(identifikacia_output)
	# print(final_id)
	return part_output


def transakcie_collector(wb, wb_length):
	'''
	Function takes extracts all data from XLS sheets from sheet 1 to sheet x as dictionaries. But Output need to be saved
	not as tags. Data should be saved as XML arguments in tag nambed by SHEET. So there must be mechanism to convert tags into XML
	arguments with every single key in dictionary should be decorated with @. This changes tags in conversion to args.
	param1::: wb - workbook to convert
	param2::: wb_length - how many sheets should be converted to XML
	return::: 
	'''
	names = iter(wb.sheet_names())
	SAVE.save_xml('\n<Transakcie>\n')
	next(names)
	for sheet in range(1, wb_length):
		sh = wb.sheet_by_index(sheet)
		name = next(names)
		# print('NAZOV LISTU : ', name)
		if sh.nrows == 1:
			print("EMPTY SHEET WITHOUT DATA")
			
			continue
		else:
			#print(sh.nrows, "ROWS")

			# print("TRANSAKCIE LIST :",name)
			transakcie = get_transactions(wb,sheet)
			# print('RAW TRANSAKCIE: ',transakcie)

			for i in transakcie[0]:
				
				prepared_dict = make_argument(i)
			
				# print(name, prepared_dict)

				pure_trans = xmltodict.unparse({name: prepared_dict})
				print(pure_trans)  # TODO Zbav sa popisu XML pri kazdej konverzii
				pure_trans = prepare_final_string(pure_trans)
				SAVE.save_xml(pure_trans)
	SAVE.save_xml('</Transakcie>\n</KVDPH_2023>')
	print('TRANSACTIONS ARE SAVED TO OUTPUT FILE')

'''
MODIFIKACIE DAT 

'''


def make_argument(raw_dict: dict):  # TU SA MENI DATOVA CAST NA XML ARGUMENT  PRIDAJ @ pred kazdy clen
	'''
	Funkcia este pred konverziou na XML prida na vsetky kluce vnutri dictionary @ aby z nich vytvorila XML argumenty
	param1::: raw_dict dict
	return::: prepared_dict kazdy kluc @
	'''
	prepared_dict = dict()
	for key in raw_dict.keys():
		# print(key, raw_dict[key])
		prepared_dict['@'+key] = raw_dict[key]
	del raw_dict
	return prepared_dict


'''
TRANSAKCIE MODS

'''
def prepare_final_string(xml_string: str):
	'''
	Function takes Transactions data and removes all <?xml?> tags to write output file
	param1::: xml_string - raw string to teardown and modify
	return::: clean xml string to write output
	'''
	teardown1 = xml_string.split('><')
	# print('TEARDOWN 1: ',teardown1)
	teardown2 = teardown1[0].split('\n')
	# print('TEARDOWN 2: ',teardown2)
	return teardown2[1] + ' />\n'
	

def get_rid_id_xml(xml_string):
	'''
	Output file is assembled with multiple conversions from multiple dictionaries. Everytime converted string starts with
	<?xml version="1.0" encoding="utf-8"?>. We do need to get rid of them. In this function we are using another methods. 
	Instead of split XML to tags and manipulate them we use SLICING to get rid of unwanted string.
	param1::: xml_string - id xml with <?xml version="1.0" encoding="utf-8"?> at start
	return::: xml_string - id xml without <?xml version="1.0" encoding="utf-8"?>
	'''
	unwanted = '<?xml version="1.0" encoding="utf-8"?>\n'
	piece = len(unwanted)
	if xml_string[:piece] == unwanted:
		xml_string = xml_string[piece:]
		print('UNWANTED REMOVED')
	else:
		print('UNWANTED NOT REMOVED')
	return xml_string


#   M A I N   P R O G R A M M
if __name__ == '__main__':
	if len(sys.argv) == 1:  # ak si ho nepomenujeme inak tak 
		wb = xlrd.open_workbook(filename='KV_test_2023 xml.xls')  # otvara subor XLS

	else:
		if SaveTools.non_existing_file(sys.argv[1]) is True:
			print("FILE NOT FOUND 404")
			quit()
		else:
			wb = xlrd.open_workbook(filename=sys.argv[1])  # otvara subor XLS

	SAVE = SaveTools('output.xml')
	SAVE.erase_file()
	SAVE.save_xml('<?xml version="1.0" encoding="utf-8"?>\n')
	SAVE.save_xml('<KVDPH_2023 xmlns="https://ekr.financnasprava.sk/Formulare/XSD/kv_dph_2023.xsd" xsi:schemaLocation="https://ekr.financnasprava.sk/Formulare/XSD/kv_dph_2023.xsd schema.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n')
	
	# NATAHUJEME IDENTIFIKACIU SUBJEKTU Z XLS
	print("IDENTIFIKACIA")
	id_part = get_transactions(wb,0)
	# print(id_part)
	# HNED TO UKLADAJ AKO XML LEBO INAK SA TO POSERIE
	xml_raw = xml_string_conversion("Identifikacia", id_part)
	# print(xml_raw)
	xml_pure = identifikacia_mods(xml_raw)
	# print('IDENTIFIKACIA PURE STRING :',xml_pure)
	xml_pure = get_rid_id_xml(xml_pure)
	# print('IDENTIFIKACIA PURE STRING :',xml_pure)
	# TODO GET RID OFF <?xml?> before Identification
	SAVE.save_xml(lines=xml_pure)


	# TRANSAKCIE COLLECTOR
	transakcie_collector(wb, 8)  # TODO Get number of sheets

	print("XML BOLO VYGENEROVANE")