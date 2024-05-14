import os
import psutil
import glob
import shutil
import zipfile
import stat
import requests

#解壓縮
def extract_zip(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

#admin
def readonly_handler(func, path, execinfo):
    os.chmod(path,stat.S_IWRITE)
    func(path)

#get_folder_files
def get_allfile(dir):
    try:
        return os.listdir(dir)
    except:
        return ['0']
    
#所有硬碟掃描第一次
print('--------載入中--------',end='\n\n')
l = []
disk = [i.mountpoint for i in psutil.disk_partitions()]
for i in disk:
    l=l+([f'{i}{j}' for j in get_allfile(f'{i}')])
    
#掃描所有folder直到找到遊戲
print('-----搜尋遊戲路徑-----',end='\n\n')
flag = False
c = False
ans = []
while(flag==False):
    for i in l:
        if i.count('steamapps')==1:
            a = glob.glob(f'{i}/**/common/Lethal Company/Lethal Company.exe',recursive=True)
            if a!=[]:
                ans = a
    if ans!=[]:
        flag=True
    k = l.copy()
    l = []
    for i in k:
        l=l+([f'{i}\\{j}\\' for j in get_allfile(f'{i}')])
        
#整理路徑
# print(ans,end='\n')
ans = ans[0].split('\\')[:-1]
ans = '\\'.join(ans)+'\\'

#clone git project
print('-----正在下載模組-----',end='\n\n')
os.mkdir(ans+'/git/')
url = 'https://github.com/djhfme0/Mod_package/raw/main/LethalCompany.zip'
response = requests.get(url)
if response.status_code == 200:
    file_name = ans+'/git/LethalCompany.zip'
    with open(file_name, 'wb') as file:
        file.write(response.content)
extract_zip(ans+'/git/'+'LethalCompany.zip',ans+'/')
shutil.rmtree(ans+'/git/',onerror=readonly_handler)
