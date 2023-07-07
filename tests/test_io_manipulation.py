from output.save_tools import SaveTools


def test_fne():
	file = 'neexistujuci_subor.py'
	obj = SaveTools.non_existing_file(file)
	assert obj == True