import os
import tempfile
import argparse
import json

def create_key(key, value, storage):
	if key in storage.keys():
		storage[key].append(value)
	else:
		data = []
		data.append(value)
		storage[key] = data

def get_value(key, storage):
	if key in storage.keys():
		print(*storage[key], sep=', ')
	else:
		print(None)


def make_storage(storage_path):
	if os.path.isfile(storage_path):
		with open(storage_path, 'r') as f:
			storage = json.load(f)
	else:
		storage = {}
	return storage

def _main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--key", help="enter key that represent value")
	parser.add_argument("--value", help="enter the value to add in storage by key")
	args = parser.parse_args()
	path = tempfile.gettempdir()
	storage_path = os.path.join(path, 'storage.data')
	storage = make_storage(storage_path)
	if args.value and args.key:
		create_key(args.key, args.value, storage)
	elif args.key:
		get_value(args.key, storage)
	with open(storage_path, 'w') as f:
		json.dump(storage, f)

if __name__ == "__main__":
	_main()

