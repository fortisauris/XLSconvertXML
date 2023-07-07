
def identifikacia_mods(xml_raw: str): # TU SA MODIFIKUJE CAST IDENTIFIKACIA
	'''
	Function takes raw XML converted as string and makes multiple mods according to wanted OUTPUT.
	First we need to split XML string. Then we make tag <obdobie> accoding to data contained in XLS.
	Then we reassemble XML string back
	param1::: xml_raw - xml string before modification
	return::: id_reassembled back without last \n\t

	'''

	raw_id_list = xml_raw.split('\n\t')
	# raw_id_list = raw_id_list[0:]
	
	
	# MOD <obdobie>
	if raw_id_list[3][:8]=='<Mesiac>':  # Ak je uvedeny mesiac treba do obdobia 3 polozky
		print("NASIEL SOM MESIAC")
		Obdobie_string = "<Obdobie>\n\t\t"+raw_id_list[3]+"\n\t\t"+raw_id_list[4]+"\n\t\t"+raw_id_list[5]+"\n\t</Obdobie>"
		raw_id_list.insert(3,Obdobie_string)  # vlozi obdobie
		raw_id_list.pop(4)
		raw_id_list.pop(5)
		for i in raw_id_list:
			if i[:10] == '<Stvrtrok>':
				raw_id_list.remove(i)

	if raw_id_list[3][:10] =='<Stvrtrok>':
		print("NASIEL SOM STVRTROK")
		Obdobie_string = "<Obdobie>\n\t\t"+raw_id_list[3]+"\n\t\t"+raw_id_list[4]+"\n\t</Obdobie>"
		raw_id_list.insert(3,Obdobie_string)  # vlozi obdobie
		raw_id_list.pop(4)
		raw_id_list.pop(5)

	# REASSEMBLE XML STRING BACK STRING
	id_reassembled = str()
	for i in raw_id_list:
		id_reassembled += i + '\n\t'
	return id_reassembled[:-2]
