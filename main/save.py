# -*- coding: utf-8 -*-

# Get domains from a lot of little files.
# Launch spiders for getting and saving content.
import os
import inspect
import subprocess


OUTPUT_FILE_NAME = 'domains.txt'
STORAGE_NAME_DIR = 'data_storage'
SPIDER_NAME = 'domain_spider_2'


def run_crawler(spiderName):
    sub = subprocess.Popen('scrapy crawl %s ' % (spiderName,), shell=True,
                           cwd=spider_launch_directory)
    # import pdb;pdb.set_trace()
    # sub.wait(timeout=10)
    # sub.kill()

    return True

# import pdb;pdb.set_trace()

current_path_directory = \
    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
root_path_directory = '/'.join(current_path_directory.split('/')[:-1])

storage_path_directory = '/'.join((current_path_directory, STORAGE_NAME_DIR))
spider_launch_directory = '/'.join((root_path_directory, 'spider'))
path_output_file = '/'.join((root_path_directory, 'spider/spider/Temp', OUTPUT_FILE_NAME))

input_files_list = os.listdir(storage_path_directory)

for file_in in input_files_list:
    path_input_file = '/'.join((storage_path_directory, file_in))

    with open(path_input_file, 'r') as input_file:
        with open(path_output_file, 'w') as output_file:
            line = input_file.readlines()
            output_file.writelines(line)

    # import pdb;pdb.set_trace()

    try:
        run_crawler(SPIDER_NAME)
    except Exception as e:
        print "Couldn't launch scrapy script."