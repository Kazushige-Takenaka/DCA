import subprocess
import re
dir='result/allzeorite'

cifdir_ = subprocess.getoutput("find {0} -type d | sort".format(dir))
cifdir = cifdir_.split('\n')
del cifdir[0]
isiteinfo=list()
for i in cifdir:
    cifid=re.split('/',i)[-1]
    lasttxt=subprocess.getoutput("grep ' Si' {}/{}.txt |tail -n 1".format(i,cifid))
    try:
        maxisite=int(re.split('Si',lasttxt)[0].replace(' ',''))
    except:
        continue
    isiteinfo.append((i,maxisite))
isiteinfo.sort(key=lambda x:x[1])
h=5*60*60
estimecont=int((h/1.28/12)*1.5)
print(estimecont)
cont=0
picupadress=list()
for i in isiteinfo:
    cont+=i[1]
    picupadress.append(i)
    if cont>=estimecont:
        break
    continue
import pandas as pd
info=pd.DataFrame(picupadress,columns=['cifadress','Si_len'])
info.to_csv('{}/picupadress'.format(dir))
