#CodeRunner
import pygame
import os
import random
import time

pygame.init()
pygame.font.init()

#Game_config
IMAGE_SIZE=128
SCREEN_SIZE=512
NUM_TILES_SIDE=4
NUM_TILES_TOTAL=16
MARGIN=4

ANIMALS_DIR="Animals"
ANIMALS_FILES=[x for x in os.listdir(ANIMALS_DIR) if x[-3:].lower()=='png']


MATCHED_FONT=pygame.font.SysFont('comicsans',100)

assert len(ANIMALS_FILES)==8

#Animal Class
animals_count=dict((a,0) for a in ANIMALS_FILES)

def available_animals():
    return [a for a, c in animals_count.items() if c<2] 

class Animal:
    def __init__(self,index):
        self.index=index
        self.row=index//NUM_TILES_SIDE
        self.col=index%NUM_TILES_SIDE
        self.name=random.choice(available_animals())
        animals_count[self.name]+=1
        self.image_path=os.path.join(ANIMALS_DIR,self.name)
        self.image=pygame.image.load(self.image_path)
        self.image=pygame.transform.scale(self.image,(IMAGE_SIZE-2*MARGIN,IMAGE_SIZE-2*MARGIN))
        self.box=self.image.copy()
        self.box.fill((200,200,200))
        self.skip=False



#Game

def find_index(x,y):
    row= y//IMAGE_SIZE
    column=x//IMAGE_SIZE
    index=row*NUM_TILES_SIDE+column
    return index
pygame.display.set_caption("CodeRunner Memory Game")

screen=pygame.display.set_mode((512,512))
draw_text= MATCHED_FONT.render("Matched!!",1,(11, 223, 255))

running=True
tiles=[Animal(i) for i in range(0,NUM_TILES_TOTAL)]
current_images=[]

while running:
    current_events=pygame.event.get()

    for e in current_events:
        if e.type==pygame.QUIT:
            running=False
            pygame.quit()
        
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_ESCAPE:
                running=False
                pygame.quit()

        if e.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            index =find_index(mouse_x,mouse_y)
            if index not in current_images:
                current_images.append(index)
            if len(current_images)>2:
                current_images=current_images[1:]
    
    screen.fill((255,255,255))

    total_skipped=0

    for _,tile in enumerate(tiles):
        image_i=tile.image if tile.index in current_images else tile.box

        if not tile.skip:
            screen.blit(image_i,(tile.col*IMAGE_SIZE+MARGIN,tile.row*IMAGE_SIZE+MARGIN))
        else:
            total_skipped+=1
    
    if len(current_images)==2:
        idx1,idx2=current_images
        if tiles[idx1].name==tiles[idx2].name:
            tiles[idx1].skip=True
            tiles[idx2].skip=True
            time.sleep(1)
            screen.blit(draw_text,(512/2-draw_text.get_width()/2,512/2-draw_text.get_height()/2))
            pygame.display.flip()
            time.sleep(1)
            current_images=[]
        if total_skipped==len(tiles):
            running=False
            pygame.quit()

    pygame.display.flip()

