import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from patiancegui import *
from random import shuffle


# class factory
class Card:
    def __init__(self, number, suit, myid):
        self.number = number
        self.suit = suit
        self.id = myid


# class with cards methods
class NewCards:

    cards = []   # array with class Card instances

    sumarr = []

    # this method fill array with cards; there are two types of cards: board cards & deck cards
    @classmethod
    def define_cards(cls):

        num = 0

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

        suits = ["Diamonds", "Hearts", "Spades", "Clubs"]

        lines = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]

        for i in range(4):

            for j in range(13):

                num += 1

                cls.cards.append(Card(numbers[j], suits[i], num))

        for i in range(len(cls.cards)):

            cls.cards[i].image = "cards/card_%s.jpg" % (i + 1)

            print("cards/card_%s.jpg" % (i + 1), "   %s" % cls.cards[i].number)

        shuffle(cls.cards)

        for i in range(len(cls.cards)):

            if i < 28:

                cls.cards[i].type = "board"

                cls.cards[i].removed = False

                cls.cards[i].button = i + 1

                cls.cards[i].line = lines[i]

            elif i == 29: # 51

                cls.cards[i].type = "deck"

                cls.cards[i].blocked = False

                cls.cards[i].button = i + 1

            else:

                cls.cards[i].type = "deck"

                cls.cards[i].blocked = True

    # this method places cards on board
    @classmethod
    def block_cards(cls):

        for i in cls.cards:

            if i.type == "board":

                is_blocked = any(i.button + i.line == x.button or i.button + i.line + 1 == x.button for x in cls.cards if x.type == "board")  # is parent cards is exist

                if is_blocked:

                    i.blocked = True

                else:

                    i.blocked = False

    # this method processed commands from console
    @classmethod
    def start(cls, cards):

        do = input("\n\nEnter command: ").split(" ")

        if do[0] == "add":

            do.remove("add")

            if len(do) > 2:

                print("Error!")

                Main.draw_cards(cards)

                Main.start(cards)

            summed = 0

            for i in range(len(do)):

                item = None

                for x in cards:

                    if x.id == int(do[i]):

                        item = x

                        break

                if item and not item.blocked:

                    summed += item.number

                else:

                    print("Seems like you trying to add blocked / unexisted cards: ", cards[int(do[i])].__dict__)

            if summed == 13:

                print("\nRemoved")

                for i in range(len(do)):

                    if cards[int(do[i])].type == "board":

                        cards[int(do[i])].number = 999

                        cards[int(do[i])].name = "   "

                        cards[int(do[i])].id = 999

                        cards[int(do[i])].removed = True

                    else:

                        del cards[-1]

                        cards[-1].blocked = False

            else:

                print("\nWrong!")

        elif do[0] == "next":

            cards[-1].blocked = True

            for i in range(len(cards) - 1, 28, -1):

                cards[i], cards[i - 1] = cards[i - 1], cards[i]

            cards[-1].blocked = False

        elif do[0] == "info":

            Main.show_info()

        elif do[0] == "rules":

            Main.show_rules()

        elif do[0] == "win":

            cards[0].removed = True

        else:

            print("Unknown command!")

            Main.draw_cards(cards)

            Main.start(cards)


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        for i in range(1, 29):

            getattr(self.ui, 'button_%s' % i).setStyleSheet("QPushButton{background-color: rgba(0,0,0,0); border: None};QPushButton:hover{background-color:black}")
            getattr(self.ui, 'button_%s' % i).pressed.connect(lambda v=i: self.button_pressed(v))
            getattr(self.ui, 'button_%s' % i).setIcon(QtGui.QIcon('%s' % NewCards.cards[i].image))
            getattr(self.ui, 'button_%s' % i).setIconSize(QtCore.QSize(70, 70))
            getattr(self.ui, 'button_%s' % i).setText('')

        self.ui.deck.clicked.connect(self.deck_pressed)

    def button_pressed(self, button_num):

        if self.cards[button_num].blocked:

            return

        self.sumarr.append(self.cards[button_num])

        sumof = 0

        for i in self.sumarr:

            sumof += i.number

        if sumof == 13:

            for i in self.sumarr:

                i.number = 999

                i.removed = True

                self.sumarr = []

                print("got, cleared")

        elif len(self.sumarr) == 2:

            self.sumarr = []

            print("miss, cleared")

    def deck_pressed(self):
        print("yy")


# class with methods for process running
class Main(NewCards):

    # this methods runs game loop
    def game(self):

        NewCards.define_cards()
        NewCards.block_cards()

        # while True:
        #
        #     if self.cards[0].removed:
        #
        #         print("You won.")(
        #
        #         sys.exit()


if __name__ == "__main__":
    main = Main()
    main.game()
    app = QtWidgets.QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec_())
