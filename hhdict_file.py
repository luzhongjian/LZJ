from dict_file import DictFile
import re

RE_START_ENTRY =        re.compile('^\[@\]') #citiao
RE_START_PINYIN =       re.compile('^\[\$\]') #pinyin
RE_START_DEFINITION =   re.compile('^\[&\]') #shiyi. This may also be a cross-reference
RE_START_EXAMPLE_WORD = re.compile('^\[\*\]') #lici
RE_START_EXAMPLE_USE =  re.compile('^\[%\]') #liju
RE_START_PRON_TAG =     re.compile('^\[\^\]') #fasheng biaoji

RE_START_ENGLISH_IDIOM =re.compile(u'^\[\uffe1\]') #British pound, indicates start of English idiom for Chengyu Cidian
RE_START_STORY        = re.compile(u'^\[#\]') # Chengyu Gushi, Story of Idiom 
TAG_EXAMPLE_WORD = 0
TAG_EXAMPLE_USE = 1

class HHDictFile(DictFile):
   pass

class HHDictEntry:
   """An entry for Han-Han dictionary"""

   def __init__(self, chunk):
      """Parse the chunk from the dictionary file and generate a dictionary entry"""
      self.Entry = {}
      self.parseChunk(chunk)
 
   def _process_line(self, line):
      m = re.match(RE_START_EXAMPLE_USE, line)
      if m:
         tuple = (TAG_EXAMPLE_USE, m.string[m.end():])
         try:
            self.Entry['definition'][-1]['example'].extend([tuple])
         except IndexError:
            raise
         return

      m = re.match(RE_START_EXAMPLE_WORD, line)
      if m:
         tuple = (TAG_EXAMPLE_WORD, m.string[m.end():])
         self.Entry['definition'][-1]['example'].extend([tuple])
         return

      m = re.match(RE_START_DEFINITION, line)
      if m:
         dict = {}
         dict['meaning'] = m.string[m.end():]
         dict['example'] = []
         self.Entry['definition'].extend([dict])
         return

      # for English idiom line of Chengyu Cidian
      m = re.match(RE_START_ENGLISH_IDIOM, line)
      if m:
         self.Entry['english_idiom'] = m.string[m.end():]
         return

      # for Chengyu Diangu, Story of the Idiom
      m = re.match(RE_START_STORY, line)
      if m:
         self.Entry['story'] = [m.string[m.end():]]
         return

      m = re.match(RE_START_ENTRY, line)
      if m:
         self.Entry['entry'] = m.string[m.end():]
         self.Entry['definition'] = []
         return

      m = re.match(RE_START_PRON_TAG, line)
      if m:
         self.Entry['prontag'] = m.string[m.end():]
         return

      m = re.match(RE_START_PINYIN, line)
      if m:
         self.Entry['pinyin'] = m.string[m.end():]
         return
      # for those cannot match a pattern, it is belonging to Chengyu Diangu section of Chengyu Cidian.
      self.Entry['story'].append(line)

   def parseChunk(self, chunk):
      """this function parse the chunk and generate the Entry object.
      chunk is a list of lines previously fetched from dictionary file."""
      for line in chunk:
         self._process_line(line)

