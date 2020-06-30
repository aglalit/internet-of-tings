import redis
from flask import Flask
from MIR import essentia_main
import os
import fs
import fs.copy
import fs.memoryfs

# TODO: IMPLEMENT MEMORY FS LATER

# mem_fs = fs.memoryfs.MemoryFS()
# mem_fs.makedirs('fruit')
# mem_fs.makedirs('vegetables')
# with mem_fs.open('fruit/apple.txt', 'w') as apple:
#     apple.write('braeburn')
#     print(apple)
#
# # write to the CWD for testing...
# with fs.open_fs(".") as os_fs:  # use a custom path if you want, i.e. osfs://<base_path>
#     fs.copy.copy_fs(mem_fs, os_fs)

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


@app.route('/')
def hello():
	return essentia_main.test()
