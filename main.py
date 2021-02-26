#!/usr/bin/python

import os
import configparser

path_list = []
file_list = []
directory_list = []


def import_configurations():
    """
    Imports configurations specified in config.cfg file

    Creates lists of:
        - directories which are to be backed up, i.e. starting directories for crawler
        - directories and files which will be ignored, i.e. skipped by crawler
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

    :argument path: starting directory for crawler
    :type path: str
    """
    files_and_directories = os.listdir(path)
    new_path_list = []

    # converting list elements to paths. Loop back prevention and filtering of ignored files and directories
    for entity in files_and_directories:
        try:
            entity_path = (path + "\\" + entity)
            if entity not in path_list and entity_path not in ignored_files_and_directories:
                new_path_list.append(entity_path)
        except TypeError:
            pass
    # recursive crawling through found directories
    for directory in new_path_list:
        path_list.append(directory)
        try:
            crawler(directory)
            directory_list.append(directory)
        except NotADirectoryError:
            file_list.append(directory)


import_configurations()

for address in directories_to_be_backed_up:
    crawler(address)


print("\n\n")
print(*path_list, sep="\n")
# print(*file_list, sep="\n")
# print(*directory_list, sep="\n")
print("\n\n")
print("Files discovered:\t\t" + str(len(file_list)))
print("Directories discovered:\t\t" + str(len(directory_list)))
print(len(path_list))
