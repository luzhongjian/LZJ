# coding = utf-8
# encoding=utf-8
""" Author :ctc_prm 
    Data: 2010.7.30 """

JIANPIN_MODE0     =     0  #normal jianpin(slect each first letter of each word to form one jianpin word)
JIANPIN_MODE1     =     1  #only for double word(all letters of first word + first letter of second one)
JIANPIN_MODE2     =     2  #only for double word(first letter of first word + all letters of second one)
from hhdict_file import HHDictFile, HHDictEntry
def load_hh_dict(file, encoding):
   hhdictfile = HHDictFile(file, encoding)

   result = []
   while True:
      chunk = hhdictfile.getChunk()
      if len(chunk) == 0:
         break;
      entry = HHDictEntry(chunk)
      entry = entry.Entry

      result.append(entry)
   return result 

def ciku_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode): 
   jianpin_list = []
   bl = False
   fl_beforespace = True
   ciku_entry_pinyin.strip()
   for item in ciku_entry_pinyin:
      if (jianpin_mode == JIANPIN_MODE0):
         if(fl_beforespace == True):
            jianpin_list.append(item)
            fl_beforespace = False
         if item==" ":  #assume only one space between Chinese character and English letter,need improve in future 
            fl_beforespace = True 
      elif(jianpin_mode == JIANPIN_MODE1):
         if(fl_beforespace == True):
            if (item != " "):
               jianpin_list.append(item)
            else:
               fl_beforespace = False
         else:
            jianpin_list.append(item)
            break 
      else:
         if(fl_beforespace == True):
            jianpin_list.append(item)
            if (bl == False):
               fl_beforespace = False
         if item==" ":   
            bl = True 
            fl_beforespace = True

   return jianpin_list

def ciku_2Characters_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode): 
   jianpin_list = []
   fl_beforespace = True
   bl = False
   ciku_entry_pinyin.strip()
   for item in ciku_entry_pinyin:
      if (jianpin_mode == JIANPIN_MODE0):
         if(fl_beforespace == True):
            jianpin_list.append(item)
            fl_beforespace = False
         if item==" ":  #assume that there is on space between Chinese character and English letter,need improve in future 
            jianpin_list.append(item) 
            fl_beforespace = True

      elif(jianpin_mode == JIANPIN_MODE1):
         if(fl_beforespace == True):
            if (item == " "): 
               fl_beforespace = False
            jianpin_list.append(item)
         else:
            jianpin_list.append(item)
            break
      else:
         if(fl_beforespace == True):
            jianpin_list.append(item)
            if (bl == False):
               fl_beforespace = False
         if item==" ": 
            jianpin_list.append(item)
            bl = True 
            fl_beforespace = True

   return jianpin_list

def ciku_pinyin_parser_space(ciku_entry_pinyin): 
   i = 0
   ciku_entry_pinyin.strip()
   for item in ciku_entry_pinyin:
      if item==" ":
         i+=1
   return i

def extract_vocabulary_from_ime_entry(ime_entry):
    count = 0
    list =ime_entry.split('\x09')
    list2=list[1].split('^')
    count = len(list2[0])
    return count

""" Support 'ü' 
     """
def extract_pinyin_from_ime_entry(ime_entry):
    ime_entry_pinyin = ""
    for item in ime_entry:
       if ((ord(item) >= 0x41 and ord(item) <= 0x5A) or (ord(item) >= 0x61 and ord(item) <= 0x7A) or (item == " ") or (ord(item) == 0xfc) ):
          ime_entry_pinyin  += item
       if(ord(item) == 0x09):
          break
    return ime_entry_pinyin

def extract_pinyin_without_space_from_ime_entry(ime_entry):
    ime_entry_pinyin = ""
    for item in ime_entry:
       if ((ord(item) >= 0x41 and ord(item) <= 0x5A) or (ord(item) >= 0x61 and ord(item) <= 0x7A)or (ord(item) == 0xfc)):
          ime_entry_pinyin  += item 
       if(ord(item) == 0x09):
          break
    return ime_entry_pinyin

