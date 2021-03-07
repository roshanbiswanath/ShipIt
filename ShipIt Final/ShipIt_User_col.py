#Packages
import json, re, os, haversine , random, requests, sys, subprocess
from datetime import datetime
from termcolor import colored, cprint
os.system('cls')

#Pre-defined data
currentpath =  os.path.dirname(sys.argv[0])
data = {}
filepath = currentpath + "/shipdata.json"
datalink = "https://shipit-pantomaths.firebaseio.com/.json"
regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
datalink2 = "https://shipit-log-default-rtdb.firebaseio.com/.json"

#About Us Function
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

#-------------------------------------------------------------------------------------------------------------#

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

#-------------------------------------------------------------------------------------------------------------#

#Mail Structure Check Function
def checkvalid(email):
    if re.search(regex,email):
        return True
    else:
        return False

#-------------------------------------------------------------------------------------------------------------#

#Mail in Database Check
def checkmailexist(mail):
    mailexist = False
    for i in data["users"]:
        if mail == i["email"]:
            mailexist = True
            break
        else:
            mailexist = False
    return mailexist 

#-------------------------------------------------------------------------------------------------------------#

#Authentication Function
def checklogin(mail,passw):
    for i in data["users"]:
        if i["email"] == mail and i["pwd"] == passw :
            check = True
            break
        else:
            check = False
    return check

#-------------------------------------------------------------------------------------------------------------#

