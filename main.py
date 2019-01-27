import os,sys,subprocess

if len(sys.argv)>1:
    if "weibo.com" in sys.argv[1]:
        subprocess.run("python 'weibo.py' '"+sys.argv[1]+"'")
    elif "bcy.net" in sys.argv[1]:
        subprocess.run("python 'bcy.py' '"+sys.argv[1]+"'")
    else:
        print("Not suppost")

key=True
while key:
    key=input("\nurl ")
    if "weibo.com" in key:
        subprocess.run('python "weibo.py" '+key)
    elif "bcy.net" in key:
        subprocess.run('python "bcy.py" '+key)
    else:
        print("Not suppost")