def judget_whether_vocabulary_exist_in_ime_entry(ime_entry, ciku_vocabulary): 
   rt = False
   vocabulary = ''
   start = False 
   for item in ime_entry: 
       if (start == True):
           if(ord(item) != 0x5E):
               vocabulary +=item
           else:
               if(vocabulary == ciku_vocabulary):
                   return True
               vocabulary = ''
       if (ord(item) == 0x09):
         start = True

   if (vocabulary != ''):
      if(vocabulary == ciku_vocabulary):
         return True
      else:
         return rt
   else:
      return rt

def jianpin_string_len_without_space(ciku_entry_pinyin, jianpin_mode):
   len = 0
   bl = False
   if(jianpin_mode == JIANPIN_MODE0):
      len = ciku_pinyin_parser_space(ciku_entry_pinyin) + 1 # "abc"
   else:
      for item in ciku_entry_pinyin: 
         if(jianpin_mode == JIANPIN_MODE1):
            if (item == " "):
               len += 1
               break
            len += 1 
         else:
            if(bl== True):
               len +=1 
            if (item == " "):
               bl = True
               len += 1

   return len
def jianpin_string_len_with_space(ciku_entry_pinyin, jianpin_mode):
   len = 0
   bl = False
   if(jianpin_mode == JIANPIN_MODE0):
      len = ciku_pinyin_parser_space(ciku_entry_pinyin) + 2 # "a b"
   else:
      for item in ciku_entry_pinyin: 
         if(jianpin_mode == JIANPIN_MODE1):
            if (item == " "):
               len += 2 
               break
            len += 1 
         else:
            if(bl== True):
               len +=1 
            if (item == " "):
               bl = True
               len += 2

   return len

def string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_vocabulary,jianpinlist, jianpin_mode, bimelisttail): #first letter or each word
   rt = 0
   i  = 0
   pos = 0
   length = 0
   templist = []
   ime_entry_pinyin = extract_pinyin_from_ime_entry(ime_entry)
   for j in xrange(len(jianpinlist)):
      jianpinlist.pop()
  
   length = jianpin_string_len_without_space(ciku_entry_pinyin,jianpin_mode) 
   if (len(ime_entry_pinyin) != length):
      if (bimelisttail == True):
         templist = ciku_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
         for j in xrange(len(templist)):
            jianpinlist.append(templist[j])
      return -1
   else:
      validletter = True
      for item in ciku_entry_pinyin:
         if (jianpin_mode == JIANPIN_MODE0):
            if(validletter == True):
               validletter = False
               jianpinlist.append(ciku_entry_pinyin[pos])
               if(ciku_entry_pinyin[pos] != ime_entry_pinyin[i]):
                  if (bimelisttail == True):
                     for j in xrange(len(jianpinlist)):
                        jianpinlist.pop()
                     templist = ciku_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
                     for j in xrange(len(templist)):
                        jianpinlist.append(templist[j])
                  return -1
               else:
                  i +=1
                  if (i  == len(ime_entry_pinyin)):
                     break
            pos += 1
            if(item == " "): 
               validletter = True

         elif(jianpin_mode == JIANPIN_MODE1): #such as "anj"
            if(validletter == True):
               if (ciku_entry_pinyin[pos] != " "):
                  jianpinlist.append(ciku_entry_pinyin[pos]) 
               else:
                  pos += 1 #skip space
                  validletter = False
              
               if(ciku_entry_pinyin[pos] != ime_entry_pinyin[i]):
                  if (bimelisttail == True):                     
                     for j in xrange(len(jianpinlist)):
                        jianpinlist.pop()
                     templist = ciku_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
                     for j in xrange(len(templist)):
                        jianpinlist.append(templist[j])
                  return -1
               else:
                  pos += 1
                  i   += 1
            else:
               break
         else:    #such as "b an"
            if (ciku_entry_pinyin[pos] != " "):
               if(validletter == True):
                  jianpinlist.append(ciku_entry_pinyin[pos]) 
                  if(ciku_entry_pinyin[pos] != ime_entry_pinyin[i]):
                     if (bimelisttail == True):
                        for j in xrange(len(jianpinlist)):
                           jianpinlist.pop()
                        templist = ciku_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
                        for j in xrange(len(templist)):
                           jianpinlist.append(templist[j])
                     return -1
                  else:
                     i   += 1 
               if(pos == 0):
                  validletter = False
               pos += 1
            else:
               pos += 1 #skip space
               validletter = True 
      if (i == len(ime_entry_pinyin)):
         if (judget_whether_vocabulary_exist_in_ime_entry(ime_entry, ciku_vocabulary) == False): 
            temp_count = extract_vocabulary_from_ime_entry(ime_entry)
            if(temp_count == 1 or temp_count >2):
               return 1
            else:
               return 2
         else:                  #vocabulary exists in ime_entry
            return rt
      else:
         if (bimelisttail == True):
            for j in xrange(len(jianpinlist)):
               jianpinlist.pop()
            templist = ciku_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
            for j in xrange(len(templist)):
               jianpinlist.append(templist[j])
         return -1

