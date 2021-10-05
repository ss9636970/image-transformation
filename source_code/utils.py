import numpy as np
from torch import tensor, arange, meshgrid, floor, cat, clamp, einsum
from torch import long as lg
from torch import float as ft
from PIL import Image

class Pic_Transformations:
    def __init__(self, name='transformations'):
        self.name = name

    def image_adj(self, inputs):
        mi = inputs.min()
        if mi < 0:
            outputs = inputs - mi
            ma = outputs.max()
        
        else:
            outputs = inputs
            ma = inputs.max()

        if ma > 255:
            outputs = outputs * (255 / ma)
            return outputs
        
        else:
            return inputs

    def to_image(self, array):
        img = array.astype('uint8')
        img = Image.fromarray(img)
        return img

    def log_transformation(self, inputs, c=110):
        outputs = np.log10(inputs + 1) * c
        return self.image_adj(outputs)

    def gamma_correction(self, inputs, gamma=0.5, A=1):
        maxPixel = inputs.max()
        outputs = inputs / maxPixel
        outputs = A * (outputs ** gamma)
        outputs = outputs * maxPixel
        return self.image_adj(outputs)

    def image_nagative(self, inputs, L=256):
        outputs = (L - 1) - inputs
        return self.image_adj(outputs)

    def bilinear_transform(self, inputs, size=[600, 1100]):
        img = tensor(inputs)
        sizeOri = tensor(img.shape)
        size = tensor(size)
        adjLen = (sizeOri - 1) / (size - 1)
        height = arange(size[0]) * adjLen[0]
        width = arange(size[1]) * adjLen[1]
        meshH, meshW = meshgrid(height, width)
        meshHI, meshWI = floor(meshH), floor(meshW)       # 轉化後像素點的整數部分(對應原圖左邊或上方的點)
        meshWL = meshW - meshWI         # x 的第一個元素
        meshHL = meshH - meshHI         # y 的第一個元素
        meshWR = 1 - meshWL             # x 的第二個元素
        meshHR = 1 - meshHL
        x = cat([meshWL.unsqueeze(2), meshWR.unsqueeze(2)], dim=2).unsqueeze(2)
        y = cat([meshHL.unsqueeze(2), meshHR.unsqueeze(2)], dim=2).unsqueeze(2)
        meshQW = cat([meshWI.unsqueeze(2), (meshWI+1).unsqueeze(2)], dim=2).type(lg)   # index 要求 Q 用的
        meshQH = cat([meshHI.unsqueeze(2), (meshHI+1).unsqueeze(2)], dim=2).type(lg)
        mh, mw = sizeOri[0] - 1, sizeOri[1] - 1
        meshQW, meshQH = clamp(meshQW, max=mw), clamp(meshQH, max=mh)
        meshQ = []   # 對應一個像素要計算的元途中四個點
        for i in range(1, -1, -1):
            for j in range(1, -1, -1):
                w = meshQW[:, :, i]
                h = meshQH[:, :, j]
                meshQ.append(img[h, w].unsqueeze(2))
        meshQ = cat(meshQ, dim=2)
        a, b, c = meshQ.shape
        meshQ = meshQ.view(a, b, 2, 2).type(ft)
        temp = einsum('ijkl, ijlh->ijkh', x, meshQ)
        outputs = einsum('ijkl, ijfl->ijkf', temp, y).squeeze()
        return outputs.numpy().astype('uint8')

    def nearest_transform(self, inputs, size=[600, 1100]):
        img = tensor(inputs)
        sizeOri = tensor(img.shape)
        size = tensor(size)
        adjLen = (sizeOri - 1) / (size - 1)
        height = arange(size[0]) * adjLen[0]
        width = arange(size[1]) * adjLen[1]
        meshH, meshW = meshgrid(height, width)
        meshHI, meshWI = floor(meshH), floor(meshW)       # 轉化後像素點的整數部分(對應原圖左邊或上方的點)
        meshWL = ((meshW - meshWI) > 0.5) + 0.         # x 的第一個元素
        meshHL = ((meshH - meshHI) > 0.5) + 0.         # y 的第一個元素
        meshWR = 1 - meshWL             # x 的第二個元素
        meshHR = 1 - meshHL
        x = cat([meshWL.unsqueeze(2), meshWR.unsqueeze(2)], dim=2).unsqueeze(2)
        y = cat([meshHL.unsqueeze(2), meshHR.unsqueeze(2)], dim=2).unsqueeze(2)
        meshQW = cat([meshWI.unsqueeze(2), (meshWI+1).unsqueeze(2)], dim=2).type(lg)   # index 要求 Q 用的
        meshQH = cat([meshHI.unsqueeze(2), (meshHI+1).unsqueeze(2)], dim=2).type(lg)
        mh, mw = sizeOri[0] - 1, sizeOri[1] - 1
        meshQW, meshQH = clamp(meshQW, max=mw), clamp(meshQH, max=mh)
        meshQ = []   # 對應一個像素要計算的元途中四個點
        for i in range(1, -1, -1):
            for j in range(1, -1, -1):
                w = meshQW[:, :, i]
                h = meshQH[:, :, j]
                meshQ.append(img[h, w].unsqueeze(2))
        meshQ = cat(meshQ, dim=2)
        a, b, c = meshQ.shape
        meshQ = meshQ.view(a, b, 2, 2).type(ft)
        temp = einsum('ijkl, ijlh->ijkh', x, meshQ)
        outputs = einsum('ijkl, ijfl->ijkf', temp, y).squeeze()
        return outputs.numpy().astype('uint8')
