#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/3/30
import os
import codecs


class DirIter:
    def __init__(self, file_dir, suffix=''):
        self.file_dir = file_dir
        self.suffix = suffix
        self.files = os.listdir(self.file_dir)

    def __iter__(self):
        self.maxN = len(self.files)
        self.curN = 0
        if self.suffix:
            self.files = [file for file in self.files if self.suffix in file]
        return self

    def __next__(self):
        if self.curN < self.maxN:
            file = self.files[self.curN]
            file_path = self.file_dir + file
            data = self._read_file(file_path)
            self.curN += 1
            return data
        else:
            raise StopIteration

    @staticmethod
    def _read_file(file_path):
        fp = codecs.open(file_path, 'r', encoding='utf-8')
        data = fp.read()
        fp.close()
        return data


if __name__ == '__main__':
    directory = 'D:\\ad_work\data\spider\ccgp\\beijing\\'
    dir_iter = iter(DirIter(directory))
    # one way to use
    print(next(dir_iter))
    print(next(dir_iter))
    # another way to use
    for a_file in dir_iter:
        print(a_file)




