from PIL import Image
from PIL.ImageStat import Stat
import json
import os


def imgtoRGB(path):
    BlocksRgb = []
    count = 0
    format = ["filename","r","g","b","a"]

    for filename in os.listdir(path):
        tempimg = Image.open(os.path.join(path,filename))
        tempimg = tempimg.convert('RGBA')
        tempstatmean = Stat(tempimg).mean


        print(filename)
        print(tempstatmean)
        #tempimg.show()
        print()
        tempArr = [filename,tempstatmean[0],tempstatmean[1],tempstatmean[2],tempstatmean[3]]

        tempDict = {format: tempArr for format,
                    tempArr in zip(format,tempArr)}
        
        
        BlocksRgb.append(tempDict)
        tempimg.close()
        count += 1

    #print("Results", *BlocksRgb, sep='\n')
    print(json.dumps(BlocksRgb, indent=2))
    jsonfile = json.dumps(BlocksRgb, indent=2)
    with open("fullNewAlphaFinal.json","w") as outfile:
        outfile.write(jsonfile)


imgtoRGB("./texturesNew/block")



