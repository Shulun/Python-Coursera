# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
CARD_X_SPACE = CARD_SIZE[0] + 10
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

INIT_POS = (10, 165)
PLAYER_TEXT_POS = (INIT_POS[0], 130)
DEALER_TEXT_POS = (INIT_POS[0], 320)
DEALER_HAND_POS = (INIT_POS[0], DEALER_TEXT_POS[1] + 25)

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank 

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        out_string = "Hand contains "
        for c in self.hand:
            out_string += str(c) 
            out_string += " "
        return out_string 
    
    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        global VALUES
        num_aces = 0
        value = 0
        
        for c in self.hand:
            value += VALUES[c.get_rank()]
            if c.get_rank() == 'A':
                num_aces += 1
        
        if (num_aces > 0) and ((value + 10) <= 21):
            return value +10
        else:
            return value
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        x0 = pos[0]
        y0 = pos[1]
        for c in self.hand:
            c.draw(canvas, (x0, y0))
            x0 += CARD_X_SPACE
                
                
#define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))
        # create a Deck object

    def shuffle(self):
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        return self.deck.pop(0)	# deal a card object from the deck
    
    def __str__(self):
        out_string = "Deck contains "
        for c in self.deck:
            out_string += str(c)
            out_string += " "
        return out_string


#define event handlers for buttons
def deal():
    global outcome, in_play
    global player, dealer, game_deck
    
    player = Hand()
    dealer = Hand()

    game_deck = Deck()
    game_deck.shuffle()
    
    for i in [0,1]:
        player.add_card(game_deck.deal_card())
        dealer.add_card(game_deck.deal_card())
    
    print "Player:  " + str(player)
    print "Dealer:  " + str(dealer)
    print
    
    outcome = "Hit or stand?"
    
    in_play = True

def hit():
    global outcome, in_play, score
    global player, dealer, game_deck
    
    if in_play:
        player.add_card(game_deck.deal_card())
        print "player's hand = ", player.get_value()
    
    if player.get_value() > 21:
        in_play = False
        score += -1
        outcome = "You have busted!"
       
def stand():
    global outcome, in_play, score
    global player, dealer, game_deck
    
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(game_deck.deal_card())
            print "dealer's hand = ", dealer.get_value()
        if dealer.get_value() > 21:
            outcome = "You won!"
            in_play = False
            score += 1
        else:
            if player.get_value() > dealer.get_value():
                outcome = "You won!"
                in_play = False
                score += 1
            else:
                outcome = "Dealer wins."
                in_play = False
                score += -1

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", [230, 25], 32, 'white', 'monospace')
    canvas.draw_text("Score: " + str(score), [260, 55], 18, 'white', 'monospace')
    canvas.draw_text(outcome, [10,580], 32, 'white', 'monospace')
    
    canvas.draw_text('Player:', PLAYER_TEXT_POS, 32, 'White', 'monospace')
    player.draw(canvas, INIT_POS)
    
    canvas.draw_text('Dealer:', DEALER_TEXT_POS, 32, 'White', 'monospace')
    dealer.draw(canvas, DEALER_HAND_POS)
    
    if( in_play ):
        back_pos = [ DEALER_HAND_POS[0] + CARD_CENTER[0], DEALER_HAND_POS[1] + CARD_CENTER[1] ]
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, back_pos, CARD_BACK_SIZE )

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric