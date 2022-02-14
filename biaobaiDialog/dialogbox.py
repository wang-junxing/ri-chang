
#coding=utf-8
import tkinter
import tkinter.messagebox
import random

# pip install pillow
from PIL import Image, ImageTk
import time

class App:
    def __init__(self, root):

        self.root = root

        self.root.title("")
        self.root.geometry("600x600+600+300")

        self.canClose=False

        global image ,photo
        image = Image.open('biu.png')
        photo = ImageTk.PhotoImage(image)
        self.image1 = tkinter.Label(root, anchor='center',text="做我女朋友好吗?",fg='pink',font=('宋体',30))
        self.image1.place(x=150,y=10)

        self.label = tkinter.Label(root, anchor='center',image = photo)
        self.label.place(x=137,y=98)

        self.Hover1 = tkinter.Button(root,text="同意", font=('宋体',55),bg="SystemButtonFace" ,command=self.ok)
        self.Hover1.place(x=100,y=400)

        self.Hover2 = tkinter.Button(root,text="不同意",  font=('宋体',30),bg="SystemButtonFace")
        self.Hover2.bind("<Enter>", self.OnMouseEnter)
        self.Hover2.place(x=358,y=445)

        self.root.protocol("WM_DELETE_WINDOW",self.close)

        
    def ok(self):
        self.Hover2.place(x=358,y=445)
        if tkinter.messagebox.showwarning("恭喜", "这就对了了嘛!我们终于可以在一起了~~"):
            if tkinter.messagebox.showwarning("通知", "不要彩礼吧?"):
                self.canClose=True
                self.close()

    def close(self):
        if self.canClose :
            self.root.destroy()
        else:
            tkinter.messagebox.showerror("警告", "不同意不让你走!!!")

    def OnMouseEnter(self, event):
        x = random.randint(0,600-150)
        y = random.randint(0,600)
        #print(x,y)
        self.Hover2.place(x=x,y=y)

root=tkinter.Tk()
app = App(root)
root.mainloop()