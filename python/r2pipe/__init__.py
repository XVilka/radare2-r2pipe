#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""r2pipe

This module provides an API to interact with the radare2
commandline interface from Python using a pipe.

The pipe can be connected to the parent process to run
Python scripts from the radare2 shell itself, or it can
spawn a new process, connect via HTTP to a remote r2 http
server, etc.

Some r2 commands display the information in JSON, that's
why r2pipe provides `-j` methods to directly parse it
and return a native Python object.

Example:
  $ python
  > import r2pipe
  > r = r2pipe.open("/bin/ls")
  > print(r.cmd("pd 10"))
  > print(r.cmdj("aoj")[0]['size'])
  > r.quit()
"""

import os
import sys
import time
import socket
import urllib
        
if os.name != 'nt':
        import fcntl   

try:
        import r2lang
except:
        r2lang = None



VERSION = "0.9.5"

if sys.version_info >= (3, 0):
        import urllib.request
        urlopen = urllib.request.urlopen
        import urllib.error
        URLError = urllib.error.URLError
        from r2pipe.open_async import open
else:
        import urllib2
        urlopen = urllib2.urlopen
        URLError = urllib2.URLError
        from r2pipe.open_sync import open
     
        
   


def version():
        """Return string with the version of the r2pipe library
        """
        return VERSION

"""open class is now in open_base.py"""


# Hello World
if __name__ == "__main__":

        print("[+] Spawning r2 tcp and http servers")
        os.system("pkill r2")
        os.system("r2 -qc.:9080 /bin/ls &")
        os.system("r2 -qc=h /bin/ls &")
        time.sleep(1)
        
        if sys.version_info <= (3, 0):
                # Test r2pipe with local process
                print("[+] Testing python r2pipe local")
                rlocal = open("/bin/ls")
                print(rlocal.cmd("pi 5"))
                # print rlocal.cmd("pn")
                info = rlocal.cmdj("ij")
                print("Architecture: " + info['bin']['machine'])

                # Test r2pipe with remote tcp process (launch it with "r2 -qc.:9080 myfile")
                print("[+] Testing python r2pipe tcp://")
                rremote = open("tcp://127.0.0.1:9080")
                disas = rremote.cmd("pi 5")
                if not disas:
                        print("Error with remote tcp conection")
                else:
                        print(disas)

                # Test r2pipe with remote http process (launch it with "r2 -qc=H myfile")
                print("[+] Testing python r2pipe http://")
                rremote = open("http://127.0.0.1:9090")
                disas = rremote.cmd("pi 5")
                if not disas:
                        print("Error with remote http conection")
                else:
                        print(disas)
        else:
		# --------------------------------------------------------------------------
		# Python 3 examples, with non-blocking API and callbacks
		# --------------------------------------------------------------------------
                def callback(result):
                        print(result)

                #
                # Test r2pipe with local process
                #
                #   Start 1 task
                print("[+] Testing python r2pipe local")
                rlocal = open("/bin/ls")
                t = rlocal.cmd("pi 5", callback=callback)
                rlocal.wait(t)  # Wait for task end
                rlocal.close()

                #   Start 3 tasks with Context manager
                print("[+] Testing python r2pipe local with 3 queries")
                with open("/bin/ls") as rlocal:
                        t1 = rlocal.cmd("pi 5", callback=callback)
                        t2 = rlocal.cmd("pi 5", callback=callback)
                        t3 = rlocal.cmd("pi 5", callback=callback)

                        rlocal.wait([t1, t2, t3])

                #
                # Test r2pipe with remote tcp process (launch it with "r2 -qc.:9080 myfile")
                #
                #   Start 1 task
                print("[+] Testing python r2pipe tcp://")
                rremote = open("tcp://127.0.0.1:9080")
                t = rremote.cmd("pi 5", callback=callback)
                rremote.wait(t)
                rremote.close()

                #   Start 3 tasks with Context manager
                print("[+] Testing python r2pipe tcp:// with 3 queries")
                with open("tcp://127.0.0.1:9080") as rremote:
                        t1 = rremote.cmd("pi 5", callback=callback)
                        t2 = rremote.cmd("pi 5", callback=callback)
                        t3 = rremote.cmd("pi 5", callback=callback)

                        rremote.wait([t1, t2, t3])

                #
                # Test r2pipe with remote http process (launch it with "r2 -qc=H myfile")
                #
                print("[+] Testing python r2pipe http://")
                rremote = open("tcp://127.0.0.1:9080")
                t = rremote.cmd("pi 5", callback=callback)
                rremote.wait(t)
                rremote.close()

                #   Start 3 tasks with Context manager
                print("[+] Testing python r2pipe http:// with 3 queries")
                with open("http://127.0.0.1:9090") as rremote:
                        t1 = rremote.cmd("pi 5", callback=callback)
                        t2 = rremote.cmd("pi 5", callback=callback)
                        t3 = rremote.cmd("pi 5", callback=callback)

                        rremote.wait([t1, t2, t3])


            
        os.system("pkill -INT r2")
