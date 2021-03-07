#Packages
import json, re, os, haversine , random, requests, sys, subprocess
from passlib.hash import sha256_crypt
from datetime import datetime
from termcolor import colored,cprint

#Pre-defined data
currentpath =  os.path.dirname(sys.argv[0])
filepath = currentpath + "/shipdata.json"
datalink = "https://shipit-pantomaths.firebaseio.com/.json"
datalink2 = "https://shipit-log-default-rtdb.firebaseio.com/.json"

os.system('cls')

def aboutus():
    cprint("")
    cprint("-="*64,"blue","on_white")
    cprint(" "*60 + "ABOUT US" + " "*60,"blue","on_white")
    cprint("-="*64,"blue","on_white")
    cprint("")
    cprint("Thanks For using our Service, here is our About Us section:","blue")
    cprint("")
    cprint("We are ShipIt!, a service that aims to help you choose the best shipping service for you.","blue")
    cprint("The Developer:","blue")
    cprint("P.Biswanath Patra","blue")
    cprint("XII - A, Kendriya Vidyalaya, BAM","blue")
    cprint("For social data:","blue")
    cprint("@roshanbiswanath","blue")
    cprint("roshanbiswanathpatra@gmail.com","blue")

def checkmailexist(mail):
    mailexist = False
    for i in data["admins"]:
        if mail == i["email"]:
            mailexist = True
            break
        else:
            mailexist = False
    return mailexist

def checklogin(mail,passw):
    for i in data["admins"]:
        if i["email"] == mail and sha256_crypt.verify(passw, i["pwd"]) :
            check = True
            break
        else:
            check = False
    return check

#Online Data Functions Start
def datadownload():
    global data
    r = requests.get(datalink).text
    data = json.loads(r)

def dataupload():
    global data
    requests.patch(datalink,data = json.dumps(data))
#Online Data Functions End

#-------------------------------------------------------------------------------------------------------------#

#Offline Data Functions Start
def getdata():
    global data
    f = open(filepath,"r")
    data = json.load(f)
    f.close()

def updatedata():
    global data
    f = open(filepath,"w")
    f.write(json.dumps(data))
    f.close()
#Offline Data Functions End


def login():
    global mail
    getdata()
    while True:
        mail = None
        passwd = None
        maildone2,pwdone2,flag2 = False,False,False
        cprint("-"*128,"blue","on_white")
        cprint("|"+" "*57 + "Login Screen" + " "*57+"|" ,"blue","on_white")
        cprint("-"*128,"blue","on_white")
        while maildone2 == False and flag2 == False:
            cprint("Enter E-mail ID to login into ShipIt","blue")
            mail = input("Mail ID : ")
            cprint("You entered "+mail+" as your email ID","blue")
            cprint("To continue Press 1","magenta")
            cprint("To re-enter press 2","magenta")
            cprint("To go-back to main-screen press 3","yellow")
            while True:
                try:
                    ch2 = int(input())
                except:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1,2 and 3","yellow")
                    continue
                if ch2 not in [1,2,3]:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1,2 and 3","yellow")
                break
            if ch2 == 3:
                flag2 = True
                break
            elif ch2 == 2:
                continue
            elif not checkmailexist(mail):
                cprint("Provided E-mail doesn't exist in database.","yellow")
                continue
            else:
                maildone2 = True
                break
        while pwdone2 == False and flag2 == False and maildone2 == True:
            cprint("Enter Password to login into ShipIt","blue")
            passwd = input("Password : ")
            cprint("You entered "+passwd+" as your Password","blue")
            cprint("To continue Press 1","magenta")
            cprint("To re-enter press 2","magenta")
            cprint("To go-back to main-screen press 3","yellow")
            while True:
                try:
                    ch3 = int(input())
                except:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1,2 and 3","yellow")
                    continue
                if ch3 not in [1,2,3]:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1,2 and 3","yellow")
                    continue
                break
            if ch3 == 3:
                flag2 = True
                break
            elif ch3 == 2:
                continue
            else:
                pwdone2 = True
                break
        if flag2 == True:
            break
        elif checklogin(mail,passwd) and flag2 == False and maildone2 == True and pwdone2 == True:
            cprint("Login Successfull","green")
            startup(mail)
            break
        else:
            cprint("Username and Password don't match","red")
            cprint("To Re-enter mail-id and passwd press 1","magenta")
            cprint("To go to main- menu press 2","yellow")
            while True:
                try:
                    ch4 = int(input())
                except :
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1 and 2","yellow")
                    continue
                if ch4 not in [1,2]:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1,2 and 3","yellow")
                    continue
                break
            if ch4 == 1:
                continue
            else:
                break

