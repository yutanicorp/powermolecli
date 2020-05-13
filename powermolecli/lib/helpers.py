#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: helpers.py
#
# Copyright 2020 Vincent Schouten
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
from ..powermolecliexceptions import SetupFailed

__author__ = '''Vincent Schouten <inquiry@intoreflection.co>'''
__docformat__ = '''google'''
__date__ = '''12-05-2020'''
__copyright__ = '''Copyright 2020, Vincent Schouten'''
__license__ = '''MIT'''
__maintainer__ = '''Vincent Schouten'''
__email__ = '''<inquiry@intoreflection.co>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging.
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
LOGGER_BASENAME = '''helpers'''
LOGGER = logging.getLogger(LOGGER_BASENAME)  # non-class objects like functions can consult this Logger object
# LOGGER.addHandler(logging.NullHandler())  # method not in https://docs.python.org/3/library/logging.html


def setup_link(state, transferagent, tunnel, bootstrapagent, assistant):
    """Starts instantiated TransferAgents, opens instantiated Tunnel(s) and starts instantiated Machine(s).

    This function also passes the instantiated objects to the StateManager, which
    will stop Machines and close Tunnels after a KeyboardInterrupt (by the user
    or by the program (in COMMAND and FILE mode).

    Args:
        state (StateManager): An instantiated StateManager object.
        transferagent (TransferAgent): An instantiated TransferAgent object.
        tunnel (Tunnel): An instantiated Tunnel object.
        bootstrapagent (BootstrapAgent): <>
        assistant (Assistant): An instantiated Assistant object.

    """
    if not transferagent.start():
        raise SetupFailed(transferagent)
    LOGGER.info('agent has been transferred to last host')

    state.add_object(tunnel)
    if not tunnel.start():
        raise SetupFailed(tunnel)
    LOGGER.info('tunneling has been set up')

    # the BootstrapAgent object is a disposable one-trick pony
    if not bootstrapagent.start():
        raise SetupFailed(bootstrapagent)
    LOGGER.info('agent has been executed')

    state.add_object(assistant)
    if not assistant.start():
        raise SetupFailed(assistant)
    LOGGER.info('agent assistant has been executed')
