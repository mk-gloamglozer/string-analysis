import requests
import gzip
import shutil
import shutil
import urllib.request as request
from contextlib import closing

def download_file(url:str, outfile:str, ftp=False):
    if ftp:
        download_ftp_file(url,outfile)
    else:
        with requests.get(url,stream=True) as r:
            r.raise_for_status()
            with open(outfile, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    
def unzip(filepath:str, outfile:str):
    with gzip.open(filepath, 'rb') as f_in:
        with open(outfile, 'wb') as f_out:
            shutil.copyfileobj(f_in,f_out)

def download_ftp_file(url:str, outfile:str):
    with closing(request.urlopen(url)) as r:
        with open(outfile, 'wb') as f:
            shutil.copyfileobj(r,f)