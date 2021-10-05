import tkinter as tk
from tkinter import filedialog, dialog
from PIL import ImageTk,Image
import numpy as np
import utils
import os

class UI_Window:
    def __init__(self, name='UI'):
        self.name = name
        self.window = tk.Tk()
        self.transfer = utils.Pic_Transformations()

        self.window.title('image transfers')
        self.window.geometry('1200x700')
        self.canvas = tk.Canvas(self.window, width=1200, height=630, bg="white")
        self.canvas.place(x=0, y=70)

        self.label = tk.Label(self.window, text='請輸入參數:')
        self.label.place(x=580, y=0)

        self.parameter = tk.Text(self.window, width=20, height=1)
        self.parameter.place(x=580, y=20)

        self.bt1 = tk.Button(self.window, text='開啟圖片', width=10, height=2, command=self.open_img)
        self.bt1.place(x=0, y=0)

        self.bt2 = tk.Button(self.window, text='log', width=10, height=2, command=self.transfer_funs('log'))
        self.bt2.place(x=80, y=0)

        self.bt3 = tk.Button(self.window, text='gamma', width=10, height=2, command=self.transfer_funs('gamma'))
        self.bt3.place(x=160, y=0)

        self.bt4 = tk.Button(self.window, text='nagative', width=10, height=2, command=self.transfer_funs('negative'))
        self.bt4.place(x=240, y=0)

        self.bt5 = tk.Button(self.window, text='bilinear', width=10, height=2, command=self.transfer_funs('bilinear'))
        self.bt5.place(x=320, y=0)

        self.bt6 = tk.Button(self.window, text='nearest', width=10, height=2, command=self.transfer_funs('nearest'))
        self.bt6.place(x=400, y=0)

        self.bt7 = tk.Button(self.window, text='儲存圖片', width=10, height=2, command=self.save_img)
        self.bt7.place(x=480, y=0)

        self.img = None

    def open_img(self):
        imgPath = filedialog.askopenfile(mode='r')
        fileType = imgPath.name.split('.')[-1]
        if fileType == 'raw':
            img = np.fromfile(imgPath.name, dtype=np.uint8).reshape(512, 512)
            self.img = Image.fromarray(img)
        
        else:
            self.img = Image.open(imgPath.name)
    
        imgCanvas = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=imgCanvas)
        self.canvas.image = imgCanvas

    def save_img(self):
        imgPath = filedialog.asksaveasfile()
        path = imgPath.name
        self.img.save(path)

    def transfer_funs(self, t):
        def transfer_fun():
            if t == 'log':
                trans = self.transfer.log_transformation
                para = {'c': float(self.parameter.get(1.0, tk.END))}

            if t == 'gamma':
                trans = self.transfer.gamma_correction
                para = {'gamma': float(self.parameter.get(1.0, tk.END))}

            if t == 'negative':
                trans = self.transfer.image_nagative
                para = {'L': 256}

            if t == 'bilinear':
                trans = self.transfer.bilinear_transform
                p = self.parameter.get(1.0, tk.END).split(',')
                p = list(map(int, p))
                para = {'size': p}

            if t == 'nearest':
                trans = self.transfer.nearest_transform
                p = self.parameter.get(1.0, tk.END).split(',')
                p = list(map(int, p))
                para = {'size': p}

            img = np.asarray(self.img).astype('float')
            img = trans(img, **para)
            self.img = self.transfer.to_image(img)
            imgCanvas = ImageTk.PhotoImage(self.img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgCanvas)
            self.canvas.image = imgCanvas
        
        return transfer_fun

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    window = UI_Window()
    window.run()