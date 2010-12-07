"""Use this tool to check the newly added Han-Han entries from Seng Heng
in the mail dated 26 April 2010"""

def GetSengHengSet():
   from added_hhentries import AddedHHDictFile, AddedHHDictEntry
   added_hhdict_file = AddedHHDictFile(r'd:\MerlionColor\new_entries_sengheng_0426_manually_paste.txt', 'utf-8')
   result_l = []

   while True:
      chunk = added_hhdict_file.getChunk()
      if len(chunk) == 0:
         break;
      #print ''.join(chunk).encode('gb18030')
      #print '********************************************'

      entry = AddedHHDictEntry(chunk)
      entry = entry.Entry

      result_l.extend([entry['entry'].lstrip()])
      print "New entries: %d" % len(result_l)
      #print entry['entry'].encode('gb18030')

   SengHengSet = frozenset(result_l)
   return SengHengSet

if __name__ == '__main__':
   from test import GetSetOfHHDict
   SengHengSet = GetSengHengSet()
   HHDictSet = GetSetOfHHDict()
   print 'HHDictSet len = %d' % len(HHDictSet)
   #for i in HHDictSet:
   #   print i.encode('gb18030')
   #for i in SengHengSet:
   #   print i.encode('gb18030')
   NewlyAddedSet = (SengHengSet | HHDictSet) - HHDictSet
   print 'SengHengSet len = %d' % len(SengHengSet)
   for i in NewlyAddedSet:
      print i.encode('gb18030')

