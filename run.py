#!/usr/bin/env python
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.observers.api import EventQueue
import argparse
import os
import sys
import importlib
import subprocess

def listen():

    parser = argparse.ArgumentParser()
    parser.add_argument("settings", help="Django settings")
    parser.add_argument("--path", help="Path where to observe and where to search for the setting file", default='.')
    parser.add_argument("--tests", help="Test application list", default='')
    parser.add_argument("--now", help="Run test now", action='store_const', const=True)
    args = parser.parse_args()

    if args.path and args.path is not '.':
        sys.path.append(args.path)

    runner = None
    if args.settings:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", args.settings)
        from django.conf import settings
        module, cls = settings.TEST_RUNNER.rsplit('.' , 1)
        module = importlib.import_module(module)
        runner = getattr(module, cls)()

    if args.now:
        try:
            return runner.run_tests(args.tests.split(","))
        except KeyboardInterrupt:
            return
    else:
        print "Welcome to Django auto test runner"
        print "Using %s" % settings.TEST_RUNNER
        print

    class EventHandler(FileSystemEventHandler):

        def on_modified(self, event):

            if not event.src_path.endswith('.py'):
                return

            empty_queue()
            args = list(sys.argv)
            # in case it's run with python run.py
            if not args[0].startswith('./'):
                args[0] = './' + args[0]
            print args
            args.append("--now")
            subprocess.call(args)
            print
            empty_queue()

    def empty_queue():
        # empty the queue
        while True:
            try:
                observer.event_queue.get_nowait()
            except:
                break

    observer = Observer()
    observer.schedule(EventHandler(), args.path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    listen()

