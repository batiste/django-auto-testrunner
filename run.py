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
    parser.add_argument("runner_class", 
        help="Complete path to the test runner class", 
        default='')
    parser.add_argument("--path", 
        help="Path where to observe file changes, this value is added to sys.path", 
        default='.')
    parser.add_argument("--params", 
        help="Params to pass to the test runner", 
        default='')
    parser.add_argument("--now", 
        help="Run test now", action='store_const', 
        const=True)
    args = parser.parse_args()

    if args.path and args.path is not '.':
        sys.path.append(args.path)

    mod, cls = args.runner_class.rsplit('.', 1)
    module = importlib.import_module(mod)
    runner = getattr(module, cls)()

    if args.now:
        try:
            #args.params.split(",")
            return runner.run_tests()
        except KeyboardInterrupt:
            return

    class EventHandler(FileSystemEventHandler):

        def on_modified(self, event):

            if not event.src_path.endswith('.py'):
                return

            empty_queue()
            args = list(sys.argv)
            # in case it's run with python run.py
            if not args[0].startswith('./'):
                args[0] = './' + args[0]
            args.append("--now")
            # I call a subprocess because Django doesn't run if
            # not in the main thread
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

