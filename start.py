#author MaHu
import os, sys

"""robotization instead of manpower """

cmd=[sys.executable]
cmd.append(os.path.join(os.path.dirname(__file__), "gen_cc_bin_file.py"))
cmd.append(sys.argv[1])
cmd.append(sys.argv[2])
cmd.append(sys.argv[3])
os.system(' '.join(cmd))

cmd=r"del ccdict\ccdict_ciku.bin cgdict\cgdict_1st_index.bin,cgdict\cgdict_2nd_index.bin,cgdict\cgdict_3rd_index.bin,checkresult.txt,merged_list.txt,ccdict-idiom\chengyu_ciku.bin,chengyu.txt"
os.system(cmd)

os.rename(r"mergedchengyu_list.txt",r"chengyu.txt")

cmd=[sys.executable]
cmd.append(os.path.join(os.path.dirname(__file__), "gen_cc_bin_file.py"))
cmd.append(sys.argv[1])
cmd.append(sys.argv[2])
cmd.append(sys.argv[3])
os.system(' '.join(cmd))

