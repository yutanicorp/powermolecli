#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: helpers.py
#
# Copyright 2021 Vincent Schouten
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Import all parts from helpers here.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
import logging.config
from time import sleep
from powermolelib import (Configuration,
                          start_application)
from powermolelib.powermolelibexceptions import InvalidConfigurationFile
from powermolecli.powermolecliexceptions import SetupFailed
from powermolecli.lib.logging import LOGGER_BASENAME as ROOT_LOGGER_BASENAME

__author__ = '''Vincent Schouten <inquiry@intoreflection.co>'''
__docformat__ = '''google'''
__date__ = '''12-05-2020'''
__copyright__ = '''Copyright 2021, Vincent Schouten'''
__license__ = '''MIT'''
__maintainer__ = '''Vincent Schouten'''
__email__ = '''<inquiry@intoreflection.co>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# # This is the main prefix used for logging.
LOGGER = logging.getLogger(f'{ROOT_LOGGER_BASENAME}.helpers')  # non-class objects like fn will consult this object


def parse_config_file(config_file_path):
    """Parses the configuration file to a (dictionary) object."""
    try:
        configuration = Configuration(config_file_path)
        LOGGER.debug('Gateways: %s', configuration.gateways)
        LOGGER.debug('Destination: %s', configuration.destination)
        LOGGER.debug('Forwarders: %s', configuration.forwarders_string)
    except InvalidConfigurationFile:
        return None
    if configuration.mode == 'FOR':
        LOGGER.info('mode FOR enabled')
    elif configuration.mode == 'TOR':
        LOGGER.info('mode TOR enabled')
    elif configuration.mode == 'PLAIN':
        LOGGER.info('mode PLAIN enabled')
    return configuration


def on_send_command(instructor):
    """Sends commands to destination host and receives the response."""
    # 'the interface does not support shell meta characters \n'
    # 'such as pipe and it\'s not possible to interact with \n'
    # 'programs that need a response. hit control-c to quit \n'
    while True:
        try:
            command = input('> enter command: ')
            response_raw = instructor.send_command(command)
            response_str = response_raw.decode("utf-8")
            response_line = response_str.split('\n')
            for line in response_line:
                print('%s' % line)
        except KeyboardInterrupt:
            print('\n')
            break


def on_send_files(instructor):
    """Sends file(s) to destination host and receives the response."""
    while True:
        try:
            source_file_path = input('> enter source file path on client:')
            destination_path = input('> enter destination path on destination host:')
            result = instructor.send_file(source_file_path.strip(), destination_path.strip())
            if result:
                LOGGER.info('file has been transferred')
            else:
                LOGGER.error('file could not be transferred')
        except KeyboardInterrupt:
            print('\n')
            break


def on_application_start(config):
    """Starts the application that the user declared in the configuration file."""
    try:
        process = start_application(binary_name=config.application['binary_name'],
                                    binary_location=config.application['binary_location'])
    except TypeError:
        LOGGER.error('something went wrong starting the application or the application was not in file')
        return
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        process.terminate()
        return


def show_menu(config, instructor):
    """Shows a number of options.

    Most of these options invoke a method in the Instructor().

    """
    menu = {'1.': "Send commands",  # consider using a python_prompt_toolkit
            '2.': "Send files",
            '3.': "Start application stated in configuration file",
            '4.': "Quit (or control + c)"}
    while True:
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])
        selection = input("> please select: ")  # to exclude the Space (and or other) character
        if selection == '1':
            on_send_command(instructor)
        elif selection == '2':
            on_send_files(instructor)
        elif selection == '3':
            on_application_start(config)
        elif selection == '4':
            break
        else:
            print("Unknown Option Selected!")
            continue


def setup_link(state, transfer_agent, tunnel, bootstrap_agent,   # pylint: disable=too-many-arguments
               instructor, debug=None):  # pylint: disable=unused-argument
    """Establishes a connection to target destination host via intermediaries by starting various objects.

    This function also passes the instantiated objects to the StateManager, which
    will stop the Tunnel and Instructor after a KeyboardInterrupt (by the user
    or by the program (in COMMAND and FILE mode)).

    Args:
        state (StateManager): An instantiated StateManager object.
        transfer_agent (TransferAgent): An instantiated TransferAgent object.
        tunnel (Tunnel): An instantiated Tunnel object.
        bootstrap_agent (BootstrapAgent): An instantiated BootstrapAgent object.
        instructor (Instructor): An instantiated Assistant object.
        debug (bool): if True enable debugging mode

    """
    if not transfer_agent.start():
        raise SetupFailed(transfer_agent)
    LOGGER.info('Agent has been transferred securely to destination host')

    state.add_object(tunnel)
    if not tunnel.start(debug=False):
        raise SetupFailed(tunnel)
    LOGGER.info('Tunnel has been opened')

    # sleep(10)
    # the BootstrapAgent object is a disposable one-trick pony
    if not bootstrap_agent.start():
        raise SetupFailed(bootstrap_agent)
    LOGGER.info('Agent has been executed')

    state.add_object(instructor)
    if not instructor.start():
        raise SetupFailed(instructor)
    LOGGER.info('Instructor has been executed')
