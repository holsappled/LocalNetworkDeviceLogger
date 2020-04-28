# LocalNetworkDeviceLogger

Create a read/write pickle to log MAC addresses on your local network and notify the user when a new device is connected. 

The program will start by scanning all active IP addresses and then create a pandas dataframe with a timestamp.  When the program is run for a second time it will read the previous pandas dataframe (saved as a pickle) and compare the MAC addresses from all previous scans.  

The program will find all active IP hosts.  The program then acquires the MAC address of each device.  The MAC address is a unique identifier of hardware.  The logger dataframe keeps track of all MAC addresses that have been on the local network. 

 If a new device appears after a scan then the terminal will display the IP address the new device occupies along with the associated MAC address.
 
 If a future scan incurs the new MAC address will be considered an accepted device and will not notify the user.
