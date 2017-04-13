# -*- coding: utf-8 -*-

# Split 1 big file with domains list into a several smaller files.
import os
import inspect
import subprocess


INPUT_FILE = 'test_input_data.txt'
OUTPUT_FILE_PREFIX = 'input_data_chunk_'
LINES_NUMBER = 300

current_path_directory = \
    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

root_path_directory = '/'.join(current_path_directory.split('/')[:-1])
current_path_file = '/'.join((root_path_directory, INPUT_FILE))
storage_directory_path = '/'.join((current_path_directory, 'data_storage', OUTPUT_FILE_PREFIX))

if os.path.isfile(current_path_file):
    command_line = ['split', '-l', str(LINES_NUMBER), current_path_file, storage_directory_path]
    try:
        subprocess.Popen(command_line)
    except Exception as e:
        print "Couldn't split a % file into smaller one." % (INPUT_FILE,)
else:
    raise Exception


