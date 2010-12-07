# vim:fileencoding=utf-8
# coding=utf-8

import re

def pinyin_ord(letter):
   alphabet_order = u' 12345AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtVvUu\xfcWwXxYyZz'
   return alphabet_order.find(letter)

def pinyin_cmp(s1, s2):
   complete = frozenset(u' 12345AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtVvUu\xfcWwXxYyZz')
   sub = frozenset(s1)
   if not sub < complete:
      raise Exception, "pinyin not transformed before comparison"
   sub = frozenset(s2)
   if not sub < complete:
      raise Exception, "pinyin not transformed before comparison"

   len_s1 = len(s1)
   len_s2 = len(s2)
   minlen = min(len_s1, len_s2)
   for i in xrange(minlen):
      if pinyin_ord(s1[i]) < pinyin_ord(s2[i]):
         return -1
      elif pinyin_ord(s1[i]) > pinyin_ord(s2[i]):
         return 1
      else:
         continue

   if minlen < len_s1:
      return 1
   elif minlen < len_s2:
      return -1
   else:
      return 0

tone_to_value = {
                 u'\u0101': (u'a', 1),
                 u'\u016b': (u'u', 1),
                 u'\u014d': (u'o', 1),
                 u'\xe9':  (u'e', 2),
                 u'\u01d0': (u'i', 3),
                 u'\xed': (u'i', 2),
                 u'\xec': (u'i', 4), 
                 u'\u0113': (u'e', 1),
                 u'\u01d2': (u'o', 3), 
                 u'\u01d8': (u'\xfc', 2), #yu, two dots above u
                 u'\u011b': (u'e', 3),
                 u'\u0144': (u'n', 2),
                 u'\u01da': (u'\xfc', 3), #yu
                 u'\u012b': (u'i', 1),
                 u'\xf9': (u'u', 4), 
                 u'\xf3': (u'o', 2),
                 u'\xfa': (u'u', 2),
                 u'\xf2': (u'o', 4),
                 u'\u0148': (u'n', 3),
                 u'\ue7c8': (u'n', 4),
                 u'\xe1': (u'a', 2),
                 u'\u01ce': (u'a', 3),
                 u'\u01dc': (u'\xfc', 4), #yu
                 u'\xe0': (u'a', 4),
                 u'\xe8': (u'e', 4),
                 u'\u01d4': (u'u', 3) }
def transform_syllable(syllable):
   global tone_to_value
   transformed_syllable = []
   tone = 5 # The 5th tone, neutral tone, qingsheng
   for letter in syllable:
      if tone_to_value.has_key(letter):
         if not tone == 5:
            print "*** CRITICAL ERROR: Duplicate tone sign in a syllable ***"
         ascii_letter = tone_to_value[letter][0]
         transformed_syllable.append(ascii_letter)
         tone = tone_to_value[letter][1]
      else:
         transformed_syllable.append(letter)
   transformed_syllable.append("%d" % tone)
   return ''.join(transformed_syllable)

RE_COMMA_HALF_WIDTH = re.compile(',')
RE_COMMA_FULL_WIDTH = re.compile(u'\uff0c')

def transform_pinyin(pinyin):
   str_wo_comma = re.sub(RE_COMMA_HALF_WIDTH, ' ', pinyin)
   str_wo_comma = re.sub(RE_COMMA_FULL_WIDTH, ' ', str_wo_comma)
   pinyin = str_wo_comma
   transformed_pinyin = []
   for syllable in pinyin.split(' '):
      transformed_pinyin.append(transform_syllable(syllable))
   result = ' '.join(transformed_pinyin)
   return result

def key_func_sort_by_pinyin(d):
   return transform_pinyin(d['pinyin'])

