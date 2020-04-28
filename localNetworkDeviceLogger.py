
import os 
import pandas as pd
from getmac import get_mac_address
from datetime import datetime
import pickle


def check_ping(hostname):
  response = os.system("ping -c 1 -W 1 " + hostname+" >/dev/null 2>&1")
  if response == 0:
      #print (hostname)
      pingstatus = True
  else:
      pingstatus = False

  return pingstatus

def ipscan():
 output_ip = []
 thehost = "192.168."
 for i in range(1,2):
    host = thehost + str(i) + "."
    for j in  range(0,256):
    #for j in  range(0,35):        # for testing... scan less go faster
        newhost = host + str(j)
        output_ip.append(newhost)
        newhost = host

 return output_ip


print("SCANNING ALL ACTIVE IP's\n")
print("-------------------------------\n\n")
hosts = ipscan()
#print(hosts)


activeIPs = []
activeIPsMAC = []
for i in range(0 ,len(hosts)):
    #If the ip address is occupied
    if check_ping(hosts[i]):
        activeIPs.append(hosts[i])
        ip_mac = get_mac_address(ip=hosts[i])
        activeIPsMAC.append(ip_mac)
    else:
        activeIPs.append("NOT ACTIVE")
        activeIPsMAC.append("NOT ACTIVE")


#If you already have a previous log file, check to see if the
#    MAC address is in previous logs
try:
    dataLog_df = pd.read_pickle('data_IP_log.pickle')
    
    #Get the time of the scan
    dateTimeObj = datetime.now()
    #Add a new column from the results of the scan
    dataLog_df[dateTimeObj] = activeIPsMAC
    
    #Boolean to flag if a new MAC is detected
    #False = no new devices found
    detected = False
    
    #See if there are any MAC addresses from this scan in previous scans
    for k in range(0, len(activeIPsMAC)):
        timesMAC = dataLog_df.eq(activeIPsMAC[k]).values.sum()
        #Make sure that only one occurence of the MAC for all logs
        #Make sure that the one occurence of the MAC is in the most recent IP scan
        if timesMAC == 1 and dataLog_df[dateTimeObj].str.contains(activeIPsMAC[k]).values.sum() == 1:
            #Derek you need to make sure that this is also only in the most current scan as well
            #Use isin series
            print("SCAN RESULTS\n")
            print("-------------------------------\n\n")
            print("A new Device has been detected on your Network!!!\n")
            print("The device MAC address is " + activeIPsMAC[k] + "\n")
            print("The device currently occupies " + activeIPs[k] + "\n\n")
            print("-------------------------------\n")
            detected = True
    
    #No new MAC addresses were found
    if detected != True:
        print("SCAN RESULTS\n")
        print("-------------------------------\n\n")        
        print("No new devices detected\n\n")
        print("-------------------------------\n")
    
    #logData.append( activeIPsMAC , ignore_index=True)
    with open('data_IP_log.pickle', 'wb') as f:
        pickle.dump(dataLog_df, f)    

#If this is the first log of the file 
except:
    newLogSheet = pd.DataFrame(index = hosts)
    print("This is the first scan, tracking all current devices")

    #Mark when you makde this scan
    dateTimeObj = datetime.now()
    #Add a new column for the IP addrresses you found
    newLogSheet[dateTimeObj] = activeIPsMAC


    with open('data_IP_log.pickle', 'wb') as f:
        pickle.dump(newLogSheet, f)
































