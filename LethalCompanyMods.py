import os
import psutil
import glob
import shutil
import zipfile
import stat
import requests
from tqdm import tqdm

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
        return ['1234567890']
    
#所有硬碟掃描第一次
ans = input('\n按Enter開始自動安裝，或是貼上遊戲資料夾位置：')

if ans=='\n':
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
    x = 1
    while(flag==False):
        for i in l:
            print(i)
            if i.count('steamapps')==1:
                a = glob.glob(f'{i}/**/common/Lethal Company/Lethal Company.exe',recursive=True)
                if a!=[]:
                    ans = a
                    flag=True
        k = l.copy()
        l = []
        if x==3:
            print("\n找不到資料夾，請輸入資料夾位置："*3)
            ans = input()+'/'
            break
        for i in k:
            l=l+([f'{i}\\{j}\\' for j in get_allfile(f'{i}')])
        x += 1

            
    #整理路徑
    # print(ans,end='\n')
    if flag==False:
        pass
    else:
        ans = ans[0].split('\\')[:-1]
        ans = '\\'.join(ans)+'\\'
else:
    #clone git project
    print('\n-----正在下載模組-----',end='\n')

    try:
        for i in range(1,99999):
            url = f'https://github.com/djhfme0/Mod_package/raw/main/version/v{i}/LethalCompany.zip'
            response = requests.get(url, stream=True)
            time = int(response.headers.get('content-length', 0))
            if response.status_code == 200:
                try:
                    os.mkdir(ans+'/git/')
                except:
                    pass
                print(url)
                file_name = ans+'/git/LethalCompany.zip'
                with open(file_name, 'wb') as file, tqdm(
                    desc=f'v{i}',
                    total=time,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                )as bar:
                    for data in response.iter_content(chunk_size=1024):
                        size = file.write(data)
                        bar.update(size)
            extract_zip(ans+'/git/'+'LethalCompany.zip',ans+'/')
            shutil.rmtree(ans+'/git/',onerror=readonly_handler)
    except:
        pass