#! /usr/bin/env python

import extargsparse
import logging
import os
import sys
import platform
import shutil


def set_logging(args):
	loglvl= logging.ERROR
	if args.verbose >= 3:
		loglvl = logging.DEBUG
	elif args.verbose >= 2:
		loglvl = logging.INFO
	curlog = logging.getLogger(args.lognames)
	#sys.stderr.write('curlog [%s][%s]\n'%(args.logname,curlog))
	curlog.setLevel(loglvl)
	if len(curlog.handlers) > 0 :
		curlog.handlers = []
	formatter = logging.Formatter('%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d<%(levelname)s>\t%(message)s')
	if not args.lognostderr:
		logstderr = logging.StreamHandler()
		logstderr.setLevel(loglvl)
		logstderr.setFormatter(formatter)
		curlog.addHandler(logstderr)

	for f in args.logfiles:
		flog = logging.FileHandler(f,mode='w',delay=False)
		flog.setLevel(loglvl)
		flog.setFormatter(formatter)
		curlog.addHandler(flog)
	for f in args.logappends:		
		if args.logrotate:
			flog = logging.handlers.RotatingFileHandler(f,mode='a',maxBytes=args.logmaxbytes,backupCount=args.logbackupcnt,delay=0)
		else:
			sys.stdout.write('appends [%s] file\n'%(f))
			flog = logging.FileHandler(f,mode='a',delay=0)
		flog.setLevel(loglvl)
		flog.setFormatter(formatter)
		curlog.addHandler(flog)
	return

def load_log_commandline(parser):
	logcommand = '''
	{
		"verbose|v" : "+",
		"logname" : "root",
		"logfiles" : [],
		"logappends" : [],
		"logrotate" : true,
		"logmaxbytes" : 10000000,
		"logbackupcnt" : 2,
		"lognostderr" : false
	}
	'''
	parser.load_command_line_string(logcommand)
	return parser


class ReadFileLarge(object):
    def __init__(self,fname=None):
        self.fname = fname
        if fname is not None:
            self.fh = open(fname,'r')
        else:
            self.fh = sys.stdin
        self.readb = b''
        self.sidx = 0
        self.linenum = 0
        return

    def __del__(self):
        if self.fh != sys.stdin and self.fh is not None:
            self.fh.close()
        self.fh = None
        return

    def _append_rbuf(self,blocksize):
        if 'b' in self.fh.mode:
            curb = self.fh.read(blocksize)
        else:
            curb = self.fh.buffer.read()
        if curb is None or len(curb) == 0:
            return b''
        logging.info('curb %d'%(len(curb)))
        return curb

    def _search_linefeed(self):
        news = None
        curidx = self.sidx
        while curidx < len(self.readb):
            if self.readb[curidx] == 0xa:
                try:
                    if sys.version[0] == '3':
                        news = self.readb[self.sidx:(curidx+1)].decode('utf-8')
                    else:
                        news = str(self.readb[self.sidx:(curidx+1)])
                    self.sidx = curidx + 1
                    return news
                except:
                    self.readb = self.readb[(curidx+1):]
                    self.sidx = 0
                    return None
            curidx += 1
        if self.sidx != 0:
            self.readb = self.readb[self.sidx:]
            self.sidx = 0
        return None

    def _next_step(self):
        while True:
            nline = self._search_linefeed()
            if nline is not None:
                self.linenum += 1
                return nline
            #logging.info('readb %d'%(len(self.readb)))
            # it is none so read again
            nb = self._append_rbuf((1 << 20))
            if nb is None or len(nb) == 0:
                if len(self.readb) > 0:
                    try:
                        if sys.version[0] == '3':
                            news = self.readb.decode('utf-8')
                        else:
                            news = str(self.readb)
                        self.readb = b''
                        self.sidx = 0
                        self.linenum += 1
                        return news
                    except:
                        raise StopIteration
                else:
                    raise StopIteration
            else:
                self.readb += nb

    def __iter__(self):        
        while True:
            try:
                val = self._next_step()
                yield val
            except StopIteration:
                break

    def __next__(self):
        return self._next_step()


class Utf8Encode(object):
    def __dict_utf8(self,val):
        newdict =dict()
        for k in val.keys():
            newk = self.__encode_utf8(k)
            newv = self.__encode_utf8(val[k])
            newdict[newk] = newv
        return newdict

    def __list_utf8(self,val):
        newlist = []
        for k in val:
            newk = self.__encode_utf8(k)
            newlist.append(newk)
        return newlist

    def __encode_utf8(self,val):
        retval = val

        if sys.version[0]=='2' and isinstance(val,unicode):
            retval = val.encode('utf8')
        elif isinstance(val,dict):
            retval = self.__dict_utf8(val)
        elif isinstance(val,list):
            retval = self.__list_utf8(val)
        return retval

    def __init__(self,val):
        self.__val = self.__encode_utf8(val)
        return

    def __str__(self):
        return self.__val

    def __repr__(self):
        return self.__val
    def get_val(self):
        return self.__val

