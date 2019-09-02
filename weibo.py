import subprocess as sp
import sys

p = sp.Popen([sys.executable, "weibo_output.py"],
             stdin=sp.PIPE, bufsize=1, universal_newlines=True,creationflags=sp.CREATE_NEW_CONSOLE)
while True:
    keyword=input("\nweibo url :")
    if not keyword:
        continue
    p.stdin.write(keyword+"\n")
    p.stdin.flush()
    if keyword=="exit":
        break
