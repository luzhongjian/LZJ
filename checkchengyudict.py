"""1.original list is create by original chengyu.txt
   2.newlist is the output file  :mergedchengyu_list.txt  renamed:hhdict-tmp.txt
   3.return is a lost list after merge
"""
def checkchengyudict(originallist,newlist):
   len1=len(originallist)
   len2=len(newlist)
   print "len1=%d    len2=%d"%(len1,len2)
   for i in xrange(len2):
      len1=len(originallist)
      for j in xrange(len1):
         if newlist[i]['entry']==originallist[j]['entry'] and  newlist[i]['pinyin']==originallist[j]['pinyin'] and  newlist[i]['definition']==originallist[j]['definition'] :
            originallist.remove(originallist[j])
            break
   return originallist