#Anonymous Startup Function
def startupano():
    while True:
        datadownload()
        updatedata()
        getdata()
        cprint("-"*128,"blue","on_white")
        cprint("|"+" "*54 +"Welcome to ShipIt!" + " "*54+"|","blue","on_white")
        cprint("-"*128,"blue","on_white")
        cprint("")
        cprint("Hello User","blue")
        cprint("Press 1 to check existing tracks","magenta")
        cprint("Press 2 to find suitable delivery service","magenta")
        cprint("Press 3 to go to main menu","yellow")
        while True:
            try:
                ch26 = int(input())
            except:
                cprint("Invalid Input Provided","yellow")
                cprint("Pleae input values between 1,2 and 3","yellow")
                continue
            if ch26 not in [1,2,3]:
                cprint("Invalid Input Provided","yellow")
                cprint("Pleae input values between 1,2 and 3","yellow")
                continue
            break
        if ch26 == 3:
            cprint("Re-directing to main-menu","cyan")
            
            break
        elif ch26 == 1:
            while True:
                cprint("Existing Tracks","blue")
                datadownload()
                updatedata()
                getdata()
                cprint("Enter Tracking Id to check Consignment","magenta")
                while True:
                    try:
                        tid = int(input())
                    except:
                        cprint("Invalid Input provided","yellow")
                        cprint("Please input the 8 digit tracking id provided while registering.","yellow")
                        continue
                    if len(str(tid)) != 8 :
                        cprint("Invalid Input provided","yellow")
                        cprint("Please input the 8 digit tracking id provided while registering.","yellow")
                        continue
                    break
                if str(tid) not in data["tracks"]:
                    cprint("Given Tracking ID not found in Database.","yellow")
                    cprint("Press 1 to re-enter Tracking ID","magenta")
                    cprint("Else Going to Previous Screen","cyan")
                    ch27 = input()
                    if ch27 == "1":
                        
                        continue
                    else:
                        cprint("Redirecting to previous screen","cyan")
                        
                        break
                else:
                    cprint("Details of Consignment","magenta")
                    pkg = data["tracks"][str(tid)]
                    cprint("Details of shipment with tracking ID "+str(tid),"magenta")
                    cprint("Package Weight : "+ str(pkg["pkgwt"]))
                    cprint("Dilevery Start Location : "+str(pkg["startlocation"]),"magenta")
                    cprint("Dilevery End Location : "+str(pkg["endlocation"]))
                    cprint("Current Location of Package : "+str(pkg["location"]),"magenta")
                    cprint("Price of package : "+str(pkg["price"]))
                    cprint("Courier Used : "+str(pkg["Courier Used"]),"magenta")
                    cprint("Registration Time : "+str(pkg["issuetime"]))
                    if pkg["location"] == pkg["endlocation"] :
                        cprint("Package Delivered to location.","green")
                    elif pkg["location"] == pkg["startlocation"]:
                        cprint("Package hasn't started delivery.","green")
                    cprint("Press 1 to check another tracking id","magenta")
                    cprint("Else going to previous screen","cyan")
                    ch28 = input()
                    if ch28 == "1":
                        
                        continue
                    else:
                        cprint("Redirecting to previous screen","cyan")
                        
                        break
        else:
            while True:
                cprint("Find the most suitable shipping service for you","green")
                cprint("Provide the details of the package","blue")
                while True:
                    try:
                        mass2 = float(input("Enter the mass of the package in kgs"))
                    except:
                        cprint("invalid Input provided","yellow")
                        cprint("Re-enter mass","yellow")
                        continue
                    if mass2 <= 0:
                        cprint("invalid Input provided","yellow")
                        cprint("Re-enter mass","yellow")
                        continue
                    break
                cprint("")
                cprint("Press Y for fast delivery","magenta")
                cprint("Press any other key for Normal Delivery","cyan")
                shipchoice = input()
                if shipchoice == 'y' or shipchoice == "Y":
                    x = "fast"
                    cprint("Fast delivery choosen","cyan")
                else:
                    x = "normal"
                    cprint("Normal Delivery Choosen","cyan")
                while True:
                    datadownload()
                    updatedata()
                    getdata()
                    locatdict = data["Locations"]
                    cprint("Choose start location","blue")
                    for i in range(1,len(locatdict["locid"])+1):
                        cprint("Press "+str(i)+" for "+str(locatdict["Name"][locatdict["locid"][i-1]]),"magenta")
                    while True:
                        try:
                            ch29 = int(input())
                        except:
                            cprint("Invalid Input given, please re-enter","yellow")
                            continue
                        if ch29 not in range(1,len(locatdict["locid"])+1):
                            cprint("Invalid Input Given, please re-enter","yellow")
                            continue
                        break
                    startid = locatdict["locid"][ch29 -1]
                    startlocation = locatdict["Name"][startid]
                    cprint("Start Location Choosen : "+startlocation,"magenta")
                    cprint("Choose Delivery Location","blue")
                    for i in range(1,len(locatdict["locid"])+1):
                        if locatdict["locid"][i-1] == startid:
                            continue
                        cprint("Press "+str(i)+" for "+str(locatdict["Name"][locatdict["locid"][i-1]]),"magenta")
                    while True:
                        try:
                            ch30 = int(input())
                        except:
                            cprint("Invalid Input given, please re-enter","yellow")
                            continue
                        if ch30 not in range(1,len(locatdict["locid"])+1) or locatdict["locid"][ch30-1] == startid:
                            cprint("Invalid Input Given, please re-enter","yellow")
                            continue
                        break
                    endid = locatdict["locid"][ch30-1]
                    endlocation = locatdict["Name"][endid]
                    cprint("Delivery Location Choosen : "+str(endlocation)+str(endid),"magenta")
                    cprint("To Confirm Choice Press 1","magenta")
                    cprint("To choose location again Press 2","blue")
                    while True:
                        try:
                            ch31 = int(input())
                        except:
                            cprint("You have entered Invalid Data","yellow")
                            cprint("Choose any option between 1 and 2","yellow")
                            continue
                        if ch31 not in [1,2]:
                            cprint("You have entered Invalid Data","yellow")
                            cprint("Choose any option between 1 and 2 ","yellow")
                            continue
                        break
                    if ch31 == 2:
                        cprint("Re-choosing Location","cyan")
                        continue
                    else:
                        break
                cprint("Delivery from "+startlocation+" to "+endlocation,"magenta")
                datadownload()
                updatedata()
                getdata()
                locdata = data["Locations"]["locdata"]
                startlocdata = locdata[startid]
                endlocdata = locdata[endid]
                kms = haversine.haversine(startlocdata,endlocdata)
                if mass2 <= 1 and mass2>0:
                    pid = "01"
                elif mass2 <= 5 and mass2>1:
                    pid = "15"
                elif mass2 <= 10 and mass2>5:
                    pid = "510"
                elif mass2>10:
                    pid = "100"
                if mass2 <= 10:
                    price_couriera = data["courier_prices"][x][pid]["startpricec1"] + (data["courier_prices"][x][pid]["pricekmc1"])*(kms/5)
                    price_courierb = data["courier_prices"][x][pid]["startpricec2"] + (data["courier_prices"][x][pid]["pricekmc2"])*(kms/5)
                    price_courierc = data["courier_prices"][x][pid]["startpricec3"] + (data["courier_prices"][x][pid]["pricekmc3"])*(kms/5)
                    price_courierd = data["courier_prices"][x][pid]["startpricec4"] + (data["courier_prices"][x][pid]["pricekmc4"])*(kms/5)
                else:
                    price_couriera = data["courier_prices"][x][pid]["startpricec1"] + (data["courier_prices"][x][pid]["pricekmc1"])*(kms/5)*(mass2 - 9)
                    price_courierb = data["courier_prices"][x][pid]["startpricec2"] + (data["courier_prices"][x][pid]["pricekmc2"])*(kms/5)*(mass2 - 9)
                    price_courierc = data["courier_prices"][x][pid]["startpricec3"] + (data["courier_prices"][x][pid]["pricekmc3"])*(kms/5)*(mass2 - 9)
                    price_courierd = data["courier_prices"][x][pid]["startpricec4"] + (data["courier_prices"][x][pid]["pricekmc4"])*(kms/5)*(mass2 - 9)
                cprint("")
                cprint("The prices provided by Courier Services for","blue")
                cprint(" Package of weight :"+ str(mass2),"magenta")
                cprint("From "+startlocation+" To "+endlocation,"magenta")
                cprint("Covering distance "+str(kms),"magenta")
                cprint("Courier Services","blue")
                cprint("Courier Service A :"+str(price_couriera),"magenta")
                cprint("Courier Service B :"+str(price_courierb),"magenta")
                cprint("Courier Service C :"+str(price_courierc),"magenta")
                cprint("Courier Service D :"+str(price_courierd),"magenta")
                cprint("Now you can choose the most suitable shipping service for you.","green")
                cprint("")
                print("For courier service A press 1","For courier service B press 2", sep ='\n')
                print("For courier service C press 3","For courier service D press 4", sep ='\n')
                k = input()
                while k == "" or (k != "1" and k != "A" and k != "a" and k != "2" and k != "B" and k != "b" and k != "3" and k != "C" and k != "c" and k != "4" and k != "D" and k != "d"):
                    cprint("Please enter a valid choice between a,b,c,d or 1,2,3,4","yellow")
                    k = input()
                cprint("")
                if k == "1" or k == "A" or k == "a":
                    cid = "c1"
                    price2 = price_couriera
                elif k == "2" or k == "b" or k == "B":
                    cid = "c2"
                    price2 = price_courierb
                elif k == "3" or k == "c" or k == "C":
                    cid = "c3"
                    price2 = price_courierc
                elif k == "4" or k == "d" or k == "D":
                    cid = "c4"
                    price2 = price_courierd
                cprint("Link to Courier"+str(data["couriers"][cid]),"magenta")
                urltext = data["courierurl"][cid]
                cprint(urltext)
                cprint("Press 1 to save this track","green")
                cprint("Else, going to Previous Screen","cyan")
                ch32 = input()
                if ch32 == "1":
                    pid2 = random.randint(10000000,99999999)
                    while pid2 in data["tracks"]:
                        pid2 = random.randint(10000000,99999999) 
                    cprint("courier Id : "+str(pid2),"magenta")
                    cprint("Note down this Courier Id for future reference.","yellow")
                    datadownload()
                    updatedata()
                    getdata()
                    trackdict2 = {}
                    trackdict2["issuetime"] = str(datetime.now())
                    trackdict2["pkgwt"] = str(mass2)
                    trackdict2["startlocation"] = str(startid)
                    trackdict2["endlocation"] = str(endid)
                    trackdict2["location"] = str(startid)
                    trackdict2["Courier Used"] = str(cid)
                    trackdict2["price"] = str(price2)
                    data["tracks"][str(pid2)] = trackdict2
                    updatedata()
                    dataupload()
                    datadownload()
                    updatedata()
                    getdata()
                    cprint("To check suitable prices for another package press 1","green")
                    cprint("else going to User Startup Screen","cyan")
                    ch33 = input()
                    if ch33 == "1":
                        continue
                    else:
                        
                        break
                else:
                    
                    break

