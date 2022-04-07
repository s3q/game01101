from ast import And, arguments
import asyncio
import random
from time import sleep 
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import subprocess
import optparse
import threading 



    

root = Tk()
root.title("Pgame")
root.geometry('950x625') 
root.configure(bg="black")
root.state('zoomed')

# function to open images
def openImg(path):
    return ImageTk.PhotoImage(Image.open(path))



# this code bring the player's names from login window (main3.py)

parser = optparse.OptionParser()
parser.add_option("-o", "--player1", dest= "player1")
                      
parser.add_option("-x", "--player2", dest= "player2")

(options,arguments) = parser.parse_args()

##################################################################

# dictionary for players to store thier data
players = {
    "player0": {
        "scores": 0,
        "name": options.player1,
        "rdice": "_._._"
    },
    "player1": {
        "scores": 0,
        "name": options.player2,
        "rdice": "_._._"
    },
    "winer": None 
}

# dictionary for all the icons and images used in the programm 
icons = {
    "settings": openImg("./icons/settings.png"),
    "help": openImg("./icons/idea.png"),
    "user": openImg("./icons/user.png"),
    "players": {
        "p0": openImg("./icons/players/m0.png"),
        "p1": openImg("./icons/players/m2.png"),
    },
    "dice":{
        "dice": openImg("./icons/dice/dices.png"),
        "numbers": [],
        "next": openImg("./icons/dice/next.png"),
        "turn": [
            openImg("./icons/dice/turn/0.png"),
            openImg("./icons/dice/turn/1.png"),
        ]
    },
    "buttons": {
        "button_icont0": openImg("./buttons/m1.png"),
        "button_icont1": openImg("./buttons/m1.png"),
        "buttons_icon0": [],  
        "buttons_icon1": []  
    }
}


# for loop to append the disks's and dice's images to the icons dictionary 
for i in range(6):
    disks = openImg(f"./buttons/0{i+1}.png")
    icons["buttons"]["buttons_icon0"].append(disks)
    disks = openImg(f"./buttons/1{i+1}.png")
    icons["buttons"]["buttons_icon1"].append(disks)

    dicon = openImg(f"./icons/dice/numbers/{i+1}.png")
    icons["dice"]["numbers"].append(dicon)

hash_dicon = openImg(f"./icons/dice/numbers/hash.png")
icons["dice"]["numbers"].append(hash_dicon)


mouse_x = 0
mouse_y = 0




navbar = Label(root, bg="#313131")
navbar.pack(fill=X)

settings_button = Button(navbar, image=icons["settings"], bg="black", width=40, height=30, bd=0, activebackground="#404040")
settings_button.grid(row=0, column=0)

settings_button = Button(navbar, image=icons["help"], bg="black", width=40, height=30, bd=0, activebackground="#404040")
settings_button.grid(row=0, column=1)


settings_button = Button(navbar, image=icons["user"], bg="black", width=40, height=30, bd=0, activebackground="#404040")
settings_button.grid(row=0, column=2)

timerdev =  Label(root, text="0:0", font=("Arial", 25))
timerdev.pack()

###############
divheader = Label(root, bg="black")
divheader.pack(fill=X, padx=20, pady=20)

divfooter = Label(root, bg="black")
divfooter.pack(fill=X, side=BOTTOM, padx=20, pady=20)
################



player0_picture = Label(divheader, bg="black", image=icons["players"]["p0"])
player0_picture.pack(side=LEFT)

player1_picture = Label(divfooter, bg="black", image=icons["players"]["p1"])
player1_picture.pack(side=LEFT)

player0_label = Label(divheader, bg="black")
player0_label.pack(side=LEFT)

player1_label = Label(divfooter, bg="black")
player1_label.pack(side=LEFT)



player0_name = Label(player0_label, bg="black", fg="white", text=players["player0"]["name"],   font=("Arial", 25))
player0_name.grid(row=0 , column=0)

player1_name = Label(player1_label, bg="black", fg="white", text=players["player1"]["name"],   font=("Arial", 25))
player1_name.grid(row=0, column=0)

player0_scores = Label(player0_label, bg="black", fg="white", text=f"Scores: {players['player0']['scores']}",   font=("Arial", 14))
player0_scores.grid(row=1, column=0)

player1_scores = Label(player1_label, bg="black", fg="white", text=f"Scores: {players['player1']['scores']}",   font=("Arial", 14))
player1_scores.grid(row=1, column=0)





cardui0 = Label(divheader, bg="black")
cardui0.pack(side=RIGHT)


cardui_center = Label(root, bg="black", fg="white")
cardui_center.pack(fill=X, padx=100, pady=20)


cardui1 = Label(divfooter, bg="black")
cardui1.pack(side=RIGHT)

# for loop to postion the disks button 
for i in range(6):
    button_p01 = Button(cardui0, image=icons["buttons"]["buttons_icon0"][i], bg="black", activebackground="black", height=64, width=64, relief=GROOVE)
    button_p01.attr = {"index": f"0.0.{i+1}", "protection": False}
    button_p01.grid(row=0, column=i)
    button_p02 = Button(cardui0, image=icons["buttons"]["buttons_icon0"][i], bg="black", activebackground="black", height=64, width=64, relief=GROOVE)
    button_p02.attr = {"index": f"1.0.{i+1}", "protection": False}
    button_p02.grid(row=1, column=i)

    button_p11 = Button(cardui1, image=icons["buttons"]["buttons_icon0"][i], bg="black", activebackground="black", height=64, width=64, relief=GROOVE)
    button_p11.attr = {"index": f"0.1.{i+1}", "protection": False}
    button_p11.grid(row=0, column=i)
    button_p12 = Button(cardui1, image=icons["buttons"]["buttons_icon0"][i], bg="black", activebackground="black", height=64, width=64, relief=GROOVE)
    button_p12.attr = {"index": f"1.1.{i+1}", "protection": False}
    button_p12.grid(row=1, column=i)



# check if the botton is located in the players lables to determine if it disk or not 
def findL(st, li):
    
    for l in li:
        #if str(".!label4.!button11").lower().find("") < 0: 
        if str(st).lower().find(l) < 0: 
            return False
    return True
# check if the clicked disk is in the dice's list 
def findS(st, li):
    i = 0
    for l in li:
        if str(st).lower().find(str(l)) >= 0: 
            return [True, i]
        i += 1
    return [False, i]

all_widgets = []

# append all widgets in one list
# 1 
def getAllWidgets(widget):
    for c in widget:
        all_widgets.append(c)
        if isinstance(c, str):
            continue
        if len(c.children.values()) == 0:
            continue
        getAllWidgets(c.children.values())

getAllWidgets(root.children.values())
print(all_widgets)


# return the widget postion (xstart, ystart)
def widgetPositionStart(widget):
    return widget.winfo_rootx() - root.winfo_rootx(), widget.winfo_rooty() - root.winfo_rooty()

# return the widget postion (xend, yend)
def widgetPositionEnd(widget):
    return widget.winfo_rootx() - root.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() - root.winfo_rooty() + widget.winfo_height()

def selectByPosation(x, y, widgets_name):

#check if the botton is located in players label for loop for check the botton of each players. 
    def wN(wns):
        for widget_name in wns: # label2.button -> ["label2", "button"]
           
            if findL(widget.__str__(), widget_name.split(".")):
                return True
        return False


    # determine the clicked button
    for widget in all_widgets:
        if wN(widgets_name):
            xs, ys = widgetPositionStart(widget)
            xe, ye = widgetPositionEnd(widget)
            if  xs < x < xe and ys < y < ye:
                
                return widget
    
    return None

# determine the mouse coordinates acoording to the game window
def motion(e):
    global mouse_x, mouse_y
    mouse_x = root.winfo_pointerx() - root.winfo_rootx()
    mouse_y = root.winfo_pointery() - root.winfo_rooty()


# update the values in motion function 
root.bind("<Motion>", motion)




round_status = {
    "finished": True, #is not used 
    "round": 1, # for round counting
    "start_from": 0, # which player will be start and it is value in first game equal for cycle 
    "cycle": 0, # which player play now [ 0 or 1 ] 
    "play": 0, # this for how many times did the player play, and it should dont increse than 3 
    "timer": 0
}


round_timer ={
    "timer": 5,
    "turn_status": False
}

Label(cardui_center, bg="black", text="                               ").grid(row=0, column=1)


pdrandom0 = Label(cardui_center, bg="black", image=icons["dice"]["numbers"][6])
pdrandom0.grid(row=0, column=2)

pdrandom1 = Label(cardui_center, bg="black", image=icons["dice"]["numbers"][6])
pdrandom1.grid(row=0, column=3)

pdrandom2 = Label(cardui_center, bg="black", image=icons["dice"]["numbers"][6])
pdrandom2.grid(row=0, column=4)


Label(cardui_center, bg="black", text="                               ").grid(row=0, column=5)

pdturn = Label(cardui_center, bg="black", image=icons["dice"]["turn"][round_status["cycle"]])
pdturn.grid(row=0, column=6)


# the dice function
def fdice():
    # asyncio.run(timer(10))
    
      
    countdown_thread = threading.Thread(target=playTimer) 
    countdown_thread.start()

    n1 = random.randint(1,6)
    n2 = random.randint(1,6)
    n3 = random.randint(1,6)
    pdrandom0.configure(image=icons["dice"]["numbers"][int(n1)-1])
    pdrandom1.configure(image=icons["dice"]["numbers"][int(n2)-1])
    pdrandom2.configure(image=icons["dice"]["numbers"][int(n3)-1])

    players["player"+str(round_status["cycle"])]["rdice"] = f"{n1}.{n2}.{n3}" #########

    bdice.configure(state="disable") # disable the dice after the thrown
    round_status["finished"] = False
    

# dice button 


# # @unsync

# change cycle between 0 and 1
def toggle(va, l1, l2):
    if va == l1:
        va = l2
    elif va == l2:
        va = l1
    return va

def fiplay():
    round_status["play"] += 1
def rejoinC_rdice(ind, adds):
    # 1.4.6
    # ind:index = 0 - 2  
    # ind:index = 0 - 2  
    if ind != len(players["player"+str(round_status["cycle"])]["rdice"].split("."))-1: 
        return adds
    else: 
        return ""

