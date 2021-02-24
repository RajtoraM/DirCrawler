#!/usr/bin/python

import os

path_list = []
file_list = []
directory_list = []


def crawler(path):
    files_and_directories = os.listdir(path)
    new_path_list = []

    for fd in files_and_directories:
        try:
            new_path_list.append(path + "\\" + fd)
            path_list.append()
        except TypeError:
            pass

    for directory in new_path_list:
        try:
            crawler(directory)
            directory_list.append(directory)
        except NotADirectoryError:
            file_list.append(directory)


crawler("D:\Coding\Local")
print(path_list)
print("\n\n")
print(len(file_list))
print(len(directory_list))
