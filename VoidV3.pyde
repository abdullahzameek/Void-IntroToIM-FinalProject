add_library('serial')
add_library('sound')

import os, random,time, processing
path=os.getcwd()         #will give you the relative path of the file

class Game:
  def __init__(self,w,h,g):
    self.w=w #width
    self.h=h #height 
    self.g=g #ground level
    self.hero=Hero(100,100,32,self.g,"player sheet1.png",64,64,6) #There are four total frames
    self.music=SoundFile(this,path+'/openWorld2.mp3') # windows '\\'
    #self.music.play() #We put it here so that the music will only play once
    self.x = 0 #The position in the screen, it begins at zero
    self.pause=False
    self.pauseSound=SoundFile(this,path+'/pauseSound.mp3')
    self.state='menu'
    self.name=""
    self.stage=1
    self.menuImg = loadImage(path + "/MenuScreen.png")
    self.menuMusic = SoundFile(this,path + '/menu.mp3')
    self.bossTheme  = SoundFile(this, path + '/boss.mp3')
    self.victory = SoundFile(this,path + '/victory.mp3')
    self.enemiesKilled = SoundFile(this,path+ '/enemiesKilled.mp3')
    self.menuMusic.play()
    self.mnStnMusic = SoundFile(this, path +'/moonStone.mp3')
    self.loadStage()
    self.restore = SoundFile(this, path + '/moonstone.mp3')
    self.nextStageImg = loadImage(path+'/arrow.png')
    
  def loadStage(self): #loads the resources that are responsible for each stage

    self.platforms=[]
    self.enemies=[]
    self.bg=[]    #to store the images of the background
    self.potions = []
    self.ending = []
    
    for i in range(1,2): #We will store 5 layers of the background
      self.bg.append(loadImage(path+'/layer_0'+str(i)+'.png'))
    f = open(path+'/stage'+str(self.stage)+'.csv',"r") #open the stage

    for l in f: #for line in f        the for loop automatically reads through the file line by line
      l=l.strip().split(",") #make it into a list
        
      if l[0]=='Platform':
        self.platforms.append(Platform(int(l[1]),int(l[2]),int(l[3]),int(l[4])))
      elif l[0]=='Silverbat':
        self.enemies.append(Silverbat(int(l[1]),int(l[2]),int(l[3]),int(l[4]),l[5],int(l[6]),int(l[7]),int(l[8])))
      elif l[0]=='Tonberry':
        self.enemies.append(Tonberry(int(l[1]),int(l[2]),int(l[3]),int(l[4]),l[5],int(l[6]),int(l[7]),int(l[8])))
      elif l[0]=='Bahamut':
        self.enemies.append(Bahamut(int(l[1]),int(l[2]),int(l[3]),int(l[4]),l[5],int(l[6]),int(l[7]),int(l[8])))
      elif l[0] == 'Splash':
        self.ending.append(Ending(l[1],int(l[2]),int(l[3]),int(l[4]),int(l[5])))
      elif l[0]=='Potion':
        self.potions.append(Potion(int(l[1]),int(l[2]),int(l[3]),int(l[4]),l[5],int(l[6]),int(l[7]),int(l[8])))
    f.close()
    
    
        
    
    
#     self.enemies.append(Gomba(random.randint(200,self.w),random.randint(100,400),35,self.g,"gomba.png",70,70,5))   #for loop allows each gomba to be regularly spaced apart   #radius half of width and height
#     self.platforms.append(Platform(500,400,200,52))
#     self.stars.append(Star(300+i*50,300+i*50,20,self.g,"star.png",40,40,6)) 

    
  def display(self):          #first display the background and then the remaining stuff
    if self.state == 'menu':
       image(self.menuImg,0,0,self.w,self.h)

    elif self.state=='play':
        self.menuMusic.stop()
        # for i in range(len(self.bg)):
        #     try:
        #         x = (self.x//(5-2*i))%self.w  # a modular operator that keeps on reiterating the screen over and over, each image will have a different velocity
        #     except:
        x = self.x%self.w #Move at the speed of hero

        image(self.bg[0],0,0,self.w-x,self.h,x,0,self.w,self.h) #Checkered area
        # image(self.bg[0],self.w-x-2,0,x,self.h,0,0,x,self.h) #Dashed area, we subtracted one so that the extra pixel would not ruin the image
        #image(self.bg[-i-1],0-self.x,0) #We want to print the images in reversed order, 0 0 is the x and y location
    
        for p in self.platforms:
            p.display()
        
        self.hero.display()
        
        for e in self.enemies:
            e.display()

        for p in self.potions:
            p.display()
            
        for ed in self.ending:
            ed.display()
            
    
  
