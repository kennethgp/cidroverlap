# Install python3 and required modules:
# pip install ipaddr
# pip install pandas
# pip install openpyxl

import ipaddr
import sys
import pandas as pd

# Receives 2 arguments: target cidr and file containing list of cidrs (Excel export from ASC) to check for colisions
# python cidroverlap.py 10.28.168.0/24 '2305050030002153_NIC Effective Routes_aks-rollover01-15204975-vmss_6.xlsx'
def main():
    args = sys.argv[1:]
    target = ipaddr.IPNetwork(args[0])
    try:
        effectiveRoutes = pd.read_excel(args[1],dtype=str,na_filter=False)
    except Exception as e:
        print("Unable to open Excel file: " + str(e))
        sys.exit(1)

    print("\nRoutes overlapping with " + str(target) + ":\n")
    for index,row in effectiveRoutes[['RouteSource','DestinationSubnets', 'DestinationServiceTags','NextHops','NextHopType','IsEnabled']].iterrows():
        if ',' in row['DestinationSubnets']:
            dests = row['DestinationSubnets'].split(',')
            for dest in dests:
                cidr = ipaddr.IPNetwork(dest.strip())
                if cidr.overlaps(target):
                    print("[Row " + str(index+2) + "] " + row['RouteSource'] + " " + str(cidr) + ", DestinationServiceTags: " + row['DestinationServiceTags'] + ", NextHops: " + row['NextHops'] + ", NextHopType: " + row['NextHopType'] + ", IsEnabled: " + row['IsEnabled'])
        else:
            cidr = ipaddr.IPNetwork(row['DestinationSubnets'])
            if cidr.overlaps(target):
                print("[Row " + str(index+2) + "] " + row['RouteSource'] + " " + str(cidr) + ", DestinationServiceTags: " + row['DestinationServiceTags']  + ", NextHops: " + row['NextHops'] + ", NextHopType: " + row['NextHopType'] + ", IsEnabled: " + row['IsEnabled'])

if __name__ == "__main__":
    main()