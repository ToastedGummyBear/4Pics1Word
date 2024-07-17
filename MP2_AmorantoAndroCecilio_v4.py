from tkinter import *
from tkinter import messagebox
import random

num = 0
val = 100

try:
    player_file = open("Player_Progress.txt","r")
    progress = player_file.read().split(",")
    num = int(progress[0]) 
    val = int(progress[1]) 
    player_file.close()
except:
    player_file = open("Player_Progress.txt","w")
    player_file.write(str(num))
    player_file.write(str(val))

            
class Window(Frame):
    def __init__(self,*arg,**kw):
        super().__init__(*arg,**kw)
        self.topframe()
        self.image()
        self.answer_box()
        self.jumbled_letters()
        self.filename = "Player_Progress.txt"


    def topframe(self):
        global num
        global val
        top_frame = Frame(self, bg = "blue")
        self.level_indicator = Label(top_frame, text = "Level:"+str(num+1),font = "Arial 20 bold", fg = "white", bg = "blue")
        self.coin = Label(top_frame, text = val, font = "Arial 20 bold", fg = "white", bg = "blue")
        self.img = PhotoImage(file = "coin.png")
        self.coin_img = Label(top_frame,image = self.img, bg = "blue")
        self.level_indicator.pack(side = LEFT)
        self.coin.pack(side = RIGHT)
        self.coin_img.pack(side = RIGHT)
        top_frame.pack(ipadx = 500, ipady = 10)


    def image(self):
        global num
        image_frame = Frame(self)
        img = open("picList.txt","r")
        img_read = img.readlines()
        self.pic = list()
        for data in img_read:
            name = data.strip().split(";")
            self.pic.append(name[1])

        self.picture = PhotoImage(file = self.pic[num]+".png")
        picture = Label(image_frame, image = self.picture)
        picture.pack()
        image_frame.pack()


    def answer_box(self):
        global num
        self.answer_frame = Frame(self)
        self.box = [None for _ in range(len(self.pic[num]))]
        for boxes in range(len(self.pic[num])):
            self.box[boxes] = Button(self.answer_frame,width = 5, height = 3, relief = RAISED, bg = "light grey", command = lambda boxes=boxes:self.remove_letter(boxes))
            self.box[boxes].pack(side = LEFT, pady = 5)
        self.answer_frame.pack()
        
        
    def jumbled_letters(self):
        global num
        self.ans_btn = [None for _ in range(12)]
        self.jum_frame1 = Frame(self)
        self.jum_frame2 = Frame(self)
        self.answers = self.pic[num].upper()
        self.letters = "QWERTYUIOPASDFGHJKLZXCVBNM"
        self.log = list()     
        x = 0
        for data in self.answers:
            self.log.append(data)

        while x < 12 - len(self.answers):
            info = str(random.choice(self.letters))
            if info in self.log:
                continue
            else:
                self.log.append(info)
            x+=1
        random.shuffle(self.log)

        for i in range(12):
            if i<6:
                self.ans_btn[i] = Button(self.jum_frame1,width = 5, height = 3, text =self.log[i],relief = RAISED, command = lambda i=i:self.add_letter(i))
                self.ans_btn[i].pack(side = LEFT,pady = 5)
            else:
                self.ans_btn[i] = Button(self.jum_frame2,width = 5, height = 3, text = self.log[i],relief = RAISED, command = lambda i=i:self.add_letter(i))
                self.ans_btn[i].pack(side = LEFT,pady = 5)
                
        self.hint_img = PhotoImage(file = "hint.png")
        self.hint_btn = Button(self.jum_frame1, image = self.hint_img, command = self.hint_cmd, relief = FLAT)
        self.hint_btn.pack(ipadx = 5, ipady = 6, pady = 5, padx = 5)
        self.pass_img = PhotoImage(file = "pass.png")
        self.pass_btn = Button(self.jum_frame2, image = self.pass_img, command = self.pass_level, relief = FLAT)
        self.pass_btn.pack(ipadx = 5, ipady = 8, pady = 5, padx = 5)
        self.jum_frame1.pack()
        self.jum_frame2.pack()


    def pass_level(self):
        global num
        global val
        val-=10
        num+=1
        if num == 50:
            num = 0
        self.picture.config(file = self.pic[num]+".png")
        self.level_indicator.config(text = "Level:"+str(num+1),font = "Arial 20 bold", fg = "white", bg = "blue")
        self.coin.config(text = val, font = "Arial 20 bold", fg = "white", bg = "blue")
        for frame in self.box:
            frame.destroy()
        for frame in self.ans_btn:
            frame.destroy()
        self.answer_frame.destroy()
        self.jum_frame1.destroy()
        self.jum_frame2.destroy()
        self.answer_box()
        self.jumbled_letters()
        self.player_progress()
        if val <=0:
            messagebox.showerror("Error","You have no coin.")
            self.pass_btn.config(state = DISABLED)
            self.hint_btn.config(state = DISABLED)

    def next_level(self):
        global num
        global val
        val+=10
        num+=1
        if num == 50:
            num = 0
        self.picture.config(file = self.pic[num]+".png")
        self.level_indicator.config(text = "Level:"+str(num+1),font = "Arial 20 bold", fg = "white", bg = "blue")
        self.coin.config(text = val, font = "Arial 20 bold", fg = "white", bg = "blue")            
        for frame in self.box:
            frame.destroy()     
        for frame in self.ans_btn:
            frame.destroy()
        self.answer_frame.destroy()
        self.jum_frame1.destroy()
        self.jum_frame2.destroy()
        self.answer_box()
        self.jumbled_letters()
        self.player_progress()


    def hint_cmd(self):
        global num
        global val
        val-=2
        letter = self.pic[num].upper()
        self.coin.config(text = val, font = "Arial 20 bold", fg = "white", bg = "blue")
        for i in range(len(self.box)):
            if self.box[i]["text"] == "":
                self.box[i].config(text = letter[i])
                self.ans_btn[i].config(text = "")
                if self.box[i]["text"] == letter[i]:
                    self.ans_btn[i].config(text = "")
                    print(self.box[i]["text"])
                    break

                else:
                    continue
        empty = ""
        
        for letters in self.box:
            empty = empty+letters["text"]
        if empty == self.pic[num].upper():
            self.next_level()


    def add_letter(self,counter):
        global num
        for i in range(len(self.box)):
            if self.box[i]["text"] == "":
                self.box[i].config(text = self.ans_btn[counter]["text"])
                self.ans_btn[counter].config(text = "")
                
                
                
                
                break
            else:
                continue
        empty = ""
        for letters in self.box:
            empty = empty+letters["text"]
        if empty == self.pic[num].upper():
            self.next_level()
        elif len(empty) != len(self.pic[num].upper()):
            self.remove_redbg()
        elif len(empty) == len(self.pic[num].upper()):
            self.wrong_answer()

            


    def remove_letter(self,boxes):
            
        for i in range(len(self.ans_btn)):
            
            if self.ans_btn[i]["text"] == "":
                self.ans_btn[i].config(text = self.box[boxes]["text"])
                break
            else:
                continue
     
        self.box[boxes].config(text = "")
        self.remove_redbg()

    def wrong_answer(self):
        for i in range(len(self.box)):
            if len(self.box) == len(self.pic[num].upper()):
                self.box[i].config(bg = "salmon")

    def remove_redbg(self):
        for i in range(len(self.box)):
            if len(self.box) == len(self.pic[num].upper()):
                self.box[i].config(bg = "light grey")


    def player_progress(self):
        global num
        global val
        try:
            data = open(self.filename, "w")

        except FileNotFoundError:
            data = open(self.filename,"w")
            
        else:
            data.write("{},{},{}".format(num,val,self.pic[num]))
            data.close()


root = Tk()
root.title("4 Pics 1 Word")
root.geometry("500x600")
#root.config(bg = "#1D2951")
main = Window(root)
main.pack()
#main.config(bg = "#1D2951")
root.mainloop()
        




