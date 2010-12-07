#coding=utf-8
""" added by prm """
from dict_file import EcDictFile
import re               #import regular expression

RE_START_ENTRY               =  re.compile('^\[@\]')   #citiao
RE_START_YINBIAO             =  re.compile('^\[#\]')   #yinbiao
RE_START_SEARCH_OTHER        =  re.compile('^\[\*\]')  #search other related vocabulary
RE_START_DEFINITION          =  re.compile('^\[\$\]')  #cixing
RE_START_MEANING             =  re.compile('^\[%\]')   #shiyi. This may also be a cross-reference
RE_START_EXAMPLE_SENTENCE    =  re.compile('^\[\^\]')  #liju
RE_START_EXAMPLE_TRANSLATION =  re.compile('^\[&\]')   #liju translation
RE_START_DUANYU              =  re.compile(u'^\[\u77ed\u8bed\]')       #duan yu
RE_START_SYNONYM             =  re.compile(u'^\[\u540c\u4e49\u8bcd\]') #synonym
RE_START_ANTONYM             =  re.compile(u'^\[\u53cd\u4e49\u8bcd\]') #antonym 
RE_START_DERIVATIVE          =  re.compile(u'^\[\u6d3e\u751f\u8bcd\]') #derivative
RE_START_REFER_TO            =  re.compile(u'^\[\u53c2\u89c1\]')       #canjian
RE_START_PICK_OUT            =  re.compile(u'^\[\u8fa8\u6790\]')       #bianxi
RE_START_REMARK              =  re.compile(u'^\[\u5907\u6ce8\]')       #note


TAG_START_MEANING       = 0
TAG_EXAMPLE_SENTENCE    = 1
TAG_EXAMPLE_TRANSLATION = 2
TAG_DUANYU              = 3
TAG_START_SYNONYM       = 4
TAG_START_ANTONYM       = 5
TAG_START_DERIVATIVE    = 6
TAG_START_REFER_TO      = 7 
TAG_START_PICK_OUT      = 8
TAG_START_REMARK        = 9
TAG_OTHERS_NONE              = 10
TAG_MEANING_AND_EXAMPLE_NONE = 11
class ECDictFile(EcDictFile):
   pass