def make_directory_safe(dname,mode=0o755):
    retval = True
    try:
        if dname is not None:
            os.makedirs(dname,mode=mode,exist_ok=True)
    except:
        logging.error('%s'%(traceback.format_exc()))
        retval = False
    return retval


def mktemp_dir(ind=None):
    tempd = None
    try:
        if ind is None:
            ind = os.getcwd()
        retval = make_directory_safe(ind)
        if not retval:
            return None
        tempd = tempfile.mkdtemp(dir=ind)
    except:
        logging.error('%s'%(traceback.format_exc()))
    return tempd


def read_file(infile=None):
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')
    rets = ''
    if 'b' in fin.mode:
        rdata = b''
        while True:
            try:
                l = fin.read(64 * 1024)
                if l is None or len(l) == 0:
                    break
                rdata += l
            except:
                break
        if sys.version[0] == '3':
            rets = rdata.decode('utf-8')
        else:
            rets = rdata
    else:        
        for l in fin:
            s = l
            rets += s

    if fin != sys.stdin:
        fin.close()
    fin = None
    return rets

def read_file_bytes(infile=None):
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')
    retb = b''
    while True:
        if fin != sys.stdin:
            curb = fin.read(1024 * 1024)
        else:
            curb = fin.buffer.read()
        if curb is None or len(curb) == 0:
            break
        retb += curb
    if fin != sys.stdin:
        fin.close()
    fin = None
    return retb


def write_file(s,outfile=None):
    fout = sys.stdout
    if outfile is not None:
        fout = open(outfile, 'w+b')
    outs = s
    if 'b' in fout.mode:
        outs = s.encode('utf-8')
    fout.write(outs)
    if fout != sys.stdout:
        fout.close()
    fout = None
    return 

def write_file_bytes(sarr,outfile=None):
    fout = sys.stdout
    if outfile is not None:
        fout = open(outfile, 'wb')
    if 'b' not in fout.mode:
        fout.buffer.write(sarr)
    else:        
        fout.write(sarr)
    if fout != sys.stdout:
        fout.close()
    fout = None
    return 

def is_in_windows():
    s = platform.system().lower()
    if s == 'windows':
        return True
    return False

def copy_inst_file(srcf,bdir):
	make_directory_safe(bdir)
	dstf = os.path.join(bdir,os.path.basename(srcf))
	logging.info('copy [%s] => [%s]'%(srcf,dstf))
	shutil.copyfile(srcf,dstf)
	return

def copy_exe_from_build(builddir,exename,bdir):
	srcf = os.path.join(builddir,'bin','Release',exename)
	return copy_inst_file(srcf,bdir)


def search_copy_file(sdirs,dllname,bdir):
	for sdir in sdirs:
		for ps,ds,fs in os.walk(sdir):
			for f in fs:
				if is_in_windows():
					if f.lower() == dllname.lower():
						srcf = os.path.join(ps,f)
						copy_inst_file(srcf,bdir)
						return True
				else:
					if f == dllname:
						srcf = os.path.join(ps,f)
						copy_inst_file(srcf,bdir)
						return True
	return False

		 
DLL_NAMES = ['event_core.dll','event_extra.dll','sqlite3.dll']

def packetwin_handler(args,parser):
	set_logging(args)

	if not is_in_windows():
		sys.stderr.write('not in windows mode\n')
		sys.exit(5)
	instdir = args.instdir
	# first to copy exe
	builddir = args.builddir
	copy_exe_from_build(builddir,'bitcoin-cli.exe',instdir)
	copy_exe_from_build(builddir,'bitcoind.exe',instdir)
	copy_exe_from_build(builddir,'bitcoin.exe',instdir)
	for dllname in DLL_NAMES:
		retval = search_copy_file(args.subnargs,dllname,instdir)
		if not retval:
			logging.error('not found %s'%(dllname))
			sys.exit(5)
	sys.exit(0)
	return

def main():
    commandline_fmt='''
    {
    	"instdir" : "installed",
    	"builddir" : "%s",
        "packetwin<packetwin_handler>##to packet to directory default [installed]##": {
        	"$" : "*"
        }
    }
    '''
    builddef = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','build'))
    if is_in_windows():
    	builddef = builddef.replace('\\','\\\\')
    commandline = commandline_fmt%(builddef)
    parser = extargsparse.ExtArgsParse()
    load_log_commandline(parser)
    parser.load_command_line_string(commandline)
    parser.parse_command_line(None,parser)
    raise Exception('can not here for no command handle')
    return


if __name__ == '__main__':
    main()