def twocharacters_string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_vocabulary,jianpinlist, jianpin_mode, bimelisttail): #example: ban g(bang)
   rt = 0
   i  = 0
   pos = 0
   templist = [] 
   ime_entry_pinyin = extract_pinyin_from_ime_entry(ime_entry) #extract_pinyin_without_space_from_ime_entry(ime_entry)
   
   for j in xrange(len(jianpinlist)):
      jianpinlist.pop()
   if (len(ime_entry_pinyin) != jianpin_string_len_with_space(ciku_entry_pinyin, jianpin_mode)): 
      if (bimelisttail == True):
         templist = ciku_2Characters_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
         for j in xrange(len(templist)):
            jianpinlist.append(templist[j])
      return -1
   else:
      validletter = True 
      for item in ciku_entry_pinyin:
         if (jianpin_mode == JIANPIN_MODE0):
            if(validletter == True):
               validletter = False
               jianpinlist.append(ciku_entry_pinyin[pos])
               if(ciku_entry_pinyin[pos] != ime_entry_pinyin[i]):
                  if (bimelisttail == True):
                     for j in xrange(len(jianpinlist)):
                        jianpinlist.pop()
                     templist = ciku_2Characters_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
                     for j in xrange(len(templist)):
                        jianpinlist.append(templist[j])
                  return -1
            pos += 1
            if(item == " "):
               i += 1 
               if (ime_entry_pinyin[i] == " "):
                  jianpinlist.append(item)
                  i += 1
                  validletter = True
               else:
                  if (bimelisttail == True):
                     for j in xrange(len(jianpinlist)):
                        jianpinlist.pop()
                     templist = ciku_2Characters_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
                     for j in xrange(len(templist)):
                        jianpinlist.append(templist[j])
                  return -1
         elif (jianpin_mode == JIANPIN_MODE1):
            if(validletter == True):
               if (ciku_entry_pinyin[pos] != " "):
                  jianpinlist.append(ciku_entry_pinyin[pos]) 
               else:
                  pos += 1 #skip space
                  if (ime_entry_pinyin[i] == " "):
                     jianpinlist.append(ciku_entry_pinyin[pos]) 
                     validletter = False
                     i += 1
                  else:
                     if (bimelisttail == True):
                        for j in xrange(len(jianpinlist)):
                           jianpinlist.pop()
                        templist = ciku_2Characters_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
                        for j in xrange(len(templist)):
                           jianpinlist.append(templist[j])
                     return -1

               if(ciku_entry_pinyin[pos] != ime_entry_pinyin[i]):
                  if (bimelisttail == True):
                     for j in xrange(len(jianpinlist)):
                        jianpinlist.pop()
                     templist = ciku_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
                     for j in xrange(len(templist)):
                        jianpinlist.append(templist[j])
                  return -1
               else:
                  if(i < len(ime_entry_pinyin) -1):
                     pos += 1
                     i   += 1
            else:
               break
         else:
            if (ciku_entry_pinyin[pos] != " "):
               if(validletter == True):
                  jianpinlist.append(ciku_entry_pinyin[pos]) 
                  if(ciku_entry_pinyin[pos] != ime_entry_pinyin[i]):
                     if (bimelisttail == True):
                        for j in xrange(len(jianpinlist)):
                           jianpinlist.pop()
                        templist = ciku_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
                        for j in xrange(len(templist)):
                           jianpinlist.append(templist[j])
                     return -1
                  else:
                     if(i < len(ime_entry_pinyin) -1):
                        i   += 1
               if(pos == 0):
                  validletter = False
               pos += 1
            else:
               pos += 1 #skip space
               if (ime_entry_pinyin[i] == " "):
                  jianpinlist.append(ciku_entry_pinyin[pos]) 
                  validletter = True
                  i += 1
               else:
                  if (bimelisttail == True):
                     for j in xrange(len(jianpinlist)):
                        jianpinlist.pop()
                     templist = ciku_2Characters_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
                     for j in xrange(len(templist)):
                        jianpinlist.append(templist[j])
                  return -1
              
      if (i+1 == len(ime_entry_pinyin)):
         return 1 
      else:
         if (bimelisttail == True):
            for j in xrange(len(jianpinlist)):
               jianpinlist.pop()
               templist = ciku_2Characters_pinyin_parser_jianpin_letter(ciku_entry_pinyin, jianpin_mode)
            for j in xrange(len(templist)):
               jianpinlist.append(templist[j])
         return -1

