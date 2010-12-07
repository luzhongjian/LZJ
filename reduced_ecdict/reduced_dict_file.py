""" added by prm, used for English chinese dictionary"""
class reducedEcDictFile:
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
      meetCiTiaoCount = 0
      chunk = []
      if len(self.peek_line) != 0:
         chunk.extend([self.peek_line.strip()])  
         meetCiTiaoCount = 1
         self.peek_line = ''
      while True:
         self.peek_line = self.getLine()         
         if len(self.peek_line) != 0:
            #if len(self.peek_line.strip()) != 0:
            if not (self.peek_line == u'\r\n' or self.peek_line == u'\n'):
               if self.peek_line.startswith(u'[@]') and meetCiTiaoCount == 1:
                  print 'ddd=%s' % self.peek_line.encode('gbk')
                  break
               if self.peek_line.startswith(u'[@]') and meetCiTiaoCount == 0:
                  meetCiTiaoCount = 1 
               chunk.extend([self.peek_line.strip()])
               #print "add to chunk: %s" % self.peek_line.strip().encode('gbk')
            else:
               self.peek_line = ''
         else:   #end of file
            break
      return chunk
       
