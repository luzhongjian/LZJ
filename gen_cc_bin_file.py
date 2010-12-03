# coding = utf-8
# encoding=utf-8
from hhdict_file import HHDictFile, HHDictEntry
from merge_third_index_for_cc import dict_merge_for_indexing
from test import repr_entry ,repr_new_entry,repr_chengyu_entry
import codecs
from checkchengyudict import checkchengyudict

ENUM_DICTIONARY_HANSVISION = 0
ENUM_DICTIONARY_CHENGYU = 1

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

DICT_ENTRY_CONST_LEN = 6
from struct import pack, unpack
def generate_hh_dict_file(f, entrylist, mode):
   global DICT_ENTRY_CONST_LEN
   
   if f.name.endswith('ccdict_ciku.bin'):
      offset_record_files = codecs.open('d:\\1\\gen_cc_offset.txt', 'w', 'utf-16')
   elif f.name.endswith('chengyu_ciku.bin'):
      offset_record_files = codecs.open('d:\\1\\gen_chengyu_offset.txt', 'w', 'utf-16')

   s = pack('H', len(entrylist))
   f.write(s)
   prev_offset = 0
   next_offset = 0
   cur = f.tell()
   for entry in entrylist:
      if mode == 1:
         entry_text = repr_entry_for_dict_file(entry)
      elif mode == 2:
         entry_text = repr_entry_for_ce_dict_file(entry)
      #print entry_text
      entry_name = entry['entry']
      name_len = len(entry_name) * 2
 
      pinyin_len = 0
      if entry.has_key('pinyin'):
         pinyin_len = len(entry['pinyin']) * 2  
      next_offset = DICT_ENTRY_CONST_LEN + len(entry_text) * 2
      s = pack('HH', prev_offset, next_offset)
      s = s + pack('H', pinyin_len | (name_len << 8))
      f.write(s)
      f.write(entry_text.encode('utf-16le'))
      offset_record_files.write("%s @ 0x%x\n" % (entry_name, cur))
      cur = cur + next_offset
      prev_offset = next_offset

   f.close()

