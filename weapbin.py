#This script writes all the data from weapons.bin into JSON
import struct
import json
import os
import sys

def leBytesInt(file):
    #converts the next 2 bytes to an integer
    next2 = file.read(2)
    print(next2)
    converted2Bytes = int.from_bytes(next2, "little",signed = True)
    return converted2Bytes

def leBytesFloat(file):
    #converts the next 4 bytes to a float
    converted4Bytes = struct.unpack("<f", file.read(4))
    print(converted4Bytes)
    return converted4Bytes


def extract():
    with open("weapons.bin", "rb") as f:
        end = False
        #list for the loadorder.txt (needed for later)
        loadorder = []
        while not end:
            nextID = f.read(2)
            #check if next 2 bytes are empty
            if nextID == b'':
                break
            
            #if they are not empty -> store it as the ship ID
            shipID = int.from_bytes(nextID, byteorder="little")
            #total amount of hardpoints the ship possesses
            totalAmount = leBytesInt(f)

            primary = []
            primaryX = []
            primaryY = []
            primaryZ = []
            primaryCoords = [primaryX, primaryY, primaryZ]

            secondary = []
            secondaryX = []
            secondaryY = []
            secondaryZ = []
            secondaryCoords = [secondaryX, secondaryY, secondaryZ]

            turret = []
            turretX = []
            turretY = []
            turretZ = []
            turretCoords = [turretX, turretY, turretZ]

            engine = []
            engineX = []
            engineY = []
            engineZ = []
            engineSizeX = []
            engineSizeY = []
            engineSizeZ = []

            engineSizes = [engineSizeX, engineSizeY, engineSizeZ]
            engineCoords = [engineX, engineY, engineZ]

            primAmount = 0
            secAmount = 0
            turrAmount = 0
            engAmount = 0

            for i in range(0, totalAmount):
                

                raw = f.read(2)
                nextBytes = int.from_bytes(raw, byteorder="little")

                #check if the next 2 bytes are empty
                if raw == b'':
                    end = True
                    break
                
                #check for primary hardpoint indicator (00 00)
                if nextBytes == 0:
                    print("bytes = 0")
                    primAmount += 1
                    primary.append(f"primary_{primAmount}")
                    #add coordinates to lists
                    for i in primaryCoords:
                        i.append(leBytesInt(f))
                
                #check for secondary hardpoint indicator (01 00)
                elif nextBytes == 1:
                    print("bytes = 1")
                    secAmount += 1
                    secondary.append(f"secondary_{secAmount}")
                    #add coordinates to lists
                    for i in secondaryCoords:
                        i.append(leBytesInt(f))

                #check for turret hardpoint indicator (02 00)
                elif nextBytes == 2:
                    print("bytes = 2")
                    turrAmount += 1
                    turret.append(f"turret_{turrAmount}")
                    #add coordinates to lists
                    for i in turretCoords:
                        i.append(leBytesInt(f))

                #check for engine hardpoint indicator (03 00)
                elif nextBytes == 3:
                    print("bytes = 3")
                    engAmount += 1
                    engine.append(f"engine_{engAmount}")
                    #add coordinates to lists
                    for i in engineCoords:
                        i.append(leBytesInt(f))
                    #add engine plume sizes to lists
                    for i in engineSizes:
                        i.append(leBytesFloat(f))

            #create dictionary
            shipDict = {'ID': shipID, 'total': totalAmount}

            for i in range(0, totalAmount):
                if end:
                    break

                pIteration = 0
                for i in primary:
                    shipDict[i + "_key"] = i
                    shipDict[i + "_coordX"] = primaryX[pIteration]
                    shipDict[i + "_coordY"] = primaryY[pIteration]
                    shipDict[i + "_coordZ"] = primaryZ[pIteration]
                    pIteration += 1

                sIteration = 0
                for i in secondary:
                    shipDict[i + "_key"] = i
                    shipDict[i + "_coordX"] = secondaryX[sIteration]
                    shipDict[i + "_coordY"] = secondaryY[sIteration]
                    shipDict[i + "_coordZ"] = secondaryZ[sIteration]
                    sIteration += 1

                tIteration = 0
                for i in turret:
                    shipDict[i + "_key"] = i
                    shipDict[i + "_coordX"] = turretX[tIteration]
                    shipDict[i + "_coordY"] = turretY[tIteration]
                    shipDict[i + "_coordZ"] = turretZ[tIteration]
                    tIteration +=1

                eIteration = 0
                for i in engine:
                    shipDict[i + "_key"] = i
                    shipDict[i + "_coordX"] = engineX[eIteration]
                    shipDict[i + "_coordY"] = engineY[eIteration]
                    shipDict[i + "_coordZ"] = engineZ[eIteration]

                    shipDict[i + "_sizeX"] = engineSizeX[eIteration]
                    shipDict[i + "_sizeY"] = engineSizeY[eIteration]
                    shipDict[i + "_sizeZ"] = engineSizeZ[eIteration]
                    eIteration += 1

            #put dictionary into JSON file
            with open(f"ship_{shipID}.json", 'w') as g:
                json.dump(shipDict, g, indent=4)
                g.close()    
                print("End reached")
            
            loadorder.append(f"ship_{shipID}.json")

        #append to loadorder file
        with open(f"loadorder.txt", 'w') as load:

            loadorderstr = ""
            for i in loadorder:
                loadorderstr += f"{i}\n"

            load.write(loadorderstr)
            load.close()
    f.close()

