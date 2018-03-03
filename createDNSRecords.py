#!/usr/bin/env python

import json
import CloudFlare
import sys, getopt
import os

def connectCloudFlare():
    return CloudFlare.CloudFlare()

def getZoneID(cf, zone_name):
    try:
        zones = cf.zones.get(params = {'name':zone_name,'per_page':1})
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.get %d %s - api call failed' % (e, e))
    except Exception as e:
        exit('/zones.get - %s - api call failed' % (e))

    if len(zones) == 0:
        sys.exit('No zones found')
    zone = zones[0]
    return zone['id']

def displayDNSRecordsCF(records):
    print('DNS records :')
    for dns_record in records:
        r_name = dns_record['name']
        r_type = dns_record['type']
        r_value = dns_record['content']
        r_id = dns_record['id']
        print ('\t', r_id, r_name, r_type, r_value)

def getDNSRecordsFromCF(cf, zone_name, zone_id):
    try:
        dns_records = cf.zones.dns_records.get(zone_id)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records.get %d %s - api call failed' % (e, e))
    print('DNS ZONE :')
    print (zone_id, zone_name)
    displayDNSRecordsCF(dns_records)
    return dns_records

def getDNSRecordsFromFiles(input_file):
    records = []
    with open(input_file) as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == '#':
                continue
            tmp = line.split(' ')
            records.append({
                'type': tmp[0],
                'name': tmp[1],
                'content': tmp[2].replace('\n','')
            })
    return records

def createMissingDNSRecords(local_list, cf_list, cf, zone_id):
    for dns in local_list:
        exist = False
        for cf_dns in cf_list:
            if dns['name'] == cf_dns['name']:
                exist = True
                break
        if (exist):
            print(dns['name'], "Already exist")
        else:
            print(dns['name'], "Doesn't exist")
            print('Creating ', dns['name'], ' on CloudFlare...')
            cf.zones.dns_records.post(zone_id, data=dns)
            print(dns['name'], ' successfully created!')

def main(argv):
    if (os.environ['CF_API_EMAIL'] == ""):
        print("Setup CF_API_EMAIL before run")
        sys.exit()
    if (os.environ['CF_API_KEY'] == ""):
        print("Setup CF_API_KEY before run")
        sys.exit()
    if (os.environ['CF_API_CERTKEY'] == ""):
        print("Setup CF_API_CERTKEY before run")
        sys.exit()
    inputfile = ''
    domaine = ''
    try:
        opts, args = getopt.getopt(argv,"hi:d:",["ifile=", "domaine="])
    except getopt.GetoptError:
        print ('createDNSRecords.py -i <inputfile> -d <domaine>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('createDNSRecords.py -i <inputfile> -d <domaine>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-d", "--domaine"):
            domaine = arg
    zone_name = domaine
    cf = connectCloudFlare()
    zone_id = getZoneID(cf, domaine)
    local_dns_list = getDNSRecordsFromFiles(inputfile)
    cf_dns_list = getDNSRecordsFromCF(cf, zone_name, zone_id)
    createMissingDNSRecords(local_dns_list, cf_dns_list, cf, zone_id)

if __name__ == '__main__':
    main(sys.argv[1:])