#-------------------------------------------------------------------------------------------------------------#

#Authenticated Startup Function
def startup(mail):
    while True:
        datadownload()
        updatedata()
        getdata()
        cprint("+"+"-"*126+"+","blue","on_white")
        cprint("|"+" "*54 +"Welcome to ShipIt!" + " "*54+"|","blue","on_white")
        cprint("+"+"-"*126+"+","blue","on_white")     
        for i in data["users"]:
            if i["email"] == mail:
                userdict = i
                break
        cprint("Hello " +userdict["name"],"blue")
        cprint("Email Id : "+userdict["email"],"blue")
        cprint("To Check existing tracks press 1","magenta")
        cprint("To add new delivery press 2","magenta")
        cprint("To edit user details such as Name, E-mail id, password press 3","magenta")
        cprint("To log-out press 4","red")
        while True:
            try:
                ch11 = int(input())
            except:
                cprint("You have entered Invalid Data","yellow")
                cprint("Choose any option between 1,2,3 and 4","yellow")
                continue
            if ch11 not in [1,2,3,4]:
                cprint("You have entered Invalid Data","yellow")
                cprint("Choose any option between 1,2 and 3","yellow")
                continue
            break
        if ch11 == 4:
            
            break
        elif ch11 == 1:
            while True:
                cprint("Existing Tracks","blue")
                tracks = userdict["tracks"]
                if len(tracks) == 1:
                    cprint("There are no existing tracks, Going to user screen","yellow")
                    
                    break
                else:
                    cprint("Choose tracking id to check details :","blue")
                    for i in range(1,len(tracks)):
                        cprint(
                        "Press "+str(i)+" for "+ str(tracks[i])+" ( from "+
                        data["Locations"]["Name"][data["tracks"][tracks[i]]["startlocation"]]+
                        " to "+
                        data["Locations"]["Name"][data["tracks"][tracks[i]]["endlocation"]]+' ) ',"magenta" 
                        )
                    while True:
                        try:
                            ch12 = int(input())
                        except:
                            cprint("Invalid Input Provided please re-enter.","yellow")
                            cprint("Enter value between 1 to"+str(len(tracks)),"yellow")
                            continue
                        if ch12 not in range(1,len(tracks)+1):
                            cprint("Invalid Input Provided please re-enter.")
                            cprint("Enter value between 1 to"+str(len(tracks)),"yellow")
                            continue
                        break
                    trackid = ch12
                    print("Details of shipment with tracking ID",tracks[trackid])
                    print("Package Weight :",data["tracks"][tracks[trackid]]["pkgwt"])
                    print("Dilevery Start Location :",data["Locations"]["Name"][data["tracks"][tracks[trackid]]["startlocation"]])
                    print("Dilevery End Location :",data["Locations"]["Name"][data["tracks"][tracks[trackid]]["endlocation"]])
                    print("Current Location of Package :",data["Locations"]["Name"][data["tracks"][tracks[trackid]]["location"]])
                    print("Price of package : ",data["tracks"][tracks[trackid]]["price"])
                    print("Courier Used : ",data["couriers"][data["tracks"][tracks[trackid]]["Courier Used"]])
                    print("Registration Time : ",data["tracks"][tracks[trackid]]["issuetime"])
                    if data["tracks"][tracks[trackid]]["location"] == data["tracks"][tracks[trackid]]["endlocation"] :
                        cprint("Package Delivered to location.","green")
                    elif data["tracks"][tracks[trackid]]["location"] == data["tracks"][tracks[trackid]]["startlocation"]:
                        cprint("Package hasn't started delivery.","green")
                    cprint("To check another track press 1","magenta")
                    cprint("Else, Going Back to User Screen","cyan")
                    ch13 = input()
                    if ch13 == "1":
                        
                        continue
                    else:
                        
                        break
        elif ch11 == 2:
            while True:
                cprint("Let us find the most suitable shipping service for you!","magenta")
                cprint("Provide the details of the package","blue")
                while True:
                    try:
                        mass = float(input("Enter the mass of the package to be delivered in kgs."))
                    except:
                        cprint("You have entered an invalid data. Please re-enter.","yellow")
                        cprint("")
                        continue
                    if mass <= 0:
                        cprint("You have entered an invalid data. Please re-enter.","yellow")
                        cprint("")
                        continue
                    break
                cprint("")
                cprint("Press Y for fast delivery","magenta")
                cprint("Else Press any other key","magenta")
                ship_choice = input()
                if ship_choice == 'y' or ship_choice == "Y":
                    x = "fast"
                    cprint("Fast Delivery choosen","green")
                else:
                    x = "normal"
                    cprint('Normal Delivery chosen',"green")
                while True:
                    datadownload()
                    updatedata()
                    getdata()
                    locatdict = data["Locations"]
                    cprint("Choose start location","blue")
                    for i in range(1,len(locatdict["locid"])+1):
                        print("Press",i,"for",locatdict["Name"][locatdict["locid"][i-1]])
                    while True:
                        try:
                            ch14 = int(input())
                        except:
                            cprint("Invalid Input given, please re-enter","yellow")
                            continue
                        if ch14 not in range(1,len(locatdict["locid"])+1):
                            cprint("Invalid Input Given, please re-enter","yellow")
                            continue
                        break
                    startid = locatdict["locid"][ch14-1]
                    startlocation = locatdict["Name"][startid]
                    cprint("Start Location Choosen : "+startlocation+" "+str(startid),"green")
                    cprint("Choose Delivery Location","blue")
                    for i in range(1,len(locatdict["locid"])+1):
                        if locatdict["locid"][i-1] == startid:
                            continue
                        print("Press",i,"for",locatdict["Name"][locatdict["locid"][i-1]])
                    while True:
                        try:
                            ch15 = int(input())
                        except:
                            cprint("Invalid Input given, please re-enter","yellow")
                            continue
                        if ch15 not in range(1,len(locatdict["locid"])+1) or locatdict["locid"][ch15-1] == startid:
                            cprint("Invalid Input Given, please re-enter","yellow")
                            continue
                        break
                    endid = locatdict["locid"][ch15-1]
                    endlocation = locatdict["Name"][endid]
                    cprint("Delivery Location Choosen : "+endlocation+" "+str(endid),"green")
                    cprint("To Confirm Choice Press 1","green")
                    cprint("To choose location again Press 2","magenta")
                    while True:
                        try:
                            ch16 = int(input())
                        except:
                            cprint("You have entered Invalid Data","yellow")
                            cprint("Choose any option between 1 and 2","yellow")
                            continue
                        if ch16 not in [1,2]:
                            cprint("You have entered Invalid Data","yellow")
                            cprint("Choose any option between 1,2 and 3","yellow")
                            continue
                        break
                    if ch16 == 2:
                        cprint("Re-choosing Location","cyan")
                        continue
                    else:
                        break
                cprint("Delivery from "+startlocation+" to "+endlocation,"green")
                datadownload()
                updatedata()
                getdata()
                locdata = data["Locations"]["locdata"]
                startlocdata = locdata[startid]
                endlocdata = locdata[endid]
                kms = haversine.haversine(startlocdata,endlocdata)
                if mass <= 1 and mass>0:
                    pid = "01"
                elif mass <= 5 and mass>1:
                    pid = "15"
                elif mass <= 10 and mass>5:
                    pid = "510"
                elif mass>10:
                    pid = "100"
                if mass <= 10:
                    price_couriera = data["courier_prices"][x][pid]["startpricec1"] + (data["courier_prices"][x][pid]["pricekmc1"])*(kms/5)
                    price_courierb = data["courier_prices"][x][pid]["startpricec2"] + (data["courier_prices"][x][pid]["pricekmc2"])*(kms/5)
                    price_courierc = data["courier_prices"][x][pid]["startpricec3"] + (data["courier_prices"][x][pid]["pricekmc3"])*(kms/5)
                    price_courierd = data["courier_prices"][x][pid]["startpricec4"] + (data["courier_prices"][x][pid]["pricekmc4"])*(kms/5)
                else:
                    price_couriera = data["courier_prices"][x][pid]["startpricec1"] + (data["courier_prices"][x][pid]["pricekmc1"])*(kms/5)*(mass - 9)
                    price_courierb = data["courier_prices"][x][pid]["startpricec2"] + (data["courier_prices"][x][pid]["pricekmc2"])*(kms/5)*(mass - 9)
                    price_courierc = data["courier_prices"][x][pid]["startpricec3"] + (data["courier_prices"][x][pid]["pricekmc3"])*(kms/5)*(mass - 9)
                    price_courierd = data["courier_prices"][x][pid]["startpricec4"] + (data["courier_prices"][x][pid]["pricekmc4"])*(kms/5)*(mass - 9)
                cprint("")
                cprint("The prices provided by Courier Services for","blue")
                cprint(" Package of weight :"+str( mass),"magenta")
                cprint("From " + startlocation+" To "+endlocation,"magenta")
                cprint("Covering distance"+str(kms),"magenta")
                cprint("Courier Services","blue")
                print("Courier Service A :",price_couriera)
                print("Courier Service B :",price_courierb)
                print("Courier Service C :",price_courierc)
                print("Courier Service D :",price_courierd)
                cprint("Now you can choose the most suitable shipping service for you.","green")
                cprint("")
                print("For courier service A press 1","For courier service B press 2", sep ='\n')
                print("For courier service C press 3","For courier service D press 4", sep ='\n')
                k = input()
                while k == "" or (k != "1" and k != "A" and k != "a" and k != "2" and k != "B" and k != "b" and k != "3" and k != "C" and k != "c" and k != "4" and k != "D" and k != "d"):
                    cprint("Please enter a valid choice between a,b,c,d or 1,2,3,4","yellow")
                    k = input()
                cprint("")
                if k == "1" or k == "A" or k == "a":
                    cid = "c1"
                    price = price_couriera
                elif k == "2" or k == "b" or k == "B":
                    cid = "c2"
                    price = price_courierb
                elif k == "3" or k == "c" or k == "C":
                    cid = "c3"
                    price = price_courierc
                elif k == "4" or k == "d" or k == "D":
                    cid = "c4"
                    price = price_courierd
                cprint("Link to Courier"+data["couriers"][cid],"green")
                urltext = data["courierurl"][cid]
                cprint(urltext)
                cprint("To save this track to your account press 1","green")
                cprint("else going to User Screen","cyan")
                ch17 = input()
                if ch17 == "1":
                    pid = random.randint(10000000,99999999)
                    while pid in data["tracks"]:
                        pid = random.randint(10000000,99999999) 
                    cprint("courier Id : "+str(pid))
                    datadownload()
                    updatedata()
                    getdata()
                    trackdict = {}
                    trackdict["issuetime"] = str(datetime.now())
                    trackdict["pkgwt"] = str(mass)
                    trackdict["startlocation"] = str(startid)
                    trackdict["endlocation"] = str(endid)
                    trackdict["location"] = str(startid)
                    trackdict["Courier Used"] = str(cid)
                    trackdict["price"] = str(price)
                    for i in data["users"]:
                        if i["email"] == userdict["email"]:
                            i["tracks"].append(str(pid))
                    data["tracks"][str(pid)] = trackdict
                    updatedata()
                    dataupload()
                    datadownload()
                    updatedata()
                    getdata()
                    cprint("To check suitable prices for another package press 1","green")
                    cprint("else going to User Startup Screen","cyan")
                    ch18 = input()
                    if ch18 == "1":
                        
                        continue
                    else:
                        
                        break
                else:
                    cprint("Re-directing to User Screen","cyan")
                    
                    break
        else:
            while True:
                datadownload()
                updatedata()
                getdata()
                for i in data["users"]:
                    if i["email"] == mail:
                        userdict = i
                        break
                cprint("Editing User Details","yellow")
                cprint("Press 1 to edit UserName","magenta")
                cprint("Press 2 to edit Mail Id","magenta")
                cprint("Press 3 to edit Password","magenta")
                cprint("Press 4 to go to User Screen","yellow")
                while True:
                    try:
                        ch19 = int(input())
                    except:
                        cprint("Invalid Input Provided","yellow")
                        cprint("Enter a value between 1 to 4","yellow")
                        continue
                    if ch19 not in [1,2,3,4]:
                        cprint("Invalid Input Provided","yellow")
                        cprint("Enter a value between 1 to 4","yellow")
                        continue
                    break
                if ch19 == 4:
                    cprint("Redirecting to User Screen","cyan")
                    break
                elif ch19 == 1:
                    while True:
                        datadownload()
                        updatedata()
                        getdata()
                        for i in data["users"]:
                            if i["email"] == mail:
                                userdict = i
                                break
                        cprint("Editing Username","blue")
                        cprint("Current Username : "+ userdict["name"],"magenta")
                        newname = input("Enter new Username : ")
                        cprint("You entered "+newname+" as your new Username.","magenta")
                        cprint("To confirm Press 1","yellow")
                        cprint("To re-enter press 2","magenta")
                        cprint("To go back press 3","yellow")
                        while True:
                            try:
                                ch20 = int(input())
                            except:
                                cprint("Invalid Input provided","yellow")
                                cprint("Please enter any value between 1,2 and 3","yellow")
                                continue
                            if ch20 not in [1,2,3]:
                                cprint("Invalid Input provided","yellow")
                                cprint("Please enter any value between 1,2 and 3","yellow")
                                continue
                            break
                        if ch20 == 3:
                            
                            break
                        elif ch20 == 2:
                            
                            continue
                        else:
                            userdict["name"] = newname
                            for i in range (0,len(data["users"])):
                                if data["users"][i]["uid"] == userdict["uid"]:
                                    data["users"][i] = userdict
                                    break
                            updatedata()
                            dataupload()
                            datadownload()
                            getdata()
                            cprint("Username changed to "+newname,"green")
                            cprint("To change username again press 1","magenta")
                            cprint("Else going back","cyan")
                            ch21 = input()
                            if ch21 == "1":
                                continue
                            else:
                                cprint("Going to Edit User Section...","cyan")
                                
                                break
                elif ch19 == 2:
                    while True:
                        datadownload()
                        updatedata()
                        getdata()
                        for i in data["users"]:
                            if i["email"] == mail:
                                userdict = i
                                break
                        cprint("Editing Email Address","blue")
                        cprint("Current email : "+ userdict["email"],"magenta")
                        newmail = input("Enter new email address : ")
                        cprint("You entered "+newmail+" as your new email address.","magenta")
                        cprint("To confirm Press 1","yellow")
                        cprint("To re-enter press 2","magenta")
                        cprint("To go back press 3","yellow")
                        while True:
                            try:
                                ch22 = int(input())
                            except:
                                cprint("Invalid Input provided","yellow")
                                cprint("Please enter any value between 1,2 and 3","yellow")
                                continue
                            if ch22 not in [1,2,3]:
                                cprint("Invalid Input provided","yellow")
                                cprint("Please enter any value between 1,2 and 3","yellow")
                                continue
                            break
                        if ch22 == 3:
                            
                            break
                        elif ch22 == 2:
                            
                            continue
                        else:
                            userdict["email"] = newmail
                            for i in range (0,len(data["users"])):
                                if data["users"][i]["uid"] == userdict["uid"]:
                                    data["users"][i] = userdict
                                    break
                            updatedata()
                            dataupload()
                            datadownload()
                            getdata()
                            cprint("Email-address changed to "+newmail,"green")
                            cprint("To change email again press 1","magenta")
                            cprint("Else going back","cyan")
                            ch23 = input()
                            if ch23 == "1":
                                continue
                            else:
                                cprint("Going to Edit User Section...","cyan")
                                
                                break
                else:
                    while True:
                        datadownload()
                        updatedata()
                        getdata()
                        for i in data["users"]:
                            if i["email"] == mail:
                                userdict = i
                                break
                        cprint("Editing Password","blue")
                        cprint("Current Password : "+ userdict["pwd"],"magenta")
                        newpwd = input("Enter new password : ")
                        cprint("You entered "+ newpwd+" as your new password.","magenta")
                        cprint("To confirm Press 1","yellow")
                        cprint("To re-enter press 2","magenta")
                        cprint("To go back press 3","yellow")
                        while True:
                            try:
                                ch24 = int(input())
                            except:
                                cprint("Invalid Input provided","yellow")
                                cprint("Please enter any value between 1,2 and 3","yellow")
                                continue
                            if ch24 not in [1,2,3]:
                                cprint("Invalid Input provided","yellow")
                                cprint("Please enter any value between 1,2 and 3","yellow")
                                continue
                            break
                        if ch24 == 3:
                            
                            break
                        elif ch24 == 2:
                            continue
                        else:
                            userdict["pwd"] = newpwd
                            for i in range (0,len(data["users"])):
                                if data["users"][i]["uid"] == userdict["uid"]:
                                    data["users"][i] = userdict
                                    break
                            updatedata()
                            dataupload()
                            datadownload()
                            getdata()
                            cprint("Password changed to "+newpwd,"green")
                            cprint("To change password again press 1","magenta")
                            cprint("Else going back","cyan")
                            ch25 = input()
                            if ch25 == "1":
                                
                                continue
                            else:
                                cprint("Going to Edit User Section...","cyan")
                                
                                break

