"""author lzj"""

class DictFile:
   def __init__(self, dictfilename, encoding):
      self.peek_line = ''
      try:
         from codecs import open
         self.openFile = open(dictfilename, 'r', encoding)
      except Exception, e:
         print 'DictFile.__init__' + ' : ' + str(e)

   def getLine(self):
      return self.openFile.readline()

   def getChunk(self):
      """ Currently for Han-Han dictionary, a chunk is an entry with pronounciation,
      explanation, and examples grouped together. Please keep an eye on this method
      during development to ensure dictionaries other than Han-Han also can conform
      this base method. !!!!Assuming the chunks in the dictionary is separated by a
      empty line"""
      chunk = []
      count = 0
      reach_next_chunk = False
      if len(self.peek_line) != 0:
         chunk.extend([self.peek_line.strip()])
         self.peek_line = ''
      while True:
         if reach_next_chunk:
            break
         line = self.getLine()
         if len(line) != 0:
            if line == u'\r\n' or line == u'\n':
               if(count == 0):  #CTC_prm skip the blank line in the file head
                  continue
               # peek more lines to see if there are empty lines
               while True:
                  self.peek_line = self.getLine()
                  #print self.peek_line
                  if len(self.peek_line) == 0:
                     break;
                  if not (self.peek_line == u'\r\n' or self.peek_line == u'\n'):
                     if self.peek_line.startswith(u'[@]'):
                        reach_next_chunk = True
                        #print 'aaaaa'
                        break
                     else:
                        chunk.extend([self.peek_line.strip()])
                        self.peek_line = ''
                        if count == 0:
                           count = count + 1
                        print self.peek_line.strip()
                  else:
                     self.peek_line = ''
                     #print 'ccccc'
            else:
               if count == 0:     #CTC_prm increase count if it equal 0
                  count = count + 1  
               if (len(chunk) >= 1):
                  if line.startswith(u'[@]'):
                     self.peek_line = line
                     reach_next_chunk = True
                     break
               chunk.extend([line.strip()])
         else: 
            break
      return chunk

""" added by prm, used for English chinese dictionary"""
class EeDictFile:
   def __init__(self, dictfilename, encoding):
      self.peek_line = ''
      try:
         from codecs import open
         self.openFile = open(dictfilename, 'r', encoding)
      except Exception, e:
         print 'DictFile.__init__' + ' : ' + str(e)

   def getLine(self):
      return self.openFile.readline()

   def getChunk(self):
      count = 0
      meetCiTiaoCount = 0
      chunk = []
      if len(self.peek_line) != 0:
         chunk.extend([self.peek_line.strip()])  
         meetCiTiaoCount = 1
         self.peek_line = ''
      while True:
         self.peek_line = self.getLine()         
         if len(self.peek_line) != 0:
            if self.peek_line == u'\r\n' or self.peek_line == u'\n':
               if(count == 0):  #skip the blank line in the file head
                  continue
            if not (self.peek_line == u'\r\n' or self.peek_line == u'\n'):
               if self.peek_line.startswith(u'[@]') and meetCiTiaoCount == 1:
                  #print 'ddd=%s' % self.peek_line.encode('gbk')
                  break
               if self.peek_line.startswith(u'[@]') and meetCiTiaoCount == 0:
                  meetCiTiaoCount = 1
               if count == 0:     #increase count if it equal 0
                  count = count + 1
               chunk.extend([self.peek_line.strip()])
               #print "add to chunk: %s" % self.peek_line.strip().encode('gbk')
            else:
               self.peek_line = ''
         else:   #end of file
            break
      return chunk
       
