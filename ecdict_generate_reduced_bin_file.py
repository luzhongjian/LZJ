"""Added by prm for generating reduced English-Chinese dictionary extracted index file"""
#encoding = utf-8
SEQ_NUM_IN_CHINESE = [u'\u2488', u'\u2489', u'\u248a', u'\u248b', u'\u248c', u'\u248d',
      u'\u248e', u'\u248f', u'\u2490', u'\u2491', u'\u2492', u'\u2493', u'\u2494', u'\u2495',
      u'\u2496', u'\u2497', u'\u2498', u'\u2499', u'\u249a', u'\u249b', #TWENTY FULL STOP
      #u'\u3251', u'\u3252', u'\u3253', u'\u3254', u'\u3255', u'\u3256']
      u'21.', u'22.', u'23.', u'24.', u'25.', u'26.',u'27.', u'28.', u'29.', u'30.', u'31.', u'32.',
      u'33.', u'34.', u'35.', u'36.', u'37.', u'38.',u'39.', u'40.', u'41.', u'42.', u'43.', u'44.',u'45.', u'46.', u'47.', u'48.', u'49.', u'50.',
      u'51.', u'52.', u'53.', u'54.', u'55.', u'56.']
def restore_origin_entry(entry):
   out_line = []
   out_line.extend([entry['entry']])
   if entry.has_key('searchRelatedVocabulary'):
      out_line.extend([u'[C]' + u'missing'])  # entry['searchRelatedVocabulary']])
   seq_num = 0
   for meaning in entry['meaning']:  
      (tag, str) = meaning 
      if seq_num >= 56:
         print "Exeed: " + entry['entry']
         #raise Exception
      if (len(entry['meaning']) > 1):
         if (seq_num <=55):
            seq_prefix = SEQ_NUM_IN_CHINESE[seq_num]
         else:
            seq_prefix = SEQ_NUM_IN_CHINESE[55]
      else:
         seq_prefix = ''
      if tag == 0:
         prefix = seq_prefix 
         seq_num += 1
      elif tag ==1:
         prefix = u''
      out_line.extend([prefix + str])  
   return u''.join(out_line) # + 2 * u'\r\n'

def repr_entry(entry, indent = 0):
   out_line = []
   out_line.extend([entry['entry']])   
   if entry.has_key('searchRelatedVocabulary'):
      out_line.extend([u'[C]' + u'missing'])  # entry['searchRelatedVocabulary']])
   seq_num = 0
   out_line.append(u' ')
   for meaning in entry['meaning']:  
      (tag, str) = meaning 
      if seq_num >= 56:
         print "Exeed: " + entry['entry']
         #raise Exception
      if (len(entry['meaning']) > 1):
         if (seq_num <=55):
            seq_prefix = SEQ_NUM_IN_CHINESE[seq_num]
         else:
            seq_prefix = SEQ_NUM_IN_CHINESE[55]
      else:
         seq_prefix = ''
      if tag == 0:
         prefix =  seq_prefix
         seq_num += 1
      elif tag ==1:
         prefix = u''
      out_line.extend([indent * 3 * u' ' + prefix + str])  
   return u''.join(out_line) #+ 2 * u'\r\n'


from reduced_ecdict.reduced_ecdict_file import ReducedECDictFile, ReducedECDictEntry
#from util.stringGenerator import stringGenerator
def load_ec_dict(file, encoding):
   ecdictfile = ReducedECDictFile(file, encoding)
   result = []
   while True:
      chunk = ecdictfile.getChunk()
      if len(chunk) == 0:
         break;
      #print chunk
      entry = ReducedECDictEntry(chunk)
      entry = entry.Entry
      result.append(entry)
   print "%d total entries size" % len(result)    
   """Added by zhong jian for sort entrys"""
   from pinyin_sort import pinyin_cmp
   from operator import itemgetter
   #sorted_result = sorted(result, cmp = pinyin_cmp, key = itemgetter('entry'))
   return result

DICT_ENTRY_CONST_LEN = 8
from struct import pack, unpack
#from test import repr_entry
def generate_origin_dict_file(f, entrylist):
   for entry in entrylist:
      #print entry
      entry_text = restore_origin_entry(entry)
      f.write(entry_text)

