import sys
import client

url = "http://0.0.0.0:8080/filepath/"
print("==================================================================")
print("\t\tWelcome to Distributed File System")
print("==================================================================\n")
filepath = input("Enter the file name:")
url = url+filepath
with open(filepath, 'wtc') as f:
    f.write('Hello world')

    f = client.File.from_cache(filepath)
    if f == None:
        print(sys.stderr, ' Cache expired.')
    else:
        print(f.read())