def  compare_current_pinyin_with_remain_entry_in_ciku(current_ciku_entry_pinyin, current_index, ciku_entrylist, jianpin_mode):
   bDiff= False
   jianpinlist = ciku_pinyin_parser_jianpin_letter(current_ciku_entry_pinyin, jianpin_mode)
   jp = "".join(jianpinlist)
   for curIndex in xrange(current_index, len(ciku_entrylist)):   #jianpin
      if (ciku_entrylist[curIndex].has_key('pinyin')):
         if(ciku_pinyin_parser_space(ciku_entrylist[curIndex]['pinyin']) == 0):  #compare with single character
            ciku_entry_pinyin = ime_transform_syllable(ciku_entrylist[curIndex]['pinyin']) 
            ciku_entry_pinyin = ciku_entry_pinyin.lower()
            if (len(jp) == len(ciku_entry_pinyin)): 
               ipos = 0
               bDiff = False
               for ipos in xrange(len(jp)):
                  if (ciku_entry_pinyin[ipos] != jp[ipos]):
                     bDiff = True
                     break
               if (bDiff == False and ipos == len(jp) -1): 
                  return True
   return False

def string_quanpin_compare(ime_entry, ciku_entry_pinyin, ciku_vocabulary, btail):
   rt = 0
   i  = 0
   ime_entry_pinyin = extract_pinyin_from_ime_entry(ime_entry)
   py_list = ciku_entry_pinyin.split(' ')
   ck_entry_pin_without_space = ''.join(py_list)
   if (len(ime_entry_pinyin) != len(ck_entry_pin_without_space)):
      return -1
   else:
      for item in ck_entry_pin_without_space:
         if(item != ime_entry_pinyin[i]):
            return -1
         i +=1
      if (i == len(ime_entry_pinyin)):
         if (judget_whether_vocabulary_exist_in_ime_entry(ime_entry, ciku_vocabulary) == False):
            return 1
         else:                  #vocabulary exists in ime_entry
            return rt
      else:
         return -1
 
