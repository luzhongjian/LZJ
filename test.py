#encoding=utf-8
from hhdict_file import HHDictFile, HHDictEntry

ENUM_DICTIONARY_HANSVISION=0
CHENGYU=1

def GetSetOfHHDict(file, encoding):
   hhdictfile = HHDictFile(file, encoding)
   result = []
   while True:
      chunk = hhdictfile.getChunk()
      if len(chunk) == 0:
         break;
      entry = HHDictEntry(chunk)
      entry = entry.Entry

      result.extend([entry['entry'].rstrip()])

   print "%d entries" % len(result)
   return frozenset(result)

def TestHHDict():
   """
   capable of sorting entries by the pinyin of the entry, useful for process the
   ciku file before development
   """
   inputfile = 'd:\\1\\hhdict-tmp.txt'
   hhdictfile = HHDictFile(inputfile, 'utf-16')

   result = []
   import codecs
   #result_f = codecs.open(r'd:\result-hhdict.txt', 'w', 'utf-16')
   while True:
      chunk = hhdictfile.getChunk()
      if len(chunk) == 0:
         break;
      entry = HHDictEntry(chunk)
      entry = entry.Entry

      result.extend([entry])

   print "Originally %d entries" % len(result)

   #for entry in result:
   #   out_line = []
   #   out_line.extend(u'[@]' + entry['entry'])
   #   out_line.extend(u'[$]' + entry['pinyin'])
   #   for definition in entry['definition']:
   #      out_line.extend(u'[&]' + definition['meaning'])
   #      for example in definition['example']:
   #         (tag, str) = example
   #         if tag == 0:
   #            prefix = u'[*]'
   #         elif tag == 1:
   #            prefix = u'[%]'
   #         out_line.extend(prefix + str)
   #   if entry.has_key('prontag'):
   #      out_line.extend(u'[^]' + entry['prontag'])
   #   result_f.write(u'\r\n'.join(out_line) + u'\r\n')

   #result_f.close()

   from pinyin_sort import pinyin_cmp
   from pinyin_sort import key_func_sort_by_pinyin
   single_character_list = filter(lambda x: (len(x['entry']) == 1), result)
   print "Single-character entries = %d" % len(single_character_list)
   sorted_single_character_list = sorted(single_character_list, cmp = pinyin_cmp, key = key_func_sort_by_pinyin)
   paraphrases_groups = []
   for i in xrange(len(sorted_single_character_list)):
      paraphrases = filter(lambda x: len(x['entry']) > 1
            and x['entry'][:1] == sorted_single_character_list[i]['entry']
            and x['pinyin'][:len(sorted_single_character_list[i]['pinyin'])].lower() == sorted_single_character_list[i]['pinyin'].lower(),
            result)
      sorted_paraphrases = sorted(paraphrases, cmp = pinyin_cmp, key = key_func_sort_by_pinyin);
      paraphrases_groups.append(sorted_paraphrases)

   from random import random
   sortedfilename = 'd:\\1\\sorted_result-hhdict' + str(random())[5:8] + '.txt'
   result_f = codecs.open(sortedfilename, 'w', 'utf-16')
  
   for i in xrange(len(sorted_single_character_list)):
      entry = sorted_single_character_list[i]
      result_f.write(repr_entry(entry))
      for paraphrase in paraphrases_groups[i]:
         result_f.write(repr_entry(paraphrase))
   result_f.close()

   del paraphrases_groups
   print "sorted list without orphan phrases generated: " + sortedfilename
   from gen_cc_bin_file import load_hh_dict
   full_list = load_hh_dict(inputfile, 'utf-16')
   sorted_result = load_hh_dict(sortedfilename, 'utf-16')
   delta_set = frozenset([d['entry'] for d in full_list]) - frozenset([d['entry'] for d in sorted_result])
   print "delta set len %d" % len(delta_set)
   delta = []
   for i in full_list:
      for j in delta_set:
         if i['entry'] == j:
            delta.append(i)
   sorted_delta = sorted(delta, cmp = pinyin_cmp, key = key_func_sort_by_pinyin)
   del delta
   i = 0
   j = 0
   new_result = []
   max_j = len(sorted_result)
   max_i = len(sorted_delta)
   found = False
   from pinyin_sort import transform_pinyin
   while True:
      if found:
         pass
      print "sorted_delta length = %d, sorted_result length = %d" % (len(sorted_delta), len(sorted_result))
      if (max_j != 0):
         if (pinyin_cmp(transform_pinyin(sorted_delta[i]['pinyin']), transform_pinyin(sorted_result[j]['pinyin'])) >= 0):
            #print ">=0"
            #try:
            #   print "delta is bigger " + sorted_delta[i]['entry'] + sorted_delta[i]['pinyin'] +\
            #      sorted_result[j]['entry'] + sorted_result[j]['pinyin']
            #except UnicodeEncodeError:
            #   pass
            new_result.append(sorted_result[j])
            j = j + 1
            if j == max_j:
               break
         if (pinyin_cmp(transform_pinyin(sorted_delta[i]['pinyin']),
               transform_pinyin(sorted_result[j]['pinyin'])) < 0):
            #print "<0"
            new_result.append(sorted_delta[i])
            #print "append " + sorted_delta[i]['entry'] + sorted_delta[i]['pinyin']
            new_result.append(sorted_result[j])
            #print "append " + sorted_result[j]['entry'] + sorted_result[j]['pinyin']
            found = True
            j = j + 1
            i = i + 1
            if j == max_j or i == max_i:
               break
      else:
         new_result.append(sorted_delta[i])
         i = i + 1
         if i == max_i:
            break

   added_file_name = 'd:\\1\\added_file' + str(random())[5:8] + '.txt'
   af = codecs.open(added_file_name, 'w', 'utf-16')
   for i in new_result:
      af.write(repr_entry(i))
   af.close()
   print "generated %s" % added_file_name

