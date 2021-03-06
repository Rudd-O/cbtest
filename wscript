#! /usr/bin/env python
# -*- coding: utf-8 -*-

# the following two variables are used by the target "waf dist"
# if you change 'em here, you need to change it also in cloud.spec, add a %changelog entry there, and add an entry in debian/changelog
VERSION = '1.0.0'
APPNAME = 'cloud-bridge'

import shutil,os
import email,time
import optparse
import platform
import Utils,Node,Options,Logs,Scripting,Environment,Build,Configure
from subprocess import Popen as _Popen,PIPE
import os
import sys
from os import unlink as _unlink, makedirs as _makedirs, getcwd as _getcwd, chdir as _chdir
from os.path import abspath as _abspath, basename as _basename, dirname as _dirname, exists as _exists, isdir as _isdir, split as _split, join as _join, sep, pathsep, pardir, curdir
from glob import glob as _glob
import zipfile,tarfile
try:
  from os import chmod as _chmod,chown as _chown
  import pwd,stat,grp
except ImportError:
  _chmod,_chown,pwd,stat,grp = (None,None,None,None,None)
import xml.dom.minidom
import re

# CENTOS does not have this -- we have to put this here
try:
	from subprocess import check_call as _check_call
	from subprocess import CalledProcessError
except ImportError:
	def _check_call(*popenargs, **kwargs):
		import subprocess
		retcode = subprocess.call(*popenargs, **kwargs)
		cmd = kwargs.get("args")
		if cmd is None: cmd = popenargs[0]
		if retcode: raise CalledProcessError(retcode, cmd)
		return retcode

	class CalledProcessError(Exception):
		def __init__(self, returncode, cmd):
			self.returncode = returncode ; self.cmd = cmd
		def __str__(self): return "Command '%s' returned non-zero exit status %d" % (self.cmd, self.returncode)

# these variables are mandatory ('/' are converted automatically)
srcdir = '.'
blddir = 'artifacts'

Configure.autoconfig = True

# things never to consider when building or installing
for pattern in ["**/.project","**/.classpath"]: Node.exclude_regs += "\n%s"%pattern

# Support functions

# this will enforce the after= ordering constraints in the javac task generators
from TaskGen import after, feature
@feature('*')
@after('apply_core', 'apply_java', 'apply_subst')
def process_after(self):
	lst = self.to_list(getattr(self, 'after', []))
	for x in lst:
		obj = self.bld.name_to_obj(x,self.bld.env)
		if not obj: break
		obj.post()
		for a in obj.tasks:
			for b in self.tasks:
				b.set_run_after(a)

Build.BuildContext.process_after = staticmethod(process_after)

def _getbuildcontext():
	ctx = Build.BuildContext()
	ctx.load_dirs(_abspath(srcdir),_abspath(blddir))
	ctx.load_envs()
	return ctx

def set_options(opt):
	"""Register command line options"""
	opt.tool_options('gnu_dirs')
	
        inst_dir = opt.get_option_group('--bindir') # get the group that contains bindir
	inst_dir.add_option('--javadir', # add javadir to the group that contains bindir
		help = 'Java class and jar files [Default: ${DATADIR}/java]',
		default = '',
		dest = 'JAVADIR')
	inst_dir.add_option('--no-dep-check',
		action='store_true',
		help = 'Skip dependency check and assume JARs already exist',
		default = False,
		dest = 'NODEPCHECK')
	inst_dir.add_option('--fast',
		action='store_true',
		help = 'does ---no-dep-check',
		default = False,
		dest = 'NODEPCHECK')

def showconfig(conf):
	"""prints out the current configure environment configuration"""
	conf = _getbuildcontext()
	
	Utils.pprint("WHITE","Build environment:")
	for key,val in sorted(conf.env.get_merged_dict().items()):
		if "CLASSPATH" in key:
			Utils.pprint("BLUE","  %s:"%key)
			for v in val.split(pathsep):
				Utils.pprint("BLUE","     %s"%v)
			continue
		Utils.pprint("BLUE","  %s:	%s"%(key,val))

def runant(tsk):
	environ = dict(os.environ)
	environ["CATALINA_HOME"] = tsk.env.TOMCATHOME
	environ["AXIS2_HOME"] = "."
	if tsk.generator.env.DISTRO == "Windows":
		stanzas = [
			"ant",
			"-Dcloud-bridge.classpath=\"%s\""%(tsk.env.CLASSPATH.replace(os.pathsep,",")),
		]
	else:
		stanzas = [
			'ant',
			"-Dcloud-bridge.classpath=%s"%(tsk.env.CLASSPATH.replace(os.pathsep,",")),
		]
	stanzas += tsk.generator.antargs + tsk.generator.anttgts
	return Utils.exec_command(" ".join(stanzas),cwd=tsk.generator.bld.srcnode.abspath(),env=environ,log=True,shell=False)
Utils.runant = runant

def relpath(path, start="."):
    if not path: raise ValueError("no path specified")

    start_list = os.path.abspath(start).split(sep)
    path_list = os.path.abspath(path).split(sep)

    # Work out how much of the filepath is shared by start and path.
    i = len(os.path.commonprefix([start_list, path_list]))

    rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list:
        return curdir
    return os.path.join(*rel_list)
Utils.relpath = relpath