#-------------------------------------------------------------------------------------------------------------#

#Login Function
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
                    ch7 = int(input())
                except:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1,2 and 3","yellow")
                    continue
                if ch7 not in [1,2,3]:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1,2 and 3","yellow")
                break
            if ch7 == 3:
                flag2 = True
                break
            elif ch7 == 2:
                continue
            elif not checkmailexist(mail):
                cprint("Provided E-mail doesn't exist in database.","yellow")
                cprint("To re-enter email press 1","magenta")
                cprint("To register press 2","magenta")
                while True:
                    try:
                        ch8 = int(input())
                    except:
                        cprint("You have entered Invalid Data","yellow")
                        cprint("Choose any option between 1 and 2","yellow")
                        continue
                    if ch8 not in [1,2]:
                        cprint("You have entered Invalid Data","yellow")
                        cprint("Choose any option between 1 and 2","yellow")
                        continue
                    break
                if ch8 == 1:
                    continue
                else:
                    signup()
                    flag2 = True
                    break
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
                    ch9 = int(input())
                except:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1,2 and 3","yellow")
                    continue
                if ch9 not in [1,2,3]:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1,2 and 3","yellow")
                    continue
                break
            if ch9 == 3:
                flag2 = True
                break
            elif ch9 == 2:
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
                    ch10 = int(input())
                except :
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1 and 2","yellow")
                    continue
                if ch10 not in [1,2]:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1,2 and 3","yellow")
                    continue
                break
            if ch10 == 1:
                continue
            else:
                break