tone_to_value = {
                 u'ā': (u'a', 1), u'ū': (u'u', 1), u'ō': (u'o', 1), u'é': (u'e', 2),
                 u'ǐ': (u'i', 3), u'í': (u'i', 2), u'ì': (u'i', 4), u'ē': (u'e', 1),
                 u'ǒ': (u'o', 3), u'ǘ': (u'ü', 2), u'ě': (u'e', 3), u'ń': (u'n', 2),
                 u'ǚ': (u'ü', 3), u'ī': (u'i', 1), u'ù': (u'u', 4), u'ó': (u'o', 2),
                 u'ú': (u'u', 2), u'ò': (u'o', 4), u'ň': (u'n', 3), u'\ue7c8': (u'n', 4), #u'ǹ': (u'n', 4),
                 u'á': (u'a', 2), u'ǎ': (u'a', 3), u'ǜ': (u'ü', 4), u'à': (u'a', 4),
                 u'è': (u'e', 4), u'ǔ': (u'u', 3), u'Ｑ': (u'q', 4) }

def ime_transform_syllable(syllable):
   global tone_to_value
   transformed_syllable = []
   #tone = 5 # The 5th tone, neutral tone, qingsheng
   for letter in syllable:
      if tone_to_value.has_key(letter):
         ascii_letter = tone_to_value[letter][0]
         transformed_syllable.append(ascii_letter)
         #tone = tone_to_value[letter][1]
      else:
         transformed_syllable.append(letter)
  # transformed_syllable.append("%d" % tone)
   return ''.join(transformed_syllable)

def keyfunc(list):
   #return list.split('\x09')[0]
   return ''.join(list).split(u'\u0009')[0]

def ime_list_sorted(list, keyfunc):
   ime_list = sorted(list,key = keyfunc)
   return ime_list
