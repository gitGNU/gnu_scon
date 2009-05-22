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

# This aplication depends of "mpg123", "oggenc", "flac", "catdoc"

from glob import glob
import subprocess
import mimetypes
import threading
import os.path

""" Clase de conversion de tipos de archvos audio. """
class AudioConverter:
  def __init__(self):
    self.files = []

  """ Metodo protegido, que se encarga de convertir un archivo mp3 a ogg. """
  def __convert_mp3_ogg(self,infile,outfile,rate,ch,q):
    mpg123 = subprocess.Popen(["mpg123", "-q", "-s", infile], stdout=subprocess.PIPE)
    oggenc = subprocess.Popen(["oggenc", "-q", q, "--quiet", "--raw", "--raw-rate="+rate, "--raw-chan=" + ch, "-o", outfile, "-"], stdin=mpg123.stdout, stdout=subprocess.PIPE)
    oggenc.wait()

  """ Metodo protegido, que se encarga de convertir un archivo wav a ogg. """
  def __convert_wav_ogg(self,infile,outfile,rate,ch,q):
    oggenc = subprocess.Popen(["oggenc", "-q", q, "--quiet", "--raw", "--raw-rate="+rate, "--raw-chan=" + ch, "-o", outfile, infile], stdout=subprocess.PIPE)
    oggenc.wait()

  def __convert_flac_ogg(self,infile,outfile,rate,ch,q):
    flac = subprocess.Popen(["flac", "-d", "-c", "--totally-silent", infile], stdout=subprocess.PIPE)
    oggenc = subprocess.Popen(["oggenc", "-q", q, "--quiet", "--raw", "--raw-rate="+rate, "--raw-chan=" + ch, "-o", outfile, "-"], stdin=flac.stdout, stdout=subprocess.PIPE)
    oggenc.wait()

  def __convert_doc_txt(self, infile, outfile):
    catdoc = subprocess.Popen(["catdoc", "-s", "UTF-*", "-a", infile], stdout=subprocess.PIPE)
    catdoc.wait()
    txt = open(outfile, "w")
    txt.write(catdoc.communicate()[0])
    txt.close()

  def SetFile(self, file, types):
    if os.path.isfile(file) and self.__get_extension(file) in self.types.keys():
      self.files.append(file)

  """ Metodo para devolver el tipo (extension) del archivo. """
  def __get_extension(self, file):
    return file.split(".")[-1].lower()

  def __confirm(self, text):
    return self.confirm and raw_input("\n\n%s [Y/n] " % (text)).lower() not in ["s", "si","y","yes"]

  def start(self):
    if not self.files: return
    print "Ogg sets (Quality(1-10): %s, Rate: %sHz, Channels: %s)\n" % (self.quality, self.rate, self.channel)
    print "Objetives (%d):" % (len(self.files))
    for file in self.files:
      print "\t(%s) %s" % (self.types[mimetypes.guess_type(file)[0]][0], file)


    for p_format in self.types.keys():
      print "\n%s will be converted into %s." % (self.types[p_format][0], self.types[p_format][1]),

    if self.__confirm('Continue?'):
      return
    print

    self.sem = threading.Semaphore(self.nthr)
    for file in self.files:
      self.sem.acquire()
      p = threading.Thread(target=self.convert, args=(file,))
      p.start()

    print
    if self.delete: self.DeleteFiles();
    #elif self.__confirm('Delete'): self.DeleteFiles();

  """ Metodo para el uso de multihilo. """
  def convert(self, file):
    minetype = mimetypes.guess_type(file)[0]
    extension = self.types[minetype][1]
    if file.split("/")[-1].find(".") != -1 and file.split(".")[-1] in [type[0] for type in self.types.values()]:
      outfile = "".join(file.split(".")[:-1]) + "." + extension
    else:
      outfile = file + "." + self.types[extension][1]


    print '(%d/%d) Converting "%s" to %s.' % (self.files.index(file) + 1, len(self.files), file.split("/")[-1], extension)

    if self.types[minetype][:-1] == ["wav", 'ogg']:
      self.__convert_wav_ogg(file,outfile,self.rate,self.channel,self.quality)
    elif self.types[minetype][:-1] == ["mp3", "ogg"]:
      self.__convert_mp3_ogg(file,outfile,self.rate,self.channel,self.quality)
    elif self.types[minetype][:-1] == ["flac", "ogg"]:
      self.__convert_flac_ogg(file,outfile,self.rate,self.channel,self.quality)
    elif self.types[minetype][:-1] == ["doc", "txt"]:
      self.__convert_doc_txt(file,outfile)
    self.sem.release()

  def __toConvert(self, file):
    minetype = mimetypes.guess_type(file)[0]
    splitFile = [char.lower() for char in file.split(".")]
    return os.path.isfile(file) and\
           minetype in self.types.keys() and not\
           [type for type in self.types[minetype][2] if type in splitFile]

  def scan_dir(self, dir, isRecursive, types):
    for file in glob(os.path.abspath(dir) + "/*"):
      if os.path.isdir(file) and isRecursive:
        self.scan_dir(file, isRecursive, types)
      elif self.__toConvert(file):
        self.files.append(file)

    

  """ Metodo que elimina los archivos despues de su conversion
  en caso de que el usuario especifique implicitamente. """
  def DeleteFiles(self):
    for file in self.files:
      print "(%d/%d) Deleting \"%s\"" % (self.files.index(file) + 1, len(self.files), file.split("/")[-1])
      os.remove(file)
