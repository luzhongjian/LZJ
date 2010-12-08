"""Added by prm for generating English-Ehinese dictionary extracted index file"""
#encoding = utf-8

def restore_origin_entry(entry):
   out_line = []
   out_line.extend([u'[@]' + entry['entry']])
   if entry.has_key('yinbiao'):
      out_line.extend([u'[#]' + entry['yinbiao']])
   for others in entry['others']:
      (tag, str) = others
      #if (tag == 1):  
      out_line.extend([str])
      #print '%s' % str
   return u'\n'.join(out_line)  + 2 * u'\n'
   #return u'\r\n'.join(out_line) + 2 * u'\r\n'

def repr_entry(entry, indent = 0):
   result = []
   out_line = []
   result.append(entry['entry'])
   #print out_line
   if entry.has_key('yinbiao'):
      result.append(entry['yinbiao'] + u'\n')
      #print out_line
   if entry.has_key('others'):
      for others in entry['others']:
         (tag, str) = others
         #if (tag == 1):
         out_line.extend([str])
         #print out_line
   result.append(u'\n'.join(out_line)) #+ 2 * u'\r\n')
   return u''.join(result)

from eedict.eedict_file import EEDictFile, EEDictEntry
#from util.stringGenerator import stringGenerator
def load_ee_dict(file, encoding):
   eedictfile = EEDictFile(file, encoding)
   result = []
   while True:
      chunk = eedictfile.getChunk()
      if len(chunk) == 0:
         break;
      #print chunk
      entry = EEDictEntry(chunk)
      entry = entry.Entry
      result.append(entry)
   print "%d total entries size" % len(result)   
   """Added by zhong jian for sort entrys"""
   #from pinyin_sort import pinyin_cmp
   #from operator import itemgetter
   #sorted_result = sorted(result, cmp = pinyin_cmp, key = itemgetter('entry'))
   return result

DICT_ENTRY_CONST_LEN = 8 
from struct import pack, unpack
def generate_origin_dict_file(f, entrylist):
   for entry in entrylist:
      #print entry
      entry_text = restore_origin_entry(entry)
      f.write(entry_text.encode('utf-16le'))

def generate_ee_dict_file(f, entrylist):
   global DICT_ENTRY_CONST_LEN
   s = pack('H', len(entrylist))
   f.write(s)
   prev_offset = 0
   next_offset = 0
   cur = f.tell() 
   name_len    = 0
   yinbiao_len = 0
   for entry in entrylist:
      name_len = 0
      yinbiao_len = 0
      entry_text = repr_entry(entry)
      entry_name = entry['entry']
      name_len = len(entry_name) * 2
      #print entry_text

      if entry.has_key('yinbiao'):
         entry_yinbiao = entry['yinbiao'] 
         #print entry_yinbiao
         yinbiao_len = len(entry_yinbiao) * 2  
      next_offset = DICT_ENTRY_CONST_LEN + len(entry_text) * 2
      s = pack('HH', prev_offset, next_offset)
      s = s + pack('HH', name_len, yinbiao_len)
      f.write(s)
      f.write(entry_text.encode('utf-16le'))
      cur = cur + next_offset 
      prev_offset = next_offset  

def keyfunc(s):
   return s['entry'].lower()

