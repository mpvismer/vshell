'''
Useful functionality for the IPython Shell

@author Mark Vismer
'''

import os
import sys
_path = os.path.realpath(os.path.abspath(os.path.join(__file__,'../..')))
sys.path.append(_path)
try:
    import utils
except:
    import pyutils as utils

#import pprint
#import logging
#import glob
import ctypes


_LOG_DIR = "_logs"

utils.mkdir_p(_LOG_DIR)


def reloadall():
    '''
    Reload all the modules in the space.
    '''
    done = []
    import inspect

    def loadall(items):
        for key, val in items:
            if inspect.ismodule(val):
                if not repr(val) in done:
                    done.append(repr(val))
                    loadall(inspect.getmembers(val))
                    reload(val)
                    #print('Reloading "' + repr(val) + '"...')
    loadall(globals().iteritems())


def script(filePath):
    '''
    An alias for "run -i ...
    '''
    if not os.path.exists(filePath):
        filePath = os.path.join('scripts',filePath)
    get_ipython().magic(u'run -i %s' % filePath)


def configure_ipython():
    get_ipython().magic(u'autocall 2');

    get_ipython().magic(u'automagic on')

    get_ipython().magic(u'logstart -ot ' + os.path.join(_LOG_DIR,'ipython.log') + ' rotate');


    #
    if 0:
        def _none():
            return None

        class ExcWrapper:
            def fn(self, etype, value, tb, tb_offset):
                _handle_exception.old_excepthook = _none
                return _handle_exception(etype, value, tb)
        _except_cls_instance = ExcWrapper()
        #get_ipython().set_custom_exc( (Exception,), _except_cls_instance.fn)
        #sys.excepthook = Configuration._handle_exception


def printglobals():
    import inspect
    import types

    modules = []
    functions = []
    classes = []
    others = []

    for key, val in globals().iteritems():
        if key.startswith('_'):
            pass
        elif inspect.ismodule(val):
            modules.append((key, utils.first_line(val.__doc__)))
        elif inspect.isroutine(val):
            functions.append((key, utils.first_line(val.__doc__)))
        elif inspect.isclass(val):
            classes.append((key, utils.first_line(val.__doc__)))
        else:
            others.append((key,str(type(val))))

    def formatit(item, maxlen=60):
        if len(item) > maxlen:
            return item[:maxlen-3]+'...'
        return item

    if modules:
        print('Modules:')
        for item in modules:
            print '  %-15s  %s' % (item[0], formatit(item[1]))

    if functions:
        print('\nFunctions:')
        for item in functions:
            print '  %-15s  %s' % (item[0], formatit(item[1]))

    if classes:
        print('\nClasses:')
        for item in classes:
            print '  %-15s  %s' % (item[0], formatit(item[1]))

    if others:
        print('\nOthers:')
        for item in others:
            print '  %-15s  %s' % (item[0], formatit(item[1]))


def sample_make_h2pyex_ctypes():
    import h2pyex
    from StringIO import StringIO
    s = StringIO()
    w = h2pyex.WriterCTypes(output=s)
    w = w.write_struct_class('notNested', 'A comment', [
            ('abyte', 'int8_t', -1, 'this is a byte'),
            ('somebytes', 'int8_t', 2, 'this is len 2 array of bytes'),
            ('abool', 'bool_t', -1, 'this is a boolean'),
            ('somebools', 'bool_t', 10, 'this is an array of booleans'),
            ('df', 'float64_t', -1, 'a double') ],
            'End of notNested')
    env = {}
    exec(s.getvalue(), env)
    print(s.getvalue())
    cls = env['notNested']
    return cls



if __name__=='__main__':
    utils.configure_rotating_logging(os.path.join(_LOG_DIR,'logging.log'))
    configure_ipython()
    print('')
    printglobals()
    print('\nUse printglobals() to list modules and functions in the workspace.\nUse "help x" for help on something.')

    import h2pyex
    hr = h2pyex.import_cheader('../h2pyex/sample.h')
    x = sample_make_h2pyex_ctypes()
