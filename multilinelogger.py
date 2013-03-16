#!/usr/bin/python

import sys
import syslog
from optparse import OptionParser

priorities = {
        'emerg': syslog.LOG_EMERG,
        'alert': syslog.LOG_ALERT,
        'crit': syslog.LOG_CRIT,
        'err': syslog.LOG_ERR,
        'warning': syslog.LOG_WARNING,
        'notice': syslog.LOG_NOTICE,
        'info': syslog.LOG_INFO,
        'debug': syslog.LOG_DEBUG,
        }

facilities = {
        'kern': syslog.LOG_KERN,
        'user': syslog.LOG_USER,
        'mail': syslog.LOG_MAIL,
        'daemon': syslog.LOG_DAEMON,
        'auth': syslog.LOG_AUTH,
        'lpr': syslog.LOG_LPR,
        'news': syslog.LOG_NEWS,
        'uucp': syslog.LOG_UUCP,
        'cron': syslog.LOG_CRON,
        'syslog': syslog.LOG_SYSLOG,
        'local0': syslog.LOG_LOCAL0,
        'local1': syslog.LOG_LOCAL1,
        'local2': syslog.LOG_LOCAL2,
        'local3': syslog.LOG_LOCAL3,
        'local4': syslog.LOG_LOCAL4,
        'local5': syslog.LOG_LOCAL5,
        'local6': syslog.LOG_LOCAL6,
        'local7': syslog.LOG_LOCAL7,
        }
#     Logger makes entries in the system log.  It provides a shell command interface to the syslog(3) system log module.

#     Write the message to log; if the -f flag is not provided, standard input is logged.

#     The logger utility exits 0 on success, and >0 if an error occurs.
parser = OptionParser()
parser.add_option("-i", dest="pid", metavar="pid", help="Log the specified number as the process process id.")
parser.add_option("-s", dest="stderr", action="store_true", help="Log the message to standard error, as well as the system log.")
parser.add_option("-f", dest="filename", metavar="file", default='-', help="Log the specified file.")
parser.add_option("-p", dest="priority", metavar="pri", default="user.notice", help="Enter the message with the specified priority.  The priority is specified as a ``facility.level'' pair.  For example, ``-p local3.info'' logs the message(s) as informational level in the local3 facility.  The default is ``user.notice.''")
parser.add_option("-t", dest="tag", metavar="tag", default="multilinesyslog", help="Mark the message in the log with the specified tag.")

(options, args) = parser.parse_args()

tag = options.tag
if options.pid:
    tag = tag + '[' + options.pid + ']'
facility, priority = options.priority.split('.')
if not priority:
    priority = 'notice'
if not facility:
    facility = 'user'
fac = facilities.get(facility, 'user')
prio = priorities.get(priority, 'notice')

syslog.openlog(tag, 0, syslog.LOG_LOCAL2)
if options.filename == '-':
    stream = sys.stdin
else:
    stream = open(options.filename, 'r')
message = stream.read().strip()
if message:
    syslog.syslog(prio, message)
if options.stderr:
    sys.stderr.write(tag + ': ')
    sys.stderr.write(message)
    sys.stderr.write("\n")
