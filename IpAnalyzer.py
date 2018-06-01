import sys
import re as regex

def parseIp(ip1, ip2):

    ipGroup = [ip1, ip2]
    separetedBytes = []
    masks = []

    for index in range(0, len(ipGroup)):
        separetedBytes.append(ipGroup[index].split("."))

        if(len(separetedBytes[index]) != 4):
            print("Incorrect ip type")
            sys.exit(0)

        if "/" in separetedBytes[index][3]:
            masks.append(separetedBytes[index][3].split("/"))
            separetedBytes[index][3] = regex.sub("/.*$", "", separetedBytes[index][3])
        else:
            print("Incorect syntax")
            sys.exit(1)

    for i in range(0, len(masks)):
        del masks[i][0]

    return separetedBytes, masks


def createSubnetMask(maskBits):

    tempMask = [0, 0, 0, 0]

    #because bitwise left me wanting to kill myself :)
    index = 0
    threshhold = 0
    for i in range(0, int(maskBits)):
        threshhold += 1
        if(threshhold is 8):
            tempMask[index] = (2**threshhold)-1
            index += 1
            threshhold = 0

    if(threshhold > 0 and index < 4):
        tempMask[index] = (2 ** threshhold) - 1

    return tempMask

def checkIfIpsCanComunicate(broadcastAddress, ipArr, networkAddress):
    ok = True
    for i in range(len(ipArr[1])):
        if int(ipArr[1][i]) < networkAddress[i] or int(ipArr[1][i]) > broadcastAddress[i]:
            ok = False
    if ok is True:
        print("The ip addresses can comunicate")
    else:
        print("Scuze boss da nu mere")

def buildAddresses(ipArr, masks):

    ip1, networkAddress = buildNetworkAddress(ipArr, masks)

    #get higherlimit
    broadcastAddress = buildBroadcastArray(ip1, masks)

    checkIfIpsCanComunicate(broadcastAddress, ipArr, networkAddress)


def buildNetworkAddress(ipArr, masks):
    subnetMask1 = createSubnetMask(masks[0][0])
    ip1 = ipArr[0]
    networkAddress = []
    # get networkAddress **lowerlimit
    for i in range(len(ip1)):
        networkAddress.append(int(ip1[i]) & subnetMask1[i])
    return ip1, networkAddress


def buildBroadcastArray(ip1, masks):

    cidr = 32 - int(masks[0][0])
    broadcastMask = createSubnetMask(cidr)
    broadcastMask.reverse()
    broadcastAddress = []
    for i in range(len(ip1)):
        broadcastAddress.append(int(ip1[i]) | broadcastMask[i])
    return broadcastAddress


def checkIp(ip1, ip2):

    ipArr, masks = parseIp(ip1,ip2)
    buildAddresses(ipArr, masks)


#check number of arguments
if(len(sys.argv) != 3):
    print("You can't do that")

else:
    checkIp(sys.argv[1], sys.argv[2])