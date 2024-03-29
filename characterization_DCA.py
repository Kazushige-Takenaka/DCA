from subprocess import run
import os,subprocess
from Distance_based_on_Cluster_Analysis.read_info import make_sort_ciffile
import pandas as pd

import argparse
def pares_args():
    pares=argparse.ArgumentParser()
    pares.add_argument('--cifdir',default='cifdirs/sort_volume_ciffiles_top_100',help='zeolitecif')
    pares.add_argument('--adjacent_num',default=2,help='(int)')
    pares.add_argument('--database_path',default='cluster_database',help='database path')
    return pares.parse_args()

def main():
  pares=pares_args()
  cifdir=pares.cifdir
  adjacent_num=pares.adjacent_num
  databaseadress=pares.database_path
  #cifから隣接情報の取出し
  run('python3 Distance_based_on_Cluster_Analysis/make_adjacent_table.py --codpath {} --output2 {}'.format(cifdir,cifdir),shell=True)
  print('emd make_adjacent_tabel')
  run('python3 Distance_based_on_Cluster_Analysis/make_nn_data.py --output2 {}'.format(cifdir),shell=True)
  print('emd make_nn_data')
  #隣接情報からクラスターを生成
  from Distance_based_on_Cluster_Analysis.make_cluster import make_cluster_dataset
  picdata=make_sort_ciffile('result/{}'.format(cifdir),estimecont='all')
  allciflen=picdata.shape[0]
  for i,data in picdata.iterrows():
      print('\r{} {}/{}'.format(data.cifid,i+1,allciflen),end='')
      nn_data_adress= subprocess.getoutput("find {0} -name nb_*.pickle".format(data.cifadress))
      make_cluster_dataset(cifid=data.cifid,nn_data_adress=nn_data_adress,adjacent_num=adjacent_num,rotation=False,outdir=data.cifadress)
  print()

  #各cifファイルの特徴量を計算
  from Distance_based_on_Cluster_Analysis.cluster_pointing import make_crystall_point
  from Distance_based_on_Cluster_Analysis.cluster_adress_func import cluster_list
  d=make_crystall_point(databaseadress)
  import pandas as pd
  resulttxt='result/{}/cifpoint'.format(cifdir)
  text_file=open(resulttxt,'w')
  text_file.write('cifid,point\n')
  text_file.close()
  cifadress_list=pd.read_csv('result/{}/picupadress'.format(cifdir),index_col=0).cifadress.to_list()
  import os
  for i,cifadress in enumerate(cifadress_list):
    cifid=os.path.basename(cifadress)
    print('cif {}/{}'.format(i+1,len(cifadress_list)))
    print(cifid)
    d.cal_crystal_point(cifadress,n_job=-1)
    text_file=open(resulttxt,'a')
    text_file.write('{},{}\n'.format(cifid,d.crystal_point))
    text_file.close()

if __name__=='__main__':
  main()