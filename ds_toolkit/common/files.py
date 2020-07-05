import os
import shutil
import inspect

from ds_toolkit.logger import logger

log = logger()


def list_dir(folder_path, full_path=False):
	"""
	List all files/folders in a directory
	
	Args:
		folder_path (str):
		full_path (bool): Return full paths

	Returns:
		list:
	"""
	
	file_names = os.listdir(folder_path)
	if full_path:
		return [os.path.join(folder_path, file_name) for file_name in file_names]
	else:
		return file_names


def list_dir_files(folder_path, full_path=False):
	"""
	List all files in directory.
	
	Args:
		folder_path (str):
		full_path (bool): Return full file paths

	Returns:
		list: Files list
	"""
	
	file_names = os.listdir(folder_path)
	files_list = []
	
	for file_name in file_names:
		file_path = os.path.join(folder_path, file_name)
		
		if os.path.isfile(file_path):
			files_list.append(file_path if full_path else file_name)
	
	return files_list


def list_dir_folders(folder_path, full_path=False):
	"""
	List all folders from a parent folder.
	
	Args:
		folder_path (str):
		full_path (bool): Return full folder path.

	Returns:
		list: Folders list
	"""
	
	file_names = os.listdir(folder_path)
	
	folder_paths = []
	for file_name in file_names:
		file_path = os.path.join(folder_path, file_name)
		
		if os.path.isdir(file_path):
			folder_paths.append(file_path + '/' if full_path else file_name)
	
	return folder_paths


def list_dir_tree(root_folder):
	"""
	Returns every single file path from a root folder.

	Args:
		root_folder (str):

	Returns:
		list: List of all file paths from root folder
	"""
	
	subfile_paths = []
	for root, directories, files in os.walk(root_folder):
		for file in files:
			fp = os.path.join(root, file)
			if not os.path.isdir(fp):
				subfile_paths.append(fp)
	return subfile_paths


def get_file_type(file_path):
	"""
	Gets file type for given file path.

	Args:
		file_path (str):

	Returns:
		dict: { file_path: (str), info: (str), type: (str) }
	"""
	
	try:
		import magic
	
	except Exception as e:
		log.error(f'''
		Exception importing magic library.
		See how to set up for your OS here. https://pypi.org/project/python-magic/
		Exception: {str(e)}
		''')
		return
	
	return {
		'file_path': file_path,
		'info': magic.from_file(file_path),
		'type': magic.from_file(file_path, True)
	}


def create_file(file_path):
	"""
	Creates a file.

	Args:
		file_path (str):
	"""
	
	if os.path.isfile(file_path):
		raise FileExistsError('File path already exists')
	else:
		os.mknod(file_path)


def write_to_file(file_path, data, overwrite=True):
	"""
	Writes data to file.

	Args:
		file_path (str):
		data (str):
		overwrite (bool): If file exists, overwrite file
	"""
	
	if not overwrite:
		if os.path.isfile(file_path):
			raise FileExistsError('File path already exists')
	
	with open(file_path, 'w+') as file:
		file.write(data)
	
	file.close()


def read_file(file_path):
	"""
	Reads and returns file content.

	Args:
		file_path (str):

	Returns:
		str:
	"""
	
	with open(file_path, 'r') as file:
		return file.read()


def delete_file(file_path):
	"""
	Delete a file.

	Args:
		file_path (str):
	"""
	if os.path.isfile(file_path):
		os.remove(file_path)


def move_file(from_file_path, to_file_path):
	"""
	Moves a file to a new destination.

	Args:
		to_file_path (str):
		from_file_path (str):
	"""
	if os.path.isfile(to_file_path):
		raise FileExistsError('File path already exists')
	
	shutil.move(from_file_path, to_file_path)


def rename_file(file_path, new_name):
	"""
	Renames a file.
	
	Args:
		file_path (str):
		new_name (str):
	"""
	head, tail = os.path.split(file_path)
	
	to_file_path = os.path.join(head, new_name)

	if os.path.isfile(to_file_path):
		raise FileExistsError('File path already exists')

	os.rename(file_path, to_file_path)


def make_folder(folder_path):
	"""
	Make a folder.

	Args:
		folder_path (str):
	"""
	if not os.path.isdir(folder_path):
		os.makedirs(folder_path)


def delete_folder(folder_path):
	"""
	Delete a folder.

	Args:
		folder_path (str):
	"""
	if os.path.isdir(folder_path):
		shutil.rmtree(folder_path)


def fix_encoding(file_path, read_as='utf-8', write_as='utf-8', remove_chars=None):
	"""
	Ignores data encoding errors and writes to utf-8.

	Args:
		file_path (str):
		read_as (str):
		write_as (str):
		remove_chars (list):
	"""
	
	with open(file_path, encoding=read_as, errors='ignore') as file:
		text = file.read()
		file.close()
	
	if remove_chars:
		for remove_char in remove_chars:
			text = text.replace(remove_char, '')
	
	with open(file_path, 'w+', encoding=write_as) as file:
		file.write(text)
		file.close()


def move_all_files_from_root(root_folder, to_folder):
	"""
	Moves all files from a folder root to a new folder.
	
	Args:
		root_folder (str):
		to_folder (str):
	"""
	
	file_paths = list_dir_tree(root_folder)
	for file_path in file_paths:
		if os.path.isfile(file_path):
			head, tail = os.path.split(file_path)
			move_file(file_path, os.path.join(to_folder, tail))


def current_directory():
	"""
	
	Returns:
		 str:

	"""
	file_path = inspect.stack()[1][1]
	return os.path.dirname(file_path) + '/'









