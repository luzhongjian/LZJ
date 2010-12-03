import re
import codecs
RE_START_ENTRY = re.compile(u'\[@\]') #citiao
if __name__ == '__main__':
   Found = False
   from gen_cc_bin_file import load_hh_dict, repr_entry_for_ce_dict_file
   from gen_ce_bin_file import MergeMeanings
   ce_entry_list = load_hh_dict(r'd:\1\hhdict-tmp.txt', 'gbk') # put ce dictionary content file here
   ce_entry_list = MergeMeanings(ce_entry_list)
   d = {}
   for idx in xrange(len(ce_entry_list)):
      if not d.has_key(ce_entry_list[idx]['entry']):
         d[ce_entry_list[idx]['entry']] = idx
      else:
         raise IndexError

   print ce_entry_list[0]
   fh = codecs.open(r'F:\MerlionColor-Workspace\MerlionColor_git_repo_lzj\bin\creaf\MerlionColor\ccentry.txt', 'r', 'gbk')
   out_fh = codecs.open(r'F:\MerlionColor-Workspace\MerlionColor_git_repo_lzj\bin\creaf\MerlionColor\ccentry_w_ce_def.txt', 'w', 'utf-8')
   while (True):
      line = fh.readline()
      if len(line) == 0:
         break
      out_text = []
      line = line.strip()
      m = re.search(RE_START_ENTRY, line)
      if m:
         entry = m.string[m.end():] # entry is now the entry word from CC list
         if entry == u'\u554a':
            Found = True
            print "Found"
         ce_idx = d.get(entry)
         if Found:
            print ce_idx
            Found = False
         if ce_idx is None:
            out_text.append(line)
            out_text.append(u'(missing)')
         else:
            #out_text.append(line)
            #out_text.append(repr_entry_for_ce_dict_file(ce_entry_list[ce_idx]))
            pass
         out_fh.write('\r\n'.join(out_text))
         out_fh.write('\r\n' * 2)

fh.close()
out_fh.close()