#-------------------------------------------------------------------------------------------------------------#

#SignUp Function
def signup():
    flag1 = False
    maildone,pwdone,namedone = False,False,False
    cprint("-"*128,"blue","on_white")
    cprint(" "*57 + "Sign-Up Screen" + " "*57,"blue","on_white" )
    cprint("-"*128,"blue","on_white")
    while maildone == False and flag1 == False:
        cprint("Enter E-mail ID to register into ShipIt","blue")
        regmail = input("Mail ID : ")
        cprint("You entered "+regmail+" as your email ID","blue")
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
            flag1 = True
            break
        elif ch3 == 2:
            continue
        elif checkmailexist(regmail):
            cprint("Entered e-mail address already exists","green")
            cprint("To Login Press 1","magenta")
            cprint("To re-enter mail id Press 2","magenta")
            while True:
                try:
                    ch4 = int(input())
                except:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1 and 2","yellow")
                    continue
                if ch4 not in [1,2]:
                    cprint("You have entered Invalid Data","yellow")
                    cprint("Choose any option between 1 and 2","yellow")
                    continue
                break
            if ch4 == 1:
                cprint("Going to Login Screen...","cyan")
                login()
                break
            else:
                continue
        elif checkvalid(regmail):
            maildone = True
            break
        else:
            cprint("Entered e-mail Id is invalid.","red")
            continue
    while pwdone == False and flag1 == False and maildone == True:
        cprint("Enter Password","blue")
        pwd = input("Password : ")
        cprint("You entered "+pwd+" as your password","blue")
        cprint("To continue Press 1","magenta")
        cprint("To re-enter press 2","magenta")
        cprint("To go-back to main-screen press 3","yellow")
        while True:
            try:
                ch5 = int(input())
            except:
                cprint("You have entered Invalid Data","yellow")
                cprint("Choose any option between 1,2 and 3","yellow")
                continue
            if ch5 not in [1,2,3]:
                cprint("You have entered Invalid Data","yellow")
                cprint("Choose any option between 1,2 and 3","yellow")
                continue
            break
        if ch5 == 3:
            flag1 = True
            break
        elif ch5 == 2:
            continue
        else:
            pwdone = True
            break
    while namedone == False and flag1 == False and maildone == True and pwdone == True:
        cprint("Enter Username","blue")
        name = input("Name : ")
        cprint("You entered "+name+" as your name","blue")
        cprint("To continue Press 1","magenta")
        cprint("To re-enter press 2","magenta")
        cprint("To go-back to main-screen press 3","yellow")
        while True:
            try:
                ch6 = int(input())
            except:
                cprint("You have entered Invalid Data","yellow")
                cprint("Choose any option between 1,2 and 3","yellow")
                continue
            if ch6 not in [1,2,3]:
                cprint("You have entered Invalid Data","yellow")
                cprint("Choose any option between 1,2 and 3","yellow")
                continue
            break
        if ch6 == 3:
            flag1 = True
            break
        elif ch6 == 2:
            continue
        else:
            namedone = True
            break
    if namedone == True and pwdone == True and maildone == True and flag1 == False:
        cprint("Please Wait.....","cyan")
        datadownload()
        updatedata()
        getdata()
        l = []
        for i in data["users"]:
            l.append(i["uid"])
        uid = random.randint(10000,99999)
        while uid in l:
            uid = random.randint(10000,99999)
        del l

        data["users"].append({"name":name,"email":regmail,"pwd":pwd,"tracks":["00000000"],"uid":uid})
        updatedata()
        dataupload()    
        getdata()
        cprint("Registration Complete with","green")
        cprint("Name :"+name,"cyan")
        cprint("E-mail : "+ regmail,"cyan")
        cprint("Password : "+pwd,"cyan")
        cprint("Please Note the ID and passwd","yellow")

