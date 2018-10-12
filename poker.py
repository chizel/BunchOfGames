#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import random


class Deck():
    def __init__(self, ):
        self.suits = [0, 1, 2, 3]
        self.generate_deck()
        #Hearts 0, Diamonds 1, Clubs 2, Spades 3

    def generate_deck(self):
        cards = []
        #ranks = list(range(2, 11)) + ['J', 'Q', 'K', 'A']
        #2-10 same as cards rank, 11-J, 12-Q, 13-K, 14-A
        ranks = list(range(2, 15))
        for suit in self.suits:
            for rank in ranks:
                cards.append((rank, suit))
        random.shuffle(cards)
        self.cards = cards

    def get_cards(self, number):
        return random.sample(self.cards, number)

    def sort_cards(self, cards):
        cards.sort(key=lambda x: (x[1], x[0]))
        return cards

    def calculate_hand(self, hand):
        if len(hand) < 5 or len(hand) > 7:
            print('Error! Hand contains wrong number of cards: ' + len(hand))
            return None
        hand.sort(key=lambda x: x[0], reverse=True)
        #is hand contains royal flush
        #for card in hand:
        #    if card[1] == def_rank:
        #is hand contains street flush
        #is hand contains 4 of a kind
        #is hand contains full house
        #is hand contains flush
        #sum(x.count(1) for x in L)
        #is hand contains street

        #is hand contains 3 of a kind
        for i in range(len(hand)):
            for j in range(i + 1, len(hand)):
                if hand[i][0] == hand[j][0]:
                    for k in range(j + 1, len(hand)):
                        if hand[i][0] == hand[k][0]:
                            #removing pair from the hand
                            combination = [hand[i], hand[j], hand[k]]
                            del(hand[k])
                            del(hand[j])
                            del(hand[i])
                            hand.sort(key=lambda x: x[0])
                            return combination + hand[-2:]

        #is hand contains 2 pairs
        for i in range(len(hand)):
            for j in range(i + 1, len(hand)):
                if hand[i][0] == hand[j][0]:
                    #first pair is found
                    #removing pair from the hand
                    combination = [hand[i], hand[j]]
                    del(hand[j])
                    del(hand[i])

                    #searching for second pair
                    for k in range(len(hand)):
                        for l in range(k + 1, len(hand)):
                            if hand[k][0] == hand[l][0]:
                                combination += [hand[k], hand[l]]
                                del(hand[l])
                                del(hand[k])
                                hand.sort(key=lambda x: x[0])
                                return combination + hand[-1:]

                    #there is only one pair, return it
                    hand.sort(key=lambda x: x[0])
                    return combination + hand[-3:]
        #hand hasn't any combination
        hand.sort(key=lambda x: x[0])
        return hand[-5:]


class BlackJack():
    def __init__(self):
        self.deck = Deck()
        #hand = self.deck.get_cards(7)
        hand = [
            (2, 0),
            (3, 1),
            (2, 1),
            (4, 1),
            (4, 3),
            (3, 3),
            (5, 3),
            ]
        #print(self.deck.cards)
        print(self.deck.calculate_hand(hand))
        pass


def main():
    mg = BlackJack()
    return


if __name__ == "__main__":
    main()
