# encoding=utf-8
from pinyin_sort import transform_pinyin


#count = 0
#print_count = 0
#"""check nearby entries"""
#def check_nearby_entries(list, entry):
#   global count
#   global print_count
#   print_count += 1
#   if (print_count == 1000):
#      print "*%d" % count #'\n***### check %s against' % entry['entry'].encode('gbk'),
#      print_count = 0
#   count += 1
#   bottom = -len(list) #max(-len(list), -500)
#   for i in xrange(-1, bottom, -1):
#      try:
#         #print list[i]['entry'].encode('gbk'),
#         if (list[i]['entry'] == entry['entry']):
#            if (True): #transform_pinyin(list[i]['pinyin']) == transform_pinyin(entry['pinyin'])):
#               return i
#      except IndexError:
#         break
#         print "check_nearby_entries: silently caught IndexError"
#         pass
#   return 0
HANSVISION=0
CHENGYU=1

"""list1 and list2 should be sorted. Merge list2 INTO list1. i.e., list2 should
be far shorter than list1"""
def dict_merge_for_indexing(list1, list2):
   str=''
   py=''
   new_result = []
   from pinyin_sort import transform_pinyin, pinyin_cmp
   i, j ,doubleDic= 0, 0 ,0
   max_i, max_j = len(list1), len(list2)
   print "max_i=%d"%max_i
   print "max_j=%d"%max_j
   for i in xrange(max_i):
      new_dict={}
      new_dict[HANSVISION]=list1[i]#hs dict
      #new_dict[CHENGYU]={}#cy dict
      new_result.append(new_dict)
   for m in xrange(max_j):
      #print "m=%d"%m
      positionL,positionR,position,flag=0,0,0,0
      max_i=len(new_result)
      #print "max_i--->%d"%max_i
      for n in xrange(max_i):
         if HANSVISION in new_result[n].keys():
            str= new_result[n][HANSVISION]['entry'][:1]
            py=new_result[n][HANSVISION]['pinyin']
         else:
            str= new_result[n][CHENGYU]['entry'][:1]
            py=new_result[n][CHENGYU]['pinyin']
         if str==list2[m]['entry'][:1]:
             flag=1
             x=pinyin_cmp(transform_pinyin(py), transform_pinyin(list2[m]['pinyin']))
             #print "x=%d"%x
             if x>0:
                positionL=n
             elif x<0:
                positionR=n
             else:
                position=n
                break
      if flag==0:
         #print "no words"
            #x=pinyin_cmp(transform_pinyin(new_result[n]['pinyin']), transform_pinyin(list2[m]['pinyin']))
         new_dict={}
         new_dict[CHENGYU]=list2[m]
         new_result.append(new_dict)
         
      if position==0 and flag==1 :
         #print "positionL=%d"%positionL
         #print "positionR=%d"%positionR 
         if positionR==0:
            #print list2[m]['entry']
            new_dict={}
            new_dict[CHENGYU]=list2[m]
            new_result.insert(positionL,new_dict)
         else:
            new_dict={}
            new_dict[CHENGYU]=list2[m]
            new_result.insert(positionR,new_dict)
        
      else:
         #print "p----->%d"%position
         if flag==1:
            #new_result[position]['dictionary_type'].extend(list2[m]['dictionary_type'])
            if new_result[position][HANSVISION]['entry']==list2[m]['entry']:
               new_result[position][CHENGYU]=list2[m]
            else:
              if new_result[position+1][HANSVISION]['entry']==list2[m]['entry']:                     
                  new_result[position+1][CHENGYU]=list2[m]
              else:
                  new_dict={}
                  new_dict[CHENGYU]=list2[m]
                  new_result.insert(position+1,new_dict)

         
  

   return new_result

