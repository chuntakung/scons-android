#!/usr/bin/env python

from subprocess import Popen, PIPE
import errno
import os
import shutil
import tempfile
import unittest

class SConsTestCase(unittest.TestCase):
    def setUp(self):
        self.basedir = tempfile.mkdtemp()

    def tearDown(self):
        self.done()

    def CompareContents(self, expected, filename):
        if type(filename) == str:
            data = open(filename).readlines()
        else:
            data = filename.readlines()
        expected_data = expected.split('\n')
        for x in zip(expected_data, data):
            x0 = x[0].strip()
            x1 = x[1].strip()
            self.assertEquals(x0, x1)

    def write_file(self, filename, data):
        f = os.path.join(self.basedir, filename)
        fp = open(f, 'w')
        fp.write(data)
        fp.close()

    def subdir(self, name):
        try:
            os.makedirs(os.path.join(self.basedir, name))
        except OSError, exc:
            if exc.errno != errno.EEXIST:
                raise

    def exists(self, name, variant='build'):
        filename = os.path.join(self.basedir, variant, name)
        return os.path.exists(filename)

    def get_file(self, name, variant='build'):
        filename = os.path.join(self.basedir, variant, name)
        return open(filename)

    def run_scons(self, args=None):
        start = os.getcwd()
        try:
            os.chdir(self.basedir)
            cwd = os.getcwd()
            cmd = ['scons']
            if args:
                cmd.extend(args)
            prog = Popen(cmd, shell=False, stdout=PIPE, stderr=PIPE)
            out = prog.stdout.readlines()
            err = prog.stderr.readlines()
            rc = prog.wait()
            if rc != 0:
                print ''.join(out), ''.join(err)
            return out, err, rc
        finally:
            os.chdir(start)

    def done(self):
        shutil.rmtree(self.basedir)
        #print self.basedir