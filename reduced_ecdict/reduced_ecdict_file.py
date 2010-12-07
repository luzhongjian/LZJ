"""Added by prm """
#coding=utf-8
from reduced_dict_file import reducedEcDictFile
import re        #import regular expression

RE_START_ENTRY               =  re.compile('^\[@\]') #citiao
#RE_START_PINYIN =       re.compile('^\[\$\]') #pinyin
RE_START_YINBIAO             =  re.compile('^\[#\]')   #yinbiao
RE_START_SEARCH_OTHER        =  re.compile('^\[\*\]')   #search other related vocabulary
RE_START_DEFINITION          =  re.compile('^\[\$\]')   #cixing
RE_START_MEANING             =  re.compile('^\[%\]')   #shiyi. This may also be a cross-reference
RE_START_EXAMPLE_SENTENCE    =  re.compile('^\[\^\]')  #liju
RE_START_EXAMPLE_TRANSLATION =  re.compile('^\[&\]')   #liju translation
RE_START_DUANYU              =  re.compile(u'^\[\u77ed\u8bed\]') #duan yu
RE_START_SYNONYM             =  re.compile(u'^\[\u540c\u4e49\u8bcd\]') #synonym
RE_START_ANTONYM             =  re.compile(u'^\[\u53cd\u4e49\u8bcd\]') #antonym 
RE_START_DERIVATIVE          =  re.compile(u'^\[\u6d3e\u751f\u8bcd\]')   #derivative
RE_START_REFER_TO            =  re.compile(u'^\[\u53c2\u89c1\]')       #canjian
RE_START_PICK_OUT            =  re.compile(u'^\[\u8fa8\u6790\]')       #bianxi
RE_START_REMARK              =  re.compile(u'^\[\u5907\u6ce8\]')       #note


TAG_START_MEANING         = 0
TAG_START_MEANING_NONE    = 1 
class ReducedECDictFile(reducedEcDictFile):
   pass

class ReducedECDictEntry:
   """An entry for EC dictionary"""
   def __init__(self, chunk):
      """Parse the chunk from the dictionary file and generate a dictionary entry"""
      self.Entry = {}
      self.parseChunk(chunk)
 
   def _process_line(self, line, start_flag):
      #print "process line: %s" % line
      tuple = 0
      m = re.match(RE_START_MEANING, line)
      if m:
         start_flag[0] = 1 
         tuple = (TAG_START_MEANING, m.string[m.end():])
         self.Entry['meaning'].extend([tuple])
         return

      m = re.match(RE_START_EXAMPLE_SENTENCE, line)
      if m:
         start_flag[0] = 2 
         return

      m = re.match(RE_START_EXAMPLE_TRANSLATION, line)
      if m:
         start_flag[0] = 2
         return
      
      m = re.match(RE_START_DEFINITION, line)
      if m:
         start_flag[0] = 2 
         return  

      m = re.match(RE_START_ENTRY, line) 
      if m:
         #print 'entry=%s' % line
         self.Entry['entry'] = m.string[m.end():]
         self.Entry['meaning'] = []  
         start_flag[0] = 0
         return

      m = re.match(RE_START_YINBIAO, line)
      if m:
         start_flag[0] = 2 
         return 

      m = re.match(RE_START_SEARCH_OTHER, line)
      if m:
         self.Entry['searchRelatedVocabulary'] = m.string[m.end():]
         return

      m = re.match(RE_START_DUANYU, line)
      if m:
         start_flag[0] = 2 
         return

      m = re.match(RE_START_SYNONYM, line)
      if m:
         start_flag[0] = 2 
         return  

      m = re.match(RE_START_ANTONYM, line)
      if m:
         start_flag[0] = 2 
         return 

      m = re.match(RE_START_DERIVATIVE, line)
      if m:
         start_flag[0] = 2 
         return

      m = re.match(RE_START_REFER_TO, line)
      if m:
         start_flag[0] = 2 
         return

      m = re.match(RE_START_PICK_OUT, line)
      if m:
         start_flag[0] = 2 
         return

      m = re.match(RE_START_REMARK, line)
      if m:
         start_flag[0] = 2 
         return

      #analyze mutil rows for meaning tag
      if start_flag[0] == 1: 
         tuple = (TAG_START_MEANING_NONE, line)
         self.Entry['meaning'].extend([tuple])
         return
      else:
         pass

   def parseChunk(self, chunk):
      """this function parse the chunk and generate the Entry object.
      chunk is a list of lines previously fetched from dictionary file."""
      start_flag = [0]   # :citiao 1:meaning 2: all others 
      for line in chunk:
         self._process_line(line, start_flag)
     

