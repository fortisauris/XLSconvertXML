
"""
form_comparator.py
Compares two XML form files line by line and prints whether lines are equal or not.
"""

def compare_forms(file1_path, file2_path, max_lines=100):
	"""
	Compares two XML files line by line and prints the result for each line.
	Args:
		file1_path (str): Path to the first XML file.
		file2_path (str): Path to the second XML file.
		max_lines (int): Maximum number of lines to compare.
	Returns:
		list: List of tuples (line_number, status, line1, line2)
	"""
	results = []
	with open(file1_path, mode='r', encoding='ascii') as form1, \
		 open(file2_path, mode='r', encoding='ascii') as form2:
		for i in range(1, max_lines + 1):
			try:
				row1 = form1.readline()
				row2 = form2.readline()
				if row1 == row2:
					print(i, 'EQUAL')
					status = 'EQUAL'
				else:
					print(i, 'NON EQUAL')
					print(row1, '\n', row2)
					status = 'NON EQUAL'
				results.append((i, status, row1, row2))
				if row1 == '':
					break
			except IndexError:
				break
	return results
