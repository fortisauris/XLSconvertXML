


class SaveTools(object):

	def __init__(self, filename: str):
		self.file=filename
		self.mode='a'  # default mode adds strings to file
		# self.lines = lines

	def save_xml(self, lines):
		with open(file=self.file, mode=self.mode, encoding='utf8') as f:
			f.write(lines)
		return True

	def erase_file(self):
		with open(file=self.file, mode='w', encoding='utf8') as f:
			f.write('\n')
		return True

	@staticmethod
	def non_existing_file(file):
		'''
		Function tests if file exist and returns Bool if 
		param1:: file - filename with path String()
		return:: Bool()
		'''
		try:
			with open(file=file, mode='rb') as f:  # FILE MUST BE READ AS BINARY BECAUSE XLS FORMAT
				text = f.read()
				return False
		except FileNotFoundError:
			print('FILE NOT FOUND')
			return True
		finally:
			pass
