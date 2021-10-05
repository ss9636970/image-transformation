import numpy as np
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
        img = inputs
        sizeOri = np.array(img.shape)
        size = np.array(size)
        adjLen = (sizeOri - 1) / (size - 1)
        height = np.arange(size[0]) * adjLen[0]
        width = np.arange(size[1]) * adjLen[1]
        meshH, meshW = np.meshgrid(height, width)
        meshH, meshW = meshH.transpose(), meshW.transpose()
        meshHI, meshWI = np.floor(meshH), np.floor(meshW)       # 轉化後像素點的整數部分(對應原圖左邊或上方的點)
        meshWL = meshW - meshWI         # x 的第一個元素
        meshHL = meshH - meshHI         # y 的第一個元素
        meshWR = 1 - meshWL             # x 的第二個元素
        meshHR = 1 - meshHL
        x = np.concatenate([np.expand_dims(meshWL, axis=2), np.expand_dims(meshWR, axis=2)], axis=2)
        x = np.expand_dims(x, axis=2)
        y = np.concatenate([np.expand_dims(meshHL, axis=2), np.expand_dims(meshHR, axis=2)], axis=2)
        y = np.expand_dims(y, axis=2)
        meshQW = np.concatenate([np.expand_dims(meshWI, axis=2), np.expand_dims(meshWI+1, axis=2)], axis=2).astype('long')   # index 要求 Q 用的
        meshQH = np.concatenate([np.expand_dims(meshHI, axis=2), np.expand_dims(meshHI+1, axis=2)], axis=2).astype('long')
        mh, mw = sizeOri[0] - 1, sizeOri[1] - 1
        meshQW, meshQH = np.clip(meshQW, a_max=mw, a_min=0), np.clip(meshQH, a_max=mh, a_min=0)
        meshQ = []   # 對應一個像素要計算的元途中四個點
        for i in range(1, -1, -1):
            for j in range(1, -1, -1):
                w = meshQW[:, :, i]
                h = meshQH[:, :, j]
                meshQ.append(np.expand_dims(img[h, w], axis=2))

        meshQ = np.concatenate(meshQ, axis=2)
        a, b, c = meshQ.shape
        meshQ = meshQ.reshape([a, b, 2, 2]).astype('float')
        temp = np.einsum('ijkl, ijlh->ijkh', x, meshQ)
        outputs = np.einsum('ijkl, ijfl->ijkf', temp, y).squeeze()
        return outputs.astype('uint8')

    def nearest_transform(self, inputs, size=[600, 1100]):
        img = inputs
        sizeOri = np.array(img.shape)
        size = np.array(size)
        adjLen = (sizeOri - 1) / (size - 1)
        height = np.arange(size[0]) * adjLen[0]
        width = np.arange(size[1]) * adjLen[1]
        meshH, meshW = np.meshgrid(height, width)
        meshH, meshW = meshH.transpose(), meshW.transpose()
        meshHI, meshWI = np.floor(meshH), np.floor(meshW)       # 轉化後像素點的整數部分(對應原圖左邊或上方的點)
        meshWL = ((meshW - meshWI) > 0.5) + 0.         # x 的第一個元素
        meshHL = ((meshH - meshHI) > 0.5) + 0.         # y 的第一個元素
        meshWR = 1 - meshWL             # x 的第二個元素
        meshHR = 1 - meshHL
        x = np.concatenate([np.expand_dims(meshWL, axis=2), np.expand_dims(meshWR, axis=2)], axis=2)
        x = np.expand_dims(x, axis=2)
        y = np.concatenate([np.expand_dims(meshHL, axis=2), np.expand_dims(meshHR, axis=2)], axis=2)
        y = np.expand_dims(y, axis=2)
        meshQW = np.concatenate([np.expand_dims(meshWI, axis=2), np.expand_dims(meshWI+1, axis=2)], axis=2).astype('long')   # index 要求 Q 用的
        meshQH = np.concatenate([np.expand_dims(meshHI, axis=2), np.expand_dims(meshHI+1, axis=2)], axis=2).astype('long')
        mh, mw = sizeOri[0] - 1, sizeOri[1] - 1
        meshQW, meshQH = np.clip(meshQW, a_max=mw, a_min=0), np.clip(meshQH, a_max=mh, a_min=0)
        meshQ = []   # 對應一個像素要計算的元途中四個點
        for i in range(1, -1, -1):
            for j in range(1, -1, -1):
                w = meshQW[:, :, i]
                h = meshQH[:, :, j]
                meshQ.append(np.expand_dims(img[h, w], axis=2))

        meshQ = np.concatenate(meshQ, axis=2)
        a, b, c = meshQ.shape
        meshQ = meshQ.reshape([a, b, 2, 2]).astype('float')
        temp = np.einsum('ijkl, ijlh->ijkh', x, meshQ)
        outputs = np.einsum('ijkl, ijfl->ijkf', temp, y).squeeze()
        return outputs.astype('uint8')
