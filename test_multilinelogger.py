import unittest

import multilinelogger

import sys
import syslog
from StringIO import StringIO
from mock import Mock, patch

class TestMain(unittest.TestCase):

    def setUp(self):
        sys.stdin = StringIO()
        sys.stderr = StringIO()
        syslog.openlog = Mock()
        syslog.syslog = Mock()

    def test_defaults(self):
        sys.stdin.write('test')
        sys.stdin.seek(0)
        multilinelogger.main()
        syslog.openlog.assert_called_with('multilinelogger', 0, syslog.LOG_USER)
        syslog.syslog.assert_called_with(
                syslog.LOG_NOTICE,
                'test'
                )
        assert sys.stderr.read() == ''

    def test_pid(self):
        sys.stdin.write('test')
        sys.stdin.seek(0)
        sys.argv = ['multilinelogger', '-i', '1000']
        multilinelogger.main()
        syslog.openlog.assert_called_with('multilinelogger[1000]', 0, syslog.LOG_USER)
        syslog.syslog.assert_called_with(
                syslog.LOG_NOTICE,
                'test'
                )
        assert sys.stderr.read() == ''

    def test_stderr(self):
        sys.stdin.write('test')
        sys.stdin.seek(0)
        sys.argv = ['multilinelogger', '-s']
        multilinelogger.main()
        syslog.openlog.assert_called_with('multilinelogger', 0, syslog.LOG_USER)
        syslog.syslog.assert_called_with(
                syslog.LOG_NOTICE,
                'test'
                )
        assert 'multilinelogger: test\n' == sys.stderr.getvalue()

    @patch('__builtin__.open')
    def test_filename(self, open_mock):
        open_mock.return_value = StringIO('test')
        sys.argv = ['multilinelogger', '-f', 'a_filename']
        multilinelogger.main()
        open_mock.assert_called_once_with('a_filename', 'r')
        syslog.openlog.assert_called_with('multilinelogger', 0, syslog.LOG_USER)
        syslog.syslog.assert_called_with(
                syslog.LOG_NOTICE,
                'test'
                )
        assert '' == sys.stderr.getvalue()

    def test_priority(self):
        sys.stdin.write('test')
        sys.stdin.seek(0)
        sys.argv = ['multilinelogger', '-p', 'local3.info']
        multilinelogger.main()
        syslog.openlog.assert_called_with('multilinelogger', 0,
                syslog.LOG_LOCAL3)
        syslog.syslog.assert_called_with(
                syslog.LOG_INFO,
                'test'
                )

    def test_priority_without_a_dot(self):
        sys.stdin.write('test')
        sys.stdin.seek(0)
        sys.argv = ['multilinelogger', '-p', 'local3']
        multilinelogger.main()
        syslog.openlog.assert_called_with('multilinelogger', 0,
                syslog.LOG_LOCAL3)
        syslog.syslog.assert_called_with(
                syslog.LOG_NOTICE,
                'test'
                )

    def test_priority_starts_with_a_dot(self):
        sys.stdin.write('test')
        sys.stdin.seek(0)
        sys.argv = ['multilinelogger', '-p', '.info']
        multilinelogger.main()
        syslog.openlog.assert_called_with('multilinelogger', 0,
                syslog.LOG_USER)
        syslog.syslog.assert_called_with(
                syslog.LOG_INFO,
                'test'
                )

    def test_priority_ends_with_a_dot(self):
        sys.stdin.write('test')
        sys.stdin.seek(0)
        sys.argv = ['multilinelogger', '-p', 'local3.']
        multilinelogger.main()
        syslog.openlog.assert_called_with('multilinelogger', 0,
                syslog.LOG_LOCAL3)
        syslog.syslog.assert_called_with(
                syslog.LOG_NOTICE,
                'test'
                )

if __name__ == '__main__':
    unittest.main()
