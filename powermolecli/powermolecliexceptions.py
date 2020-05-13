#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: minitorcliexceptions.py
#
# Copyright 2019 Vincent Schouten
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
Custom exception code for minitorcli.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
from powermolelib import TransferAgent, BootstrapAgent, Tunnel, Assistant

__author__ = '''Vincent Schouten <inquiry@intoreflection.co>'''
__docformat__ = '''google'''
__date__ = '''12-05-2020'''
__copyright__ = '''Copyright 2019, Vincent Schouten'''
__credits__ = ["Vincent Schouten"]
__license__ = '''MIT'''
__maintainer__ = '''Vincent Schouten'''
__email__ = '''<inquiry@intoreflection.co>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


class SetupFailed(Exception):
    """The setup has failed."""

    def __init__(self, obj):
        self.message = 'Unknown object provided'
        if isinstance(obj, TransferAgent):
            self.message = f'could not copy agent module to last host'
        if isinstance(obj, BootstrapAgent):
            self.message = f'could not execute agent module'
        if isinstance(obj, Tunnel):
            self.message = f'could setting up tunneling'
        if isinstance(obj, Assistant):
            self.message = f'could not set up assistant to interact with agent on target destination host'
        # Call the base class constructor with the parameters it needs
        super().__init__(self.message)
