import os
import tempfile
from datetime import datetime

class File_iter():
	def __init__(self, path, cursor):
		self._lst = self._do_lst(path)
		self._cursor = cursor

	def __next__(self):
		if self._cursor + 1 >= len(self._lst):
			raise StopIteration()
		self._cursor += 1
		return self._lst[self._cursor]

	def __iter__(self):
		return self

	def _do_lst(self, path):
		with open(path, 'r') as f:
			return list(f)

class File():
	def __init__(self, path):
		self._path = self._check_file(path)

	def __str__(self):
		return self._path

	def __add__(self, other):
		now = datetime.now()
		path = os.path.join(tempfile.gettempdir(), 'data' + str(now))
		new = File(path)
		new.write(self.read() + other.read())
		return new

	def __iter__(self):
		return File_iter(self._path, -1)
	
	def _check_file(self, path):
		if os.path.exists(path) and os.path.isfile(path):
			return path
		with open(path, 'w') as f:
			pass
		return path

	def read(self):
		with open(self._path, 'r') as f:
			return f.read()

	def write(self, text_str):
		with open(self._path, 'w') as f:
			return f.write(text_str)

