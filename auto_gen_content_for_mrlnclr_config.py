Content_Processor_Config = {
      'chinese-chinese dictionary' : {
         'filename'   : r'hansvision.txt'
         ,'encoding'  : 'utf-16'
         ,'processor' : r'start.py'
         ,'encryption': 'ER_Key'
         },
      'chinese-idiom dictionary' : {
         'filename'  : r'chengyu.txt',
         'encoding'  : 'utf-16',
         'encryption': 'ER_Key'
         },
      'english-english dictionary' : {
         'filename'  : r'oxford.txt',
         'processor' : r'eedict_generate_bin_file.py',
         'encoding'  : 'utf-16'
         },
      'english-chinese dictionary' : {
         'filename' : r'ec.txt',
         'encoding' : 'utf-16',
         'processor': 'ecdict_generate_reduced_bin_file.py'
         },
      'chinese-english dictionary' : {
         'filename'  : r'ce.txt'
         ,'encoding' : 'gb18030'
         ,'processor': 'gen_ce_bin_file.py'
         },
      }
