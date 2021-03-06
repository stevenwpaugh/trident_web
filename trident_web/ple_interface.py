#!/usr/bin/env python

"""
pleweb.py -- Web interface for PLE

This CGI expects two POST variables, nt1 and nt2, which contain micro RNA and DNA sequences, respectively.

The output of ple will be printed as preformated text in an html document.

"""

#import cgi
import os, re
from django.http import HttpResponse
from django.shortcuts import render_to_response


def init():
    print("Content-type: text/html\n\n");

def header(title):
    print("""
    <html>
    <head>
    <title>""" + title + """</title>
    </head>
    """)

def footer():
    print("""
    </pre>
    </body>
    </html>""")

def run_ple(form):
    """
    Wrapper function for trident. Requires a dict-like object with the following keys: 'nt1', 'nt2', 'long_format' and 'use_miranda'
    
    Raises trident.FastaError exception if there is a problem with the input sequences.
    """
    import tempfile
    from subprocess import Popen,PIPE
    from local_settings import TRIDENT_EXE_PATH
    
    pid = os.getpid()
    ple_path = TRIDENT_EXE_PATH
    if not ple_path:
        ple_path = "trident"
    init()
    
    tmpfiles = {}
    for i in ["nt1", "nt2"]:
        if len(re.findall(r"[^agcutnAGCUTN\s]",form[i])):
            from trident import FastaError
            raise FastaError("Invalid sequence \"%s\"" % form[i])
        
        try:
            file = tempfile.NamedTemporaryFile(mode="w",dir="/tmp")
        except IOError as ioe:
            from os import path
            from trident import FastaError
            raise FastaError("ERROR #%d: %s\nFile: \"%s\"\nCWD: \"%s\"" % (ioe.errno, ioe.strerror, path.abspath(file.name),os.getcwd()))
        file.write(">%s\n" % file.name)
        file.write("%s" % form[i])
        file.flush()
        tmpfiles[i] = file
        
    opts = ""
    if not form["long_format"]:
        opts += " -brief "
    if form["use_miranda"]:
        opts += " -miranda "

    from sys import stderr
    proc = Popen("{0} {1} {2} {3} 2>&1".format(ple_path, tmpfiles["nt1"].name, tmpfiles["nt2"].name, opts),shell=True,bufsize=0,stdout=PIPE)
    proc.wait()
    stdout_file = proc.stdout

    if proc.returncode:
        print("Trident process exited with value {0}".format(proc.returncode))
    
    tmpfiles["nt1"].close()
    tmpfiles["nt2"].close()

    return stdout_file

