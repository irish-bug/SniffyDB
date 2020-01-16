# SniffyDB
Evolution of Sniffy to include database functionality, visualization and analytics

############################################################ 
                    WELCOME TO SNIFFY 2.0
############################################################ 
#                                                          # 
# Sniffy 2.0 is a packet sniffer and quite easy to use.    # 
# Just run  ./sniffy2.0 from the command line              # 
# choose the pcap you would like to extract info           # 
# and then choose the protocol of the packets you'd like   # 
# to see information about                                 # 
#                                                          # 
#                                                          #  
# Sniffy will extract all information available from all   # 
# packets of that protocol inside of your pcap,            #
# including packet data if available and will write all    #
# of the data to the screen and then into a file           # 
# named sniffy_output.txt in your current directory.       # 
#                                                          #  
############################################################ 
 Sniffy2.0  was written and is maintained by Shane Rogers  
 Python and the Scapy library 2015   shane@shanerogers.info    
############################################################ 


NOTE: Please make sure you have Python and Scapy installed 
before using Sniffy.  If you see the following error:
    Traceback (most recent call last):
    File "./sniffy2.0", line *, in <module>
    from scapy.all import *
    ImportError: No module named scapy.all
This means that you need to install Scapy. 

On Debian based systems you can install scapy by running
sudo apt-get install scapy

Other instructions for installing Scapy can be found here:

    http://www.secdev.org/projects/scapy/doc/installation.html#debian-ubuntu



Copyright 2015 Shane Rogers

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Citations:

"Apache License, Version 2.0," Open Source Initiative [online] 
http://opensource.org/licenses/Apache-2.0 (Accessed 14 December 2014)

"Get all IP layer packages from pcap file in Scapy", 
(asked Nov 20, '13 at 10:23) by reox on stackoverflow, 
http://stackoverflow.com/questions/20093238/get-all-ip-layer-
packages-from-pcap-file-in-scapy (Accessed 13 December 2014)

"Scapy v2.1.1-dev documentation," [online], 
http://www.secdev.org/projects/scapy/doc/index.html 
(Accessed 3 December 2014, 7 December 2014, and 14 December 2014)

"Wireshark Internet_Protocol" [online], 
http://wiki.wireshark.org/Internet_Protocol 
(Accessed 12 December 2014)