def repr_entry(entry, indent = 0):
   out_line = []
   english_idiom_written = False
   story_written = False
   if entry.has_key('entry'):
      out_line.extend([indent * 3 * u' ' + u'[@]' + entry['entry']])
   if entry.has_key('pinyin'):
      out_line.extend([indent * 3 * u' ' + u'[$]' + entry['pinyin']])
   for definition in entry['definition']:
      out_line.extend([indent * 3 * u' ' + u'[&]' + definition['meaning']])
      for example in definition['example']:
         (tag, str) = example
         if tag == 0:
            prefix = u'[*]'
         elif tag == 1:
            prefix = u'[%]'
         out_line.extend([indent * 3 * u' ' + prefix + str])
         if (tag == 0) and (not english_idiom_written) and (entry.has_key('english_idiom')):
            out_line.append(indent * 3 * u' ' + u'[\uffe1]' + entry['english_idiom'])
            english_idiom_written = True
         if (tag == 0) and (not story_written) and (entry.has_key('story')):
            out_line.append(indent * 3 * u' ' + u'[#]' + '\n'.join(entry['story']))
   if entry.has_key('prontag'):
      out_line.extend([indent * 3 * u' ' + u'[^]' + entry['prontag']])
   return u'\r\n'.join(out_line) + 2 * u'\r\n'

