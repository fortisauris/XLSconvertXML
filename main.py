from openpyxl import load_workbook  # nevie pracovat so starym xls
import xlrd  # toto pracuje so starym xls
import datetime  # na konverziu xls datumov do normalneho formatu
import xmltodict  # na konverziu medzi pythonom a xls stringami
import sys   # na nahravanie suborov do programu ako argumentov
from output.save_tools import SaveTools  # nastroje na manipulaciu so subormi
from mods.identifikacia_mods import identifikacia_mods


def multiple_rows(wb, sh):
	'''
	Processes multiple rows of data within a given sheet.
	Args:
		wb: The workbook object (openpyxl or xlrd).
		sh: The sheet object to process.
	Returns:
		list: A list of dictionaries, each representing a row of data.
	'''
	multiple = list()
	for row in range(1, sh.nrows):
		# For each row (except header), extract values as a dictionary
		row_value = get_values_from_row(wb, sh, row)
		multiple.append(row_value)
	return multiple


def process_single_row(wb, sh):
	'''
	Processes a single row of data from a given sheet.
	Args:
		wb: The workbook object (openpyxl or xlrd).
		sh: The sheet object to process.
	Returns:
		dict: A dictionary representing the row of data.
	'''
	# Extract the first row as a dictionary
	row_value = get_values_from_row(wb, sh, 0)
	return row_value


def get_values_from_row(wb, sh, row):
	'''
	Extracts data from a specific row in a given sheet.
	Automatically reads columns and uses them as keys in the result dictionary.
	Args:
		wb: The workbook object.
		sh: The sheet object to extract data from.
		row: The row index to extract.
	Returns:
		dict: Dictionary prepared for XML conversion.
	'''
	b1 = dict()
	for rx in range(sh.ncols):
		# For each column in the row
		# If the cell is a date, convert it to ISO format
		if sh.col(rx)[row].ctype == 3:  # 3 means xldate
			excel_date = sh.col(rx)[1].value
			python_date = datetime.datetime(*xlrd.xldate_as_tuple(excel_date, 0))
			iso_date = python_date.strftime('%Y-%m-%d')
			b1[sh.col(rx)[0].value] = iso_date
		else:
			# Remove 'ns1:' prefix from key if present
			key_name = sh.col(rx)[0].value
			if key_name[0:4] == 'ns1:':
				key_name = key_name[4:]
			b1[key_name] = sh.col(rx)[row].value  # Store value in dictionary
	return b1


def get_transactions(wb, sheet):
	'''
	Collects all data from a given sheet and returns as a list of dictionaries.
	Args:
		wb: The workbook object.
		sheet: The sheet index to process.
	Returns:
		list: List of dictionaries for each row.
	'''
	b1total = list()
	sh = wb.sheet_by_index(sheet)
	# If more than one row, process as multiple rows
	if sh.nrows > 1:
		multiple_list = multiple_rows(wb, sh)
		# Optionally process each row dictionary
		for rows in multiple_list:
			pass
		b1total.append(multiple_list)
	else:
		# Only one row in sheet
		print('SINGLE ROW DETECTED', sh.nrows)
		single_row = process_single_row(wb, sh)
		b1total.append(single_row)
	return b1total


def process_row_dict(row_dict):  # vypise postupne vsetky hodnoty a ich kluce pre kontrolu
	'''
	Prints all keys and values in a row dictionary for inspection.
	Args:
		row_dict: Dictionary representing a row.
	'''
	b1 = row_dict
	for key in b1.keys():
		# Print key-value pairs for debugging
		print("KLUC: {0} \tHODNOTA:  {1}".format(key, b1[key]))
	
def xml_string_conversion(name, part):
	'''
	Converts a list of dictionaries to XML string using xmltodict.
	Args:
		name: The XML tag name for the part.
		part: List of dictionaries to convert.
	Returns:
		str: XML string output.
	'''
	for i in part:
		# Convert each dictionary to XML under the given tag name
		part = {name: i}
		part_output = xmltodict.unparse(part, pretty=True)
		print(part_output)
	return part_output


def transakcie_collector(wb, wb_length):
	'''
	Extracts all data from XLS sheets (from sheet 1 to wb_length) as dictionaries and saves as XML arguments.
	Args:
		wb: The workbook to convert.
		wb_length: Number of sheets to convert to XML.
	Returns:
		None
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
	Adds '@' to all keys in a dictionary to prepare for XML argument conversion.
	Args:
		raw_dict (dict): The dictionary to process.
	Returns:
		dict: Dictionary with '@' prefixed keys.
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
	Removes all <?xml?> tags from the XML string for output file writing.
	Args:
		xml_string (str): Raw XML string to modify.
	Returns:
		str: Cleaned XML string for output.
	'''
	teardown1 = xml_string.split('><')
	# print('TEARDOWN 1: ',teardown1)
	teardown2 = teardown1[0].split('\n')
	# print('TEARDOWN 2: ',teardown2)
	return teardown2[1] + ' />\n'
	

def get_rid_id_xml(xml_string):
	'''
	Removes the <?xml version="1.0" encoding="utf-8"?> tag from the start of the XML string.
	Args:
		xml_string (str): XML string with the unwanted tag.
	Returns:
		str: XML string without the unwanted tag.
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
	try:
		if len(sys.argv) == 1:
			filename = 'KV_test_2023 xml.xls'
		else:
			filename = sys.argv[1]
		if SaveTools.non_existing_file(filename):
			print(f"FILE NOT FOUND: {filename}")
			sys.exit(1)
		try:
			wb = xlrd.open_workbook(filename=filename)
		except Exception as e:
			print(f"Error opening workbook: {e}")
			sys.exit(1)

		SAVE = SaveTools('output.xml')
		try:
			SAVE.erase_file()
			SAVE.save_xml('<?xml version="1.0" encoding="utf-8"?>\n')
			SAVE.save_xml('<KVDPH_2023 xmlns="https://ekr.financnasprava.sk/Formulare/XSD/kv_dph_2023.xsd" xsi:schemaLocation="https://ekr.financnasprava.sk/Formulare/XSD/kv_dph_2023.xsd schema.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n')
		except Exception as e:
			print(f"Error initializing output file: {e}")
			sys.exit(1)

		print("IDENTIFIKACIA")
		try:
			id_part = get_transactions(wb, 0)
			xml_raw = xml_string_conversion("Identifikacia", id_part)
			xml_pure = identifikacia_mods(xml_raw)
			xml_pure = get_rid_id_xml(xml_pure)
			SAVE.save_xml(lines=xml_pure)
		except Exception as e:
			print(f"Error processing identification: {e}")
			sys.exit(1)

		try:
			transakcie_collector(wb, 8)  # TODO Get number of sheets
		except Exception as e:
			print(f"Error processing transactions: {e}")
			sys.exit(1)

		print("XML BOLO VYGENEROVANE")
	except Exception as e:
		print(f"Unexpected error: {e}")
		sys.exit(1)