#!/usr/bin/python
#encoding=utf8
import os
import getopt
import sys
import pdb
sys.path.append('../src')
from dataloader import DataLoader
from log import log, DEBUG, INFO, WARN, ERROR, FATAL

def usage():
    print 'Usage:'
    print '\t%s -f final_fname -k kaoqin_dir -j jixiao_dir [-d]' % sys.argv[0]


def run(final_file, kaoqin_dir, jixiao_dir, fenc='utf8'):
    dl = DataLoader()
    dl.load(kaoqin_dir, jixiao_dir, final_file, fenc)
    dl.check()

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "f:k:j:d", ['help', 'kaoqin=', 'jixiao=', 'debug'])
    except getopt.GetoptError, e:
        # print help information and exit:
        print str(e) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    debug = False
    kaoqin_dir = ''
    jixiao_dir = ''
    final_fname = ''
    for o, v in opts:
        if o in ("-d", '--debug'):
            debug = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-k", '--kaoqin'):
            kaoqin_dir = v.strip()
        elif o in ("-j", "--jixiao"):
            jixiao_dir = v.strip()
        elif o in ("-f", "--final"):
            final_fname = v.strip()
        else:
            assert False, "unhandled option"
    # ...
    if not os.path.isdir(kaoqin_dir):
        log(FATAL, 'kaoqin[%s] does not exists!' % kaoqin_dir)
    if not os.path.isdir(jixiao_dir):
        log(FATAL, 'jixiao[%s] does not exists!' % jixiao_dir)
    if not os.path.isfile(final_fname):
        log(FATAL, 'final[%s] does not exists!' % final_fname)
    run(final_fname, kaoqin_dir, jixiao_dir, fenc='utf8')

if __name__ == '__main__':
    main()
