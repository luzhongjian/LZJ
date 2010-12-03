s = ['', '', 'a', 'A', 'b', 'B', 'c', 'C', 'd',
     'D', 'e', 'E', 'f', 'F', 'g', 'G',
     'h', 'H', 'i', 'I', 'j', 'J', 'k',
     'K', 'l', 'L', 'm', 'M', 'n', 'N',
     'o', 'O', 'p', 'P', 'q', 'Q', 'r',
     'R', 's', 'S', 't', 'T', 'u', 'U',
     'v', 'V', 'w', 'W', 'x', 'X', 'y',
     'Y', 'z', 'Z']

def stringGenerator():
   i = 2
   j = 1
   k = 0
   len_s = len(s)
   while i < len_s:
      while j < len_s:
         while k < len_s:
            yield s[i] + s[j] + s[k]
            #print "i = %s j = %s k = %s" % (s[i], s[j], s[k])
            k = k + 1
            if k == 1 and j == 1:
               j = j + 1
         j = j + 1
         k = 1
      i = i + 1
      j = 1
      k = 0

if __name__ == '__main__':
   for i in stringGenerator():
      print i