def build():
    
    #replace weapons_built.bin, if it's already been created
    if os.path.isfile("weapons_built.bin"):
        os.remove("weapons_built.bin")

    with open("loadorder.txt") as load:

        loadData = load.read()

        loadList = loadData.split("\n")

        with open("weapons_built.bin", 'ab') as w:
            for i in loadList:
                if i != "":
                    l = open(i, 'r')
                    loadedJSON = json.load(l)

                    #keywords for short ints
                    shorts = ["primary", "secondary", 'turret', 'engine']
                    
                    for j in loadedJSON:
                        #  This loop checks what type of data the key 'j' is, writing it's value 
                        #  in the corresponding types (ID, total, indicators and coordinates are shorts,
                        #  engine sizes are floats)

                        #print("current " + str(j))

                        if j == 'ID' or j == 'total':
                            print("writing " + j)
                            inBytes = struct.pack('<h', loadedJSON[j])
                            w.write(inBytes)
                            #print(inBytes)
                        else: 
                            for k in shorts:

                                if k in j and "coord" in j:
                                    print("writing " + j)
                                    inBytes = struct.pack('<h', loadedJSON[j])
                                    w.write(inBytes)
                                
                                elif k in j and "size" in j:
                                    print("writing " + j)
                                    # Float is inside a list object, that's why
                                    # there's the loadedJSON[j][0] statement.
                                    inBytes = struct.pack('<f', loadedJSON[j][0])
                                    w.write(inBytes)

                                elif k in j and "key" in j:
                                    # "if a keyword AND the word 'key' are in dictionary key -> hardpoint indicator"
                                    # What a mouth-full

                                    if k == "primary":
                                        print("Writing primary seperator")
                                        inBytes = struct.pack('<h', 0)
                                        w.write(inBytes)
                                        
                                    elif k == "secondary":
                                        print("Writing secondary seperator")
                                        inBytes = struct.pack('<h', 1)
                                        w.write(inBytes)

                                    elif k == "turret":
                                        print("Writing turret seperator")
                                        inBytes = struct.pack('<h', 2)
                                        w.write(inBytes)

                                    elif k == "engine":
                                        print("Writing engine seperator")
                                        inBytes = struct.pack('<h', 3)
                                        w.write(inBytes)

argNum = len(sys.argv)

if argNum > 2:
    print("Please only enter one argument\n1. python .\weapbin.py extract\n2. python .\weapbin.py build")
elif argNum == 1:
    print("Please enter an argument:\n1.python .\weapbin.py extract\n2. python .\weapbin.oy build")

else:
    if sys.argv[1] == "extract":
        extract()
    elif sys.argv[1] == "build":
        build()
    else:
        print("Argument not valid. Please enter either 'extract' or 'build' as an argument.")