class Chara: 
  def __init__(self,x,y,r,g,img,w,h,F):
    self.x=x
    self.y=y
    self.vx=0
    self.vy=0
    self.w=w
    self.h=h
    self.F=F #frames, 
    self.f=0 #current frame
    self.r=r #radius let's think of the character as a circle for collison detection
    self.g=g
    self.dir=1 #If the direction is 1, hero is facing right
    self.img=loadImage(path+'/'+img) # windows '\\'
  
  def gravity(self):          #since both the gomba and hero share gravity, we keep the platform here
    if self.y+self.r < self.g:#If he is higher than his absolute ground, he falls
      self.vy+=0.2 #vy is the velocity in, character is accelerated
    else:
      self.vy=0
      
    if self.g-(self.y+self.r) < self.vy: #we need this if statement to avoid the dip underneath ground level
      self.vy = self.g-(self.y+self.r)
      
    for p in game.platforms:
      if self.x > p.x and self.x < p.x+p.w and self.y+self.r <= p.y:
        self.g=p.y         #the ground changes to the platform
        break
      self.g=game.g
      
  def update(self): #y is the center of the circle, so y + radius to compare to ground level
    self.gravity()
      
    self.x+=self.vx
    self.y+=self.vy
    
  def display(self):
    self.update()
    if self.vx != 0: #The frame will only change when hero is running
        self.f=(self.f+0.1)%self.F
    else:
        self.f=0       #standing hero when there is no movement
    
    if self.dir >=0:
        image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h) #subtract r to align image with circle, cropping, we cast this into an integer because frames cant be decimals
    else:
        image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h) #If we are going back, we need to reflect the image, swap the x directions and mirror image
   
