import os
import json
from ipwhois import IPWhois
import time

fileName = "./data.json"


def executeTraceroute():
    stream = os.popen('traceroute -q 1 www.google.de')
    return stream


def parseToJSON(stream):
    for line in stream.readlines():
        # print(line)
        # print(line.split("  "))
        splittedLine = line.split("  ")
        # print(line)
        try:
            hop = extractHop(splittedLine[0])
            ip = extractIP(splittedLine[1])
            if ip == "*":
                domainName = "*"
                rtt = 0
                writeToJSON(hop, ip, domainName, rtt)
            else:
                domainName = extractDomainName(splittedLine[1])
                rtt = extractRTT(splittedLine[2])
                writeToJSON(hop, ip, domainName, rtt)
                # return hop, ip, domainName, rtt
        except:
            # print(line)
            print("except", line)


def writeToJSON(hop, ip, domainName, rtt):
    if not os.path.isfile(fileName):
        print('File does not exist.')
    else:
        # Open the file as f.
        # The function readlines() reads the file.
        fileRead = open(fileName, 'r')
        data = json.loads(fileRead.read())

        try:
            checkIfExist = data[hop]
            hopExist(hop, ip, domainName, rtt, data)
            # print("hopExisted")
        except:
            hopNotExist(hop, ip, domainName, rtt, data)
        # print(open(fileName).read())
        fileRead.close()

        fileSave = open(fileName, 'w')
        fileSave.write(json.dumps({int(x): data[x] for x in data.keys()}, indent=4, sort_keys=True))
        fileSave.close()


def hopExist(hop, ip, domainName, rtt, data):
    lenOfHop = len(data[hop])
    ipfound = False
    for x in range(0, lenOfHop):
        if data[hop][x]["ip"] == ip:
            ipfound = True
            data[hop][x]["count"] += 1
            if ip == "*":
                break
            data[hop][x]["RTT"].append(rtt)
            if domainName not in data[hop][x]["name"]:
                data[hop][x]["name"].append(domainName)
            break

    if not ipfound:
        if ip == "*":
            data[hop].append({
                "ip": ip,
                "count": 1,
            })
        else:
            data[hop].append({
                "ip": ip,
                "name": [domainName],
                "count": 1,
                "RTT": [rtt]
            })


def hopNotExist(hop, ip, domainName, rtt, data):
    if ip == "*":
        data[hop] = [
            {
                "ip": ip,
                "count": 1,
            }
        ]
    else:
        data[hop] = [
            {
                "ip": ip,
                "name": [domainName],
                "count": 1,
                "RTT": [rtt]
            }
        ]


def extractIP(s):
    if "*" in s:
        return s.replace("\n", "")
    return s.split(" ")[1].replace("(", "").replace(")", "")


def extractDomainName(s):
    return s.split(" ")[0]


def extractRTT(s):
    return s.split(" ")[0]


def extractHop(s):
    return str(int(s))


def fetchInfo(ip):
    try:
        obj = IPWhois(ip)
        result = obj.lookup_whois()
        description = {"labels": [], "range": ""}
        for net in result["nets"]:
            description["labels"].append(net["description"])

        try:
            description["range"] = result["nets"][0]["range"]
        except:
            description["range"] = "not Available"
        return description
    except:
        return {
            "labels": [
            ],
            "range": ""
        }


def addRipeNCCdescribtion():
    if not os.path.isfile(fileName):
        print('File does not exist.')
    else:
        # Open the file as f.
        # The function readlines() reads the file.
        fileRead = open(fileName, 'r')
        data = json.loads(fileRead.read())
        for hop in data:
            for date in data[hop]:
                if not date["ip"] == "*":
                    description = fetchInfo(date["ip"])
                    date["description"] = description
        fileRead.close()

        fileSave = open(fileName, 'w')
        fileSave.write(json.dumps({int(x): data[x] for x in data.keys()}, indent=4, sort_keys=True))
        fileSave.close()

def addRTTcalc():
    return 0

def main():

    # print(fetchInfo("134.102.22.124"))
    # writeToJSON(1, 1, 1, 1)
    # for x in range(0, 10):
    #     parseToJSON(executeTraceroute())
    #     time.sleep(20)

    # fileReader = open("/home/spinach/Documents/Uni/google4.txt", 'r')
    # fileReader = open("/home/spinach/Documents/Uni/google6.txt", 'r')
    fileReader = open("/home/spinach/Documents/Uni/uni4.txt", 'r')
    parseToJSON(fileReader)
    addRipeNCCdescribtion()

if __name__ == "__main__":
    main()
