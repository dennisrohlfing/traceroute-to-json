import os
import json
from ipwhois import IPWhois
import statistics
import time


def executeTraceroute():
    stream = os.popen('traceroute -q 1 www.google.de')
    return stream


def parseToJSON(stream, outputFile):
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
                writeToJSON(hop, ip, domainName, rtt, outputFile)
            else:
                domainName = extractDomainName(splittedLine[1])
                rtt = extractRTT(splittedLine[2])
                writeToJSON(hop, ip, domainName, rtt, outputFile)
                # return hop, ip, domainName, rtt
        except:
            # print(line)
            print("except", line)


def writeToJSON(hop, ip, domainName, rtt, outputFile):
    if not os.path.isfile(outputFile):
        print('File does not exist.')
    else:
        # Open the file as f.
        # The function readlines() reads the file.
        fileRead = open(outputFile, 'r')
        data = json.loads(fileRead.read())

        try:
            checkIfExist = data[hop]
            hopExist(hop, ip, domainName, rtt, data)
            # print("hopExisted")
        except:
            hopNotExist(hop, ip, domainName, rtt, data)
        # print(open(outputFile).read())
        fileRead.close()

        fileSave = open(outputFile, 'w')
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


def addRipeNCCdescribtion(outputFile):
    if not os.path.isfile(outputFile):
        print('File does not exist.')
    else:
        # Open the file as f.
        # The function readlines() reads the file.
        fileRead = open(outputFile, 'r')
        data = json.loads(fileRead.read())
        for hop in data:
            for date in data[hop]:
                if not date["ip"] == "*":
                    description = fetchInfo(date["ip"])
                    date["description"] = description
        fileRead.close()

        fileSave = open(outputFile, 'w')
        fileSave.write(json.dumps({int(x): data[x] for x in data.keys()}, indent=4, sort_keys=True))
        fileSave.close()


def convertToFloat(list):
    floatList = []
    for str in list:
        floatList.append(float(str))
    return floatList


def addRTTcalc(outputFile):
    if not os.path.isfile(outputFile):
        print('File does not exist.')
    else:
        # Open the file as f.
        # The function readlines() reads the file.
        fileRead = open(outputFile, 'r')
        data = json.loads(fileRead.read())
        for hop in data:
            for date in data[hop]:
                if not date["ip"] == "*":
                    floatList = convertToFloat(date["RTT"])
                    minimum = round(min(floatList),1)
                    maximum = round(max(floatList),1)
                    meanvalue = round(statistics.mean(floatList),1)
                    date["RTT"] = {"min": minimum, "max": maximum, "mean": meanvalue}

        fileRead.close()

        fileSave = open(outputFile, 'w')
        fileSave.write(json.dumps({int(x): data[x] for x in data.keys()}, indent=4, sort_keys=True))
        fileSave.close()
    return 0


def clearFile(file):
    data = {}
    fileSave = open(file, 'w')
    fileSave.write(json.dumps({int(x): data[x] for x in data.keys()}, indent=4, sort_keys=True))
    fileSave.close()


def rotation(inputFile, outputFile):
    clearFile(outputFile)
    fileReader = open(inputFile, 'r')
    parseToJSON(fileReader, outputFile)
    addRipeNCCdescribtion(outputFile)
    addRTTcalc(outputFile)


def doTraceroute():
    for x in range(0, 10):
        parseToJSON(executeTraceroute())
        time.sleep(20)


def main():

    rotation("/path/to/input.json", "/path/to/output.json")


if __name__ == "__main__":
    main()