#mahu add merged_entry_list[entry][ENUM_DICTIONARY_HANSVISION]
def repr_new_entry(entry, indent = 0):
   out_line = []
   english_idiom_written = False
   story_written = False
   if entry[ENUM_DICTIONARY_HANSVISION].has_key('entry'):
      out_line.extend([indent * 3 * u' ' + u'[@]' + entry[ENUM_DICTIONARY_HANSVISION]['entry']])
   if entry[ENUM_DICTIONARY_HANSVISION].has_key('pinyin'):
      out_line.extend([indent * 3 * u' ' + u'[$]' + entry[ENUM_DICTIONARY_HANSVISION]['pinyin']])
   for definition in entry[ENUM_DICTIONARY_HANSVISION]['definition']:
      out_line.extend([indent * 3 * u' ' + u'[&]' + definition['meaning']])
      for example in definition['example']:
         (tag, str) = example
         if tag == 0:
            prefix = u'[*]'
         elif tag == 1:
            prefix = u'[%]'
         out_line.extend([indent * 3 * u' ' + prefix + str])
         if (tag == 0) and (not english_idiom_written) and (entry[ENUM_DICTIONARY_HANSVISION].has_key('english_idiom')):
            out_line.append(indent * 3 * u' ' + u'[\uffe1]' + entry[ENUM_DICTIONARY_HANSVISION]['english_idiom'])
            english_idiom_written = True
         if (tag == 0) and (not story_written) and (entry[ENUM_DICTIONARY_HANSVISION].has_key('story')):
            out_line.append(indent * 3 * u' ' + u'[#]' + '\n'.join(entry[ENUM_DICTIONARY_HANSVISION]['story']))
   if entry[ENUM_DICTIONARY_HANSVISION].has_key('prontag'):
      out_line.extend([indent * 3 * u' ' + u'[^]' + entry[ENUM_DICTIONARY_HANSVISION]['prontag']])
   return u'\r\n'.join(out_line) + 2 * u'\r\n'

def repr_chengyu_entry(entry,indent = 0):
   out_line = []
   english_idiom_written = False
   story_written = False
   if entry[CHENGYU].has_key('entry'):
      out_line.extend([indent * 3 * u' ' + u'[@]' + entry[CHENGYU]['entry']])
   if entry[CHENGYU].has_key('pinyin'):
      out_line.extend([indent * 3 * u' ' + u'[$]' + entry[CHENGYU]['pinyin']])
   for definition in entry[CHENGYU]['definition']:
      out_line.extend([indent * 3 * u' ' + u'[&]' + definition['meaning']])
      for example in definition['example']:
         (tag, str) = example
         if tag == 0:
            prefix = u'[*]'
         elif tag == 1:
            prefix = u'[%]'
         out_line.extend([indent * 3 * u' ' + prefix + str])
         if (tag == 0) and (not english_idiom_written) and (entry[CHENGYU].has_key('english_idiom')):
            out_line.append(indent * 3 * u' ' + u'[\uffe1]' + entry[CHENGYU]['english_idiom'])
            english_idiom_written = True
         if (tag == 0) and (not story_written) and (entry[CHENGYU].has_key('story')):
            out_line.append(indent * 3 * u' ' + u'[#]' + '\n'.join(entry[CHENGYU]['story']))
   if entry[CHENGYU].has_key('prontag'):
      out_line.extend([indent * 3 * u' ' + u'[^]' + entry[CHENGYU]['prontag']])
   return u'\r\n'.join(out_line) + 2 * u'\r\n'

def TestWriteBackHHDict():
   inputfile = 'd:\\1\\hhdict-tmp.txt'
   hhdictfile = HHDictFile(inputfile, 'utf-16')

   result = []
   import codecs
   result_f = codecs.open(r'd:\1\writeback-hhdict.txt', 'w', 'utf-16')
   while True:
      chunk = hhdictfile.getChunk()
      if len(chunk) == 0:
         break;
      entry = HHDictEntry(chunk)
      entry = entry.Entry

      result.extend([entry])

   print "Originally %d entries" % len(result)

   for entry in result:
      #out_line = []
      #out_line.append(u'[@]' + entry['entry'])
      #out_line.append(u'[$]' + entry['pinyin'])
      #for definition in entry['definition']:
      #   out_line.append(u'[&]' + definition['meaning'])
      #   for example in definition['example']:
      #      (tag, str) = example
      #      if tag == 0:
      #         prefix = u'[*]'
      #      elif tag == 1:
      #         prefix = u'[%]'
      #      out_line.append(prefix + str)
      #if entry.has_key('prontag'):
      #   out_line.append(u'[^]' + entry['prontag'])
      #result_f.write(u'\r\n'.join(out_line) + u'\r\n' * 2)
      result_f.write(repr_entry(entry))

   result_f.close()

if __name__ == '__main__':
   TestWriteBackHHDict()

