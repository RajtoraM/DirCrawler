#!/usr/bin/python
import os
import configparser
import host_info
# import db_module

global delimiter_slash
delimiter_slash = "\\"               # slash delimiter in path, default is backslash

path_list = []                       # list of files and directories, which will be examined by crawler
file_list = []                       # files found by crawler
directory_list = []                  # directories found by crawler
directories_to_be_backed_up = []     # starting directories for crawler
ignored_files_and_directories = []   # files and directories in this list will be ignored by the program


def import_configurations():
    """
    Imports configurations specified in config.cfg file

    Creates lists of:
        - directories which are to be backed up, i.e. starting directories for crawler
        - directories and files which will be ignored (skipped) by crawler
    """
    config = configparser.ConfigParser()
    config.read("config.cfg")

    # defines lists containing starting directories and ignored directories and files
    global directories_to_be_backed_up, ignored_files_and_directories

    directories_to_be_backed_up = config.get("TO BE BACKED UP", "path", fallback="").split()
    ignored_files_and_directories = config.get("IGNORED", "path", fallback="").split()

    # in case there is not specified starting directory
    if not directories_to_be_backed_up:
        print("INPUT ERROR:\tDirectories cannot be backed up,\n"
              "\t\tpaths are not specified in configuration file (see config.cfg)")
        quit()


def crawler(path):
    """
    Crawls through directories and creates lists of paths, files and directories.

    :argument path: starting crawled_path for crawler
    :type path: str
    """
    files_and_directories = os.listdir(path)
    new_path_list = []

    # converting list elements to paths. Loop back prevention and filtering of ignored files and directories
    for entity in files_and_directories:
        try:
            entity_path = (path + delimiter_slash + entity)
            if entity not in path_list and entity_path not in ignored_files_and_directories:
                new_path_list.append(entity_path)
        except TypeError:
            pass
    # recursive crawling through found directories
    for crawled_path in new_path_list:
        path_list.append(crawled_path)
        try:
            crawler(crawled_path)
            directory_list.append(crawled_path)
        except NotADirectoryError:
            file_list.append(crawled_path)





host_info.system_compatibility_check()

import_configurations()
# db_module.db_init()

for directory in directories_to_be_backed_up:
    crawler(directory)



# with open("path_list.txt","c") as list:
#     list.write(*path_list)

print("\n\n")
print(*path_list, sep="\n")
# print(*file_list, sep="\n")
# print(*directory_list, sep="\n")
print("\n\n")
print("Files discovered:\t\t" + str(len(file_list)))
print("Directories discovered:\t\t" + str(len(directory_list)))
print(len(path_list))
