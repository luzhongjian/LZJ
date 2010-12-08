"""author lzj"""
import sys

class DictFile:
   def __init__(self, dictfilename, encoding):
      self.peek_line = ''
      try:
         from codecs import open
         self.openFile = open(dictfilename, 'r', encoding)
      except Exception, e:
         print >> sys.stderr, 'DictFile.__init__' + ' : ' + str(e)

   def getLine(self):
      return self.openFile.readline()

   def getChunk(self):
      """ Currently for Han-Han dictionary, a chunk is an entry with pronounciation,
      explanation, and examples grouped together. Please keep an eye on this method
      during development to ensure dictionaries other than Han-Han also can conform
      this base method. !!!!Assuming the chunks in the dictionary is separated by a
      empty line"""
      chunk = []
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
                        #print 'bbbbb'
                  else:
                     self.peek_line = ''
                     #print 'ccccc'
            else:
               if (len(chunk) >= 1):
                  if line.startswith(u'[@]'):
                     self.peek_line = line
                     reach_next_chunk = True
                     break
               chunk.extend([line.strip()])
         else:
            break
      return chunk

