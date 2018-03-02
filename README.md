# CreateDNSRecordsCloudFlare
A small script that automatically creates dns records on cloudflare

### Prerequisites

What things you need to install the software and how to install them

Linux/OSX
```bash
sudo pip3 install --upgrade pip
sudo pip3 install cloudflare
```

Windows
```bash
pip3 install --upgrade pip
pip3 install cloudflare
```

### Installing

```bash
git clone https://github.com/Nicolas-Constanty/CreateDNSRecordsCloudFlare.git
```

## Running the tests

Linux/OSX

```bash
cd CreateDNSRecordsCloudFlare
./createDNSRecords.py -h
```

Windows

```bash
cd CreateDNSRecordsCloudFlare
py.exe ./createDNSRecords.py -h
```

### Getting Started
### Setup shell environment variables
```bash
$ export CF_API_EMAIL='user@example.com'
$ export CF_API_KEY='00000000000000000000000000000000'
$ export CF_API_CERTKEY='v1.0-...'
$
```
### Create your record file

A Record's file is a simple text file where each line as 3 informations :

| Type | Name | Content        |
| ----------------------------------------------- |:-------------:| --------------|
| A, AAAA, CNAME, TXT, SRV, LOC, MX, NS, SPF | "example.com" | "127.0.0.1" |
cf [Cloudflare API](https://api.cloudflare.com/#dns-records-for-a-zone-create-dns-record)

exemple_records.txt
```
A mydomain.io 127.0.0.1
A api.mydomain.io 127.0.0.1
A s3.mydomain.io 127.0.0.1
```

### Run the script

Linux/OSX

```bash
./createDNSRecords.py -i exemple_records.txt -d mydomain.io
```

Windows

```bash
py.exe ./createDNSRecords.py -i exemple_records.txt -d mydomain.io
```

## Credit
This script implementation is based on [python-cloudflare](https://github.com/cloudflare/python-cloudflare/blob/master/README.md)

This is based on work by [Felix Wong (gnowxilef)](https://github.com/gnowxilef) found [here](https://github.com/cloudflare-api/python-cloudflare-v4).
It has been seriously expanded upon.

## Copyright

Portions copyright [Felix Wong (gnowxilef)](https://github.com/gnowxilef) 2015 and Cloudflare 2016.
