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

import os.path
import main.DefaultSettings
from main.AudioConverter import AudioConverter
from optparse import OptionGroup, OptionParser, SUPPRESS_HELP

class MainClass():
  def __init__(self):
    def check_mytype(option, opt, value):
      print option
      print opt
      print value
    parser = OptionParser()
    aConverter = AudioConverter()
    mainOptD = main.DefaultSettings.mainOptD()
    oggOptD = main.DefaultSettings.oggOptD()

    parser.add_option("-a", "--about", action="store_true", help="Show About message.", dest="about", default=False)
    parser.add_option("-v", "--version", action="store_true", help=SUPPRESS_HELP, dest="about", default=False)
    parser.add_option("-l", "--license", action="store_true", dest="license", help="Show License message.", default=False)

    parser.add_option("-d", "--dir", dest="directory", help="Select directory contains files or file to convert.", metavar="DIR")
    parser.add_option("--select-format", dest="selectFormat", action="store_true", help="Show format selection messages.", default=False)

    parser.add_option("-r", "--delete", action="store_true", help="After conversion delete files.", dest="delete", default=False)
    parser.add_option("--no-confirm", action="store_false", help="Bypass any and all 'Continue?' and 'Delete files converted?' messages.", dest="confirm", default=True)
    #parser.add_option("--scan-mode", action="store_true",help="Launch in the Scan Mode.", dest="scanMode", default=False)
    parser.add_option("-e","--recursive", help="Scan directories. MODE=Recursive.", action="store_true", dest="recursive", default=False )
    parser.add_option("--nth", dest="nthr", metavar="n", help="Specify number of threads. (Default: Number of CPUs in system)", default=mainOptD.nthr)

    oggOpt = OptionGroup(parser, "OGG options", "Options to convertios to OGG format.")
    oggOpt.add_option("--fflac", dest="fromFlac", action="store_true", help="Convert flac files into OGG", default=False)
    oggOpt.add_option("--quality", dest="quality", help="Set quality to OGG file.(1-10) (Default:8)", metavar="n", default=oggOptD.quality)
    oggOpt.add_option("--rate", dest="rate", help="Set rate to OGG file.(44100 - 48000) (Default: 44100)", metavar="n", default=oggOptD.rate)
    oggOpt.add_option("--channels", dest="chans", help="Set channels to OGG file.(1 - 255) (Default: 2)", metavar="n", default=oggOptD.channels)
    parser.add_option_group(oggOpt)

    (Options, args) = parser.parse_args()

    aConverter.nthr = Options.nthr
    types = mainOptD.types

    aConverter.rate = Options.rate
    aConverter.quality = Options.quality
    aConverter.channel = Options.chans
    aConverter.types = types
    if Options.fromFlac: types["audio/flac"] = ['flac', 'ogg']
    aConverter.delete = aConverter.DeleteFiles()
    aConverter.confirm = Options.confirm
    if Options.selectFormat:
      print
      for format in types.keys():
        if raw_input("Don't convert %s files? [Y/n] " % (types[format][0])).lower() in ["s", "si","y","yes"]:
          del types[format]
      print

    if Options.about:
      print mainOptD.__about__
      return

    elif Options.license:
      print mainOptD.__license__
      return

    elif Options.directory:
      if os.path.isdir(Options.directory): aConverter.scan_dir(Options.directory, Options.recursive, types)
      elif os.path.isfile(Options.directory): aConverter.SetFile(Options.directory, types)
      aConverter.start()

    else: parser.print_help()