def build_three_level_index(f1, f2, f3, entrylist, mode):
   global DICT_ENTRY_CONST_LEN
   f_dbg_record_cc_dict_offset = codecs.open('d:\\1\\idx_cc_offset.txt', 'w', 'utf-16')
   f_dbg_thirdindex_offset = codecs.open('d:\\1\\idx_third_offset.txt', 'w', 'utf-16')

   cc_bin_dict_file = open(r'd:\1\ccdict_ciku.bin', 'wb')
   cc_bin_dict_file.seek(2)
   chengyu_bin_dict_file = open(r'd:\1\chengyu_ciku.bin', 'wb')
   chengyu_bin_dict_file.seek(2)
   CONST_LEN = 14
   SYNTHESIZED_DICT_CONST_LEN = 18
   DUOYINZI_FLAG_OFFSET = 4
   prev_offset = 0
   next_offset = 0
   dict_offset = 2
   d_prev = {ENUM_DICTIONARY_HANSVISION: 0, ENUM_DICTIONARY_CHENGYU: 0}
   d_next = {ENUM_DICTIONARY_CHENGYU: 0, ENUM_DICTIONARY_CHENGYU: 0}
   d_level2 = {}
   initial_character = {}
   s = pack('H', len(entrylist))
   f3.write(s)
   count = {ENUM_DICTIONARY_HANSVISION: 0, ENUM_DICTIONARY_CHENGYU: 0}
   for entry in entrylist:
      cur = f3.tell()
      if (entry.has_key('entry')):
         entry_pinyin = entry['pinyin']
         entry_text = entry['entry']
      else:
         entry_pinyin = entry[entry.keys()[0]]['pinyin']
         entry_text = entry[entry.keys()[0]]['entry']
      entry_initial_char = entry_text[0]
      #entry_pinyin = entry['pinyin']
      if not initial_character.has_key(entry_initial_char):
         initial_character[entry_initial_char] = (entry_pinyin.split(' ')[0].lower(), cur)
      else: # duoyinzi found
         initial_pinyin, tmp_offset = initial_character[entry_initial_char]
         if (initial_pinyin != entry_pinyin.split(' ')[0].lower()):
            f3.seek(tmp_offset + DUOYINZI_FLAG_OFFSET)
            f3.write(pack('I', cur - tmp_offset))
            f3.seek(cur)
            initial_character[entry_initial_char] = (entry_pinyin.split(' ')[0].lower(), cur)
            #print "duoyinzi %s %d" % (entry['entry'].encode('gb18030'), cur - tmp_offset)
      #entry_text = entry['entry']
      #if entry.has_key('pinyin'):
      #   entry_pinyin = entry['pinyin']
      #else:
      #   entry_pinyin = ''
      text_len = len(entry_text) * 2
      pinyin_len = len(entry_pinyin) * 2
      if mode == 2:
         next_offset = (text_len + pinyin_len) + CONST_LEN
      if mode == 1:
         next_offset = (text_len + pinyin_len) + SYNTHESIZED_DICT_CONST_LEN
      s = pack('HH', prev_offset, next_offset)
      s = s + pack('I', 0) #duoyinzi
      s = s + pack('H', pinyin_len | (text_len << 8))
      if not d_level2.has_key(ord(entry_text[0])):
         d_level2[ord(entry_text[0])] = cur
      f3.write(s)
      f3.write(entry_text.encode('utf-16le') + entry_pinyin.encode('utf-16le'))
      f_dbg_thirdindex_offset.write('%s @ 0x%08X\n' % (entry_text, cur)) 
      if (mode == 2):
         s = pack('I', dict_offset)
         dict_offset += DICT_ENTRY_CONST_LEN + len(repr_entry_for_ce_dict_file(entry)) * 2
      elif (mode == 1):
         offset = {ENUM_DICTIONARY_HANSVISION: 0xFFFFFFFF, ENUM_DICTIONARY_CHENGYU: 0xFFFFFFFF}
         de = {ENUM_DICTIONARY_HANSVISION: '', ENUM_DICTIONARY_CHENGYU: ''}
         of = {ENUM_DICTIONARY_HANSVISION: cc_bin_dict_file,\
               ENUM_DICTIONARY_CHENGYU: chengyu_bin_dict_file}
         for k in entry.keys():
            count[k] += 1
            de[k] = repr_entry_for_dict_file(entry[k])
            offset[k] = of[k].tell()
            d_next[k] = DICT_ENTRY_CONST_LEN + 4 + len(de[k]) * 2 #N.B. '+4' is because below 'pack('I', cur)'
            t = pack('3H', d_prev[k], d_next[k], (len(entry_pinyin) << 1)  | (len(entry_text) << 1) << 8)
            of[k].write(t)
            of[k].write(de[k].encode('utf-16le'))
            of[k].write(pack('I', cur))
            f_dbg_record_cc_dict_offset.write("%s @ 0x%08X\n" % (entry_text, cur))
            d_prev[k] = d_next[k]

         s = pack('2I', offset[ENUM_DICTIONARY_HANSVISION], offset[ENUM_DICTIONARY_CHENGYU])
 
      f3.write(s)
      prev_offset = next_offset
   d_level1 = {}
   cur = 0
   for i in xrange(0x10000):
      key = i
      value = d_level2.get(i)
   #for item in d_level2.items():
      if (value):
         s = pack('H', key)
         s = s + pack('I', value)
         #if (key == 0x91c7):
            #print value
         high_byte = (key & 0xFF00) >> 8
         if not d_level1.has_key(high_byte):
            d_level1[high_byte] = f2.tell()
            #print "set level1 high byte 0x%x" % high_byte
         f2.write(s)
   for i in xrange(0x100):
   #for item in d_level1.items():
      key = i
      value = d_level1.get(i)
      #print d_level1[0x4e]
      if not (value is None):
         s = pack('HH', key, value)
         f1.write(s)
   f_dbg_record_cc_dict_offset.close()
   f_dbg_thirdindex_offset.close()
   cc_bin_dict_file.seek(0)
   cc_bin_dict_file.write(pack('H', count[ENUM_DICTIONARY_HANSVISION]))
   cc_bin_dict_file.close()
   chengyu_bin_dict_file.seek(0)
   chengyu_bin_dict_file.write(pack('H', count[ENUM_DICTIONARY_CHENGYU]))
   chengyu_bin_dict_file.close()

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
   print "%d entries" % len(result)
   return result

SEQ_NUM_IN_CHINESE = [u'\u2488', u'\u2489', u'\u248a', u'\u248b', u'\u248c', u'\u248d',
      u'\u248e', u'\u248f', u'\u2490', u'\u2491', u'\u2492', u'\u2493', u'\u2494', u'\u2495',
      u'\u2496', u'\u2497', u'\u2498', u'\u2499', u'\u249a', u'\u249b', #TWENTY FULL STOP
      #u'\u3251', u'\u3252', u'\u3253', u'\u3254', u'\u3255', u'\u3256']
      u'21.', u'22.', u'23.', u'24.', u'25.', u'26.', u'27.', u'28.', u'29.',
      u'30.', u'31.', u'32.']

def repr_entry_for_ce_dict_file(entry):
   result_str = ''
   out_line = []
   result_str += entry['entry']
   if entry.has_key('pinyin'):
      pinyin = entry['pinyin']
   else:
      pinyin = ''
   result_str += pinyin
   seq_num = 0
   result_str += u' '
   for definition in entry['definition']:
      if seq_num >= len(SEQ_NUM_IN_CHINESE):
         print "Exeed: " + entry['entry']
         raise Exception
      if (len(entry['definition']) > 1):
         seq_prefix = SEQ_NUM_IN_CHINESE[seq_num]
      else:
         seq_prefix = ''
      #out_line.append(seq_prefix + definition['meaning'])
      out_line.append(definition['meaning'])
      seq_num += 1
      for example in definition['example']:
         (tag, str) = example
         if tag == 0:
            prefix = u'\u25b3'
         elif tag == 1:
            prefix = u'\u25b2'
         out_line.append(prefix + str)
   #if entry.has_key('prontag'):
   #   out_line.extend([indent * 3 * u' ' + u'[^]' + entry['prontag']])
   return result_str + u'\u25c7'.join(out_line)

