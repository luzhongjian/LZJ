#coding=utf-8
from xml.sax import make_parser, SAXException
from xml.sax.handler import ContentHandler
from xml.sax.handler import EntityResolver
from xml.sax.handler import ErrorHandler
from gen_cc_bin_file import SEQ_NUM_IN_CHINESE
import codecs
import re

RE_PHR_V = re.compile(u'\uE003')
RE_SYN   = re.compile(u'\uE004')
RE_IDM   = re.compile(u'\uE002')
RE_2022  = re.compile(u'\u2022')
RE_2009  = re.compile(u'\u2009')

RawOxfordFileNameList = []

class OxfordContentErrorHandler(ErrorHandler):
   pass

class OxfordContentEntityResolver(EntityResolver):
   def resolveEntity(self, publicId, systemId):
      print "publicId = %d, systemId = %d" % (publicId, systemId)
from random import random
class OxfordContentHandler(ContentHandler):
    def __init__(self,name):
        self.look_for = name
        self.is_name, self.is_mobile = None, None
        self.buffer = ''
        self._discard = False
        self.outputfilename = r'd:\merlioncolor\oxford' + str(random())[5:8] + '.txt'
        RawOxfordFileNameList.append(self.outputfilename)
        self.outputfh = codecs.open(self.outputfilename, 'w', 'utf-16')
        self.entrylines = []
        self._in_headword_group = False
        self._sense_discriminator_exists = False
    #### >>> Method handler starts ###
    # Start
    ##################################
    ## 'd'
    #def start_64(self):
    #    self.entrylines.append(self.buffer)
    #    self.entrylines.append(u'\n')
    ## 'h-g'
    def start_68x2dx67(self):
        self._in_headword_group = True

    ## 'fm'
    def start_66x6d(self):
        self.entrylines.append(self.buffer)
        self.buffer = ''
    ## 'pv'
    def start_70x76(self):
        self.entrylines.append(self.buffer)
        self.buffer = ''
        self.entrylines.append(u'\n')
    ## 'sd'
    def start_73x64(self):
        self._sense_discriminator_exists = True
        if u'\u25b8' in self.entrylines[-1]:
           self.entrylines[-1] = u'\n' + self.entrylines[-1]
    ## 'unbox' omit Language Bank / Vocabulary Building etc.
    def start_75x6ex62x6fx78(self):
       self._discard = True

    ## 'x'
    def start_78(self):
        self.entrylines.append(self.buffer)
        self.buffer = ''
        self.entrylines.append(u'\uE010')

    ## 'z_awlsym'
    def start_7ax5fx61x77x6cx73x79x6d(self):
        self.entrylines.append(self.buffer)
        self.buffer = ''

    ## 'z_oppsym'
    def start_7ax5fx6fx70x70x73x79x6d(self):
       self.entrylines.append(u' [')
    # End
    ##################################
    ## 'z_i-g'
    #def end_7ax5fx69x2dx67(self):
    #    if self._in_headword_group:
    #       pass
    #    else:
    #       raise AttributeError
    ## 'cf'
    def end_63x66(self):
       self.entrylines.append(u'\n')
       self.entrylines.append(self.buffer)
       self.entrylines.append(u':')
    ## 'fm'
    def end_66x6d(self):
        self.entrylines.append(u'\u2018')
        self.entrylines.append(self.buffer)
        self.entrylines.append(u'\u2019')
    ## 'h'
    def end_68(self):
        pass
    ## 'id'
    def end_69x64(self):
       self.entrylines.append(u'\n')
       self.entrylines.append(self.buffer)
       self.entrylines.append(u':')
    ## 'cf'
    def end_63x66(self):
       self.entrylines.append(self.buffer)
       self.entrylines.append(u':')
    ## 'n-g'
    #def end_6ex2dx67(self):
    #    self.buffer += '\n'
    #    self.entrylines.append(self.buffer)
    ## 'z_p'
    #def end_7ax5fx70(self):
    #    pass
    ## 'pv'
    def end_70x76(self):
       self.entrylines.append(self.buffer)
       self.entrylines.append(u':')
    ## z_p_in_p-g
    def  end_7ax5fx70x5fx69x6ex5fx70x2dx67(self):
        #self.entrylines.append(u'[$]' + u'\u25A0' + self.buffer)
        self.entrylines.append(u'\u25A0' + self.buffer)
    ## 'i'
    #def end_69(self):
    #    if self._in_headword_group:
    #       self.entrylines.append(u'[#]' + self.buffer.strip() + u'\n')
    #    else:
    #       raise AttributeError
    ## 'runhd'
    def end_72x75x6ex68x64(self):
        self.outputfh.write(u'[@]' + self.buffer + u'\n')
        self.entrylines = []
        self._sense_discriminator_exists = False
    ## 'entry'
    def end_65x6ex74x72x79(self):
        self.outputfh.write(repl_str(u''.join(self.entrylines) + u'\n'))
        self.entrylines = []

    ## 'unbox' omit Language Bank / Vocabulary Building etc.
    def end_75x6ex62x6fx78(self):
       self._discard = False

    ## 'z_etymsym'
    def end_7ax5fx65x74x79x6dx73x79x6d(self):
       self.buffer = '[' + self.buffer + ']'
       self.entrylines.append(self.buffer)

    ## 'h-g'
    def end_68x2dx67(self):
        self.outputfh.write(repl_str(u'[#]' + u''.join(self.entrylines).strip() + u'\n'))
        self.entrylines = []
        self._in_headword_group = False
    ## 'p-g'
    def end_70x2dx67(self):
        self.entrylines.append(u'\n')
    ## 'x'
    def end_78(self):
        self.entrylines.append(self.buffer)
        self.buffer = ''
        self.entrylines.append(u'\uE011')
    ## 'z'
    def end_7a(self):
        if self.buffer == u'\u25A0':
           self.buffer = ''
        else:
           self.entrylines.append(self.buffer)
    ## 'z_awlsym'
    def end_7ax5fx61x77x6cx73x79x6d(self):
       pass
    ## 'z_core_h'
    def end__7ax5fx63x6fx72x65x5fx68(self):
       pass
    ## 'z_coresym'
    def end_7ax5fx63x6fx72x65x73x79x6d(self):
       pass
    ## 'z_coresym2'
    def end_7ax5fx63x6fx72x65x73x79x6dx32(self):
       pass
    ## 'z_helpsym'
    def end_7ax5fx68x65x6cx70x73x79x6d(self):
       HELP_STR = 'HELP'
       self.buffer = self.buffer[:-len(HELP_STR)] + '[' + HELP_STR +']'
       self.entrylines.append(self.buffer)
    ## 'z_oppsym'
    def end_7ax5fx6fx70x70x73x79x6d(self):
       self.entrylines.append(self.buffer)
       self.entrylines.append(u'] ')
    ## 'z_spc_pre'
    #def end_7ax5fx73x70x63x5fx70x72x65(self):
    #   pass
    ## 'zn'
    def end_7ax6e(self):
       value = int(self.buffer, 10)
       if self._sense_discriminator_exists:
          self._sense_discriminator_exists = False
       else:
          self.entrylines.append(u'\n')
       try:
          self.buffer = SEQ_NUM_IN_CHINESE[value - 1]
       except IndexError:
          self.buffer = "%d." % value
       self.entrylines.append(self.buffer)
    ## 'z_unbox'
    #def end_7ax5fx75x6ex62x6fx78(self):
    #   self.buffer = '[' + self.buffer + ']'
    #   self.entrylines.append(self.buffer)

    #### <<< Method handler ends ###
    def startElement(self,name,attrs):
        #print "startElement " + name
        def hexrepr(x):
           return "%02x" % x
        methodname = 'start_' +'x'.join(map(hexrepr, map(ord, name)))
        try:
           method = getattr(self, methodname)
           method()
        except AttributeError:
           pass

    def endElement(self,name):
        def hexrepr(x):
           return "%02x" % x
        #print "endElement " + name,
        methodname = 'end_' +'x'.join(map(hexrepr, map(ord, name)))
        try:
           method = getattr(self, methodname)
           method()
        except AttributeError:
           #if not self._in_headword_group:
           if (not self._discard):
              self.entrylines.append(self.buffer)
           #print "*** no method", methodname
        self.buffer = ""

    def characters(self,chars):
       self.buffer += chars