def build_four_level_index(f1, f2, f3, f4, entrylist):
   global DICT_ENTRY_CONST_LEN
   CONST_LEN = 12
   prev_offset = 0
   next_offset = 0
   dict_offset = 2

   i   = 0
   d_3letters = {}
   d_2letters = {}
   d_1letters = {}

   d_level3 = {}
   d_level3_key = []
   temp_index = 0
   s = pack('H', len(entrylist))
   f4.write(s)

   #entrylist = sorted(entrylist, key = keyfunc)
   #test_file = open(r'd:\ciku_test.txt', 'wb')
   for entry in entrylist:
      yinbiao_len = 0
      text_len    = 0
      cur = f4.tell()
      entry_text = entry['entry']
      #test_file.write(entry_text.encode('utf-16le'))
      #test_file.write('\n'.encode('utf-16le'))
      text_len = len(entry_text) * 2
      if entry.has_key('yinbiao'):
         entry_yinbiao = entry['yinbiao'] 
         yinbiao_len = len(entry_yinbiao) * 2  
      
      next_offset = (text_len + yinbiao_len) + CONST_LEN
      s = pack('HH', prev_offset, next_offset)
      s = s + pack('HH', text_len, yinbiao_len)
      #s = s + pack('H', yinbiao_len | (text_len << 8))
      if len(entry_text) >= 3:
         entry_text_first_3letters = entry_text[0:3]           
         if not d_level3.has_key(entry_text_first_3letters):  # extract first 3 letters into one string, then compare it. 
            d_level3_key.extend([entry_text_first_3letters])
            #if (entry_text_first_3letters == 'top'):
               #print entry_text_first_3letters
               #print "f4 top address=%s" % cur
            d_level3[entry_text_first_3letters] = cur
            temp_index = temp_index + 1
      else:
         if not d_level3.has_key(entry_text):  
            d_level3_key.extend([entry_text])
            d_level3[entry_text] = cur
            temp_index = temp_index + 1

      f4.write(s)
      if yinbiao_len != 0:
         f4.write(entry_text.encode('utf-16le') + entry_yinbiao.encode('utf-16le'))
      else:
         f4.write(entry_text.encode('utf-16le'))
      s = pack('I', dict_offset)
      f4.write(s)
      prev_offset = next_offset
      dict_offset = dict_offset + DICT_ENTRY_CONST_LEN + len(repr_entry(entry)) * 2
      """try:
         print repr_entry(entry)
      except UnicodeEncodeError:
         pass """

   d_level2 = {}
   d_level2_key = [] 
   temp_index1 = 0  
   i = 0
   for i in range(temp_index):
      key = d_level3_key[i]
      value = d_level3.get(key) 
      if (value >= 0):
         s = "%03s" % key
         s = s.encode('utf-16le')
         s = s + pack('I', value)
         if len(key)== 3: 
            entry_text_first_2letters = key[0:2]
            #if (entry_text_first_2letters == 'to'):  
               #print entry_text_first_2letters
               #print " f3,top address=%s" % f3.tell() 
            if not d_level2.has_key(entry_text_first_2letters): 
               d_level2_key.extend([entry_text_first_2letters])
               d_level2[entry_text_first_2letters] = f3.tell() 
               temp_index1 = temp_index1 + 1
         elif len(key)<3:
            if not d_level2.has_key(key):  
               d_level2_key.extend([key])
               d_level2[key] = f3.tell() 
               temp_index1 = temp_index1 + 1
         f3.write(s)

   d_level1 = {}
   d_level1_key = []
   temp_index = 0 
   i = 0
   for i in range(temp_index1): 
      key = d_level2_key[i]
      value = d_level2.get(key)  
      if (value >= 0):
         s = "%02s" % key
         #print "f2 process: %s" % s
         s = s.encode('utf-16le')
         s = s + pack('H', value)
         if len(key)== 2:
            entry_text_first_1letters =  key[0:1]
            #if (entry_text_first_1letters == 't'):   
               #print entry_text_first_1letters
               #print " f2,top address=%s" % f2.tell() 
            if not d_level1.has_key(entry_text_first_1letters):  
               d_level1_key.extend([entry_text_first_1letters])
               d_level1[entry_text_first_1letters] = f2.tell()
               temp_index = temp_index + 1
         elif len(key)<2:
            if not d_level1.has_key(key):  
               d_level1_key.extend([key])
               d_level1[key] = f2.tell()  
               temp_index = temp_index + 1
         f2.write(s)
   i = 0
   for i in range(temp_index): 
      key = d_level1_key[i]
      value = d_level1.get(key) 
      if (value >= 0):
         s = "%01s" % key
         #if (key ==  't'): 
            #print key
            #print " f1,top address=%s" % value 
         s = s.encode('utf-16le')
         s = s + pack('H', value)
         f1.write(s)

if __name__ == '__main__':
   import sys, os
   entrylist = load_ee_dict(sys.argv[1], sys.argv[2])
   entrylist = sorted(entrylist, key = keyfunc)
   dirname = 'eedict'
   try:
      os.mkdir(dirname)
   except OSError, why:
      print "Failed: %s" % str(why)
   bin_dict_file = open(os.path.join('eedict', 'eedict_ciku.bin'), 'wb')
   txt_dict_file = open(r'eetdict_ciku.txt', 'wb')
   generate_ee_dict_file(bin_dict_file, entrylist)
   bin_dict_file.close()
   generate_origin_dict_file(txt_dict_file, entrylist)
   txt_dict_file.close()

   dirname = 'egdict'
   try:
      os.mkdir(dirname)
   except OSError, why:
      print "Failed: %s" % str(why)

   level1_index_file = open(os.path.join('egdict', 'egdict_1st_index.bin'), 'wb')
   level2_index_file = open(os.path.join('egdict', 'egdict_2nd_index.bin'), 'wb')
   level3_index_file = open(os.path.join('egdict', 'egdict_3rd_index.bin'), 'wb')
   level4_index_file = open(os.path.join('egdict', 'egdict_4th_index.bin'), 'wb')
   build_four_level_index(level1_index_file, level2_index_file, level3_index_file, level4_index_file,
         entrylist)
   """
   entrylist = load_ee_dict(r'd:\eedict(a-e)_lib_utf-16.txt', 'utf-16')
   entrylist = sorted(entrylist, key = keyfunc)
   bin_dict_file = open(r'd:\eedict(a-e)_ciku.bin', 'wb')
   txt_dict_file = open(r'd:\eetdict(a-e)_ciku.txt', 'wb')
   generate_ee_dict_file(bin_dict_file, entrylist)
   bin_dict_file.close()
   generate_origin_dict_file(txt_dict_file, entrylist)
   txt_dict_file.close()
   level1_index_file = open(r'd:\eedict(a-e)_1st_index.bin', 'wb')
   level2_index_file = open(r'd:\eedict(a-e)_2nd_index.bin', 'wb')
   level3_index_file = open(r'd:\eedict(a-e)_3rd_index.bin', 'wb')
   level4_index_file = open(r'd:\eedict(a-e)_4th_index.bin', 'wb')
   build_four_level_index(level1_index_file, level2_index_file, level3_index_file, level4_index_file,
         entrylist)
   """
   level1_index_file.close()
   level2_index_file.close()
   level3_index_file.close()
   level4_index_file.close()