class ECDictEntry:
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
         if (start_flag[0] != 2):
            dict = {}
            dict['cixing']  = ' ' #space
            dict['meaningAndExample'] = []  # m.string[m.end():]
            #dict['example'] = []
            self.Entry['definition'].extend([dict])
         start_flag[0] = 3
         tuple = (TAG_START_MEANING, m.string[m.end():])
         self.Entry['definition'][-1]['meaningAndExample'].extend([tuple])
         return

      m = re.match(RE_START_EXAMPLE_SENTENCE, line)
      if m:
         if (start_flag[0] != 2 and start_flag[0] != 3): 
            dict = {}
            dict['cixing']  = ' '
            dict['meaningAndExample'] = []  # m.string[m.end():]
            #dict['example'] = []
            self.Entry['definition'].extend([dict]) 
         start_flag[0] = 4
         tuple = (TAG_EXAMPLE_SENTENCE, m.string[m.end():])
         self.Entry['definition'][-1]['meaningAndExample'].extend([tuple])
         return

      m = re.match(RE_START_EXAMPLE_TRANSLATION, line)
      if m:
         if (start_flag[0] != 2 and start_flag[0] != 3 and start_flag[0] != 4): 
            dict = {}
            dict['cixing']  = ' '
            dict['meaningAndExample'] = []  # m.string[m.end():]
            #dict['example'] = []
            self.Entry['definition'].extend([dict])
         start_flag[0] = 5
         tuple = (TAG_EXAMPLE_TRANSLATION, m.string[m.end():])
         self.Entry['definition'][-1]['meaningAndExample'].extend([tuple])
         return
      
      m = re.match(RE_START_DEFINITION, line)
      if m:
         start_flag[0] = 2
         dict = {}
         dict['cixing']  = m.string[m.end():]
         dict['meaningAndExample'] = []   
         #dict['example'] = []
         self.Entry['definition'].extend([dict])
         return  

      m = re.match(RE_START_ENTRY, line) 
      if m:
         #print 'entry=%s' % line
         self.Entry['entry'] = m.string[m.end():]
         self.Entry['definition'] = []
         self.Entry['others']  = []   
         return

      m = re.match(RE_START_YINBIAO, line)
      if m:
         self.Entry['yinbiao'] = m.string[m.end():]
         return 

      m = re.match(RE_START_SEARCH_OTHER, line)
      if m:
         self.Entry['searchRelatedVocabulary'] = m.string[m.end():]
         return

      m = re.match(RE_START_DUANYU, line)
      if m:
         if start_flag[0] != 6:
            start_flag[0] = 6
         tuple = (TAG_DUANYU, m.string[m.end():])  
         self.Entry['others'].extend([tuple])
         return

      m = re.match(RE_START_SYNONYM, line)
      if m:
         if start_flag[0] != 7:
            start_flag[0] = 7
         #print  start_flag[0]
         tuple = (TAG_START_SYNONYM, m.string[m.end():])
         self.Entry['others'].extend([tuple])
         return  

      m = re.match(RE_START_ANTONYM, line)
      if m:
         if start_flag[0] != 8:
            start_flag[0] = 8
         tuple = (TAG_START_ANTONYM, m.string[m.end():])
         self.Entry['others'].extend([tuple])
         return 

      m = re.match(RE_START_DERIVATIVE, line)
      if m:
         if start_flag[0] != 9:
            start_flag[0] = 9
         tuple = (TAG_START_DERIVATIVE, m.string[m.end():])
         self.Entry['others'].extend([tuple])
         return

      m = re.match(RE_START_REFER_TO, line)
      if m:
         if start_flag[0] != 10:
            start_flag[0] = 10
         tuple = (TAG_START_REFER_TO, m.string[m.end():])
         self.Entry['others'].extend([tuple])
         return

      m = re.match(RE_START_PICK_OUT, line)
      if m:
         if start_flag[0] != 11:
            start_flag[0] = 11
         tuple = (TAG_START_PICK_OUT, m.string[m.end():])
         self.Entry['others'].extend([tuple])
         return

      m = re.match(RE_START_REMARK, line)
      if m:
         if start_flag[0] != 12:
            start_flag[0] = 12
         tuple = (TAG_START_REMARK, m.string[m.end():])
         self.Entry['others'].extend([tuple])
         return

      #analyze mutil rows for one tag
      if start_flag[0] == 3:
         tuple = (TAG_MEANING_AND_EXAMPLE_NONE, line)
         #print line
         self.Entry['definition'][-1]['meaningAndExample'].extend([tuple])
         return
      elif  start_flag[0] == 4:
         tuple = (TAG_MEANING_AND_EXAMPLE_NONE, line)
         #print line
         self.Entry['definition'][-1]['meaningAndExample'].extend([tuple])
         return 

      elif  start_flag[0] == 5:
         tuple = (TAG_MEANING_AND_EXAMPLE_NONE, line)
         self.Entry['definition'][-1]['meaningAndExample'].extend([tuple])
         return

      elif start_flag[0] == 6: 
         tuple = (TAG_OTHERS_NONE, line)
         self.Entry['others'].extend([tuple])  
         return

      elif  start_flag[0] == 7:
         tuple = (TAG_OTHERS_NONE, line)
         self.Entry['others'].extend([tuple])  
         return

      elif  start_flag[0] == 8:
         tuple = (TAG_OTHERS_NONE, line)
         self.Entry['others'].extend([tuple])
         return

      elif  start_flag[0] == 9:
         tuple = (TAG_OTHERS_NONE, line)
         self.Entry['others'].extend([tuple])
         return

      elif  start_flag[0] == 10:
         tuple = (TAG_OTHERS_NONE, line)
         self.Entry['others'].extend([tuple])
         return

      elif  start_flag[0] == 11:
         tuple = (TAG_OTHERS_NONE, line)
         self.Entry['others'].extend([tuple])
         return

      elif  start_flag[0] == 12:
         tuple = (TAG_OTHERS_NONE, line)
         self.Entry['others'].extend([tuple])
         return

   def parseChunk(self, chunk):
      """this function parse the chunk and generate the Entry object.
      chunk is a list of lines previously fetched from dictionary file."""
      start_flag = [0]   # 0:citiao 1:yinbiao 2:cixing 3:meaning 4:example sentence 5:example translation >=6 others 
      for line in chunk:
         self._process_line(line, start_flag)
     