def startup(mail):
    while True:
        datadownload()
        dataupload()
        getdata()
        cprint("+"+"-"*126+"+","blue","on_white")
        cprint("|"+" "*54 +"Welcome to ShipIt!" + " "*54+"|","blue","on_white")
        cprint("+"+"-"*126+"+","blue","on_white")
        for i in data["admins"]:
            if i["email"] == mail:
                userdict = i
                break
        cprint("Hello " +userdict["name"],"blue")
        cprint("Email Id : "+userdict["email"],"blue")
        cprint("Courier Service : "+data["couriers"][userdict["courier"]],"blue")
        cprint("To change prices press 1","magenta")
        cprint("To Log-Out press 2","red")
        while True:
            try:
                ch5 = int(input())
            except:
                cprint("Invalid Input Given. Please Re-enter","yellow")
                cprint("Enter a value between 1,2, or 3","yellow")
                continue
            if ch5 not in [1,2]:
                cprint("Invalid Input Given. Please Re-enter","yellow")
                cprint("Enter a value between 1,2, or 3","yellow")
                continue
            break
        if ch5 == 2:
            break
        else:
            while True:
                for i in data["admins"]:
                    if i["email"] == mail:
                        userdict = i
                        break
                datadownload()
                dataupload()
                getdata()
                cprint("Editing Prices","blue")
                cprint("Current Prices ","blue")
                cprint("+--- Fast -------+-------------------------------------+","blue")
                cprint("|     Weight     |     Start Price    |  Price per km  |","blue")
                cprint("+----------------+-------------------------------------+","blue")
                for i in data["courier_prices"]["fast"]:
                    if i == "01":
                        k = "    0 - 1 kg    "
                    elif i == "15":
                        k = "    1 - 5 kg    "
                    elif i == "510":
                        k = "   5 - 10 kg    "
                    elif i == "100":
                        k = "      10+ kg    "
                    d = data["courier_prices"]["fast"][i]
                    a = "pricekm"+userdict["courier"]
                    b = "startprice"+userdict["courier"]
                    x = ["₹"+str(d[b]),"₹"+str(d[a])]
                    cprint("|"+k+"|    "+x[0]+" "*(16-len(x[0]))+"|   "+x[1]+" "*(13-len(x[1]))+"|","magenta")
                cprint("+----------------+--------------------+----------------|","blue")
                cprint("")
                cprint("+-- Normal ------+-------------------------------------+","blue")
                cprint("|     Weight     |     Start Price    |  Price per km  |","blue")
                cprint("+----------------+-------------------------------------+","blue")
                for i in data["courier_prices"]["normal"]:
                    if i == "01":
                        k = "    0 - 1 kg    "
                    elif i == "15":
                        k = "    1 - 5 kg    "
                    elif i == "510":
                        k = "   5 - 10 kg    "
                    elif i == "100":
                        k = "      10+ kg    "
                    d = data["courier_prices"]["normal"][i]
                    a = "pricekm"+userdict["courier"]
                    b = "startprice"+userdict["courier"]
                    x = ["₹"+str(d[b]),"₹"+str(d[a])]
                    cprint("|"+k+"|    "+x[0]+" "*(16-len(x[0]))+"|   "+x[1]+" "*(13-len(x[1]))+"|","magenta")
                cprint("+----------------+--------------------+----------------|","blue")
                cprint("")
                cprint("To edit Fast Service prices press 1","magenta")
                cprint("To edit Normal Service prices press 2","magenta")
                cprint("To go back to main screen press 3","yellow")
                while True:
                    try:
                        ch6 = int(input())
                    except:
                        cprint("Invalid Input provided, please re-enter","yellow")
                        cprint("Enter a value between 1,2 or 3","yellow")
                        continue
                    if ch6 not in [1,2,3]:
                        cprint("Invalid Input provided, please re-enter","yellow")
                        cprint("Enter a value between 1,2 or 3","yellow")
                        continue
                    break
                if ch6 ==3 :
                    break
                elif ch6 == 2:
                    ser = "normal"
                else:
                    ser = "fast"
                cprint("")
                cprint("Choose the weight category to edit","blue")
                cprint("For 0-1  kg press 1","magenta")
                cprint("For 1-5  kg press 2","magenta")
                cprint("For 5-10 kg press 3","magenta")
                cprint("for 10+  kg press 4","magenta")
                cprint("To go back to main screen press 5","yellow")
                while True:
                    try:
                        ch7 = int(input())
                    except:
                        cprint("Invalid Input provided, please re-enter","yellow")
                        cprint("Enter a value between 1 to 5","yellow")
                        continue
                    if ch7 not in [1,2,3,4,5]:
                        cprint("Invalid Input provided, please re-enter","yellow")
                        cprint("Enter a value between 1 to 5","yellow")
                        continue
                    break
                if ch7 == 5 :
                    break
                elif ch7 == 1:
                    mas = ["01","0-1  kg"]
                elif ch7 == 2:
                    mas = ["15","1-5  kg"]
                elif ch7 == 3:
                    mas = ["510","5-10 kg"]
                else :
                    mas = ["100","10+  kg"]
                cprint("")
                cprint("To edit Startprice press 1","magenta")
                cprint("To edit per km price press 2","magenta")
                cprint("To go back to main screen press 3","yellow")
                while True:
                    try:
                        ch8 = int(input())
                    except:
                        cprint("Invalid Input provided, please re-enter","yellow")
                        cprint("Enter a value between 1,2 or 3","yellow")
                        continue
                    if ch8 not in [1,2,3]:
                        cprint("Invalid Input provided, please re-enter","yellow")
                        cprint("Enter a value between 1,2 or 3","yellow")
                        continue
                    break
                if ch8 ==3 :
                    break
                elif ch8 == 2:
                    pri = ["pricekm","Price per km"]
                else:
                    pri = ["startprice","Start Price"]
                cprint("")
                cur = data["courier_prices"][ser][mas[0]][pri[0]+userdict["courier"]]
                cprint("Current price for "+str(pri[1]),"blue")
                cprint("In mass category : "+str(mas[1]),"blue")
                cprint("for "+str(ser)+" is "+str(cur),"magenta")
                cprint("To change this press 1","magenta")
                cprint("Else going to main screen","yellow")
                ch9 = input()
                if ch9 == "1":
                    while True:
                        cprint("Enter new price")
                        newpri = float(input())
                        cprint("Press 1 to continue","magenta")
                        cprint("Press 2 to re-enter","magenta")
                        cprint("Press 3 to go back","yellow")
                        while True:
                            try:
                                ch10 = int(input())
                            except:
                                cprint("invalid input provided","yellow")
                                cprint("Re-enter a value from 1 to 3","yellow")
                                continue
                            if ch10 not in [1,2,3]:
                                cprint("invalid input provided","yellow")
                                cprint("Re-enter a value from 1 to 3","yellow")
                                continue
                            break
                        if ch10 == 3:
                            break
                        elif ch10 == 2:
                            continue
                        else:
                            cprint("Changing price for "+str(pri[1]),"magenta")
                            cprint("In mass category : "+str(mas[1]),"magenta")
                            cprint("for "+str(ser)+" from ₹"+str(cur)+" to ₹ "+str(newpri),"magenta")
                            cprint("To confirm press 1","yellow")
                            cprint("To re-enter press 2","magenta")
                            cprint("To go back press 3","yellow")
                            while True:
                                try:
                                    ch11 = int(input())
                                except:
                                    cprint("invalid input provided","yellow")
                                    cprint("Re-enter a value from 1 to 3","yellow")
                                    continue
                                if ch11 not in [1,2,3]:
                                    cprint("invalid input provided","yellow")
                                    cprint("Re-enter a value from 1 to 3","yellow")
                                    continue
                                break
                            if ch11 == 3:
                                break
                            elif ch11 == 2:
                                continue
                            else:
                                data["courier_prices"][ser][mas[0]][pri[0]+userdict["courier"]] = newpri
                                updatedata()
                                dataupload()
                                datadownload()
                                getdata()
                                prinow = data["courier_prices"][ser][mas[0]][pri[0]+userdict["courier"]]
                                cprint("Price changed","blue")
                                cprint("Current price for "+str(pri[1]),"magenta")
                                cprint("In mass category : "+str(mas[1]),"magenta")
                                cprint("for "+str(ser)+" is "+str(prinow),"magenta")
                                break
                    cprint("To edit prices again press 1","magenta")
                    cprint("else going to main screen","cyan")
                    ch12 = input()
                    if ch12 == "1":
                        continue
                    else:
                        break
                else:
                    cprint("Going to main screen","cyan")
                    break

