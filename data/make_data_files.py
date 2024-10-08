#!/usr/bin/env python

##
#  Retrieves the SCEC project location from CARC. They are
#  very big
#

import getopt
import sys
import subprocess

if sys.version_info.major >= (3) :
  from urllib.request import urlopen
else:
  from urllib2 import urlopen

model = "CS248"

def usage():
    print("\n./make_data_files.py\n\n")
    sys.exit(0)

def download_urlfile(url,fname):
  try:
    response = urlopen(url)
    CHUNK = 16 * 1024
    with open(fname, 'wb') as f:
      while True:
        chunk = response.read(CHUNK)
        if not chunk:
          break
        f.write(chunk)
  except:
    e = sys.exc_info()[0]
    print("Exception retrieving and saving model datafiles:",e)
    raise
  return True

def main():

    # Set our variable defaults.
    fname = ""
    path = ""
    mdir = ""

    # Get the dataset.
    try:
        fp = open('./config','r')
    except:
        print("ERROR: failed to open config file")
        sys.exit(1)

    ## look for model_data_path and other varaibles
    lines = fp.readlines()
    for line in lines :
        if line[0] == '#' :
          continue
        parts = line.split('=')
        if len(parts) < 2 :
          continue;
        variable=parts[0].strip()
        val=parts[1].strip()
        if (variable == 'model_data_path') :
            path = val + '/' + model
            continue
        if (variable == 'model_dir') :
            mdir = "./"+val
            continue

        continue
    if path == "" :
        print("ERROR: failed to find variables from config file")
        sys.exit(1)

    fp.close()

    print("\nDownloading model dataset\n")


    subprocess.check_call(["mkdir", "-p", mdir])

    fname=mdir+"/density.tar.gz"
    url = path + "/" + fname
    download_urlfile(url,fname)
    subprocess.check_call(["tar", "-zxvf", fname])
    subprocess.check_call(["mv", "density.dat", "cs248"])

    fname=mdir+"/vp.tar.gz"
    url = path + "/" + fname
    download_urlfile(url,fname)
    subprocess.check_call(["tar", "-zxvf", fname])
    subprocess.check_call(["mv", "vp.dat", "cs248"])

    fname=mdir+"/vs.tar.gz"
    url = path + "/" + fname
    download_urlfile(url,fname)
    subprocess.check_call(["tar", "-zxvf", fname])
    subprocess.check_call(["mv", "vs.dat", "cs248"])

    print("\nDone!")

if __name__ == "__main__":
    main()