class Hero(Chara): #inherited from Creature class so must call initializer of parent
  def __init__(self,x,y,r,g,img,w,h,F):
    Chara.__init__(self,x,y,r,g,img,w,h,F)
    self.keyHandler={RIGHT:False,LEFT:False,UP:False}
    self.maxHealth = 1000
    self.health = 100
    self.healthDecrease = 1
    self.healthBarWidth = 100
    self.gameOver = False
    self.killSound = SoundFile(this, path + "/killSound.mp3")

  def drawHealthBar(self):
      noStroke()
      fill(236,240,241)
      rectMode(CORNER)
      rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth/10,5)
      if self.maxHealth > 600 :
          fill(0,255,0)
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth/10,5)
      elif self.maxHealth > 300:
          fill(255,0,0)
          self.healthbarWidth = 50
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth/10,5)
      else:
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth/10,5)
      

  def decreaseHealth(self):
      self.maxHealth -= self.healthDecrease
      # print("Health is", self.maxHealth)
      if self.maxHealth <= 0:
          self.gameOver = True
          game.music.stop()
          game.bossTheme.stop()
          self.killSound.play()     
          game.bossTheme.stop()   
    
    
  def collision(self):
    for p in game.potions:
      if self.distance(p) <= self.r+p.r: 
        self.maxHealth += 500
        game.potions.remove(p)
        del p
        game.restore.play()

    for e in game.enemies:
      if e.type != 'bahamut':
        if self.distance(e) <= self.r+e.r: # there is a collision
          if self.vx > 0 and self.x+self.r < e.x or self.vx < 0 and self.x+self.r > e.x:    #If the enemies clash with hero, the Gomba will be removed, velocity has to be greater than zero because I have to be falling down
            e.decreaseHealth()
            if e.maxHealth == 0:
                game.enemies.remove(e)
                del e
            if game.enemies == []:
                game.enemiesKilled.play()
                image(game.nextStageImg,1400,390,150,75)
                
            self.vx=-5 
            
          else: 
            self.decreaseHealth()
            self.vx=-5
      elif e.type == 'bahamut':
          if self.distance(e) <= self.r+e.r: # there is a collision
            if self.vx > 0 and self.x+self.r < e.x or self.vx < 0 and self.x+self.r > e.x:    #If the enemies clash with hero, the Gomba will be removed, velocity has to be greater than zero because I have to be falling down
              e.decreaseHealth()
              if e.maxHealth == 0:
                self.killSound.play()
                game.bossTheme.stop()
                game.music.play()
                game.enemies.remove(e)
                del e
                game.enemiesKilled.play()
                image(game.nextStageImg,1400,390,150,75)
                self.vx = -5


            else: 
                self.decreaseHealth()
                self.vx=-5
    
          
          
  def update(self): #y is the center of the circle, so y + radius to compare to ground level
    if not self.gameOver:
      self.gravity() 
      self.collision()
      self.drawHealthBar()
      if self.keyHandler[RIGHT]: 
        self.vx=2 
        self.dir=1 #If hero goes right, he will face that direction
      elif self.keyHandler[LEFT]: #velocity in negative direction
        self.vx=-2
        self.dir=-1 #If he goes left, the direction changes
      else:
        self.vx=0

      if self.keyHandler[UP] and self.vy==0: #The if conditions are separate because we want the creature to be able to move up and left/right at the same time
        self.vy=-10 #similar to bouncing #We nnly want him to jumpt whrn the creature is at the grounf
        #self.jumpSound.play()
    else:       #die conditions: no platform, no movement to sides, jump and fall
      self.vy+=0.2
      self.vx=0 #This will make sure he doesnt move to the sides    
      if self.y-self.r > game.h: # > game height (if hero is off the screen)
        game.music.stop()
        game.bossTheme.stop()
        game.__init__(game.w,game.h,game.g)        #We restart the game, we reset everything
      
    self.x+=self.vx
    self.y+=self.vy
       
    if self.x >= game.w//2 and self.x < 500:  #When hero reaches the Middle of the screen, the background will shift       
      game.x+=self.vx #The screen will move at hero's velocity, everything has to shift at the same velocity (game.x)
  
    if self.x-self.r < 0:
      self.x=self.r
      
    if self.x-self.r > 500 +game.w//2: #if the left side of hero becomes greater than the end of the screen (2500, when the screen stops moving + half of the width of the game
      if game.enemies == []:
        game.stage+=1
        
        if game.stage == 3:
            game.music.stop()
            game.bossTheme.play()
            
        if game.stage == 4:
            game.bossTheme.stop()
            game.music.stop()
            game.victory.play()
    
        if game.stage == 5:
            self.gameOver = True      
                
        self.x=50 #move hero to the beginning
        game.x=0  #k0vement of the screen goes back to zero
        if game.stage != 5:
            game.loadStage()
        elif game.stage == 5:
            game.victory.stop()
            self.gameOver = True
      else:
          self.x = 500 + game.w//2   
  def distance(self,target):
    return ((self.x-target.x)**2+(self.y-target.y)**2)**0.5

  def display(self):
    self.update()
    if self.vx != 0: #The frame will only change when hero is running
        self.f=(self.f+0.1)%self.F
    else:
        self.f=0       #standing hero when there is no movement
    
    if self.dir >=0:
        image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h) #subtract r to align image with circle, cropping, we cast this into an integer because frames cant be decimals
    else:
        image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h) #If we are going back, we need to reflect the image, swap the x directions and mirror image
  

