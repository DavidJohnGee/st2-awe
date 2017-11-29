#!/usr/lib/python
""" Outer module that just invokes WorkflowEngine instance, set alias to
    this module
    @copyright: Ammeon Ltd
   
    StackStorm related action code, copyright David Gee, david.gee@ipengineer.net 2017
"""

import threading
import sys
import traceback
import os
import signal
from st2actions.runners.pythonrunner import Action

# This import is fugly, however, WorkflowEngine depends on the env var being set! :(
# This env needs to be hard coded in the python pip package.

os.environ['AWE_HOME'] = "/opt/stackstorm/packs/awe/actions/"
os.environ['TERM'] = "xterm"

from wfeng.workflowengine import WorkflowEngine
from wfeng import constants

def dumpstacks(signal, frame):
    f = open("/tmp/dump_workflow.log.{0}".format(os.getpid()), "w")
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId, ""), \
                                  threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % \
                         (filename, lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    f.write("\n".join(code))
    f.close()

signal.signal(signal.SIGUSR1, dumpstacks)

if not os.environ.get("AWE_HOME"):
    # Use this for when invoke via ssh and user's profile is not run
    os.environ["AWE_HOME"] = "{0}/..".format(
             os.path.dirname(os.path.realpath(__file__)))
sys.path.append("{0}/lib".format(os.environ["AWE_HOME"]))

# START OF ACTION CLASS HERE

class AWEActionClass(Action):


    def run(self, reset, version, task, hostfile, workfile, servername, servertype, alter_pause_escape, tag, outputdecorate, automate, answeryes, phase, exclude, inifile, fix, nettimeout, force, listing, nospinner, allow_multiple, parallel_delay):
        wfengargs = dict()
        wfengargs['mode'] = 'st2'

        if reset != None:
            wfengargs['reset'] = reset
        else:
            wfengargs['reset'] = False

        if version != None:
            wfengargs['version'] = version
        else:
            wfengargs['version'] = False

        if task != None:
            wfengargs['task'] = task
        else:
            wfengargs['task'] = None

        if hostfile != None:
            wfengargs['hostfile'] = hostfile
        else:
            wfengargs['hostfile'] = "./hosts.xml"

        if workfile != None:
            wfengargs['workfile'] = workfile
        else:
            wfengargs['workfile'] = "./workflow.xml"

        if servername != None:
            wfengargs['servername'] = servername
        else:
            wfengargs['servername'] = constants.ALL

        if servertype != None:
            wfengargs['servertype'] = servertype
        else:
            wfengargs['servertype'] = constants.ALL

        if alter_pause_escape != None:
            wfengargs['alter_pause_escape'] = alter_pause_escape
        else:
            wfengargs['alter_pause_escape'] = False

        if tag != None:
            wfengargs['tag'] = tag
        else:
            wfengargs['tag'] = None

        if outputdecorate != None:
            wfengargs['output'] = outputdecorate
        else:
            wfengargs['output'] = None

        if automate != None:
            wfengargs['automate'] = automate
        else:
            wfengargs['automate'] = False

        if answeryes != None:
            wfengargs['yes'] = answeryes
        else:
            wfengargs['yes'] = None

        if phase != None:
            wfengargs['phase'] = phase
        else:
           wfengargs['phase'] = None

        if exclude != None:
            wfengargs['exclude'] = exclude
        else:
            wfengargs['exclude'] = None

        if inifile != None:
            wfengargs['inifile'] = inifile
        else:
            wfengargs['inifile'] = None

        if fix != None:
            wfengargs['fix'] = fix
        else:
            wfengargs['fix'] = False

        if nettimeout != None:
            wfengargs['timeout'] = nettimeout
        else:
            wfengargs['timeout'] = 10

        if force != None:
            wfengargs['force'] = listing
        else:
            wfengargs['force'] = None

        if list != None:
            wfengargs['list'] = listing
        else:
            wfengargs['list'] = False

        if nospinner != None:
            wfengargs['nospinner'] = nospinner
        else:
            wfengargs['nospinner'] = False

        if allow_multiple != None:
            wfengargs['allow_multiple'] = allow_multiple
        else:
            wfengargs['allow_multiple'] = False

        if parallel_delay != None:
            wfengargs['parallel_delay'] = parallel_delay
        else:
            wfengargs['parallel_delay'] = 1

        # Pass into WorkflowEngine constructor a dict full of arguments.
        wfeng = WorkflowEngine(wfengargs)

        try:
            passed = wfeng.start()
        finally:
            wfeng.deletePidFile()
        if passed:
            return(True)
        else:
            return(False)
