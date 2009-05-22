#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Developed by Rafik Mas'ad (Azag).
# sCon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# sCon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/

# This aplication depends off "mpg123", "oggenc", "flac"

import os

class mainOptD:
  types = {'audio/x-wav'        : ['wav', 'ogg', []],
           'audio/mpeg'         : ['mp3', 'ogg', ['m4a', 'mp4', 'm4p', 'aac']],
           'application/msword' : ['doc', 'txt', []]}
  

  __version__ = "0.1.2"
  __license__ = "sCon %s, is free software under GNU GPL3." % (__version__)
  __about__   = "sCon, Version %s, License: GNU GPL v3, Copyright 2009, (c) Rafik Mas'ad, Some rights reserved." % (__version__)

  def __init__(self):
    # Unix:
    if hasattr(os, "sysconf"):
      if os.sysconf_names.has_key("SC_NPROCESSORS_ONLN"):
        # Linux & Unix:
        self.nthr = os.sysconf("SC_NPROCESSORS_ONLN")
       # OSX
      else:
        self.nthr = int(os.popen2("sysctl -n hw.ncpu")[1].read())
    # Windows:
    elif os.environ.has_key("NUMBER_OF_PROCESSORS"):
      self.nthr = int(os.environ["NUMBER_OF_PROCESSORS"])

    if not isinstance(self.nthr, int) or self.nthr < 0:
      self.nthr = 1

class oggOptD:
  rate = "44100"
  rates = ['44100', '48000']
  quality = "8"
  qualitys = ['1','2','3','4','5','6','7','8','9','10']
  channels = "2"
