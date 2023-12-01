from PIL import Image
import json
import random
import os



height=128
width=128
path = "./guitar.png"

img = Image.open(path)
img = img.convert('RGBA')

imgBiLin = img.resize((height,width), resample=Image.Resampling.HAMMING)

texturePack = "./texturesNew/block"



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
    #print(blocksInOrder)
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

def renderWithBlocks(blocklist):
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
    #grid.save("renderWithBlocksTest.png")
    grid.show()








def findRandomPixels():
    listp = list(imgBiLin.getdata())
    blockArray = comparePixels()
    print(blockArray)
    print(listp)
    for i in range(40):
        rand = random.randrange(500,16384)
        print(blockArray[rand])
        print(listp[rand])


#pixelArray= replacePixels(comparePixels())
renderWithBlocks(comparePixels())






#print(comparePixels())
#pixelArray = np.array(pixelArray, dtype=np.uint8)


#print(pixelArray)

#newImg = Image.fromarray(pixelArray)
#newImg.save("BWtest.png")
#newImg.show()
#imgBiLin.show()
