import random
import copy

class Sentence():
    # بازیکنان اول تا چهارم را به ترتیب خلاف جهت عقربه های ساعت میگیرد
    def __init__(self,player1,player2,player3,player4):
        # ترتیب بازیکنان خلاف جهت عقربه های ساعت
        self.orderـplayers=[player1,player2,player3,player4]
        # بازیکنی که نوبتش است
        self.current_turn=None
        # لیست کارت های روی زمین
        self.listـlandـcards=[]
        # امتیاز بردهای زمین هر تیم
        self.team_wins={'team_1':0,'team_2':0}
        # کارت های هر بازیکن
        self.players={
            f'{player1}':{"H":[],"D":[],"C":[],"P":[]},
            f'{player2}':{"H":[],"D":[],"C":[],"P":[]},
            f'{player3}':{"H":[],"D":[],"C":[],"P":[]},
            f'{player4}':{"H":[],"D":[],"C":[],"P":[]},
            }
        # لیست کارت های بازی
        self.cards={
            "H":['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
            "D":['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
            "C":['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
            "P":['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
        }
        # باقی مانده کارت های تقسیم نشده
        self.remaining_cards=copy.deepcopy(self.cards)

    # برای تعین تصادفی یک حاکم از بین بازیکنان است
    def set_earlyـruler(self):
        # انتخاب تصادفی حاکم از بین بازیکنان
        ruler=random.choice(list(self.players.keys()))
        # ثبت حاکم
        self.players['ruler']=ruler
        # تعین حاکم به عنوان شروع کننده بازی
        self.current_turn=ruler

    # برای پخش کارت ها بین بازیکنان به صورت تصادفی است (number_card: تعداد کارت ها به هر بازیکن)
    def random_distribution_cards(self,number_cards):
        for p in self.orderـplayers:
            for i in range(number_cards):
                # به دنبال خالی که کارت هایش تمام نشده میگردد
                while True:
                    mole_random=random.choice(list(self.remaining_cards.keys()))
                    if self.remaining_cards[mole_random]:break
                    else:del self.remaining_cards[mole_random]
                card_random=random.choice(self.remaining_cards[mole_random])
                self.players[p][mole_random].append(card_random)
                self.remaining_cards[mole_random].remove(card_random)

    # مقدار ورودی خود را به عنوان حکم بازی تنظیم میکند
    def set_sentence(self,sentence):
        self.cards['sentence']=sentence

    # مشخص میکند نفر بعدی نوبط کدام بازیکن است
    def nextـturn(self):
        index=self.orderـplayers.index(self.current_turn)
        if (index+1)==len(self.orderـplayers):index=0
        else:index+=1
        self.current_turn=self.orderـplayers[index]

    # یک شبیه ساز ساده برای بازیکنان است (بذون هوش مصنوعی برای بازی)
    def playerـsimulator(self):
        # اگر شروع کننده بای باشد این دستورات اجرا میشود
        if not self.listـlandـcards:
            # سعی میکند یک خال از میان کارت های بازیکن برای شروع از کازت های آن پیدا کند
            while True:
                mole_random=random.choice(list(self.players[self.current_turn].keys()))
                mole_cards=self.players[self.current_turn][mole_random]
                if not mole_cards:del self.players[self.current_turn][mole_random]
                else:break
            card=random.choice(mole_cards)
            self.players[self.current_turn][mole_random].remove(card)
            dic_card={mole_random:card,'player':self.current_turn}
            self.listـlandـcards.append(dic_card)
        else:
            # بر اساس خال اویه که روی زمین است یک کارت از بین کارت های همان خال به صورت تصادفی انتخاب میکند
            mole_ground=list(self.listـlandـcards[0].keys())[0]
            mole_cards=self.players[self.current_turn].get(mole_ground)
            # اگر آن کارتی از آن خال نداشته باشد یک کارت از خال حم به طور تصادفی انتخاب میکند
            if not mole_cards:
                if mole_cards is not None:del self.players[self.current_turn][mole_ground]
                mole_ground=self.cards['sentence']
                mole_cards=self.players[self.current_turn].get(mole_ground)
                # اگر هیچ کارتی از خال حکم هم نداشته باشد سعی میکند به وسیله کارت های خال های دیگر رد بدهد
                if not mole_cards:
                    if mole_cards is not None:del self.players[self.current_turn][mole_ground]
                    while True:
                        mole_ground=random.choice(list(self.players[self.current_turn].keys()))
                        mole_cards=self.players[self.current_turn][mole_ground]
                        if not mole_cards:del self.players[self.current_turn][mole_ground]
                        else:break
            card=random.choice(mole_cards)
            self.players[self.current_turn][mole_ground].remove(card)
            dic_card={mole_ground:card,'player':self.current_turn}
            self.listـlandـcards.append(dic_card)

    # تعین میکند با توجه به کارت های روی زمین برنده زمین کدام تیم است و کدام بازیکن دست بعدی را شروع مبکند
    def land_winner(self):
        list_points=[]
        # خال زمین را پیدا میکند
        mole_ground=list(self.listـlandـcards[0].keys())[0]
        # کارت های زمین را بر اساس ایندکس هر کارت امتیاز دهی میکند (امتیاز کارت های خال حکم ۱۳ امتیز بیشتر از کارت های دیگر است)
        for card in self.listـlandـcards:
            mole_key=list(card.keys())[0]
            if mole_key==self.cards['sentence']:
                list_points.append(self.cards[mole_key].index(card[mole_key])+13)
            elif mole_key!=mole_ground:
                list_points.append(-1)
            else:
                list_points.append(self.cards[mole_key].index(card[mole_key]))
        print(self.listـlandـcards)
        # بازیکن برنده را مشخص میکند
        player_winner=self.listـlandـcards[list_points.index(max(list_points))]['player']
        # نوبت شروع دست بعد را به بازیکن برنده میدهد
        self.current_turn=player_winner
        # ایندکس بازیکن را یافته اگر زوج باشد بازیکن تیم اول و اگر فرد باشد بازیکن تیم دوم است و یک امتیاز به آن تیم اضافه میکند 
        team_index=self.orderـplayers.index(player_winner)
        if team_index%2==0:self.team_wins['team_1']+=1
        else:self.team_wins['team_2']+=1

    # تیم برنده کل بازی را مشخص میکند (تیمی که هفت دست زمین را برده)
    def game_winner(self):
        if self.team_wins['team_1']==7:return 'team_1'
        elif self.team_wins['team_2']==7:return 'team_2'
        else:return False

        
    # بدنه اصلی بازی است که روند کلی بازی را مشخص میکند
    def main(self):
        self.set_earlyـruler()
        self.random_distribution_cards(5)
        self.set_sentence("D")
        self.random_distribution_cards(8)
        while True:
            self.playerـsimulator()
            self.nextـturn()
            if len(self.listـlandـcards)==4:
                self.land_winner()
                self.listـlandـcards=[]
                winner=self.game_winner()
                if winner:
                    print(self.team_wins)
                    print(winner)
                    break
                else:
                    print(self.team_wins,end=3*'\n')

        

# S=Sentence("A","B","C","D")
# S.main()

