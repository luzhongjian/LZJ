from gen_cc_bin_file import load_hh_dict, generate_hh_dict_file, build_three_level_index

def MergeMeanings(entrylist):
   """ Merge Meanings from duoyinzi """
   d = {}
   result = []
   for idx in xrange(len(entrylist)):
      i = entrylist[idx]
      if d.has_key(i['entry']):
         result[d[i['entry']]]['definition'] += i['definition']
      else:
         d[i['entry']] = len(result)
         result.append(i)
   return result

if __name__ == '__main__':
   import sys, os
   entrylist = load_hh_dict(sys.argv[1], sys.argv[2])
   result = MergeMeanings(entrylist)
   import codecs
   from test import repr_entry
   result_f = codecs.open(r'writeback-hhdict.txt', 'w', 'utf-16')
   for entry in result:
      result_f.write(repr_entry(entry))
   result_f.close()

   dirname = 'reduced_cedict'
   try:
      os.mkdir(dirname)
   except OSError, why:
      print "Failed: %s" % str(why)

   bin_dict_file = open(os.path.join('reduced_cedict', 'cedict_reduced_ciku.bin'), 'wb')
   generate_hh_dict_file(bin_dict_file, result, 2) # 1 for cc dictionary, 2 for ce dictionary
   bin_dict_file.close()
   level1_index_file = open(os.path.join('reduced_cedict', 'cedict_reduced_1st_index.bin'), 'wb')
   level2_index_file = open(os.path.join('reduced_cedict', 'cedict_reduced_2nd_index.bin'), 'wb')
   level3_index_file = open(os.path.join('reduced_cedict', 'cedict_reduced_3rd_index.bin'), 'wb')
   build_three_level_index(level1_index_file, level2_index_file, level3_index_file,
         result, 2) # 1 for cc dictionary, 2 for ce dictionary
   level1_index_file.close()
   level2_index_file.close()
   level3_index_file.close()