class Silverbat(Chara): #inherited from Creature class so must call initializer of parent
  def __init__(self,x,y,r,g,img,w,h,F):
    Chara.__init__(self,x,y,r,g,img,w,h,F)
    self.type = 'silverbat'
    self.vx=random.choice([1,-1])
    self.dir=self.vx
    self.x1=self.x-75 #The range at which it moves
    self.x2=self.x+75  #the gomba moves between these 2 boundaries 
    self.maxHealth = 10
    self.health = 10
    self.healthDecrease = 1
    self.healthBarWidth = 50
    
  def drawHealthBar(self):
      noStroke()
      fill(236,240,241)

      rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth*10,5)
      if self.maxHealth > 6 :
          fill(0,255,0)
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth*10,5)
      elif self.maxHealth > 3:
          fill(255,0,0)
    
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth*10,5)
      else:
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth*10,5)
      

  def decreaseHealth(self):
      self.maxHealth -= self.healthDecrease
    
    
  def update(self):
    self.gravity() #he begins by falling, just like hero
    
    if self.x+self.r > self.x2:
      self.vx=-1 #If it reaches x2, it goes in the other direction
      self.dir=-1
    elif self.x-self.r < self.x1:
      self.vx=1
      self.dir=1
    
    self.x+=self.vx
    self.y+=self.vy
    
  def display(self):
        self.update()
        if self.vx != 0: #The frame will only change when hero is running
            self.f=(self.f+0.1)%self.F
        else:
            self.f=0       #standing hero when there is no movement
    
        if self.dir >=0:
            image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h) #subtract r to align image with circle, cropping, we cast this into an integer because frames cant be decimals
        else:
            image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h) #If we are going back, we need to reflect the image, swap the x directions and mirror image
    
        self.drawHealthBar()

class Tonberry(Chara): #inherited from Creature class so must call initializer of parent
  def __init__(self,x,y,r,g,img,w,h,F):
    Chara.__init__(self,x,y,r,g,img,w,h,F)
    self.type = 'tonberry'
    self.vx=random.choice([1,-1])
    self.dir=self.vx
    self.x1=self.x-50 #The range at which it moves
    self.x2=self.x+50  #the gomba moves between these 2 boundaries 
    self.maxHealth = 10
    self.health = 10
    self.healthDecrease = 1
    self.healthBarWidth = 50
    
  def drawHealthBar(self):
      noStroke()
      fill(236,240,241)

      rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth*10,5)
      if self.maxHealth > 6 :
          fill(0,255,0)
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth*10,5)
      elif self.maxHealth > 3:
          fill(255,0,0)
    
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth*10,5)
      else:
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth*10,5)
      

  def decreaseHealth(self):
      self.maxHealth -= self.healthDecrease
    
  def update(self):
    self.gravity() #he begins by falling, just like hero
    
    if self.x+self.r > self.x2:
      self.vx=-1 #If it reaches x2, it goes in the other direction
      self.dir=-1
    elif self.x-self.r < self.x1:
      self.vx=1
      self.dir=1
    
    self.x+=self.vx
    self.y+=self.vy
    
  def display(self):
        self.update()
        if self.vx != 0: #The frame will only change when hero is running
            self.f=(self.f+0.1)%self.F
        else:
            self.f=0       #standing hero when there is no movement
    
        if self.dir >=0:
            image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h) #subtract r to align image with circle, cropping, we cast this into an integer because frames cant be decimals
        else:
            image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h) #If we are going back, we need to reflect the image, swap the x directions and mirror image
    
        self.drawHealthBar()
    # print('Enemy health is,',self.maxHealth)
    
class Bahamut(Chara): #inherited from Creature class so must call initializer of parent
  def __init__(self,x,y,r,g,img,w,h,F):
    Chara.__init__(self,x,y,r,g,img,w,h,F)
    self.type = 'bahamut'
    self.vx=random.choice([1,-1])
    self.dir=self.vx
    self.x1=self.x-random.randint(150,350) #The range at which it moves
    self.x2=self.x+random.randint(150,350)
    self.maxHealth = 10
    self.health = 100
    self.healthDecrease = 1
    self.healthBarWidth = 50
   
  def update(self):
      #the gomba moves between these 2 boundaries
    self.gravity() #he begins by falling, just like hero
    
    if self.x+self.r > self.x2:
      self.vx=-1 #If it reaches x2, it goes in the other direction
      self.dir=-1
    elif self.x-self.r < self.x1:
      self.vx=1
      self.dir=1
       
    self.x+=self.vx
    self.y+=self.vy  
    
  def drawHealthBar(self):
      noStroke()
      fill(236,240,241)

      rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth/10,5)
      if self.maxHealth > 60 :
          fill(0,255,0)
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth/10,5)
      elif self.maxHealth > 300:
          fill(255,0,0)
    
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth/10,5)
      else:
          rect(self.x-(self.healthBarWidth/2), self.y -30,self.maxHealth,5)
      

  def decreaseHealth(self):
      self.maxHealth -= self.healthDecrease
      
  def display(self):
    self.update()
    if self.vx != 0: #The frame will only change when hero is running
        self.f=(self.f+0.1)%self.F
    else:
        self.f=0       #standing hero when there is no movement
    
    if self.dir >=0:
        image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h) #subtract r to align image with circle, cropping, we cast this into an integer because frames cant be decimals
    else:
        image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h) #If we are going back, we need to reflect the image, swap the x directions and mirror image
    
    self.drawHealthBar()
    # print('Enemy health is,',self.maxHealth)
    


        
