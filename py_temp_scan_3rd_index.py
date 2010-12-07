"""Scan the HH dictionary and display duplicate entries with the same
pinyin"""
import codecs

f = codecs.open(r'e:\temp\py_temp_scan_3rd_index.py', 'r', 'utf-16')


from gen_cc_bin_file import load_hh_dict
el = load_hh_dict(r'd:\1\hhdict-tmp.txt', 'utf-16')
d = {}
for e in el:
   if len(e['pinyin'].split(' ')) > 3:
      if (d.has_key(e['pinyin'])):
         d[e['pinyin']].append(e['entry'])
         print e['entry'].encode('gbk')
      else:
         d[e['pinyin']] = [e['entry']]
#for (p, e) in d.items():
#   (p, e) = (p, e)
#   print p.encode('gbk'), [i.encode('gbk') for i in e]
   
for x in [(p, e) for (p, e) in d.items() if len(e) > 1]:
   (p, e) = x
   #print p.encode('gbk'), ': ', [i.encode('gbk') for i in e]
   print p.encode('gbk'), ': ', 
   for i in e:
      print i.encode('gbk'),
   print ' '
