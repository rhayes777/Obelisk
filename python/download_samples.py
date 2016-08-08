import urllib2
import zipfile
import os

url = "https://www.dropbox.com/sh/gmpxk8f1qv7ht1u/AADFY0c6hUwP8x-iyWm-QzUga?dl=1"
filename = "../samples.zip"

def download_samples():
    u = urllib2.urlopen(url)
    data = u.read()
    u.close()
     
    with open(filename, "wb") as f:
        f.write(data)
        
    with zipfile.ZipFile('../samples.zip', 'r') as z:
        z.extractall('../samples')
        
    os.system('rm ../samples.zip')
    
    
if __name__ == "__main__":
    download_samples()