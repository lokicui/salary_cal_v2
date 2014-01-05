import sys
from datetime import datetime

DEBUG = 1
INFO = 2
WARN = 3
ERROR = 4
FATAL = 5

def log(level, msg, fenc='utf8'):
    f = sys._getframe().f_back
    co = f.f_code
    tm = str(datetime.now())
    if level == DEBUG:
        strout = '[%s] %s:%d DEBUG:%s' % (tm, co.co_filename, f.f_lineno, msg)
    elif level == INFO:
        strout = '[%s] %s:%d INFO:%s' % (tm, co.co_filename, f.f_lineno, msg)
    elif level == WARN:
        strout = '[%s] %s:%d WARN:%s' % (tm, co.co_filename, f.f_lineno, msg)
    elif level == ERROR:
        strout = '[%s] %s:%d ERROR:%s' % (tm, co.co_filename, f.f_lineno, msg)
    elif level == FATAL:
        strout = msg.encode(fenc)
        raise RuntimeError(msg)
    print >> sys.stderr, strout.encode(fenc)


