#!/usr/bin/env python3
import random, d20, json
import jsonpickle
from json import JSONEncoder

def display_dice(dice,highest,lowest):
    y=3
    z=0

    for x in range(6):
        print("Group: {0}, Dice: {1}, Total {2}".format(x,dice[z:y], sum(dice[z:y])))
        z=y
        y=y+3

    print
    print("Lowest Dice {0}, Total {1} , Highest Dice {2}, Total {3}".format(lowest,sum(lowest),highest,sum(highest)))

def roll_dice(dice):

    random.shuffle(dice)
    y=3
    z=0

    lowest=dice[z:y]
    highest=dice[z:y]


    for x in range(6):
        if sum(lowest) <= sum(dice[z:y]):
            lowest=dice[z:y]
        if sum(highest) >= sum(dice[z:y]):
            highest=dice[z:y]

        z=y
        y=y+3

    return(dice,lowest,highest)





def hp_level_classic(hd, current_hp, con):
    result=hp_roll(hd,con)
    return result+current_hp


def hp_level_swn(lvl, hd, current_hp, con):
    # To determine their new maximum hit points, roll a number of hit dice 
    # equal to their new level, adding their Constitution modifier to each one.
    # A negative CON modifier can’t lower a die’s result below 1. 
    # If the total is greater than their current hit points, they take this new total. 
    # Otherwise, their current maximum hit points increase by one.
    # First level characters get their max hit points + CON modifier 

    if lvl ==1:
        return int(hd[1:])+attribute_mod(con)
    total = 0
    for x in range(lvl):
        result=hp_roll(hd,con)
        total=total+result
    if total > current_hp:
        return total
    return current_hp+1
        

class Dice():

    def attribute_mod(self,attribute):
       if attribute == 3:
           return -3
       if attribute in [4,5]:
           return -2
       if attribute in [6,7,8]:
           return -1
       if attribute in [9,10,11,12]:
           return 0
       if attribute in [13,14,15]:
           return 1
       if attribute in [16,17]:
           return 2
       if attribute == 18:
           return 3

    def hp_roll(self):
        hd = self.characterClass.hitdice

        result=d20.roll("1" +hd).total + self.attribute_mod(self.consitution)
        if result < 1:
            return 1
        return result


    def generate_attributes_classic(self):
        for stat in ("strength","dexterity","intelligence","wisdom","consitution","charisma"):
            setattr(self,stat,d20.roll("3d6").total)
  
    def generate_attributes_houserule1(self):
        for stat in ("strength","dexterity","intelligence","wisdom","consitution","charisma"):
            setattr(self,stat,d20.roll("4d6kh3").total)

    def generate_attributes_houserule2(self):
        for stat in ("strength","dexterity","intelligence","wisdom","consitution","charisma"):
            setattr(self,stat,d20.roll("2d6+6").total)

class CharClass():
    def __init__(self, *args, **kwargs):
       for key in kwargs:
             setattr(self, key, kwargs[key])

class ClassMgr():
    def __init__(self):
        self.classdata={}

        with open('Config/classes.json') as json_file:
           class_list = json.load(json_file)

           for classname in class_list['classes']:
               class_json={}
               try:
                  with open('Config/class_' + classname + '.json') as json_file:
                       class_json = json.load(json_file)
               except OSError as e:
                 pass

               if (class_json):
                    self.classdata[classname]=CharClass(**class_json)

class Character(Dice):
    def __init__(self, name=None, player_class=None, size=None, alignment=None, ac=None, hp=None,
                 speed=None, strength=None, dexterity=None, intelligence=None, wisdom=None,
                 consitution=None, charisma=None, inventory=[], r_ring=None, l_ring=None,
                 shield=None, armor=None, level=None,xp=None):

                 self.name=name
                 self.player_class=player_class
                 self.size = size
                 self.alignmnet=alignment
                 self.ac=ac
                 self.hp=hp
                 self.strength=strength
                 self.dexterity=dexterity
                 self.intelligence=intelligence
                 self.wisdom=wisdom
                 self.consitution=consitution
                 self.charisma=charisma
                 self.r_ring=r_ring
                 self.l_ring=l_ring
                 self.sheield=shield
                 self.armor=armor
                 self.level=level
                 self.xp=xp
   
    def set_class(self,classOBJ):
        self.characterClass = classOBJ
        self.player_class = self.characterClass.classname

    def save_character(self):
        with open("Save/" + self.name + ".json","w") as fh:
            fh.write(jsonpickle.encode(self))

    def roll_hp(self):
        self.hp=self.hp_roll()

class Display():
    def __init__(self):
        pass

    def display_attributes(playerObj):
        
        for stat in ("strength","dexterity","intelligence","wisdom","consitution","charisma"):
            print("{}: : {}".format(stat[:3].upper(),getattr(playerObj, stat)))
 
        print()
        print("HP: {}".format(playerObj.hp))


def main():
  classes = ClassMgr()

  with open("Save/Spiffy.json","r") as fh:
            test_obj = jsonpickle.decode(fh.read())

  test_obj.roll_hp()
  display=Display.display_attributes(test_obj)
  print(test_obj.characterClass.classname)


  #new_guy=Character("Spiffy",level=1)
  #new_guy.generate_attributes_classic() 

  #new_guy.set_class(classes.classdata['Elf'])
  #new_guy.roll_hp()

  #print(new_guy.characterClass.level_progression['1'])
  #print(new_guy.player_class)
  #display=Display.display_attributes(new_guy) 
  #print(new_guy.save_character())

if __name__ == "__main__":
    main()