class Platform:
  def __init__(self,x,y,w,h):
    self.x=x
    self.y=y
    self.w=w
    self.h=h
    
    self.img=loadImage(path+'/platform1.png')
    
  def display(self):
    image(self.img,self.x-game.x,self.y,self.w,self.h)

class Ending:
    def __init__(self,img,x,y,w,h):
        self.img = loadImage(path + '/'+img)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def display(self):
        image(self.img,self.x,self.y,self.w,self.h)
        
class Potion(Chara):
  def __init__(self,x,y,r,g,img,w,h,F):
    Chara.__init__(self,x,y,r,g,img,w,h,F)
    self.type = 'potion'
    self.vx=1
    self.vy=1
    self.y1=350
    self.y2=450
    
  def update(self):
    if self.y < self.y1 or self.y > self.y2: #The star will move up and down
      self.vy*=-1
      
    self.y+=self.vy
  
  def display(self):
    self.update()
    if self.vx != 0: #The frame will only change when hero is running
        self.f=(self.f+0.1)%self.F
    else:
        self.f=0       #standing hero when there is no movement
    
    if self.dir >=0:
        image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h) #subtract r to align image with circle, cropping, we cast this into an integer because frames cant be decimals
    else:
        image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h) #If we are going back, we need to reflect the image, swap the x directions and mirror image
        

game=Game(1480,800,585)


def setup():  
  size(game.w,game.h)
  background(0)
  print Serial.list()
  portIndex = 0
  LF = 10
  print " Connecting to ", Serial.list()[portIndex]
  global myPort
  myPort = Serial(this, Serial.list()[portIndex], 115200)
  myPort.bufferUntil(LF)
  
def draw():
  serialEvent(myPort)
  if not game.pause:
    background(0)  #Refresh the background so it leaves no trail
    game.display()

  else:
    textSize(40)
    fill(255,0,0)
    text("Paused",game.w//2,game.h//2)


def serialEvent(myPort):
    LF = 10
    inString = myPort.readStringUntil(LF)
    if (inString != None):
        nums = inString.strip().split(',')
        global xPos
        global yPos
        global switch
        # nums = map(int,nums)
        #print(nums)
        xPos = nums[0]
        yPos = nums[1]
        switch = nums[2]
        # print(xPos)
        # print(yPos)
        # print(switch)
    
        if xPos == u'1023':
            game.hero.keyHandler[RIGHT] = True
        else:
            game.hero.keyHandler[RIGHT] = False
    
        if xPos == u'0':
            game.hero.keyHandler[LEFT] = True
        else:
            game.hero.keyHandler[LEFT] = False
    
        if yPos == u'1023':
            game.hero.keyHandler[UP] = True
        else:
            game.hero.keyHandler[UP] = False
    
        if switch == u'0' and game.state == 'menu':
            game.state = 'play'
            game.menuMusic.stop()
            game.music.play()
        
        
    
    

def keyPressed():
  # print keyCode
  
  if game.state =="menu":
    game.state = "play"
    game.menuMusic.stop()
    game.music.play()
  
  if keyCode == 80: #ASCII for 'p' #If we press the key P
    if game.pause:
      game.pause=False
    else:
      game.pause=True
      game.pauseSound.play()
      

          
  if keyCode == LEFT:
    game.hero.keyHandler[LEFT]=True
  elif keyCode == RIGHT:
    game.hero.keyHandler[RIGHT]=True
  elif keyCode == UP:
    game.hero.keyHandler[UP]=True
  
def keyReleased():
  if keyCode == LEFT:
    game.hero.keyHandler[LEFT]=False
  elif keyCode == RIGHT:
    game.hero.keyHandler[RIGHT]=False
  elif keyCode == UP:
    game.hero.keyHandler[UP]=False
  
    
    
    