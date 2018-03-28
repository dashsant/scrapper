import os
import sys
import subprocess

d = sys.argv[1]
files =  os.listdir(d)
for f in files:
	tmp = d + f
	cmd = "gdrive upload --parent 1cWO75eoIgArvYMU_OB4TD43gNrvDN8x9 " + tmp
	print (cmd)
	subprocess.call(cmd , shell=True)
	os.remove(tmp)

		