while True:
    logincomplete = False
    datadownload()
    try:
        getdata()
        datadownload()
    except:
        updatedata()
    updatedata()
    cprint(" "*128,"white","on_cyan")
    cprint(" "*128,"white","on_cyan")
    cprint(" "*128,"white","on_cyan")
    cprint(" "*75 ,"white","on_cyan",end="")
    cprint("░██████╗██╗░░██╗██╗██████╗░██╗████████╗"+" "*14,"white","on_cyan",attrs=['bold'])
    cprint("Find the best shipping service for you."+" "*(36) ,"white","on_cyan",attrs=['bold'],end="") 
    cprint( "██╔════╝██║░░██║██║██╔══██╗██║╚══██╔══╝"+" "*14,"white","on_cyan",attrs=['bold'])
    cprint("Provide the details of your package and we will help you," + " "*18 ,"white","on_cyan",attrs=['bold'],end="")
    cprint( "╚█████╗░███████║██║██████╔╝██║░░░██║░░░"+" "*14,"white","on_cyan",attrs=['bold'])
    cprint( "to find the most suitable shipping service."+ " "*32,"white","on_cyan",attrs=['bold'],end="")
    cprint("░╚═══██╗██╔══██║██║██╔═══╝░██║░░░██║░░░"+" "*14,"white","on_cyan",attrs=['bold'])
    cprint(" "*75 +"██████╔╝██║░░██║██║██║░░░░░██║░░░██║░░░"+" "*14,"white","on_cyan",attrs=['bold'])
    cprint(" "*75 +"╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░░░░╚═╝░░░╚═╝░░░"+" "*14,"white","on_cyan",attrs=['bold'])
    cprint(" "*128,"white","on_cyan")
    cprint(" "*128,"white","on_cyan")
    cprint(" "*128,"white","on_cyan")
    cprint("-"*128,"grey","on_white")
    cprint("|"+' '*58 + "Disclaimer" +' '*58 + "|","grey","on_white")
    cprint("-"*128,"grey","on_white")
    cprint("This is a Python Project"+" "*104,"grey","on_white")
    cprint("the information provided by shipIt is for general usage purposes only."+" "*58,"grey","on_white")
    cprint("and is in no way related to any real organisation."+" "*78,"grey","on_white")
    cprint("The information entered by you wouldn't be considered for Ads but will be used for research and development of ShipIt!"+" "*10,"grey","on_white")
    cprint(" "*128,"grey","on_white")
    cprint("")
    cprint("To Login press 1","magenta")
    cprint("To End Session press 2","red")
    cprint("If encountering issues, contact","cyan",end="")
    cprint("roshanbiswanathpatra@gmail.com","blue")
    while True:
        try:
            ch1 = int(input())
        except:
            cprint("You have entered invalid data","yellow")
            continue
        if ch1 not in [1,2]:
            cprint("Enter suitable value from 1 or 2","yellow")
            continue
        break
    if ch1 == 1:
         
        login()
    elif ch1 == 2:
         
        break
    cprint("To end session enter N else continue","red")
    ch2 = input()
    if ch2 in ["N","n"]:
        cprint("Program Terminated","red")
         
        break
    cprint("Please Wait.....","cyan")
     

aboutus()

#Exit Loop
while True:
    cprint("To exit press q","red")
    q = input()
    if q == "q" or q == "Q":
        break

#-------------------------------------------------------------------------------------------------------------#

subprocess.call(["python.exe",  currentpath + "/main.py"])

#-------------------------------------------------------------------------------------------------------------#