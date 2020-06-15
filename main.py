import os
import json

fileName = "./data.json"


def executeTraceroute():
    stream = os.popen('traceroute -q 1 www.uni-bremen.de')
    return stream


def parseToJSON(stream):
    for line in stream.readlines():
        # print(line)
        # print(line.split("  "))
        splittedLine = line.split("  ")
        print(line)
        try:
            hop = extractHop(splittedLine[0])
            ip = extractIP(splittedLine[1])
            domainName = extractDomainName(splittedLine[1])
            rtt = extractRTT(splittedLine[2])
            writeToJSON(hop, ip, domainName, rtt)
            # return hop, ip, domainName, rtt
        except:
            # print(line)
            print("except")


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
        except:
            hopNotExist(hop, ip, domainName, rtt, data)
        # print(open(fileName).read())
        fileRead.close()

        fileSave = open(fileName, 'w')
        fileSave.write(json.dumps({int(x):data[x] for x in data.keys()},  indent=4, sort_keys=True))
        fileSave.close()


def hopExist(hop, ip, domainName, rtt, data):
    ipfound = False
    for target in data[hop]:
        if target["ip"] == ip:
            ipfound = True
            data[hop]["count"] = data[hop]["count"] + 1
            data[hop]["RTT"].append(rtt)
            if domainName not in target["name"]:
                data[hop]["name"].append(domainName)

    if not ipfound:
        data[hop].append({
            "ip": ip,
            "name": [domainName],
            "count": 1,
            "RTT": [rtt]
        })


def hopNotExist(hop, ip, domainName, rtt, data):
    data[hop] = [
        {
            "ip": ip,
            "name": [domainName],
            "count": 1,
            "RTT": [rtt]
        }
    ]


def extractIP(s):
    return s.split(" ")[1]


def extractDomainName(s):
    return s.split(" ")[0]


def extractRTT(s):
    return s.split(" ")[0]


def extractHop(s):
    return str(int(s))


def openJSONData():
    return 0


def saveJSONtoDisk():
    return 0


def main():
    # writeToJSON(1, 1, 1, 1)
    # for x in range(0, 3):
    parseToJSON(executeTraceroute())


if __name__ == "__main__":
    main()
