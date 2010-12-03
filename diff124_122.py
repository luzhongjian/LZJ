from gen_cc_bin_file import load_hh_dict

elist122 = load_hh_dict(r'd:\1\122.txt', 'gb18030')
elist124 = load_hh_dict(r'd:\1\124.txt', 'gb18030')

ew122 = []
for i in elist122:
   ew122.append(i['entry'])

ew124 = []
for i in elist124:
   ew124.append(i['entry'])

s122 = frozenset(ew122)
s124 = frozenset(ew124)

print "Print the 12.4 minus 12.2"
delta = s124 - s122
for i in delta:
   print i.encode('gb18030'),
   
print "Print the 12.2 minus 12.4"
delta = s122 - s124
for i in delta:
   print i.encode('gb18030'),
