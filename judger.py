from subprocess import Popen,PIPE
import time,sys,os,easygui
right=0
i=0
try:
    filename=sys.argv[1];
    userfile=sys.argv[2];
    language=sys.argv[3];
except:
    print("Usage:name [filename.py] [filepath] [language]")
print(language)
if (language=="C++"):
    print(114514)
    os.system("gcc -O2 -g -o "+filename+".exe submit/"+filename)
ansdict={"AC":0,"WA":0,"TLE":0,"CE/RE":0}
logfile=open("data.log","w",encoding="utf-8")
while True:
    try:
        timea=time.time()
        cinfile=open("testdatas/"+filename+"f/"+str(i+1)+".in","r")
        coutfile=open("testdatas/"+filename+"f/"+str(i+1)+".out","r")
        if (language=="Python"):
            p = Popen("python "+userfile,shell=True,stdout=PIPE,stdin=PIPE)
        elif (language=="C++"):
            p = Popen(filename+".exe",shell=True,stdout=PIPE,stdin=PIPE)
        proans=p.communicate(input=bytes(cinfile.read().encode()))[0]
        
        try:
            rcode=p.wait(timeout=None)
        except subprocess.TimeoutExpired:
            ansdict["TLE"]+=1
            p.kill()
            print(i+1,"TLE")
            i+=1
            continue
        timeb=time.time()
        if (timeb-timea>1):
            ansdict["TLE"]+=1
            print(i+1,"TLE "+str(int((timeb-timea)*1000))+"ms")
            logfile.write(str(i+1)+" TLE "+str(int((timeb-timea)*1000))+"ms\n")
            i+=1
            continue
        #proans=list(proans)
        #print(proans)
        tempans=[]
        gg=0
        proans=proans.decode()
        for k in proans:
            if (k!='\r'):
                tempans+=k
                gg+=1
        proans=tempans
        gg=0
        #print(tempans)
        #proans=tempans
        #proans=proans.decode()
        #proans=proans.strip("\r\n")
        cans=coutfile.readlines()
        tempcans=""
        #print(cans)
        for k in cans:
            tempcans+=k
        cans=tempcans
        #cans.strip("\n")
        #proans.strip("\n\r")
        #proans.strip("\n")
        #if (proans[-1]==' '):
        #    proans=proans[0:len(proans)-2]
        #proans.split("\r")
        #print(list(proans))
        #print(list(cans))
        cans=list(cans)
        if (cans[-1]=="\n"):
            cans.pop()
        if (proans[-1]=="\n"):
            proans.pop()
        if (cans[-1]==" "):
            cans.pop()
        if (proans[-1]==" "):
            proans.pop()
        if (str(proans)==str(cans)):
            right+=1
            ansdict["AC"]+=1
            print(i+1,"AC "+str(int((timeb-timea)*1000))+"ms")
            logfile.write(str(i+1)+" AC "+str(int((timeb-timea)*1000))+"ms\n")
        else:
            if (rcode==0):
                ansdict["WA"]+=1
                print(i+1,"WA "+str(int((timeb-timea)*1000))+"ms")
                logfile.write(str(i+1)+" WA "+str(int((timeb-timea)*1000))+"ms\n")
            else:
                ansdict["RE/CE"]+=1
                print(i+1,"RE/CE "+str(int((timeb-timea)*1000))+"ms")
                logfile.write(str(i+1)+" RE/CE "+str(int((timeb-timea)*1000))+"ms\n")
        cinfile.close()
        coutfile.close()
    except:
        break
    i+=1
try:
    print(str((right)/(i)*100)+"pts")
    logfile.write(str((right)/(i)*100)+"pts\n")
    if (ansdict["AC"]==i):
        print("Accepted")
        logfile.write("Accepted")
    elif (ansdict["AC"]>0):
        print("Partial Accepted")
        logfile.write("Partial Accepted")
    else:
        if (max(ansdict["WA"],ansdict["TLE"])==ansdict["WA"]):
            print("Wrong Answer")
            logfile.write("Wrong Answer")
        else:
            print("Time Limit Exceeded")
            logfile.write("Time Limit Exceeded")
    logfile.write("\n"+str((right)/(i)*100))
    
except:
    print("0.0pts")
    logfile.write("0.0pts\n")
    logfile.write("System Error")
    logfile.write("\n0")
logfile.close()
