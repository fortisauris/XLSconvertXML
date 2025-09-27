


class SaveTools:
	"""
	Utility class for saving, erasing, and checking files, especially for XML output.
	"""

	def __init__(self, filename: str):
		"""
		Initializes the SaveTools object.
		Args:
			filename (str): The file to operate on.
		"""
		self.file = filename
		self.mode = 'a'  # Default mode appends to file

	def save_xml(self, lines: str) -> bool:
		"""
		Saves the given string to the file in append mode.
		Args:
			lines (str): The string to write to the file.
		Returns:
			bool: True if successful.
		"""
		with open(file=self.file, mode=self.mode, encoding='utf8') as f:
			f.write(lines)
		return True

	def erase_file(self) -> bool:
		"""
		Erases the file content by overwriting it with a newline.
		Returns:
			bool: True if successful.
		"""
		with open(file=self.file, mode='w', encoding='utf8') as f:
			f.write('\n')
		return True

	@staticmethod
	def non_existing_file(file: str) -> bool:
		"""
		Checks if a file exists.
		Args:
			file (str): The filename with path to check.
		Returns:
			bool: True if file does not exist, False otherwise.
		"""
		try:
			with open(file=file, mode='rb') as f:  # FILE MUST BE READ AS BINARY BECAUSE XLS FORMAT
				_ = f.read()
				return False
		except FileNotFoundError:
			print('FILE NOT FOUND')
			return True
		finally:
			pass