def build_ime_index(genfile, ciku_entrylist):
   rt = 0
   curIndex = 0
   jianpinlist = [] 
   ime_entrylist = []
   temp_ime_entrylist = []
   try:
      from codecs import open 
      file = open(genfile, 'r', 'utf-16') 
      #file = open(genfile, 'r', 'utf-16le')
   except Exception, e:
      print 'file__' + ' : ' + str(e)
   
   ime_entrylist= file.readlines() 
   #import string
   #map(string.strip, ime_entrylist)
   for ime_entry in ime_entrylist:
      temp_ime_entrylist.append(''.join(ime_entry.strip()))
   ime_entrylist = temp_ime_entrylist
   file.close()
   file = open(r'd:\test1\PinYinIndex_utf16.txt', 'wb+') 
   for ciku_entry in ciku_entrylist:
      curIndex += 1
      if ciku_entry.has_key('pinyin'):
         ciku_entry_pinyin = ime_transform_syllable(ciku_entry['pinyin'])
         spacecount = ciku_pinyin_parser_space(ciku_entry_pinyin) 
         ciku_entry_pinyin = ciku_entry_pinyin.lower()   #convert into lower case
         if (spacecount == 0 or spacecount >= 2):    # one character or more than two characters
            if (len(ime_entrylist) == 0):
                ime_entry = ciku_entry_pinyin[0] + u'\u0009' + ciku_entry['entry']
                ime_entrylist.append(ime_entry) 
                if (len(ciku_entry_pinyin) > 1): 
                   ime_entry = ''.join(ciku_entry_pinyin.split()) + u'\u0009' + ciku_entry['entry']
                   ime_entrylist.append(ime_entry)
            else:
               i = 0
               btail = False
               """ 1. if character is same , don't add it twice.  2. don't consider capitalization, always do with pinyin according to lowercase  """
               for ime_entry in ime_entrylist:   #jianpin
                  i += 1
                  if(i == len(ime_entrylist)):
                     btail = True
                  #ime_entry_pinyin = extract_pinyin_from_ime_entry(ime_entry)
                  rt = string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], jianpinlist, JIANPIN_MODE0, btail)
                  if (rt == 1):  #add to the entry tail
                     ime_entrylist[i-1] += "^" + ciku_entry['entry']
                     #print ime_entrylist[i-1]
                     break
                  elif (rt == 0):
                     break 
                  else:
                     if(i == len(ime_entrylist)):
                        #jianpinlist = ciku_pinyin_parser_jianpin_letter(ciku_entry_pinyin, JIANPIN_MODE0)
                        ime_entry = "".join(jianpinlist) + u'\u0009' + ciku_entry['entry']
                        ime_entrylist.append(ime_entry)
                        #print ime_entrylist[i-1]
                        break
               i = 0
               btail = False
               for ime_entry in ime_entrylist:   #quanpin
                  i += 1
                  if(i == len(ime_entrylist)):
                     btail = True
                  #ime_entry_pinyin = extract_pinyin_from_ime_entry(ime_entry) 
                  rt = string_quanpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], btail)
                  if (rt == 1):  #add to the entry tail
                     ime_entrylist[i-1] += "^" + ciku_entry['entry']
                     #print ime_entrylist[i-1]
                     break
                  elif(rt == 0):
                     break
                  else:
                     if(i == len(ime_entrylist)):
                        ime_entry = ''.join(ciku_entry_pinyin.split()) + u'\u0009' + ciku_entry['entry']                        
                        ime_entrylist.append(ime_entry)
                        #print ime_entrylist[i-1]
                        break
         else: # spacecount == 1 means two characters
            """jianpin 0 for double words """  
            if(compare_current_pinyin_with_remain_entry_in_ciku(ciku_entry_pinyin, curIndex, ciku_entrylist, JIANPIN_MODE0)== True): #jian pin
               i = 0
               btail = False
               for ime_entry in ime_entrylist:   #jianpin
                  i += 1
                  if(i == len(ime_entrylist)):
                     btail = True
                  rt = twocharacters_string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], jianpinlist, JIANPIN_MODE0, btail)
                  if (rt == 1):  #add to the entry tail
                     ime_entrylist[i-1] += "^" + ciku_entry['entry']
                     #print ime_entrylist[i-1]
                     break
                  elif (rt == 0):
                     break 
                  else:
                     if(i == len(ime_entrylist)): 
                        ime_entry = "".join(jianpinlist) + u'\u0009' + ciku_entry['entry']
                        ime_entrylist.append(ime_entry)
                        #print ime_entrylist[i-1]
                        break
            else:
               bnotfound = False
               i = 0
               for ime_entry in ime_entrylist:   #jianpin
                  i += 1
                  rt = twocharacters_string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], jianpinlist, JIANPIN_MODE0, bnotfound)
                  if (rt == 1):  #add to the entry tail
                     ime_entrylist[i-1] += "^" + ciku_entry['entry']
                     #print ime_entrylist[i-1]
                     break
                  elif (rt == 0):
                     break 
                  else:
                     if(i == len(ime_entrylist)): 
                        bnotfound = True
                        break
               if (bnotfound == True):
                  i = 0
                  btail = False
                  for ime_entry in ime_entrylist:   #jianpin
                     i += 1
                     if(i == len(ime_entrylist)):
                        btail = True
                     rt = string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], jianpinlist, JIANPIN_MODE0, btail)
                     if (rt == 1):  #add to the list tail 
                        for j in xrange(len(jianpinlist)):
                           jianpinlist.pop()
                        templist = ciku_2Characters_pinyin_parser_jianpin_letter(ciku_entry_pinyin, JIANPIN_MODE0)
                        for j in xrange(len(templist)):
                           jianpinlist.append(templist[j])
                        ime_entry = "".join(jianpinlist) + u'\u0009' + ciku_entry['entry']
                        ime_entrylist.append(ime_entry)
                        break
                     elif (rt == 2):
                        ime_entrylist[i-1] += "^" + ciku_entry['entry']
                        #print ime_entrylist[i-1]
                        break
                     elif (rt == 0):
                     	break
                     else:
                        if(rt == -1 and i == len(ime_entrylist)):  #add jianpin without space
                           ime_entry = "".join(jianpinlist) + u'\u0009' + ciku_entry['entry']
                           ime_entrylist.append(ime_entry)
                           #print ime_entrylist[i-1]
                           break
            """ jianpin 1: all letters of first word + first letter of second one """
            if(compare_current_pinyin_with_remain_entry_in_ciku(ciku_entry_pinyin, curIndex, ciku_entrylist, JIANPIN_MODE1)== True): #jian pin
               i = 0
               btail = False
               for ime_entry in ime_entrylist:   #jianpin
                  i += 1
                  if(i == len(ime_entrylist)):
                     btail = True
                  rt = twocharacters_string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], jianpinlist, JIANPIN_MODE1, btail)
                  if (rt == 1):  #add to the entry tail
                     ime_entrylist[i-1] += "^" + ciku_entry['entry']
                     #print ime_entrylist[i-1]
                     break
                  elif (rt == 0):
                     break 
                  else:
                     if(i == len(ime_entrylist)): 
                        ime_entry = "".join(jianpinlist) + u'\u0009' + ciku_entry['entry']
                        ime_entrylist.append(ime_entry)
                        #print ime_entrylist[i-1]
                        break
            else:
               bnotfound = False
               i = 0
               for ime_entry in ime_entrylist:   #jianpin
                  i += 1
                  rt = twocharacters_string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], jianpinlist, JIANPIN_MODE1, bnotfound)
                  if (rt == 1):  #add to the entry tail
                     ime_entrylist[i-1] += "^" + ciku_entry['entry']
                     #print ime_entrylist[i-1]
                     break
                  elif (rt == 0):
                     break 
                  else:
                     if(i == len(ime_entrylist)):
                        bnotfound = True
                        break
               if (bnotfound == True):
                  i = 0 
                  btail = False
                  for ime_entry in ime_entrylist:   #jianpin
                     i += 1
                     if(i == len(ime_entrylist)):
                        btail = True
                     #ime_entry_pinyin = extract_pinyin_from_ime_entry(ime_entry)
                     rt = string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], jianpinlist, JIANPIN_MODE1, btail)
                     if (rt == 1):  #add to the list tail 
                        for j in xrange(len(jianpinlist)):
                           jianpinlist.pop()
                        templist = ciku_2Characters_pinyin_parser_jianpin_letter(ciku_entry_pinyin,JIANPIN_MODE1)
                        for j in xrange(len(templist)):
                           jianpinlist.append(templist[j])
                        ime_entry = "".join(jianpinlist) + u'\u0009' + ciku_entry['entry']
                        ime_entrylist.append(ime_entry)
                        #print ime_entrylist[i-1]
                        break
                     elif (rt == 2):
                        ime_entrylist[i-1] += "^" + ciku_entry['entry']
                        #print  ime_entrylist[i-1]
                        break
                     elif (rt == 0):
                        break
                     else:
                        if(rt == -1 and i == len(ime_entrylist)):  #add jianpin without space
                           ime_entry = "".join(jianpinlist) + u'\u0009' + ciku_entry['entry']
                           ime_entrylist.append(ime_entry)
                           #print ime_entrylist[i-1]
                           break
            """jianpin 2: first letter of first word + all letters of second one """ 
            if(compare_current_pinyin_with_remain_entry_in_ciku(ciku_entry_pinyin, curIndex, ciku_entrylist, JIANPIN_MODE2)== True): #jian pin
               i = 0
               btail = False
               for ime_entry in ime_entrylist:   #jianpin
                  i += 1
                  if(i == len(ime_entrylist)):
                     btail = True
                  rt = twocharacters_string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], jianpinlist, JIANPIN_MODE2, btail)
                  if (rt == 1):  #add to the entry tail
                     ime_entrylist[i-1] += "^" + ciku_entry['entry']
                     #print ime_entrylist[i-1]
                     break
                  elif (rt == 0):
                     break 
                  else:
                     if(i == len(ime_entrylist)): 
                        ime_entry = "".join(jianpinlist) + u'\u0009' + ciku_entry['entry']
                        ime_entrylist.append(ime_entry)
                        #print ime_entrylist[i-1]
                        break
            else:
               bnotfound = False
               i = 0
               for ime_entry in ime_entrylist:   #jianpin
                  i += 1
                  rt = twocharacters_string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], jianpinlist, JIANPIN_MODE2, bnotfound)
                  if (rt == 1):  #add to the entry tail
                     ime_entrylist[i-1] += "^" + ciku_entry['entry']
                     #print ime_entrylist[i-1]
                     break
                  elif (rt == 0):
                     break 
                  else:
                     if(i == len(ime_entrylist)):
                        bnotfound = True
                        break
               if (bnotfound == True):
                  i = 0 
                  btail = False
                  for ime_entry in ime_entrylist:   #jianpin
                     i += 1
                     if(i == len(ime_entrylist)):
                        btail = True
                     #ime_entry_pinyin = extract_pinyin_from_ime_entry(ime_entry)
                     rt = string_jianpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], jianpinlist, JIANPIN_MODE2, btail)
                     if (rt == 1):  #add to the list tail 
                        for j in xrange(len(jianpinlist)):
                           jianpinlist.pop()
                        templist = ciku_2Characters_pinyin_parser_jianpin_letter(ciku_entry_pinyin,JIANPIN_MODE2)
                        for j in xrange(len(templist)):
                           jianpinlist.append(templist[j])
                        ime_entry = "".join(jianpinlist) + u'\u0009' + ciku_entry['entry']
                        ime_entrylist.append(ime_entry)
                        #print ime_entrylist[i-1]
                        break
                     elif (rt == 2):
                        ime_entrylist[i-1] += "^" + ciku_entry['entry']
                        #print ime_entrylist[i-1]
                        break
                     elif (rt == 0):
                     	break 
                     else:
                        if(rt == -1 and i == len(ime_entrylist)):  #add jianpin without space
                           ime_entry = "".join(jianpinlist) + u'\u0009' + ciku_entry['entry']
                           ime_entrylist.append(ime_entry)
                           #print ime_entrylist[i-1]
                           break    
            """ quanbin for double words """
            i = 0
            btail = False
            for ime_entry in ime_entrylist:   #quanpin
               i += 1
               if(i == len(ime_entrylist)):
                  btail = True
               #ime_entry_pinyin = extract_pinyin_from_ime_entry(ime_entry) 
               rt = string_quanpin_compare(ime_entry, ciku_entry_pinyin, ciku_entry['entry'], btail)
               if (rt == 1):  #add to the entry tail
                  ime_entrylist[i-1] += "^" + ciku_entry['entry']
                  break
               elif(rt == 0):
                  break
               else:
                  if(i == len(ime_entrylist)):
                     ime_entry = ''.join(ciku_entry_pinyin.split()) + u'\u0009' + ciku_entry['entry']
                     ime_entrylist.append(ime_entry)
                     print ime_entrylist[i-1]
                     break
   ime_list = ime_list_sorted(ime_entrylist, keyfunc)
   file.write('\r\n'.join(ime_list).encode('utf-16le') + '\r\n'.encode('utf-16le'))
   #file.write('\r\n'.join(ime_list).encode('utf-16le') + '\r\n'.encode('utf-16le'))
   file.close()
if __name__ == '__main__':
   #ciku_entrylist = load_hh_dict(r'd:\hhdict-tmp.txt', 'gb18030')
   #ciku_entrylist = load_hh_dict(r'd:\hhdict-tmp.txt', 'utf-16')
   #ime_index_file = open(r'd:\PinYinIndex_utf16.txt', 'wb+')
   #ciku_entrylist = load_hh_dict(r'd:\test\hhdict-tmp.txt', 'gb18030')
   #ciku_entrylist = load_hh_dict(r'd:\test\hhdict-tmp.txt', 'utf-16')
   #ime_index_file = open(r'd:\test\PinYinIndex_utf16.txt', 'wb+') 
   #ciku_entrylist = load_hh_dict(r'd:\test1\hhdict-tmp.txt', 'gb18030')
   ciku_entrylist = load_hh_dict(r'd:\test1\hhdict-idiom-tmp.txt', 'utf-16') 
   #ime_index_file = open(r'd:\test1\PinYinIndex_utf16.txt', 'wb+') 
   #build_ime_index(ime_index_file, ciku_entrylist)
   build_ime_index(r'd:\test1\PinYinIndex_utf16.txt', ciku_entrylist)
   #ime_index_file.close() 
  

