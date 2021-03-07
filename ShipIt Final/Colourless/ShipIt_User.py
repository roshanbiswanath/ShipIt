#Packages
import json, re, os, haversine , random, requests, sys, subprocess
from datetime import datetime

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
    print()
    print("-="*64)
    print(" "*60 + "ABOUT US" + " "*60)
    print("-="*64)
    print()
    print("Thanks For using our Service, here is our About Us section:")
    print()
    print("We are ShipIt!, a service that aims to help you choose the best shipping service for you.")
    print("The Developer:")
    print("P.Biswanath Patra")
    print("XII - A, Kendriya Vidyalaya, BAM")
    print("For social data:")
    print("@roshanbiswanath")
    print("roshanbiswanathpatra@gmail.com")

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
        print("-"*128)
        print("|"+" "*54 +"Welcome to ShipIt!" + " "*54+"|")
        print("-"*128)
        print()
        print("Hello User")
        print("Press 1 to check existing tracks")
        print("Press 2 to find suitable delivery service")
        print("Press 3 to go to main menu")
        while True:
            try:
                ch26 = int(input())
            except:
                print("Invalid Input Provided")
                print("Pleae input values between 1,2 and 3")
                continue
            if ch26 not in [1,2,3]:
                print("Invalid Input Provided")
                print("Pleae input values between 1,2 and 3")
                continue
            break
        if ch26 == 3:
            print("Re-directing to main-menu")
            
            break
        elif ch26 == 1:
            while True:
                print("Existing Tracks")
                datadownload()
                updatedata()
                getdata()
                print("Enter Tracking Id to check Consignment")
                while True:
                    try:
                        tid = int(input())
                    except:
                        print("Invalid Input provided")
                        print("Please input the 8 digit tracking id provided while registering.")
                        continue
                    if len(str(tid)) != 8 :
                        print("Invalid Input provided")
                        print("Please input the 8 digit tracking id provided while registering.")
                        continue
                    break
                if str(tid) not in data["tracks"]:
                    print("Given Tracking ID not found in Database.")
                    print("Press 1 to re-enter Tracking ID")
                    print("Else Going to Previous Screen")
                    ch27 = input()
                    if ch27 == "1":
                        
                        continue
                    else:
                        print("Redirecting to previous screen")
                        
                        break
                else:
                    print("Details of Consignment")
                    pkg = data["tracks"][str(tid)]
                    print("Details of shipment with tracking ID",str(tid))
                    print("Package Weight :",pkg["pkgwt"])
                    print("Dilevery Start Location :",pkg["startlocation"])
                    print("Dilevery End Location :",pkg["endlocation"])
                    print("Current Location of Package :",pkg["location"])
                    print("Price of package : ",pkg["price"])
                    print("Courier Used : ",pkg["Courier Used"])
                    print("Registration Time : ",pkg["issuetime"])
                    if pkg["location"] == pkg["endlocation"] :
                        print("Package Delivered to location.")
                    elif pkg["location"] == pkg["startlocation"]:
                        print("Package hasn't started delivery.")
                    print("Press 1 to check another tracking id")
                    print("Else going to previous screen")
                    ch28 = input()
                    if ch28 == "1":
                        
                        continue
                    else:
                        print("Redirecting to previous screen")
                        
                        break
        else:
            while True:
                print("Find the most suitable shipping service for you")
                print("Provide the details of the package")
                while True:
                    try:
                        mass2 = float(input("Enter the mass of the package in kgs"))
                    except:
                        print("invalid Input provided")
                        print("Re-enter mass")
                        continue
                    if mass2 <= 0:
                        print("invalid Input provided")
                        print("Re-enter mass")
                        continue
                    break
                print()
                print("Press Y for fast delivery")
                print("Press any other key for Normal Delivery")
                shipchoice = input()
                if shipchoice == 'y' or shipchoice == "Y":
                    x = "fast"
                    print("Fast delivery choosen")
                else:
                    x = "normal"
                    print("Normal Delivery Choosen")
                while True:
                    datadownload()
                    updatedata()
                    getdata()
                    locatdict = data["Locations"]
                    print("Choose start location")
                    for i in range(1,len(locatdict["locid"])+1):
                        print("Press",i,"for",locatdict["Name"][locatdict["locid"][i-1]])
                    while True:
                        try:
                            ch29 = int(input())
                        except:
                            print("Invalid Input given, please re-enter")
                            continue
                        if ch29 not in range(1,len(locatdict["locid"])+1):
                            print("Invalid Input Given, please re-enter")
                            continue
                        break
                    startid = locatdict["locid"][ch29 -1]
                    startlocation = locatdict["Name"][startid]
                    print("Start Location Choosen : ",startlocation)
                    print("Choose Delivery Location")
                    for i in range(1,len(locatdict["locid"])+1):
                        if locatdict["locid"][i-1] == startid:
                            continue
                        print("Press",i,"for",locatdict["Name"][locatdict["locid"][i-1]])
                    while True:
                        try:
                            ch30 = int(input())
                        except:
                            print("Invalid Input given, please re-enter")
                            continue
                        if ch30 not in range(1,len(locatdict["locid"])+1) or locatdict["locid"][ch30-1] == startid:
                            print("Invalid Input Given, please re-enter")
                            continue
                        break
                    endid = locatdict["locid"][ch30-1]
                    endlocation = locatdict["Name"][endid]
                    print("Delivery Location Choosen : ",endlocation,endid)
                    print("To Confirm Choice Press 1")
                    print("To choose location again Press 2")
                    while True:
                        try:
                            ch31 = int(input())
                        except:
                            print("You have entered Invalid Data")
                            print("Choose any option between 1 and 2")
                            continue
                        if ch31 not in [1,2]:
                            print("You have entered Invalid Data")
                            print("Choose any option between 1 and 2 ")
                            continue
                        break
                    if ch31 == 2:
                        print("Re-choosing Location")
                        continue
                    else:
                        break
                print("Delivery from",startlocation,"to",endlocation)
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
                print()
                print("The prices provided by Courier Services for")
                print(" Package of weight :", mass2)
                print("From ",startlocation,"To",endlocation)
                print("Covering distance",kms)
                print("Courier Services")
                print("Courier Service A :",price_couriera)
                print("Courier Service B :",price_courierb)
                print("Courier Service C :",price_courierc)
                print("Courier Service D :",price_courierd)
                print("Now you can choose the most suitable shipping service for you.")
                print()
                print("For courier service A press 1","For courier service B press 2", sep ='\n')
                print("For courier service C press 3","For courier service D press 4", sep ='\n')
                k = input()
                while k == "" or (k != "1" and k != "A" and k != "a" and k != "2" and k != "B" and k != "b" and k != "3" and k != "C" and k != "c" and k != "4" and k != "D" and k != "d"):
                    print("Please enter a valid choice between a,b,c,d or 1,2,3,4")
                    k = input()
                print()
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
                print("Link to Courier",data["couriers"][cid])
                urltext = data["courierurl"][cid]
                print(urltext)
                print("Press 1 to save this track")
                print("Else, going to Previous Screen")
                ch32 = input()
                if ch32 == "1":
                    pid2 = random.randint(10000000,99999999)
                    while pid2 in data["tracks"]:
                        pid2 = random.randint(10000000,99999999) 
                    print("courier Id :",pid2)
                    print("Note down this Courier Id for future reference.")
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
                    print("To check suitable prices for another package press 1")
                    print("else going to User Startup Screen")
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
        print("+"+"-"*126+"+")
        print("|"+" "*53 +"Welcome to ShipIt!" + " "*53+"|")
        print("+"+"-"*126+"+")     
        for i in data["users"]:
            if i["email"] == mail:
                userdict = i
                break
        print("Hello" ,userdict["name"])
        print("Email Id :",userdict["email"])
        print("To Check existing tracks press 1")
        print("To add new delivery press 2")
        print("To edit user details such as Name, E-mail id, password press 3")
        print("To log-out press 4")
        while True:
            try:
                ch11 = int(input())
            except:
                print("You have entered Invalid Data")
                print("Choose any option between 1,2,3 and 4")
                continue
            if ch11 not in [1,2,3,4]:
                print("You have entered Invalid Data")
                print("Choose any option between 1,2 and 3")
                continue
            break
        if ch11 == 4:
            
            break
        elif ch11 == 1:
            while True:
                print("Existing Tracks")
                tracks = userdict["tracks"]
                if len(tracks) == 1:
                    print("There are no existing tracks, Going to user screen")
                    
                    break
                else:
                    print("Choose tracking id to check details :")
                    for i in range(1,len(tracks)):
                        print(
                        "Press",i,"for",tracks[i],"( from",
                        data["Locations"]["Name"][data["tracks"][tracks[i]]["startlocation"]],
                        "to",
                        data["Locations"]["Name"][data["tracks"][tracks[i]]["endlocation"]],')' 
                        )
                    while True:
                        try:
                            ch12 = int(input())
                        except:
                            print("Invalid Input Provided please re-enter.")
                            print("Enter value between 1 to",len(tracks))
                            continue
                        if ch12 not in range(1,len(tracks)+1):
                            print("Invalid Input Provided please re-enter.")
                            print("Enter value between 1 to",len(tracks))
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
                        print("Package Delivered to location.")
                    elif data["tracks"][tracks[trackid]]["location"] == data["tracks"][tracks[trackid]]["startlocation"]:
                        print("Package hasn't started delivery.")
                    print("To check another track press 1")
                    print("Else, Going Back to User Screen")
                    ch13 = input()
                    if ch13 == "1":
                        
                        continue
                    else:
                        
                        break
        elif ch11 == 2:
            while True:
                print("Let us find the most suitable shipping service for you!")
                print("Provide the details of the package")
                while True:
                    try:
                        mass = float(input("Enter the mass of the package to be delivered in kgs."))
                    except:
                        print("You have entered an invalid data. Please re-enter.")
                        print()
                        continue
                    if mass <= 0:
                        print("You have entered an invalid data. Please re-enter.")
                        print()
                        continue
                    break
                print()
                print("Press Y for fast delivery")
                print("Else Press any other key")
                ship_choice = input()
                if ship_choice == 'y' or ship_choice == "Y":
                    x = "fast"
                    print("Fast Delivery choosen")
                else:
                    x = "normal"
                    print('Normal Delivery chosen')
                while True:
                    datadownload()
                    updatedata()
                    getdata()
                    locatdict = data["Locations"]
                    print("Choose start location")
                    for i in range(1,len(locatdict["locid"])+1):
                        print("Press",i,"for",locatdict["Name"][locatdict["locid"][i-1]])
                    while True:
                        try:
                            ch14 = int(input())
                        except:
                            print("Invalid Input given, please re-enter")
                            continue
                        if ch14 not in range(1,len(locatdict["locid"])+1):
                            print("Invalid Input Given, please re-enter")
                            continue
                        break
                    startid = locatdict["locid"][ch14-1]
                    startlocation = locatdict["Name"][startid]
                    print("Start Location Choosen : ",startlocation)
                    print("Choose Delivery Location")
                    for i in range(1,len(locatdict["locid"])+1):
                        if locatdict["locid"][i-1] == startid:
                            continue
                        print("Press",i,"for",locatdict["Name"][locatdict["locid"][i-1]])
                    while True:
                        try:
                            ch15 = int(input())
                        except:
                            print("Invalid Input given, please re-enter")
                            continue
                        if ch15 not in range(1,len(locatdict["locid"])+1) or locatdict["locid"][ch15-1] == startid:
                            print("Invalid Input Given, please re-enter")
                            continue
                        break
                    endid = locatdict["locid"][ch15-1]
                    endlocation = locatdict["Name"][endid]
                    print("Delivery Location Choosen : ",endlocation,endid)
                    print("To Confirm Choice Press 1")
                    print("To choose location again Press 2")
                    while True:
                        try:
                            ch16 = int(input())
                        except:
                            print("You have entered Invalid Data")
                            print("Choose any option between 1 and 2")
                            continue
                        if ch16 not in [1,2]:
                            print("You have entered Invalid Data")
                            print("Choose any option between 1,2 and 3")
                            continue
                        break
                    if ch16 == 2:
                        print("Re-choosing Location")
                        continue
                    else:
                        break
                print("Delivery from",startlocation,"to",endlocation)
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
                print()
                print("The prices provided by Courier Services for")
                print(" Package of weight :", mass)
                print("From ",startlocation,"To",endlocation)
                print("Covering distance",kms)
                print("Courier Services")
                print("Courier Service A :",price_couriera)
                print("Courier Service B :",price_courierb)
                print("Courier Service C :",price_courierc)
                print("Courier Service D :",price_courierd)
                print("Now you can choose the most suitable shipping service for you.")
                print()
                print("For courier service A press 1","For courier service B press 2", sep ='\n')
                print("For courier service C press 3","For courier service D press 4", sep ='\n')
                k = input()
                while k == "" or (k != "1" and k != "A" and k != "a" and k != "2" and k != "B" and k != "b" and k != "3" and k != "C" and k != "c" and k != "4" and k != "D" and k != "d"):
                    print("Please enter a valid choice between a,b,c,d or 1,2,3,4")
                    k = input()
                print()
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
                print("Link to Courier",data["couriers"][cid])
                urltext = data["courierurl"][cid]
                print(urltext)
                print("To save this track to your account press 1")
                print("else going to User Screen")
                ch17 = input()
                if ch17 == "1":
                    pid = random.randint(10000000,99999999)
                    while pid in data["tracks"]:
                        pid = random.randint(10000000,99999999) 
                    print("courier Id :",pid)
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
                    print("To check suitable prices for another package press 1")
                    print("else going to User Startup Screen")
                    ch18 = input()
                    if ch18 == "1":
                        
                        continue
                    else:
                        
                        break
                else:
                    print("Re-directing to User Screen")
                    
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
                print("Editing User Details")
                print("Press 1 to edit UserName")
                print("Press 2 to edit Mail Id")
                print("Press 3 to edit Password")
                print("Press 4 to got to User Screen")
                while True:
                    try:
                        ch19 = int(input())
                    except:
                        print("Invalid Input Provided")
                        print("Enter a value between 1 to 4")
                        continue
                    if ch19 not in [1,2,3,4]:
                        print("Invalid Input Provided")
                        print("Enter a value between 1 to 4")
                        continue
                    break
                if ch19 == 4:
                    print("Redirecting to User Screen")
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
                        print("Editing Username")
                        print("Current Username : ", userdict["name"])
                        newname = input("Enter new Username : ")
                        print("You entered",newname,"as your new Username.")
                        print("To confirm Press 1")
                        print("To re-enter press 2")
                        print("To go back press 3")
                        while True:
                            try:
                                ch20 = int(input())
                            except:
                                print("Invalid Input provided")
                                print("Please enter any value between 1,2 and 3")
                                continue
                            if ch20 not in [1,2,3]:
                                print("Invalid Input provided")
                                print("Please enter any value between 1,2 and 3")
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
                            print("Username changed to ",newname)
                            print("To change username again press 1")
                            print("Else going back")
                            ch21 = input()
                            if ch21 == "1":
                                continue
                            else:
                                print("Going to Edit User Section...")
                                
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
                        print("Editing Email Address")
                        print("Current email : ", userdict["email"])
                        newmail = input("Enter new email address : ")
                        print("You entered",newmail,"as your new email address.")
                        print("To confirm Press 1")
                        print("To re-enter press 2")
                        print("To go back press 3")
                        while True:
                            try:
                                ch22 = int(input())
                            except:
                                print("Invalid Input provided")
                                print("Please enter any value between 1,2 and 3")
                                continue
                            if ch22 not in [1,2,3]:
                                print("Invalid Input provided")
                                print("Please enter any value between 1,2 and 3")
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
                            print("Email-address changed to ",newmail)
                            print("To change email again press 1")
                            print("Else going back")
                            ch23 = input()
                            if ch23 == "1":
                                continue
                            else:
                                print("Going to Edit User Section...")
                                
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
                        print("Editing Password")
                        print("Current Password : ", userdict["pwd"])
                        newpwd = input("Enter new password : ")
                        print("You entered",newpwd,"as your new password.")
                        print("To confirm Press 1")
                        print("To re-enter press 2")
                        print("To go back press 3")
                        while True:
                            try:
                                ch24 = int(input())
                            except:
                                print("Invalid Input provided")
                                print("Please enter any value between 1,2 and 3")
                                continue
                            if ch24 not in [1,2,3]:
                                print("Invalid Input provided")
                                print("Please enter any value between 1,2 and 3")
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
                            print("Password changed to ",newpwd)
                            print("To change password again press 1")
                            print("Else going back")
                            ch25 = input()
                            if ch25 == "1":
                                
                                continue
                            else:
                                print("Going to Edit User Section...")
                                
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
        print("-"*128)
        print("|"+" "*58 + "Login Screen" + " "*58+"|" )
        print("-"*128)
        while maildone2 == False and flag2 == False:
            print("Enter E-mail ID to login into ShipIt")
            mail = input("Mail ID : ")
            print("You entered",mail,"as your email ID")
            print("To continue Press 1")
            print("To re-enter press 2")
            print("To go-back to main-screen press 3")
            while True:
                try:
                    ch7 = int(input())
                except:
                    print("You have entered Invalid Data")
                    print("Choose any option between 1,2 and 3")
                    continue
                if ch7 not in [1,2,3]:
                    print("You have entered Invalid Data")
                    print("Choose any option between 1,2 and 3")
                break
            if ch7 == 3:
                flag2 = True
                break
            elif ch7 == 2:
                continue
            elif not checkmailexist(mail):
                print("Provided E-mail doesn't exist in database.")
                print("To re-enter email press 1")
                print("To register press 2")
                while True:
                    try:
                        ch8 = int(input())
                    except:
                        print("You have entered Invalid Data")
                        print("Choose any option between 1 and 2")
                        continue
                    if ch8 not in [1,2]:
                        print("You have entered Invalid Data")
                        print("Choose any option between 1 and 2")
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
            print("Enter Password to login into ShipIt")
            passwd = input("Password : ")
            print("You entered",passwd,"as your Password")
            print("To continue Press 1")
            print("To re-enter press 2")
            print("To go-back to main-screen press 3")
            while True:
                try:
                    ch9 = int(input())
                except:
                    print("You have entered Invalid Data")
                    print("Choose any option between 1,2 and 3")
                    continue
                if ch9 not in [1,2,3]:
                    print("You have entered Invalid Data")
                    print("Choose any option between 1,2 and 3")
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
            print("Login Successfull")
            startup(mail)
            break
        else:
            print("Username and Password don't match")
            print("To Re-enter mail-id and passwd press 1")
            print("To go to main- menu press 2")
            while True:
                try:
                    ch10 = int(input())
                except :
                    print("You have entered Invalid Data")
                    print("Choose any option between 1 and 2")
                    continue
                if ch10 not in [1,2]:
                    print("You have entered Invalid Data")
                    print("Choose any option between 1,2 and 3")
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
    print("-"*128)
    print(" "*57 + "Sign-Up Screen" + " "*57 )
    print("-"*128)
    while maildone == False and flag1 == False:
        print("Enter E-mail ID to register into ShipIt")
        regmail = input("Mail ID : ")
        print("You entered",regmail,"as your email ID")
        print("To continue Press 1")
        print("To re-enter press 2")
        print("To go-back to main-screen press 3")
        while True:
            try:
                ch3 = int(input())
            except:
                print("You have entered Invalid Data")
                print("Choose any option between 1,2 and 3")
                continue
            if ch3 not in [1,2,3]:
                print("You have entered Invalid Data")
                print("Choose any option between 1,2 and 3")
                continue
            break
        if ch3 == 3:
            flag1 = True
            break
        elif ch3 == 2:
            continue
        elif checkmailexist(regmail):
            print("Entered e-mail address already exists")
            print("To Login Press 1")
            print("To re-enter mail id Press 2")
            while True:
                try:
                    ch4 = int(input())
                except:
                    print("You have entered Invalid Data")
                    print("Choose any option between 1 and 2")
                    continue
                if ch4 not in [1,2]:
                    print("You have entered Invalid Data")
                    print("Choose any option between 1 and 2")
                    continue
                break
            if ch4 == 1:
                print("Going to Login Screen...")
                login()
                break
            else:
                continue
        elif checkvalid(regmail):
            maildone = True
            break
        else:
            print("Entered e-mail Id is invalid.")
            continue
    while pwdone == False and flag1 == False and maildone == True:
        print("Enter Password")
        pwd = input("Password : ")
        print("You entered",pwd,"as your password")
        print("To continue Press 1")
        print("To re-enter press 2")
        print("To go-back to main-screen press 3")
        while True:
            try:
                ch5 = int(input())
            except:
                print("You have entered Invalid Data")
                print("Choose any option between 1,2 and 3")
                continue
            if ch5 not in [1,2,3]:
                print("You have entered Invalid Data")
                print("Choose any option between 1,2 and 3")
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
        print("Enter Username")
        name = input("Name : ")
        print("You entered",name,"as your name")
        print("To continue Press 1")
        print("To re-enter press 2")
        print("To go-back to main-screen press 3")
        while True:
            try:
                ch6 = int(input())
            except:
                print("You have entered Invalid Data")
                print("Choose any option between 1,2 and 3")
                continue
            if ch6 not in [1,2,3]:
                print("You have entered Invalid Data")
                print("Choose any option between 1,2 and 3")
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
        print("Please Wait.....")
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
        print("Registration Complete with")
        print("Name :",name)
        print("E-mail : ", regmail)
        print("Password : ",pwd)
        print("Please Note the ID and passwd")

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
    print()
    print("-"*128)
    print("-"*128)
    print()
    print(" "*75 +                                                               "░██████╗██╗░░██╗██╗██████╗░██╗████████╗")
    print("Find the best shipping service for you." + " "*(36) +                 "██╔════╝██║░░██║██║██╔══██╗██║╚══██╔══╝")
    print("Provide the details of your package and we will help you," + " "*18 + "╚█████╗░███████║██║██████╔╝██║░░░██║░░░")
    print( "to find the most suitable shipping service."+ " "*32 +               "░╚═══██╗██╔══██║██║██╔═══╝░██║░░░██║░░░" )
    print(" "*75 +                                                               "██████╔╝██║░░██║██║██║░░░░░██║░░░██║░░░")
    print(" "*75 +                                                               "╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░░░░╚═╝░░░╚═╝░░░")
    print()
    print("-"*128)
    print("|"+' '*59 + "Disclaimer" +' '*58 + "|")
    print("-"*128)
    print("This is a Python Project")
    print("the information provided by shipIt is for general usage purposes only.")
    print("and is in no way related to ny real organisation.")
    print("The information entered by you wouldn't be considered for Ads but will be used for research and development of ShipIt!")
    print()
    print("To Login press 1")
    print("To Surf Anonmously press 2")
    print("To SignUp press 3")
    print("To End Session press 4")
    print("If encountering issues, contact roshanbiswanathpatra@gmail.com")
    while True:
        try:
            ch1 = int(input())
        except:
            print("You have entered invalid data")
            continue
        if ch1 not in [1,2,3,4]:
            print("Enter suitable value from 1,2 or 3")
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
    print("To end session enter N else continue")
    ch2 = input()
    if ch2 in ["N","n"]:
        print("Program Terminated")
        
        break
    print("Please Wait.....")
    

#-------------------------------------------------------------------------------------------------------------#

#About US
aboutus()

#-------------------------------------------------------------------------------------------------------------#

#Exit Loop
while True:
    print("To exit press q")
    q = input()
    if q == "q" or q == "Q":
        break

#-------------------------------------------------------------------------------------------------------------#

subprocess.call(["python.exe",  currentpath + "/main.py"])

#-------------------------------------------------------------------------------------------------------------#