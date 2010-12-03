"""This module is used to parse the added Han-Han entries attached in
Seng Heng's mail dated 26 April 2010"""

from dict_file import DictFile
from hhdict_file import HHDictFile, HHDictEntry
import re

RE_START_ENTRY = re.compile(r'^.*jc>')

class AddedHHDictFile(DictFile):
   def getChunk(self):
      chunk = []
      if len(self.peek_line) != 0:
         chunk.extend([self.peek_line])
         self.peek_line = ''
         #print '1*', line
      while True:
         line = self.getLine()
         if len(line) != 0:
            #print 'len = ', len(self.peek_line)
            if re.match(RE_START_ENTRY, line) and len(chunk) > 0:
               self.peek_line = line
               #print '2*', line
               break
            else:
               chunk.extend([line])
               #print '3*', line
         else:
            break
      return chunk

class AddedHHDictEntry(HHDictEntry):
   """An entry for Han-Han dictionary"""

   def _process_line(self, line):
      m = re.match(RE_START_ENTRY, line)
      if m:
         base_entry = m.string[m.end():]
         base_entry = base_entry.strip()
         self.Entry['entry'] = base_entry
         self.Entry['definition'] = []
         return

