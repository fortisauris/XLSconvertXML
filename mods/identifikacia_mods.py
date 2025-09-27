
def identifikacia_mods(xml_raw: str): # TU SA MODIFIKUJE CAST IDENTIFIKACIA
	'''
	Modifies the <Obdobie> section in the given XML string according to the data (month or quarter) found in the input.
	Args:
		xml_raw (str): The raw XML string before modification.
	Returns:
		str: The modified XML string with the correct <Obdobie> tag structure.
	'''
	# Split the XML string into lines for easier manipulation
	xml_lines = xml_raw.split('\n\t')

	# Check for <Mesiac> (month) or <Stvrtrok> (quarter) and build <Obdobie> accordingly
	if len(xml_lines) > 5 and xml_lines[3][:8] == '<Mesiac>':
		print("NASIEL SOM MESIAC")
		# Build <Obdobie> tag for month
		obdobie_tag = (
			"<Obdobie>\n\t\t" + xml_lines[3] + "\n\t\t" + xml_lines[4] + "\n\t\t" + xml_lines[5] + "\n\t</Obdobie>"
		)
		xml_lines.insert(3, obdobie_tag)
		# Remove the now redundant tags
		xml_lines.pop(4)
		xml_lines.pop(5)
		# Remove any <Stvrtrok> tags if present
		xml_lines = [line for line in xml_lines if not line.startswith('<Stvrtrok>')]

	elif len(xml_lines) > 4 and xml_lines[3][:10] == '<Stvrtrok>':
		print("NASIEL SOM STVRTROK")
		# Build <Obdobie> tag for quarter
		obdobie_tag = (
			"<Obdobie>\n\t\t" + xml_lines[3] + "\n\t\t" + xml_lines[4] + "\n\t</Obdobie>"
		)
		xml_lines.insert(3, obdobie_tag)
		# Remove the now redundant tags
		xml_lines.pop(4)
		xml_lines.pop(5)

	# Reassemble the XML string
	id_reassembled = ''
	for line in xml_lines:
		id_reassembled += line + '\n\t'
	# Remove the last '\n\t' for clean output
	return id_reassembled[:-2]
