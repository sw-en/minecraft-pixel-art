from PIL import Image
import json
import random
import os
from litemapy import Schematic, Region, BlockState



height=128
width=128
path = "ExamplePhotos/downscaleCYW.png"

img = Image.open(path)
img = img.convert('RGBA')

imgBiLin = img.resize((height,width), resample=Image.Resampling.HAMMING)

texturePack = "block"


"""

comparePixels provides a list of every block used for each pixel of the downscaled input image.
The list starts at the top left, and runs left to right, top to bottom.
The nested for loops iterate through each pixel of the downscaled reference image and compares it to the average color of each Minecraft texture.
The average color of each texture was determined through colorizeTextures, and saved as json;  "fullNewAlphaFinal.json".
The comparison made sums the absolute value of the difference between a pixel's rgba values and the texture's assigned color's rgba values
The lower the deviation value the more likely match a block is to repressent a pixel.

"""
def comparePixels():
    blocksInOrder = []

    pixelList = list(imgBiLin.getdata())
    with open("fullNewAlphaFinal.json", 'r') as openfile:
        jsonObj = json.load(openfile)
    
    for pixels in pixelList:
        tempDev = None
        tempBlock = None
        for blocks in jsonObj:
            deviation = 0

            deviation += abs(pixels[0]-blocks['r'])
            deviation += abs(pixels[1]-blocks['g'])
            deviation += abs(pixels[2]-blocks['b'])
            deviation += abs(pixels[3]-blocks['a'])

            if tempDev == None or deviation < tempDev :
                tempDev = deviation
                tempBlock = blocks['filename']
            
        blocksInOrder.append(tempBlock)
    return blocksInOrder






def replacePixels(blocklist):
    pixel = []
    finalArray = []

    with open("fullNewAlphaFinal.json", 'r') as openfile:
        jsonObj = json.load(openfile)

    for block in blocklist:
        for blockData in jsonObj:
            if block == blockData['filename']:
                temp = [blockData['r'],blockData['g'],blockData['b']]
                pixel.append(tuple(temp))
    
    for i in range(0, 128):
        currentRow = pixel[i*128 : (i*128)+128]
        finalArray.append(currentRow)
    return finalArray



"""
renderWithBlocks takes the ordered list of blocks, and opens the blocks texture image and pastes them in rows.
Finally the rows are all pasted together.

"""


def renderWithBlocks(blocklist,showOrSave):
    def image_grid(imgs, rows, cols):
        assert len(imgs) == rows*cols

        w, h = imgs[0].size
        grid = Image.new('RGB', size=(cols*w, rows*h))
        grid_w, grid_h = grid.size
        
        for i, img in enumerate(imgs):
            grid.paste(img, box=(i%cols*w, i//cols*h))
        return grid
    
    blockGridImages = []
    for blocks in blocklist:
        tempimg = Image.open(os.path.join(texturePack,blocks))
        blockGridImages.append(tempimg)
    
    grid = image_grid(blockGridImages, rows=128,cols=128)   
    
    """
    if showOrSave.lower == "show":
        grid.show()
    else:
        grid.save(path + "_blocks")
    """
    grid.show()


#renderWithBlocks(comparePixels(),"show")


def saveSchematic(blocklist,inputName,inputAuthor,):
    reg = Region(0, 0, 0, 128, -1, -128)
    schem = reg.as_schematic(name=inputName, author=inputAuthor, description="Made with litemapy")

    # Create the block state we are going to use

    # Build the planet
    yCount = 0
    for j in range(128):
        for i in range(128):
            blockstate = BlockState("minecraft:" + blocklist[(128*j)+i][:-4])
            print(blockstate)
            print(type(blockstate))
            reg.setblock(i,0,-1*j, blockstate)
        

    # Save the schematic
    schem.save("CYW_test.litematic")


#saveSchematic(comparePixels(),"CYWtest","sweeny")
renderWithBlocks(comparePixels(),"show")
#with open("file.txt", "w") as output:
 #   output.write(str(comparePixels()))


"""
testing function
pulls random pixel colors and assigned block.


def findRandomPixels():
    listp = list(imgBiLin.getdata())
    blockArray = comparePixels()
    print(blockArray)
    print(listp)
    for i in range(40):
        rand = random.randrange(500,16384)
        print(blockArray[rand])
        print(listp[rand])
"""



def buttonPressShowColors():
    colorArray = comparePixels()
    colorArray.show()

def buttonSaveShowColors():
    colorArray = comparePixels()
    colorArray.save();