def repl_str(s):
   s = RE_PHR_V.sub(u'\n[PHR V] ', s)
   s = RE_SYN.sub(u' [SYN] ', s)
   s = RE_IDM.sub(u'\n[IDM] ', s)
   s = RE_2022.sub(u'', s)
   s = RE_2009.sub(u'', s)
   return s

def ParseOxford(name):
    handler = OxfordContentHandler(name)
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(OxfordContentErrorHandler())
    try:
       parser.parse(open(r'D:\MerlionColor\OxfordForProcessing\oxford.xml'))
    except SAXException:
        #return handler.mobile
        #pass
        raise
    return None

def CookOxfordFile(name):
   """ Re-arrane the Oxford file so that no empty line within a word entry and
   only one empty line between word entries"""
   rawfh = codecs.open(name, 'r', 'utf-16')
   cookedfh = codecs.open(name[:-3] + '_cooked.txt', 'w', 'utf-16')
   lines_in_one_entry = []
   while True:
      line = rawfh.readline()
      if (len(line) == 0):
         break;
      line = line.strip()
      if line.startswith(u'[@]'):
         if (len(lines_in_one_entry) == 0):
            lines_in_one_entry.append(line)
         else:
            cookedfh.write(u'\n'.join(lines_in_one_entry) + u'\n' * 2)
            lines_in_one_entry = []
            lines_in_one_entry.append(line)
      else:
         if (len(line) != 0):
            lines_in_one_entry.append(line)
   rawfh.close()
   cookedfh.close()

if __name__ == '__main__':
    import sys
    name = ' '.join(sys.argv[1:])
    ParseOxford(name)
    CookOxfordFile(RawOxfordFileNameList[0])

    
