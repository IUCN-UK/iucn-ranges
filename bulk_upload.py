import dask.bag as db
import json
import os
import sys

from glob import glob
from functools import partial
from time import sleep

def upload_item(host, index_name, type_name, file_name):
    sleep(5)
    os.system('curl -XPOST {}/{}/{}/_bulk --data-binary @{} > {}'.format(host, index_name, type_name,
                                                                                               file_name, file_name + '.result'))
    print(file_name)

host = sys.argv[1]
index_name = sys.argv[2]
type_name = sys.argv[3]
glob_str = sys.argv[4]

files = list(glob(glob_str))
myfunc = partial(upload_item, host, index_name, type_name)
for f in reversed(files):
    myfunc(f)

#mybag = db.from_sequence(files)
#results = mybag.map(myfunc).compute()