#-------------------------------------------------------------------------------------------------------------#

#Main Loop
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
    cprint("To Surf Anonmously press 2","magenta")
    cprint("To SignUp press 3","magenta")
    cprint("To End Session press 4","red")
    cprint("If encountering issues, contact","cyan",end="")
    cprint(" roshanbiswanathpatra@gmail.com","blue")
    while True:
        try:
            ch1 = int(input())
        except:
            cprint("You have entered invalid data","yellow")
            continue
        if ch1 not in [1,2,3,4]:
            cprint("Enter suitable value from 1,2 or 3","yellow")
            continue
        break
    if ch1 == 1:
        login()
    elif ch1 == 2:
        startupano()
    elif ch1 == 123:
        break
    elif ch1 == 3:
        signup()
    elif ch1 == 4:
        break
    cprint("To end session enter N else continue","red")
    ch2 = input()
    if ch2 in ["N","n"]:
        cprint("Program Terminated","red")
        break
    cprint("Please Wait.....","cyan")
    

#-------------------------------------------------------------------------------------------------------------#

#About US
aboutus()

#-------------------------------------------------------------------------------------------------------------#

#Exit Loop
while True:
    cprint("To exit press q","red")
    q = input()
    if q == "q" or q == "Q":
        break

#-------------------------------------------------------------------------------------------------------------#

subprocess.call(["python.exe",  currentpath + "/main.py"])

#-------------------------------------------------------------------------------------------------------------#