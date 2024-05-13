import pygame
import os
from abc import *
import random
import time
import uuid
from datetime import datetime


# 선택한 캐릭터 번호 저장 변수
selected_number = None
selected_selling_number = None
selected_buying_number = None

# 버튼 클래스
class Button:
    def __init__(self, x, y, image_path, num):
        self.image = pygame.image.load(image_path)  # 이미지 로드
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.num = num
    
    def handle_select_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    global selected_number
                    selected_number = self.num
                    print(self.num,"번 선택" )


 
class BuyingButton(Button):
    def __init__(self, x, y,  image_path, num,isHaving,name):
        super().__init__(x, y, image_path, num)
        self.name = name
        self.isHaving = isHaving

    def handle_buy_evnet(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    global selected_buying_number
                    selected_buying_number = self.num
                    print(self.num,"번 선택") 

    def setIsHavingTrue(self):
        self.isHaving = True             

# 채집관련 class
class Collection:
    def __init__(self):
        self.name = None
        self.type = None
        self.rarity = None
   
    def getPrice(self):
        return self.rarity * 10000


class Fish(Collection):
    def __init__(self):
        self.type = "물고기"
        self.rarity = random.randint(1, 5)  # 희귀도 랜덤 설정
        self.name = random.choice(
            ["농어", "도미", "전갱이", "넙치", "우럭", "오징어", "문어", "연어", "자라", "잉어", "붕어", "구피", "클리오네", "흰동가리"])  # 랜덤선택
        
    

class Fruit(Collection):
    def __init__(self):
        self.type = "과일"
        self.rarity = 1  # 희귀도 랜덤 설정
        self.name = random.choice(
            ["복숭아", "오렌지", "배", "사과"])  # 랜덤선택



def isSuccess():
    return random.choice([True, False])  # 잡을 확률 50프로

class PlayerMemento:
    def __init__(self,image,name):
        self.image  = image
        self.name = name
        self.uuid = uuid.uuid4()
        self.created_time = datetime.now()


class Player:
    def __init__(self,x,y,image_path,animal):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y =y
        self.rect.center = (self.x, self.y)
        self.animal = animal
        if self.animal == "토끼":
            self.money = 10000
        else:
            self.money = 0
        self.playerList=[]
        self.collection=[]

    

    def fishing(self):
        fish = Fish()
        self.collection.append(fish)
        return fish
        

    def fruitPick(self):
        fruit = Fruit()
        self.collection.append(fruit)
        return fruit

    def sell(self):
        print(selected_selling_number)
        selling = self.collection.pop(selected_selling_number)
        self.money += selling.getPrice()
        if self.animal =="오리":
            self.money += int(selling.getPrice() / 2)
        return selling, self.money

    def buy(self):
        self.money -= 10000

    def getLenCollection(self):
        length = len(self.collection)
        if length < 10:
            return True
        else:
            return False
        
    def getMoney(self):
        return self.money
    
    
    def createMemento(self, playerBtn):
        return PlayerMemento(playerBtn.image, playerBtn.name)
    
    def restore(self,memento):
        self.image = memento.image
        self.name = memento.name

class PlayerBuilder:
    def __init__(self):
        self.image = None
        self.x = 0
        self.y = 0
        self.animal = ""
        
    def setImage(self, image_path):
        self.image = image_path

    def setXY(self,x,y):
        self.x = x
        self.y = y


    def build(self):
        player = Player(self.x, self.y, self.image, self.animal )
        return player

    """ def changePlayer(self):
        self.image = pygame.image.load(self.playerList[selected_buying_number].) """


class BearPlayerBuilder(PlayerBuilder):
    def __init__(self):
        super().__init__()
        self.skill="더 빠른 시간에 낚시 가능"
        self.animal = "곰"

    


class RabbitPlayerBuilder(PlayerBuilder):
    def __init__(self):
        super().__init__()
        self.skill="초기 더 많은 돈을 가지고 있음"
        self.animal = "토끼"
        self.money = 10000
    


class DuckPlayerBuilder(PlayerBuilder):
    def __init__(self):
        super().__init__()
        self.skill = "아이템을 더 비싼 가격에 팔 수 있음"
        self.animal="오리"




class Game:
    def __init__(self):
        self.pygame = pygame
        self.screen = 0
        self.font = 0
        self.text = ""

    def ready(self):
        self.pygame.init()
        self.pygame.font.init()

    def setDisplay(self, screen_width, screen_height):
        self.screen = self.pygame.display.set_mode((screen_width, screen_height))

    def setFont(self):
        self.font = self.pygame.font.Font(os.path.join(os.getcwd(), 'font', 'SUITE-SemiBold.ttf'), 24)

    def launch(self):
        pass

    def show_message(self, message):
        text_surface = self.font.render(message, True, (0, 0, 0))
        self.screen.blit(text_surface, (self.player_rect.centerx - text_surface.get_width() // 2,
                                         self.player_rect.y - text_surface.get_height()))
        self.pygame.display.update()
        time.sleep(1)  # 1초간 메시지 표시



class SelectPlayerGame(Game): # 캐릭터 선택할때
    def colliderect(self, restricted_rect):
        self.player.rect.x = max(self.player.rect.x, restricted_rect.left - self.player.rect.width)
        self.player.rect.x = min(self.player.rect.x, restricted_rect.right)
        self.player.rect.y = max(self.player.rect.y, restricted_rect.top - self.player.rect.height)
        self.player.rect.y = min(self.player.rect.y, restricted_rect.bottom)


    def launch(self):
        button1 = Button(150, 400, "./images/곰/곰1_머피.png",0)
        button2 = Button(350, 400, "./images/토끼/토끼1_대길.png",1)
        button3 = Button(550, 400, "./images/오리/오리1_나키.png",2)

        running = True
        while running: #캐릭터 선택
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    running = False
                if event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_RETURN:
                        running = False  # Enter 키를 누르면 게임 시작

                button1.handle_select_event(event)  # 버튼 이벤트 처리
                button2.handle_select_event(event)
                button3.handle_select_event(event)
            
            self.screen.fill((255, 255, 255))

            logo = self.pygame.image.load("./images/동물의숲로고.png")
            self.screen.blit(logo, (100, 50))

            # 버튼 그리기
            self.screen.blit(button1.image, button1.rect)
            self.screen.blit(button2.image, button2.rect)
            self.screen.blit(button3.image, button3.rect)

            main_text_surface = self.font.render("캐릭터를 고르고 엔터를 눌러주세요!", True, (0,0,0))
            self.screen.blit(main_text_surface, (250,300))

            texts = ["곰: 더 빠른 시간에 낚시 가능","토끼 : 초기 더 많은 돈을 가지고 있음",  "오리: 아이템을 더 비싼 가격에 팔 수 있음"]

            if selected_number is not None:
                text_surface = self.font.render(texts[selected_number], True, (0, 0, 0))
                self.screen.blit(text_surface, (200, 350))
            
            self.pygame.display.update()
        self.pygame.quit()


class PlayGame(Game): # 직접 플레이할때
    def __init__(self):
        super().__init__()
        self.player = None
        self.player_rect = None
        self.playerBtns = []

    def setPlayer(self):
        if selected_number == 0 :
            playerBuilder = BearPlayerBuilder()
            playerBuilder.setImage("./images/곰/곰1_머피.png")
            playerBuilder.setXY(500,400)
            self.player = playerBuilder.build()
            self.playerBtns = [BuyingButton(500, 350, "./images/곰/곰1_머피.png",0, True,"머피"),BuyingButton(650, 350, "./images/곰/곰2_아세로라.png",1, False,"아세로라"),BuyingButton(800,350, "./images/곰/곰3_올리브.png",2, False,"올리브") ]
            

        elif selected_number == 1:
            playerBuilder = RabbitPlayerBuilder()
            playerBuilder.setImage("./images/토끼/토끼1_대길.png" )
            playerBuilder.setXY(500,400)
            self.player = playerBuilder.build()
            self.playerBtns = [BuyingButton(500, 350, "./images/토끼/토끼1_대길.png",0,True,"대길"),BuyingButton(650, 350, "./images/토끼/토끼2_미랑.png",1,False, "미랑"),BuyingButton(800,350, "./images/토끼/토끼3_미첼.png",2,False,"미첼") ]
        else:
            playerBuilder = DuckPlayerBuilder()
            playerBuilder.setImage("./images/오리/오리1_나키.png")
            playerBuilder.setXY(500,400)
            self.player = playerBuilder.build()
            self.playerBtns = [BuyingButton(500, 350, "./images/오리/오리1_나키.png",0,True,"나키"),BuyingButton(650, 350, "./images/오리/오리2_리처드.png",1,False,"리처드"),BuyingButton(800,350, "./images/오리/오리3_주디.png",2,False,"주디") ]
        
        self.player.playerList.append(self.playerBtns[0]) # 초기에 0번째 캐릭터는 가지고 있음
        
        self.player_rect = self.player.rect


    def launch(self):
        clock = self.pygame.time.Clock()  # 화면을 업데이트할 때 사용할 FPS 값 설정
        is_fishing = False
        is_picking = False

        bgImg = self.pygame.image.load("./images/배경.png")
        bgImg = self.pygame.transform.scale(bgImg, (1000, 800))



        running = True
        while running:
            clock.tick(30)
            
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    running = False
                # 팔기 혹은 구매 때 유저 입력 받기
                elif event.type == self.pygame.KEYDOWN:
                    if event.unicode.isnumeric():
                        global selected_selling_number
                        selected_selling_number = int(event.unicode)
                        if selected_selling_number +1 <= len(self.player.collection):
                            print(selected_selling_number)
                            selling_thing, now_money = self.player.sell()
                            self.show_message(f"{selling_thing.name}을 팔아서 {selling_thing.getPrice()}을 벌었다!, 현재 잔고: {now_money}")
                        else:
                            self.show_message("유효한 번호를 입력해주세요!")
                        
                
                for player_btn in self.playerBtns:
                    player_btn.handle_buy_evnet(event)
            
               
            # 주인공 이동 처리

            keys = self.pygame.key.get_pressed()
            if keys[self.pygame.K_LEFT]:
                self.player_rect.x -= 5
            if keys[self.pygame.K_RIGHT]:
                self.player_rect.x += 5
            if keys[self.pygame.K_UP]:
                self.player_rect.y -= 5
            if keys[self.pygame.K_DOWN]:
                self.player_rect.y += 5

    
            """ for key, value in enumerate(keys):
                if value:
                    if key >= self.pygame.K_0 and key <= self.pygame.K_9:  # 숫자 키 검사
                        digit = chr(key)  # 키 코드를 해당 숫자 문자로 변환
                        selected_selling_number = int(digit)  # 숫자로 변환
                        print(selected_selling_number) """
            # 화면 업데이트
            self.screen.blit(bgImg, (0, 0))
            self.screen.blit(self.player.image, self.player.rect)

            fish_text_surface = self.font.render("낚시하기", True, (255,255,255))
            self.screen.blit(fish_text_surface, (800,700))

            fruit_text_surface = self.font.render("과일 수확하기", True, (255,255,255))
            self.screen.blit(fruit_text_surface, (310,100))

            
            selling_text_surface = self.font.render("팔기", True, (255,255,255))
            self.screen.blit(selling_text_surface, (200,280))
            
            buying_text_surface = self.font.render("구매", True, (255,255,255))
            self.screen.blit(buying_text_surface, (580,280))    

             # "낚시하기" 버튼 처리
            if self.player_rect.colliderect(self.pygame.Rect(800,700,90,35)) and not is_fishing:
                self.show_message("낚시 중...")
                is_fishing = True
                fishing_start_time = self.pygame.time.get_ticks()
            
            if selected_number == 0:
                fishing_time = 1000
            else:
                fishing_time = 2000

            
            # 낚시 시간이 지남에 따라
            if is_fishing and self.pygame.time.get_ticks() - fishing_start_time >= fishing_time:
                is_fishing = False
                success = isSuccess() 
                collection_len_bool = self.player.getLenCollection()
                if success:
                    if collection_len_bool:

                        fish = self.player.fishing()
                        self.show_message(fish.name+"을 낚았다!")
                    else:
                        self.show_message("가방 꽉 찼음!!!!!")
                else:
                    self.show_message("놓쳤다...")
            


             # "과일 수확하기" 버튼 처리
            if self.player_rect.colliderect(self.pygame.Rect(310,100,130,35)) and not is_picking:
                self.show_message("어떤 과일을 얻을까~?")
                is_picking = True
                picking_start_time = self.pygame.time.get_ticks()

            if is_picking and self.pygame.time.get_ticks() - picking_start_time >= 1000:
                is_picking = False
                collection_len_bool = self.player.getLenCollection()
                if collection_len_bool : 
                    fruit = self.player.fruitPick()
                    self.show_message(fruit.name + "을 얻었다!")
                else:
                    self.show_message("가방 꽉 찼음!!!!!")

    
            
            # "팔기" 버튼 처리
            if  self.player_rect.colliderect(self.pygame.Rect(200,280,90,35)):
                collection_text = "무엇을 파시겠습니까?(번호를 입력해주세요)<br>소지한 컬렉션:<br>"
                for i, item in enumerate(self.player.collection):
                    collection_text += f"{i}번: {item.name} (희귀도: {item.rarity})<br>"

                collection_text_lines = collection_text.split("<br>")
                y_offset = 320
                for line in collection_text_lines:
                    text_surface = self.font.render(line, True, (0,0,0))
                    self.screen.blit(text_surface, (200, y_offset))
                    y_offset += 20

            # "구매" 버튼 처리
            if self.player_rect.colliderect(self.pygame.Rect(580,280,90,35)):
                now_money_text = self.font.render(f"현재 잔고 : {self.player.money}", True, (0,0,0))
                self.screen.blit(now_money_text, (500,200))

                buying_info_text_surface1 = self.font.render("어떤 캐릭터를 사시겠습니까?(캐릭터당 10000원)",True,(0,0,0))
                buying_info_text_surface2 = self.font.render("(보유중인 것을 클릭하면 캐릭터가 바뀝니다)",True,(0,0,0))
                self.screen.blit(buying_info_text_surface1,(500,300))
                self.screen.blit(buying_info_text_surface2,(500,320))

                for playerBtn in self.playerBtns:
                    self.screen.blit(playerBtn.image, playerBtn.rect)
                    if  (playerBtn.isHaving):
                        isHaving_text=self.font.render("있어용", True, (0,0,0))
                        
                    else:
                        isHaving_text=self.font.render("없어용", True, (0,0,0))

                    topleft_rect = pygame.Rect(playerBtn.rect.topleft, (0, 0))
                    self.screen.blit(isHaving_text, (topleft_rect.x + 30, topleft_rect.y + 120))

                if selected_buying_number is not None:
                    if self.player.money >= 10000:
                        self.player.playerList.append(self.player.createMemento(self.playerBtns[selected_buying_number])) #메멘토 패턴 사용하여 리스트에 넣음
                        self.playerBtns[selected_buying_number].setIsHavingTrue()
                        self.player.buy()

                    if self.playerBtns[selected_buying_number].isHaving:
                        self.player.restore(self.player.playerList[selected_buying_number])

                    
                
                
            self.pygame.display.update()

class SelectGameFacade:
    def __init__(self):
        self.game = SelectPlayerGame()


    def operation(self):
        self.game.ready()
        self.game.setFont()
        self.game.setDisplay(800,600)
        self.game.launch()

class PlayGameFacde:
    def __init__(self):
        self.game = PlayGame()

    def operation(self):
        self.game.ready()
        self.game.setFont()
        self.game.setDisplay(1000,800)
        self.game.setPlayer()
        self.game.launch()


selectFacade = SelectGameFacade()
selectFacade.operation()

playFacade = PlayGameFacde()
playFacade.operation()
