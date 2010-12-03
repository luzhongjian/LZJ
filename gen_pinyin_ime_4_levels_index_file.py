"""Added by prm for generating English-Ehinese dictionary extracted index file"""
#encoding = utf-8

from codecs import open
from struct import pack, unpack
def load_ime_pinyin_file(file, encoding):
   openFile = open(file, 'r', encoding)
   result = []
   while True:
      line =openFile.readline()
      if len(line) == 0:
         break;
      else:
         result.append(line)
   print "%d total entries size" % len(result)    
   return result

def keyfunc(s):
   return s['entry'].lower()

def build_four_level_index(f1, f2, f3, f4, entrylist):
   i   = 0
   d_level3 = {}
   d_level3_key = []
   temp_index = 0 

   for entry in entrylist:
      text_len    = 0
      cur = f4.tell() 
      text_len = len(entry) * 2 
      temp_entry = entry.split('\x09')
      temp_entry = temp_entry[0]
      if len(temp_entry) >= 3:
         entry_text_first_3letters = temp_entry[0:3]           
         if not d_level3.has_key(entry_text_first_3letters):  # extract first 3 letters into one string, then compare it. 
            d_level3_key.extend([entry_text_first_3letters])
            d_level3[entry_text_first_3letters] = cur
            temp_index = temp_index + 1
      else:
         if not d_level3.has_key(temp_entry):  
            d_level3_key.extend([temp_entry])
            d_level3[temp_entry] = cur
            temp_index = temp_index + 1 
  
      if text_len != 0: 
         f4.write(entry.encode('utf-16le'))
      """try:
         pass """

   d_level2 = {}
   d_level2_key = [] 
   temp_index1 = 0  
   i = 0
   for i in range(temp_index):
      key = d_level3_key[i]
      value = d_level3.get(key) 
      if (value >= 0):
         #s = "%03s" % key
         if(len(key)==1):
            s = key + '00'
         elif(len(key)== 2):
            s = key + '0'
         else:
            s = key
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
      if (value >= 0):
         #s = "%02s" % key
         if(len(key)==1):
            s = key + '0'
         else:
            s = key
         s = s.encode('utf-16le')
         #print value
         s = s + pack('I', value)
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
      if (value >= 0):
         #s = "%01s" % key
         s = key
         s = s.encode('utf-16le')
         s = s + pack('H', value)
         f1.write(s)

if __name__ == '__main__':
   entrylist = load_ime_pinyin_file(r'D:\MerlionColor\imePinYin\PinYinIndex_utf16.txt', 'utf-16le')
   #entrylist = sorted(entrylist, key = keyfunc)
   level1_index_file = open(r'd:\MerlionColor\imePinYin\dict_ime_pinyin_1st_index.bin', 'wb')
   level2_index_file = open(r'd:\MerlionColor\imePinYin\dict_ime_pinyin_2nd_index.bin', 'wb')
   level3_index_file = open(r'd:\MerlionColor\imePinYin\dict_ime_pinyin_3rd_index.bin', 'wb')
   level4_index_file = open(r'd:\MerlionColor\imePinYin\dict_ime_pinyin_4th_index.bin', 'wb')
   build_four_level_index(level1_index_file, level2_index_file, level3_index_file, level4_index_file,
         entrylist)
   level1_index_file.close()
   level2_index_file.close()
   level3_index_file.close()
   level4_index_file.close()



