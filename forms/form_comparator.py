'''
form_comparator.py
'''


form1 = open('form2021.xml', mode='r', encoding='ascii')
form2 = open('form2023.xml', mode='r', encoding='ascii')

for i in range(1,100):
	try:
		row1 = form1.readline()
		row2 = form2.readline()
		if row1 == row2:
			print(i, 'EQUAL')
		else:
			print(i, 'NON EQUAL')
			print(row1, '\n', row2)

		if row1 == '':
			quit()
	except IndexError:
		quit()
