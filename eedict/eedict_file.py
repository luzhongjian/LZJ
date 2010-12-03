#coding=utf-8
""" added by prm """
from dict_file import EeDictFile
import re               #import regular expression

RE_START_ENTRY               =  re.compile('^\[@\]')   #citiao
RE_START_YINBIAO             =  re.compile('^\[#\]')   #yinbiao
#RE_START_OTHERS              =  re.compile('^\[\*\]')  #search other context

TAG_OTHERS              = 1
class EEDictFile(EeDictFile):
   pass

class EEDictEntry:
   """An entry for EC dictionary"""
   def __init__(self, chunk):
      """Parse the chunk from the dictionary file and generate a dictionary entry"""
      self.Entry = {}
      self.parseChunk(chunk)
 
   def _process_line(self, line, start_flag):
      #print "process line: %s" % line
      tuple = 0
      m = re.match(RE_START_ENTRY, line) 
      if m:
         #print 'entry=%s' % line
         self.Entry['entry'] = m.string[m.end():]
         self.Entry['others']  = []   
         return

      m = re.match(RE_START_YINBIAO, line)
      if m:
         self.Entry['yinbiao'] = m.string[m.end():]
         if(start_flag[0] != 1):
            start_flag[0] = 1
         return 
      
      elif start_flag[0] == 1: 
         tuple = (TAG_OTHERS, line) 
         self.Entry['others'].extend([tuple]) 
         #print tuple
         return

   def parseChunk(self, chunk):
      """this function parse the chunk and generate the Entry object.
      chunk is a list of lines previously fetched from dictionary file."""
      start_flag = [0]   # when start_flag is 1, illustrate that yinbiao has been occur(only one line)
      for line in chunk:
         #print line
         self._process_line(line, start_flag)
     