def repr_entry_for_dict_file(entry):
   result_str = ''
   out_line = []
   result_str += entry['entry']
   if entry.has_key('pinyin'):
      pinyin = entry['pinyin']
   else:
      pinyin = ''
   result_str += pinyin
   seq_num = 0
   for definition in entry['definition']:
      if seq_num >= len(SEQ_NUM_IN_CHINESE):
         print "Exeed: " + entry['entry']
         raise Exception
      if (len(entry['definition']) > 1):
         seq_prefix = SEQ_NUM_IN_CHINESE[seq_num]
      else:
         seq_prefix = ''
      out_line.append(seq_prefix + definition['meaning'])
      seq_num += 1
      for example in definition['example']:
         (tag, str) = example
         if tag == 0:
            prefix = u'\u25b3'
         elif tag == 1:
            prefix = u'\u25b2'
         out_line.append(prefix + str)
   #if entry.has_key('prontag'):
   #   out_line.extend([indent * 3 * u' ' + u'[^]' + entry['prontag']])
   english_idiom = [u'\u25a0']
   if entry.has_key('english_idiom'):
      english_idiom.append(entry['english_idiom'])
      out_line.append(''.join(english_idiom))

   chengyu_diangu = [u'\u25c7']
   if entry.has_key('story'):
      chengyu_diangu.append(''.join(entry['story']))
      out_line.append(''.join(chengyu_diangu))

   return result_str + u'\n'.join(out_line)

def tag_each_entry_dictionary_type(entrylist, dictionary_type):
   for i in xrange(len(entrylist)):
      entrylist[i]['dictionary_type'] = [dictionary_type]

if __name__ == '__main__':
   entrylist = load_hh_dict(r'd:\1\hhdict-tmp.txt', 'utf-16')
   tag_each_entry_dictionary_type(entrylist, ENUM_DICTIONARY_HANSVISION)

   bin_dict_file = open(r'd:\1\ccdict_ciku.bin', 'wb')
   #generate_hh_dict_file(bin_dict_file, entrylist, 1) # 1 for cc dictionary, 2 for ce dictionary
   bin_dict_file.close()

   cyentrylist = load_hh_dict(r'd:\1\chengyu.txt', 'utf-16')
   tag_each_entry_dictionary_type(cyentrylist, ENUM_DICTIONARY_CHENGYU)

   chengyu_bin_dict_file = open(r'd:\1\chengyu_ciku.bin', 'wb')
   #generate_hh_dict_file(chengyu_bin_dict_file, cyentrylist, 1) # 1 for cc dictionary, 2 for ce dictionary
   chengyu_bin_dict_file.close()

   level1_index_file = open(r'd:\1\cgdict_1st_index.bin', 'wb')
   level2_index_file = open(r'd:\1\cgdict_2nd_index.bin', 'wb')
   level3_index_file = open(r'd:\1\cgdict_3rd_index.bin', 'wb')

   merged_entry_list = dict_merge_for_indexing(entrylist, cyentrylist)
#### check the chengyu dict 
  # checkchengyulist=checkchengyudict(cyentrylist,entrylist)
  # check_result = codecs.open(r'd:\1\checkresult.txt', 'w', 'utf-16')
  # checklen=len(checkchengyulist)
  # for checknum in xrange(checklen):
  #    check_result.write(checkchengyulist[checknum]['entry'])
  # check_result.close()
###  end check
   #### Add a dump for test purpose here ####
   merged_result_f = codecs.open(r'd:\1\merged_list.txt', 'w', 'utf-16')
   merged_resultchengyu_f = codecs.open(r'd:\1\mergedchengyu_list.txt', 'w', 'utf-16')
   chengyunum=0
   chengyulen=len(cyentrylist)
   mergelistlen=len(merged_entry_list)
   for entry in xrange(mergelistlen):
      if ENUM_DICTIONARY_HANSVISION in merged_entry_list[entry].keys():
         merged_result_f.write(repr_new_entry(merged_entry_list[entry]))
         #merged_result_f.write('[@]' + merged_entry_list[entry][ENUM_DICTIONARY_HANSVISION]['entry'])
      if ENUM_DICTIONARY_CHENGYU in merged_entry_list[entry].keys():
         chengyunum=chengyunum+1     
         merged_resultchengyu_f.write(repr_chengyu_entry(merged_entry_list[entry]))

   merged_result_f.close()
   merged_resultchengyu_f.close()
   print "chengyunumber=%d"%chengyunum

   #### End of the procedure for data dump ####
   build_three_level_index(level1_index_file, level2_index_file, level3_index_file,
         merged_entry_list, 1) # 1 for cc dictionary, 2 for ce dictionary
   level1_index_file.close()
   level2_index_file.close()
   level3_index_file.close()
   
