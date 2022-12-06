import random
import tkinter
import time

stand_button_clicked = False
double_button_clicked = False
hit_button_clicked = False


def load_card_images(card_images):
    suits = ['heart', 'spade', 'club', 'diamond']
    face_card = ['queen', 'jack', 'king']

    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    for suit in suits:
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            images = tkinter.PhotoImage(file=name)
            card_images.append((card, images,))

        for card in face_card:
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            images = tkinter.PhotoImage(file=name)
            card_images.append((10, images,))


def deal_card(frame):
    next_card = deck_cards.pop(0)
    deck_cards.append(next_card)
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    return next_card


def take_card(frame):
    card_drop = player_deck.pop()
    split_deck.append(card_drop)
    tkinter.Label(frame, image=card_drop[1], relief='raised').pack(side='left')
    return card_drop


def deal_card_to_dealer():
    dealer_deck.append(deal_card(dealer_card_frame))
    dealer_score = hand_score(dealer_deck)
    dealer_score_Label.set(dealer_score)


def deal_card_to_player():
    player_deck.append(deal_card(player_card_frame))
    player_score = hand_score(player_deck)
    player_score_Label.set(player_score)


def hand_score(hand):
    score = 0
    ace = False
    for card in hand:
        card_value = card[0]
        if card_value == 1 and not ace:
            card_value = 11
            ace = True
        score += card_value
        if score > 21 and ace:
            score -= 10
            ace = False
        if score == 21 and ace:
            natural_blackjack = True
    return score


def calc_score():
    dealer_score = hand_score(dealer_deck)
    player_score = hand_score(player_deck)
    if player_score > 21 or player_score < dealer_score <= 21:
        result_text.set("Dealer wins")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins")
    # elif dealer_score < player_score:
    #     result_text.set("Player wins")
    #     break
    else:
        result_text.set("Push")


def dealer_turn():
    dealer_score = hand_score(dealer_deck)
    player_score = hand_score(player_deck)

    while dealer_score < 17:
        dealer_deck.append(deal_card(dealer_card_frame))
        dealer_score = hand_score(dealer_deck)
        dealer_score_Label.set(dealer_score)
        if dealer_score > player_score:
            break
    calc_score()


def disable_all_buttons():
    hit_button['state'] = 'disabled'
    double_button['state'] = 'disabled'
    stand_button['state'] = 'disabled'
    split_button['state'] = 'disabled'


def enable_buttons():
    hit_button['state'] = 'normal'
    double_button['state'] = 'normal'
    stand_button['state'] = 'normal'


def switch_button():
    player_score = hand_score(player_deck)
    if hit_button['state'] == 'normal':
        if player_score >= 21:
            disable_all_buttons()
            dealer_turn()
        double_button['state'] = 'disabled'
        split_button['state'] = 'disabled'
    if stand_button_clicked:
        disable_all_buttons()
    if double_button_clicked:
        disable_all_buttons()

    if player_deck[0][0] == player_deck[1][0]:
        split_button['state'] = 'normal'
    else:
        split_button['state'] = 'disabled'


def hit_action():
    global hit_button_clicked
    hit_button_clicked = True
    deal_card_to_player()
    switch_button()


def stand_action():
    global stand_button_clicked
    stand_button_clicked = True
    switch_button()
    dealer_turn()
    # split_second_part()


def double_action():
    global double_button_clicked
    double_button_clicked = True
    switch_button()
    hit_action()
    dealer_turn()


def split_second_part():
    if split_deck:
        for widgets in player_card_frame.winfo_children():
            widgets.destroy()
        for widgets in split_card_frame.winfo_children():
            widgets.destroy()
        player_deck.clear()
        first_card = split_deck.pop(0)
        # split_deck.clear()
        player_deck.append(first_card)
        tkinter.Label(player_card_frame, image=first_card[1], relief='raised').pack(side='left')
        deal_card_to_player()
        enable_buttons()
        split_continue_button.grid_forget()


def split_action():
    for widgets in player_card_frame.winfo_children():
        widgets.destroy()
    take_card(split_card_frame)
    player_deck.append(take_card(player_card_frame))
    deal_card_to_player()
    split_continue_button.grid(row=0, column=4, sticky='w')
    switch_button()


def clear_frame():
    for widgets in player_card_frame.winfo_children():
        widgets.destroy()
    for widgets in dealer_card_frame.winfo_children():
        widgets.destroy()
    for widgets in split_card_frame.winfo_children():
        widgets.destroy()

    player_score_Label.set(0)
    dealer_score_Label.set(0)
    result_text.set('')
    # split_continue_button.grid_forget()


def game_start():
    deal_card_to_player()
    dealer_deck.append(deal_card(dealer_card_frame))
    dealer_score_Label.set(hand_score(dealer_deck))
    deal_card_to_player()
    switch_button()


def newgame():
    clear_frame()
    player_deck.clear()
    dealer_deck.clear()
    split_deck.clear()
    game_start()
    enable_buttons()

    mainWindow.mainloop()


mainWindow = tkinter.Tk()
mainWindow.title("BlackJack")
mainWindow.geometry("640x480")
mainWindow.configure(background='green')

result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

cardFrame = tkinter.Frame(mainWindow, relief='sunken', borderwidth=1, background='green')
cardFrame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

dealer_score_Label = tkinter.IntVar()
tkinter.Label(cardFrame, text='Dealer', background='green', fg='white').grid(row=0, column=0)
tkinter.Label(cardFrame, textvariable=dealer_score_Label, background='green', fg='white').grid(row=1, column=0)

dealer_card_frame = tkinter.Frame(cardFrame, background='green')
dealer_card_frame.grid(row=0, column=1, rowspan=2, sticky='ew')

player_score_Label = tkinter.IntVar()
tkinter.Label(cardFrame, text='Player', background='green', fg='white').grid(row=2, column=0)
tkinter.Label(cardFrame, textvariable=player_score_Label, background='green', fg='white').grid(row=3, column=0)

player_card_frame = tkinter.Frame(cardFrame, background='green')
player_card_frame.grid(row=2, column=1, rowspan=2, sticky='ew')

split_card_frame = tkinter.Frame(mainWindow, background='green')
split_card_frame.grid(row=2, column=3, sticky='nw')

buttonFrame = tkinter.Frame(mainWindow, background='green')
buttonFrame.grid(row=3, column=0, columnspan=3)

split_button = tkinter.Button(buttonFrame, text='Split', command=split_action, state='disabled')
split_button.grid(row=0, column=0, sticky='w')
split_continue_button = tkinter.Button(buttonFrame, text='Continue Split', command=split_second_part)
hit_button = tkinter.Button(buttonFrame, text='Hit', command=hit_action)
hit_button.grid(row=0, column=1, sticky='w')
stand_button = tkinter.Button(buttonFrame, text='Stand', command=stand_action)
stand_button.grid(row=0, column=2, sticky='w')
double_button = tkinter.Button(buttonFrame, text='Double', command=double_action)
double_button.grid(row=0, column=3, sticky='w')
new_game_button = tkinter.Button(mainWindow, text='New game', command=newgame)
new_game_button.grid(row=0, column=0, sticky='w')

cards = []
load_card_images(cards)
deck_cards = list(cards)

random.shuffle(deck_cards)
dealer_deck = []
player_deck = []
split_deck = []

if __name__ == '__main__':
    try:
        newgame()
    except KeyboardInterrupt:
        print("Stop")
    # split_second_part()
