#author MaHu
import os 

"""robotization instead of manpower """

cmd="gen_cc_bin_file.py"
os.system(cmd)

cmd=r"del D:\1\ccdict_ciku.bin,D:\1\cgdict_1st_index.bin,D:\1\cgdict_2nd_index.bin,D:\1\cgdict_3rd_index.bin,D:\1\checkresult.txt,D:\1\merged_list.txt,D:\1\chengyu_ciku.bin,D:\1\chengyu.txt"
os.system(cmd)



os.rename(r"D:\1\mergedchengyu_list.txt",r"D:\1\chengyu.txt")


cmd="gen_cc_bin_file.py"
os.system(cmd)