# this function wipe the previuse values of dice and move thr turn to the second player and 
def next_play():
    round_timer["turn_status"] = True
    timerdev.configure(text=f"0:0")

    players["player"+str(round_status["cycle"])]["rdice"] = f"_._._"
    pdrandom0.configure(image=icons["dice"]["numbers"][6])
    pdrandom1.configure(image=icons["dice"]["numbers"][6])
    pdrandom2.configure(image=icons["dice"]["numbers"][6])

    round_status["play"] = 0

    # toggle btween tow values (0, 1) for change player turn
    round_status["cycle"] = toggle(round_status["cycle"], 0, 1)

    pdturn.configure(image=icons["dice"]["turn"][round_status["cycle"]])

    # print(round_status["cycle"])
    bdice.configure(state="normal")

    if round_status["start_from"] == round_status["cycle"]: #if the round_status["cycle"] return to the frist player, add one to the round_status["round"](the two players have already played)
        # round_status["finished"] = True
        round_status["round"] += 1


pdnext = Button(cardui_center, bg="black", border=0, image=icons["dice"]["next"], command=next_play)
pdnext.grid(row=0, column=7)

def playTimer():
    round_timer["timer"] = 5
    round_timer['turn_status'] = False
    

    for x in range(5):
        timerdev.configure(text=f"0:{round_timer['timer'] - 1}")
        sleep(1)
        round_timer["timer"] -= 1
        
        if round_timer["timer"]==0 and round_timer['turn_status'] == False:
            next_play()
        elif round_timer['turn_status'] == True: 
            return             



bdice = Button(cardui_center, bg="black", activebackground="black", border=0, image=icons["dice"]["dice"], command=fdice)
bdice.grid(row=0, column=0)

            
def play_again():
    round_status = {
        "finished": True, #is not used 
        "round": 1, # for round counting
        "start_from": 0, # which player will be start and it is value in first game equal for cycle 
        "cycle": 0, # which player play now [ 0 or 1 ] 
        "play": 0, # this for how many times did the player play, and it should dont increse than 3 
        "timer": 0
    }
        
    round_timer ={
        "timer": 5,
        "turn_status": False
    }


# this function include the game's rules 
def clicked(e):
   
    widget = selectByPosation(mouse_x, mouse_y, ["label3.button", "label2.button"])
    if widget != None:
        if widget.attr:
            # this value widget.attr["index"].split(".")[2] for disk number
            #check_target return [True, index -> for the place disk number in dice list] (check if click on disk has appeared in dice list when throwing a dice ) 
            check_target = findS(int(widget.attr["index"].split(".")[2]), players["player"+str(round_status["cycle"])]["rdice"].split("."))
            
            if round_status["play"] < 3 and check_target[0]: # check if players didn't play more than 3 times and he clicked in right disk
                pplay = round_status["play"]

                # if was player clicked on one of his disks and he have turn and not the disk not protected then will be protect it 
                # then make it disable   
                if int(widget.attr["index"].split(".")[1]) == round_status["cycle"] and not widget.attr["protection"]:
                    widget.attr["protection"] = True
                    round_status["play"] += 1
                    widget.configure(state=DISABLED)
                    
                # check if players play more than one round 
                if round_status["round"] > 1:
                    if int(widget.attr["index"].split(".")[1]) != round_status["cycle"]:
                        # print(widget.attr["protection"])
                        if widget.attr["protection"]:
                            widget.attr["protection"] = False
                            widget.configure(state="normal")
                        else:
                            widget.configure(image=icons["buttons"][f"button_icont{str(round_status['cycle'])}"])
                            #
                            players["player"+str(round_status["cycle"])]["scores"] += int(widget.attr["index"].split(".")[2]) 
                        round_status["play"] += 1

                if round_status["play"] > pplay :
                    players["player"+str(round_status["cycle"])]["rdice"] = "".join([f"{str(v)+rejoinC_rdice(i, '.')}" for i, v in enumerate(players["player"+str(round_status["cycle"])]["rdice"].split(".")) if i != check_target[1] ])
                    print(players["player"+str(round_status["cycle"])]["rdice"])


        
            if round_status["play"] == 3 or len(players["player"+str(round_status["cycle"])]["rdice"].split(".")) == 0:
                next_play()
                
               
             

            player0_scores.configure(text=f"Scores: {players['player0']['scores']}")
            player1_scores.configure(text=f"Scores: {players['player1']['scores']}")

            win()
            




def win():

    if (players['player1']['scores'] >= 10 or players['player0']['scores'] >= 10):
        if players['player1']['scores'] > players['player0']['scores']:
            players["winer"] = 1
        if players['player0']['scores'] > players['player1']['scores']:
            players["winer"] = 0

        if players["winer"] != None:
            bplay_again = messagebox.askquestion("win", f"Fuck you {players['player'+str(players['winer'])]['name']}, you are winer ! \n do you want to play again ?")
            print(bplay_again)



root.update()

root.bind("<ButtonRelease>", clicked)

root.mainloop()