def generate_ec_dict_file(f, entrylist):
   global DICT_ENTRY_CONST_LEN
   s = pack('H', len(entrylist))
   f.write(s)
   prev_offset = 0
   next_offset = 0
   cur = f.tell()
   name_len    = 0
   yinbiao_len = 0
   for entry in entrylist: 
      entry_text = repr_entry(entry)
      entry_name = entry['entry']
      name_len = len(entry_name) * 2

      next_offset = DICT_ENTRY_CONST_LEN + len(entry_text) * 2
      s = pack('HH', prev_offset, next_offset)
      s = s + pack('HH', name_len, yinbiao_len)
      f.write(s)
      f.write(entry_text.encode('utf-16le'))
      #print entry_text
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
   
   d_3letters = {}
   d_2letters = {}
   d_1letters = {}

   d_level3 = {}
   d_level3_key = []
   temp_index = 0
   s = pack('H', len(entrylist))
   f4.write(s)
   for entry in entrylist:
      yinbiao_len = 0
      cur = f4.tell()
      entry_name = entry['entry']
      text_len = len(entry_name) * 2
      """if entry.has_key('meaning'):
         for meaning in entry['meaning']:
            (tag, str) = meaning
            if tag == 0:  
               prefix = u'[%]'
            elif tag == 1:
               prefix = u''
            entry_meaning =  prefix + str #content need to be append 
            meaning_len = meaning_len + len(entry_meaning) * 2"""  
      
      #next_offset = (text_len + meaning_len) + CONST_LEN
      next_offset = text_len + CONST_LEN
      s = pack('HH', prev_offset, next_offset)
      s = s + pack('HH', text_len, yinbiao_len)
      if len(entry_name) >= 3:
         entry_text_first_3letters = entry_name[0:3]           
         if not d_level3.has_key(entry_text_first_3letters):  # extract first 3 letters into one string, then compare it. 
            d_level3_key.extend([entry_text_first_3letters])
            #print "f4 %s" % entry_text_first_3letters
            d_level3[entry_text_first_3letters] = cur
            temp_index = temp_index + 1
      else:
         if not d_level3.has_key(entry_name):  
            d_level3_key.extend([entry_name])
            d_level3[entry_name] = cur
            temp_index = temp_index + 1

      f4.write(s)
      #print entry_text
      f4.write(entry_name.encode('utf-16le'))
      s = pack('I', dict_offset)
      f4.write(s)
      prev_offset = next_offset
      dict_offset = dict_offset + DICT_ENTRY_CONST_LEN + len(repr_entry(entry)) * 2

   d_level2 = {}
   d_level2_key = [] 
   temp_index1 = 0 
   #while (True):
   i = 0
   for i in range(temp_index):
      key = d_level3_key[i]
      value = d_level3.get(key)
     # if not value:
     #    break
  #for item in d_level3.items():
      if (value >= 0):
         s = "%03s" % key
         s = s.encode('utf-16le')
         s = s + pack('I', value)
         if len(key)== 3:
            entry_text_first_2letters = key[0:2]
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
     # if not value:
      #   break
   #for item in d_level2.items():
      if (value >= 0):
         s = "%02s" % key
         #print "f2 process: %s" % s
         s = s.encode('utf-16le')
         s = s + pack('H', value)
         if len(key)== 2:
            entry_text_first_1letters =  key[0:1]
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
   #for item in d_level1.items():  
     # if not value:
      #   break
      if (value >= 0):
         s = "%01s" % key
         print "f1 process key: %s" % s
         s = s.encode('utf-16le')
         s = s + pack('H', value)
         f1.write(s)

if __name__ == '__main__':
   #entrylist = load_ec_dict(r'd:\1\hhdict-tmp.txt', 'gb18030')
   entrylist = load_ec_dict(r'd:\MerlionColor\reduced_ecdict\ecdict_lib_utf-16.txt', 'utf-16')
   entrylist = sorted(entrylist, key = keyfunc)
   bin_dict_file = open(r'd:\MerlionColor\reduced_ecdict\ecdict_reduced_ciku.bin', 'wb')
   import codecs
   txt_dict_file = codecs.open(r'd:\MerlionColor\reduced_ecdict\ectdict_reduced_ciku.txt', 'wb', 'utf-16')
   generate_ec_dict_file(bin_dict_file, entrylist)
   bin_dict_file.close()
   generate_origin_dict_file(txt_dict_file, entrylist)
   txt_dict_file.close()
   level1_index_file = open(r'd:\MerlionColor\reduced_ecdict\ecdict_reduced_1st_index.bin', 'wb')
   level2_index_file = open(r'd:\MerlionColor\reduced_ecdict\ecdict_reduced_2nd_index.bin', 'wb')
   level3_index_file = open(r'd:\MerlionColor\reduced_ecdict\ecdict_reduced_3rd_index.bin', 'wb')
   level4_index_file = open(r'd:\MerlionColor\reduced_ecdict\ecdict_reduced_4th_index.bin', 'wb')
   build_four_level_index(level1_index_file, level2_index_file, level3_index_file, level4_index_file,
         entrylist)
   level1_index_file.close()
   level2_index_file.close()
   level3_index_file.close()
   level4_index_file.close()


