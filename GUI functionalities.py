import math
import re
from functools import partial
import sys
import copy
# sys.executable

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor,QIcon,QFont
from PyQt5.QtWidgets import *

import main_real6
from main_real6 import Ui_MainWindow
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore
import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.dark_palet = QPixmap("darkPalet.png")
        self.flu_palet = QPixmap("fluPalet.png")

        self.give_parameters()

        self.width = round(self.x * (self.dark_palet.width() / self.palet_width))
        self.height = round(self.y * (self.dark_palet.height() / self.palet_height))

        # this function has all connection between widgets and functions

        self.original_box = QPixmap("box.png").scaled(self.width, self.height)  # Orjinal box resmi

        # scale orignal palet
        self.ui.leftPalet.setPixmap(self.dark_palet)

        self.ui.box.setPixmap(self.original_box)
        self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

        self.ui.leftPalet.setPixmap(self.dark_palet)
        self.ui.leftPalet.setFixedSize(self.dark_palet.width(), self.dark_palet.height())

        self.ui.pushButton_10.setIcon(QIcon('save.png'))
        self.ui.pushButton_10.setIconSize(QtCore.QSize(50, 50))
        self.ui.pushButton_7.setIcon(QIcon('switch.png'))
        self.ui.pushButton_7.setIconSize(QtCore.QSize(50, 50))
        self.ui.pushButton_8.setIcon(QIcon('undo.png'))
        self.ui.pushButton_8.setIconSize(QtCore.QSize(50, 50))

        self.ui.lineEdit.setPlaceholderText('second :Enter the repeated range here')
        self.ui.lineEdit2.setPlaceholderText('first :Enter range of what to repeat')


        self.ui.tableWidget.setColumnWidth(1, self.dark_palet.width())

        font = QFont()
        font.setPointSize(20)  # Set the font size
        font.setBold(True)  # Set the font weight to bold
        self.ui.pushButton_9.setFont(font)
        self.ui.pushButton_9.setStyleSheet('QPushButton {color: black;}')

        self.ui.tableWidget.setHorizontalHeaderLabels(['palet name', 'pallete review'])
        ###hesham added

        self.mode = "Standard"
        # self.mode = "Random"


        self.main_dic = {'Left_palette': {}, 'Right_palette': {}}
        self.repeated_dic={'Left_palette': {}, 'Right_palette': {}}
        self.moved_dic = {'Left_palette': {}, 'Right_palette': {}}
        # this variable will increse after adding box and will decrease after removing it
        self.highlight1 = 0
        self.highlight2 = 0
        self.repeat_flag=0

        # lists of grid list
        self.full_left_palet_number = 0
        self.full_right_palet_number = 0
        self.grid_list_left = []
        self.grid_list_right = []

        self.lists_of_grid_list = []
        self.lists_of_left_boxes = []
        self.lists_of_right_boxes = []
        self.next_pallet_flag = 0

        # last place where the mouse clicked
        self.last_clicked = 0

        # placment variables
        self.left_placement = 1
        # dragging variables
        self.dragging = False  # Sürükleme durumu
        self.offset = None  # Sürükleme konumu
        self.boxes1 = []  # Klonlanmış box'ların listesi
        self.boxes2 = []

        # degree and rotate
        self.left_box_degree = 0
        self.right_box_degree = 0
        self.left_degree_counter = 1
        self.right_degree_counter = 1

        #add to table
        self.table_counter = 0
        self.double_clicked_flag=0
        self.row=0

        #repeat
        self.last_left_palet_number=-1
        self.last_right_palet_number=-1

        #rotate
        self.degree_check = -1
        self.rotate_when_rtrev1=0
        self.rotate_when_rtrev2=0

        self.ui.frame_3.setAcceptDrops(True)
        self.ui.frame_4.setAcceptDrops(True)
        self.ui.leftPalet.setAcceptDrops(True)

        # self.setPaddingAndMargin(self.ui.leftPalet)
        self.setPaddingAndMargin(self.ui.frame_3)
        self.setPaddingAndMargin(self.ui.box)

        self.firstFlag = -1
        self.get_placement_list()
        self.create_shortcuts()  # to make shortcut for (undo)

        #numbering
        self.left_box_numbering=1
        self.right_box_numbering = 1

        self.connects()


    def give_parameters(self):
        self.palet_width = 800
        self.palet_height = 500
        self.palet_depth = 100

        self.x =90
        self.y= 120
        self.box_depth = 30
    def connects(self):
        self.ui.pushButton_7.clicked.connect(self.switch_placement)
        self.ui.pushButton_8.clicked.connect(self.undo_last_step)
        self.ui.pushButton_10.clicked.connect(self.next_pallete)
        self.ui.pushButton_9.clicked.connect(self.rotate)
        self.ui.tableWidget.doubleClicked.connect(self.retrieve_palet)
        self.ui.lineEdit.returnPressed.connect(self.repeate_palet) #go to function when i stand on lineedit and press (enter)
        self.ui.pushButton_6.clicked.connect(partial(self.generate_paletization, self.main_dic))




    def calculate_left_palet_placement(self, box_h, box_w, palet_h, palet_w, offset_h, offset_w):
        print(box_h, box_w, palet_h, palet_w, offset_h, offset_w)
        self.boxCountPerLine1 = math.ceil(palet_w / (box_w + offset_w))
        self.boxLineCount1 = math.ceil(palet_h / (box_h + offset_h))

        print("Lines", self.boxLineCount1, self.boxLineCount1)
        placement = []
        pos = {}
        myList = {}

        for line in range(self.boxLineCount1 - 1):
            key = f'line{line}'

            # line_placement = []
            for i in range(self.boxCountPerLine1 - 1):
                # print(i)
                x = i * (box_w + offset_w) + offset_w
                y = palet_h - (line + 1) * (box_h + offset_h)
                placement.append((x, y,box_w,box_h,self.left_box_degree))
        # myList[key] = line_placement
        # placement.append(line_placement)
        # return myList
        return placement

    def calculate_right_palet_placement(self, box_h, box_w, palet_h, palet_w, offset_h, offset_w):
        print(box_h, box_w, palet_h, palet_w, offset_h, offset_w)
        self.boxCountPerLine2 = math.ceil((palet_w) / (box_w + offset_w))
        self.boxLineCount2 = math.ceil((palet_h) / (box_h + offset_h))

        print(self.boxLineCount2, self.boxLineCount2)
        placement = []
        pos = {}
        myList = {}

        for line in range(self.boxLineCount2 - 1):
            key = f'line{line}'

            # line_placement = []
            for i in range(self.boxCountPerLine2 - 1):
                # print(i)
                # x = palet_w-( ((i+1) * (box_w+offset_w)) + (offset_w))
                x = palet_w - ((i + 1) * (box_w + offset_w) + offset_w)
                # y = palet_h-( ((line+1) * box_h) + (line * offset_h) )  #i removed 1 to get the higher line (top left ())
                y = palet_h - (line + 1) * (box_h + offset_h)

                placement.append((x,y,box_w,box_h,self.right_box_degree))
                # myList[key] = line_placement
            # placement.append(line_placement)
        # return myList
        return placement

    def get_placement_list(self):
        #temp added
        if self.mode == "Standard":
            box_h = self.original_box.height()
            box_w = self.original_box.width()
            palet_h = self.dark_palet.height()
            palet_w = self.dark_palet.width()
            offset_h = 5
            offset_w = 5

            self.grid_list_left = self.calculate_left_palet_placement(box_h, box_w, palet_h, palet_w, offset_h,
                                                                  offset_w)
            print("left grid list: ", self.grid_list_left)
            self.grid_list_right = self.calculate_right_palet_placement(box_h, box_w, palet_h, palet_w, offset_h,
                                                                    offset_w)

    def switch_placement(self):
        if (self.left_placement == 1):
            self.left_placement = 0
            self.firstFlag = 2
            self.ui.leftPalet.setPixmap(self.flu_palet)
            self.ui.rightPalet.setPixmap(self.dark_palet)
            # to set the text in buttons
            if (self.right_box_degree == 0):
                self.ui.pushButton_9.setText("0 deg")
                self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                self.ui.box.setPixmap(self.original_box)
                self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

            elif (self.right_box_degree == 90):
                self.ui.pushButton_9.setText("90 deg")
                self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                self.ui.box.setPixmap(self.original_box)
                self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

            elif (self.right_box_degree == 180):
                self.ui.pushButton_9.setText("180 deg")
                self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                self.ui.box.setPixmap(self.original_box)
                self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

            elif (self.right_box_degree == 270):
                self.ui.pushButton_9.setText("270 deg")
                self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                self.ui.box.setPixmap(self.original_box)
                self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())



        elif (self.left_placement == 0):
            self.left_placement = 1
            self.firstFlag = 0
            self.ui.leftPalet.setPixmap(self.dark_palet)
            self.ui.rightPalet.setPixmap(self.flu_palet)
            # to set the text in buttons
            if (self.left_box_degree == 0):
                self.ui.pushButton_9.setText("0 deg")
                self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                self.ui.box.setPixmap(self.original_box)
                self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

            elif (self.left_box_degree == 90):
                self.ui.pushButton_9.setText("90 deg")
                self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                self.ui.box.setPixmap(self.original_box)
                self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

            elif (self.left_box_degree == 180):
                self.ui.pushButton_9.setText("180 deg")
                self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                self.ui.box.setPixmap(self.original_box)
                self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())
            elif (self.left_box_degree == 270):
                self.ui.pushButton_9.setText("270 deg")
                self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                self.ui.box.setPixmap(self.original_box)
                self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

        self.get_placement_list()
        self.update()

    def rotate(self):
        if(self.mode=="Standard"):
            print('rotate here', self.degree_check)
            if (self.highlight1 == 0 and self.left_placement == 1 or self.rotate_when_rtrev1==1):
                print('rotate here 2', self.degree_check)
                if self.left_degree_counter % 4 == 0 or  self.degree_check== 0:
                    self.left_degree_counter=0  #added latley
                    self.ui.pushButton_9.setText("0 deg")
                    self.left_box_degree = 0
                    self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())
                    self.degree_check=-1
                    self.rotate_when_rtrev1=0

                elif self.left_degree_counter % 4 == 1 or  self.degree_check== 90:
                    self.left_degree_counter = 1  # added latley
                    self.ui.pushButton_9.setText("90 deg")
                    self.left_box_degree = 90
                    self.original_box = QPixmap("box.png").scaled( self.height,self.width)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())
                    self.degree_check = -1
                    self.rotate_when_rtrev1 = 0

                elif self.left_degree_counter % 4 == 2 or  self.degree_check== 180:
                    self.left_degree_counter = 2  # added latley
                    self.ui.pushButton_9.setText("180 deg")
                    self.left_box_degree = 180
                    self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())
                    self.degree_check = -1
                    self.rotate_when_rtrev1 = 0

                elif self.left_degree_counter % 4 == 3 or  self.degree_check == 270:
                    self.left_degree_counter = 3  # added latley
                    self.ui.pushButton_9.setText("270 deg")
                    self.left_box_degree = 270
                    self.original_box = QPixmap("box.png").scaled(self.height,self.width)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())
                    self.degree_check = -1
                    self.rotate_when_rtrev1 = 0

                self.left_degree_counter += 1

            elif (self.highlight2 == 0 and self.left_placement == 0 or self.rotate_when_rtrev2==1):
                if self.right_degree_counter % 4 == 0 or  self.degree_check== 0:
                    self.right_degree_counter=0
                    self.ui.pushButton_9.setText("0 deg")
                    self.right_box_degree = 0
                    self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())
                    self.degree_check = -1
                    self.rotate_when_rtrev2 = 0

                elif self.right_degree_counter % 4 == 1 or  self.degree_check== 90:
                    self.right_degree_counter=1
                    self.ui.pushButton_9.setText("90 deg")
                    self.right_box_degree = 90
                    self.original_box = QPixmap("box.png").scaled(self.height,self.width)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())
                    self.degree_check = -1
                    self.rotate_when_rtrev2 = 0

                elif self.right_degree_counter % 4 == 2 or  self.degree_check== 180:
                    self.right_degree_counter=2
                    self.ui.pushButton_9.setText("180 deg")
                    self.right_box_degree = 180
                    self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())
                    self.degree_check = -1
                    self.rotate_when_rtrev2 = 0

                elif self.right_degree_counter % 4 == 3 or  self.degree_check== 270:
                    self.right_degree_counter=3
                    self.ui.pushButton_9.setText("270 deg")
                    self.right_box_degree = 270
                    self.original_box = QPixmap("box.png").scaled(self.height,self.width)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())
                    self.degree_check = -1
                    self.rotate_when_rtrev2 = 0
                self.right_degree_counter += 1

        elif(self.mode=='Random'):
            if (self.left_placement == 1):
                if self.left_degree_counter % 4 == 0 :
                    self.ui.pushButton_9.setText("0 deg")
                    self.left_box_degree = 0
                    self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

                elif self.left_degree_counter % 4 == 1:
                    self.ui.pushButton_9.setText("90 deg")
                    self.left_box_degree = 90
                    self.original_box = QPixmap("box.png").scaled(self.height, self.width)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

                elif self.left_degree_counter % 4 == 2:
                    self.ui.pushButton_9.setText("180 deg")
                    self.left_box_degree = 180
                    self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

                elif self.left_degree_counter % 4 == 3:
                    self.ui.pushButton_9.setText("270 deg")
                    self.left_box_degree = 270
                    self.original_box = QPixmap("box.png").scaled(self.height, self.width)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())
                self.left_degree_counter += 1

            elif ( self.left_placement == 0):
                if self.right_degree_counter % 4 == 0:
                    self.ui.pushButton_9.setText("0 deg")
                    self.right_box_degree = 0
                    self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

                elif self.right_degree_counter % 4 == 1:
                    self.ui.pushButton_9.setText("90 deg")
                    self.right_box_degree = 90
                    self.original_box = QPixmap("box.png").scaled(self.height, self.width)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

                elif self.right_degree_counter % 4 == 2:
                    self.ui.pushButton_9.setText("180 deg")
                    self.right_box_degree = 180
                    self.original_box = QPixmap("box.png").scaled(self.width, self.height)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())

                elif self.right_degree_counter % 4 == 3:
                    self.ui.pushButton_9.setText("270 deg")
                    self.right_box_degree = 270
                    self.original_box = QPixmap("box.png").scaled(self.height, self.width)
                    self.ui.box.setPixmap(self.original_box)
                    self.ui.box.setFixedSize(self.original_box.width(), self.original_box.height())
                self.right_degree_counter += 1

        self.get_placement_list()
        self.update()

    def create_shortcuts(self):
        # Creating a shortcut for the Exit action
        self.undo_shortcut = QShortcut(QKeySequence("Ctrl+z"), self)
        self.undo_shortcut.activated.connect(
            self.undo_last_step)  # when we press the shortcut it calls the function (undo last step)

    def setPaddingAndMargin(self, member):

        member.setContentsMargins(0, 0, 0, 200)
        member.setStyleSheet("QLabel { padding: 0px; }")

    def paintEvent(self, event):
        if self.firstFlag == 1 and self.left_placement == 1:

            # keeps the original box
            self.ui.box.setPixmap(self.original_box)
            painter = QPainter(self.ui.box.pixmap())

            if self.dragging:
                # to draw any moving box
                painter.drawPixmap(int(self.offset.x() - self.original_box.width() / 2),
                                   int(self.offset.y() - self.original_box.height() / 2),
                                   self.original_box)


        # if iam inside the left palet
        elif self.firstFlag == 0 and self.left_placement == 1:
            self.ui.leftPalet.setPixmap(self.dark_palet)
            self.ui.rightPalet.setPixmap(self.flu_palet)
            # to draw any moving box
            painter1 = QPainter(self.ui.leftPalet.pixmap())  # determie the painter of the painter device(left palet)

            if self.dragging:
                painter1.setPen(Qt.black)
                painter1.setBrush(QColor(237, 29, 36))  # Orijinal dikdörtgen rengi
                painter1.setOpacity(0.5)
                # this part need to be modified
                # for axis in self.grid_list:
                if self.mode == "Standard":

                    painter1.drawRect(self.grid_list_left[self.highlight1][0], self.grid_list_left[self.highlight1][1],
                                  self.original_box.width(), self.original_box.height())
                    painter1.setOpacity(1)
                    painter1.drawPixmap(int(self.offset.x() - self.original_box.width() / 2),
                                    int(self.offset.y() - self.original_box.height() / 2),
                                    self.original_box)




                elif self.mode == "Random":
                    print("out paint event1")
                    if len(self.boxes1) > 0:
                        for item in self.boxes1:  # Tüm mevcut dikdörtgenler için kontrol yap
                            box=QRect(item[0],item[1],item[2], item[3])
                            if box.intersects(QRect(int(self.offset.x() - self.original_box.width() / 2),
                                                int(self.offset.y() - self.original_box.height() / 2),
                                                self.original_box.width(), self.original_box.height())):
                                painter1.setBrush(QColor(237, 29, 36))
                                painter1.setOpacity(1)
                                painter1.drawRect(QRect(int(self.offset.x() - self.original_box.width() / 2),
                                                    int(self.offset.y() - self.original_box.height() / 2),
                                                    self.original_box.width(), self.original_box.height()))
                                self.RelaseNotAllowed = 1

                            else:
                                print("out paint event4")
                                self.RelaseNotAllowed = 0
                                painter1.setOpacity(1)

                                painter1.drawRect(QRect(int(self.offset.x() - self.original_box.width() / 2),
                                                    int(self.offset.y() - self.original_box.height() / 2),
                                                    self.original_box.width(), self.original_box.height()))
                    else:
                        print("out paint event5")
                        self.RelaseNotAllowed = 0
                        painter1.setOpacity(0.5)

                        painter1.drawRect(QRect(int(self.offset.x() - self.original_box.width() / 2),
                                            int(self.offset.y() - self.original_box.height() / 2),
                                            self.original_box.width(), self.original_box.height()))
            #temp added
            if self.mode == "Standard":
                for item in range(len(self.boxes1)):
                    if item < len(self.grid_list_left):
                        if (self.boxes1[item][4] == 0 or self.boxes1[item][4] == 180):
                            painter1.drawPixmap(self.boxes1[item][0], self.boxes1[item][1],
                                            self.original_box.scaled(self.width,self.height))
                            painter1.drawText(self.boxes1[item][0] + int(self.width / 2),
                                              self.boxes1[item][1] + int(self.height / 2), str(self.boxes1[item][5]))
                        if (self.boxes1[item][4] == 90 or self.boxes1[item][4] == 270):
                            painter1.drawPixmap(self.boxes1[item][0], self.boxes1[item][1],
                                                self.original_box.scaled(self.height,self.width))
                            painter1.drawText(self.boxes1[item][0] + int(self.width / 2),
                                              self.boxes1[item][1] + int(self.height / 2), str(self.boxes1[item][5]))


            #temp i modified here
            elif self.mode == "Random":
                for item in range(len(self.boxes1)):
                    if(self.boxes1[item][4]==0 or self.boxes1[item][4]==180):
                        painter1.drawPixmap(self.boxes1[item][0], self.boxes1[item][1],self.original_box.scaled(self.width,self.height))
                        painter1.drawText(self.boxes1[item][0] + int(self.width / 2),
                                          self.boxes1[item][1] + int(self.height / 2), str(self.boxes1[item][5]))


                    if (self.boxes1[item][4] == 90 or self.boxes1[item][4] == 270):
                        painter1.drawPixmap(self.boxes1[item][0], self.boxes1[item][1], self.original_box.scaled(self.height,self.width))
                        painter1.drawText(self.boxes1[item][0] + int(self.height / 2),
                                          self.boxes1[item][1] + int(self.width / 2), str(self.boxes1[item][5]))



        # if iam inside the right palet
        elif self.firstFlag == 2 and self.left_placement == 0:

            self.ui.leftPalet.setPixmap(self.flu_palet)
            self.ui.rightPalet.setPixmap(self.dark_palet)

            painter2 = QPainter(self.ui.rightPalet.pixmap())  # determie the painter of the painter device(left palet)

            if self.dragging:
                ##added as a copy by hesham
                painter2.setPen(Qt.black)
                painter2.setBrush(QColor(237, 29, 36))  # Orijinal dikdörtgen rengi
                painter2.setOpacity(0.5)

                if self.mode == "Standard":
                    painter2.drawRect(self.grid_list_right[self.highlight2][0], self.grid_list_right[self.highlight2][1],
                                  self.original_box.width(), self.original_box.height())
                    painter2.setOpacity(1)
                    painter2.drawPixmap(int(self.offset.x() - self.original_box.width() / 2),
                                    int(self.offset.y() - self.original_box.height() / 2),
                                    self.original_box)

                elif self.mode == "Random":
                    if len(self.boxes2) > 0:
                        for item in self.boxes2:  # Tüm mevcut dikdörtgenler için kontrol yap
                            box = QRect(item[0], item[1], item[2], item[3])
                            if box.intersects(QRect(int(self.offset.x() - self.original_box.width() / 2),
                                                    int(self.offset.y() - self.original_box.height() / 2),
                                                    self.original_box.width(), self.original_box.height())):
                                painter2.setBrush(QColor(237, 29, 36))
                                painter2.setOpacity(1)
                                painter2.drawRect(QRect(int(self.offset.x() - self.original_box.width() / 2),
                                                        int(self.offset.y() - self.original_box.height() / 2),
                                                        self.original_box.width(), self.original_box.height()))
                                self.RelaseNotAllowed = 1
                            else:
                                self.RelaseNotAllowed = 0
                                painter2.setOpacity(1)

                                painter2.drawRect(QRect(int(self.offset.x() - self.original_box.width() / 2),
                                                        int(self.offset.y() - self.original_box.height() / 2),
                                                        self.original_box.width(), self.original_box.height()))
                    else:
                        self.RelaseNotAllowed = 0
                        painter2.setOpacity(0.5)

                        painter2.drawRect(QRect(int(self.offset.x() - self.original_box.width() / 2),
                                                int(self.offset.y() - self.original_box.height() / 2),
                                                self.original_box.width(), self.original_box.height()))

            if self.mode == "Standard":
                # should be right boxes not left boxes only
                for item in range(len(self.boxes2)):
                    if item < len(self.grid_list_right):
                        if (self.boxes2[item][4] == 0 or self.boxes2[item][4] == 180):
                            painter2.drawPixmap(self.boxes2[item][0], self.boxes2[item][1],
                                            self.original_box.scaled(self.width, self.height))
                            painter2.drawText(self.boxes2[item][0] + int(self.width / 2),
                                              self.boxes2[item][1] + int(self.height / 2), str(self.boxes2[item][5]))
                        elif (self.boxes2[item][4] == 90 or self.boxes2[item][4] == 270):
                            painter2.drawPixmap(self.boxes2[item][0], self.boxes2[item][1],
                                                self.original_box.scaled( self.height,self.width))
                            painter2.drawText(self.boxes2[item][0] + int(self.width / 2),
                                              self.boxes2[item][1] + int(self.height / 2), str(self.boxes2[item][5]))

            elif self.mode == "Random":
                for item in range(len(self.boxes2)):
                    if (self.boxes2[item][4]==0 or self.boxes2[item][4]==180 ):
                        painter2.drawPixmap(self.boxes2[item][0],self.boxes2[item][1],self.original_box.scaled(self.width, self.height))
                        painter2.drawText(self.boxes2[item][0] + int(self.width / 2),
                                          self.boxes2[item][1] + int(self.height / 2), str(self.boxes2[item][5]))
                    elif (self.boxes2[item][4]==90 or self.boxes2[item][4]==270 ):
                        painter2.drawPixmap(self.boxes2[item][0],self.boxes2[item][1],self.original_box.scaled( self.height,self.width))
                        painter2.drawText(self.boxes2[item][0] + int(self.height / 2),
                                          self.boxes2[item][1] + int(self.width/ 2), str(self.boxes2[item][5]))


    def next_pallete(self):
        print('next palet enter')
        # note for future if we want to change the size of boxes we will modify grid list
        # if we press next pallete we will save the array in a global dictionary (x,y,degree)
        # self.main_dic={'left_palet_dic':{},'right_palet_dic':{}}
        if self.left_placement == 1:
            if self.mode == "Standard":
                left_or_right='Left_palette'
                boxes_limit_counter=0
                my_list={}
                for line in range(self.boxLineCount1 - 1):
                    if boxes_limit_counter < len(self.boxes1):
                        key = f'line{line}'
                        line_placement = []
                        for i in range(self.boxCountPerLine1 - 1):
                            if boxes_limit_counter<len(self.boxes1):
                                line_placement.append(self.boxes1[boxes_limit_counter])
                                boxes_limit_counter+=1
                            else:
                                break
                        my_list[key] = line_placement

                    else:
                        break
                self.draw_my_list(my_list,left_or_right)


            elif self.mode == "Random":
                left_or_right = 'Left_palette'
                boxes_limit_counter = 0
                my_list = {}

                key = f'line{10}'
                line_placement = []
                for i in range(len(self.boxes1)):
                    if boxes_limit_counter < len(self.boxes1):
                        line_placement.append(self.boxes1[i])
                        boxes_limit_counter += 1
                    else:
                        break
                my_list[key] = line_placement
                self.draw_my_list(my_list, left_or_right)


        elif self.left_placement == 0:
            if self.mode == "Standard":
                left_or_right = 'Right_palette'
                boxes_limit_counter = 0
                my_list = {}
                for line in range(self.boxLineCount2 - 1):
                    if boxes_limit_counter < len(self.boxes2):
                        key = f'line{line}'
                        line_placement = []
                        for i in range(self.boxCountPerLine2 - 1):
                            if boxes_limit_counter < len(self.boxes2):
                                line_placement.append(self.boxes2[boxes_limit_counter])
                                boxes_limit_counter += 1
                            else:
                                break
                        my_list[key] = line_placement

                    else:
                        break

                self.draw_my_list(my_list, left_or_right)


            elif self.mode == "Random":
                left_or_right = 'Right_palette'
                boxes_limit_counter = 0
                my_list = {}

                key = f'line{10}'
                line_placement = []
                for i in range(len(self.boxes2)):
                    if boxes_limit_counter < len(self.boxes2):
                        line_placement.append(self.boxes2[i])
                        boxes_limit_counter += 1
                    else:
                        break
                my_list[key] = line_placement
                self.draw_my_list(my_list, left_or_right)

        if self.double_clicked_flag == 1:
            self.update_numbers()
            self.double_clicked_flag = 0
            self.rotate_when_rtrev1=0
            self.rotate_when_rtrev2= 0


    def draw_my_list(self,my_list,left_or_right):
        print('iam in draw my list')
        if self.left_placement == 1 or left_or_right=='Left_palette':
            print("mylist =", my_list)
            self.add_to_table(my_list, left_or_right)

            if self.double_clicked_flag == 1:
                print('iam enter the double')
                self.main_dic['Left_palette'][self.palette_layer] = my_list
                print("main_dic00 :", self.main_dic)
                # self.double_clicked_flag = 0
            else:
                print('fullpalet_layer_check0', self.full_left_palet_number)
                self.main_dic['Left_palette'][f'layer{self.full_left_palet_number}'] = my_list
                print("main_dic00 :", self.main_dic)
                self.full_left_palet_number += 1

            # self.full_left_palet_number += 1
            self.boxes1 = []
            self.highlight1 = 0
            #self.left_box_numbering = 0
            self.update()

        elif self.left_placement == 0:
            print("mylist =", my_list)
            self.add_to_table(my_list, left_or_right)

            if self.double_clicked_flag == 1:
                self.main_dic['Right_palette'][self.palette_layer] = my_list
                print("main_dic :", self.main_dic)
                # self.double_clicked_flag = 0
                print('next palet exit')

            else:
                self.main_dic['Right_palette'][f'layer{self.full_right_palet_number}'] = my_list
                print("main_dic2 :", self.main_dic)
                print('next palet exit')
                self.full_right_palet_number += 1

            # self.full_right_palet_number += 1
            self.boxes2 = []
            self.highlight2 = 0
            #self.right_box_numbering = 0
            self.update()

    def add_to_table(self,mylist,left_or_right):
        print('add to table enter')
        #if we clicked on the table and modify on one
        if self.double_clicked_flag==1 :
            row_position=self.row

            if (left_or_right == 'Right_palette'):
                chkBoxItem = QTableWidgetItem(left_or_right + ' - ' + self.palette_layer)
                chkBoxItem.setCheckState(Qt.Unchecked)
                self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(chkBoxItem))
            elif (left_or_right == 'Left_palette'):
                chkBoxItem = QTableWidgetItem(left_or_right + ' - ' + self.palette_layer)
                chkBoxItem.setCheckState(Qt.Unchecked)
                self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(chkBoxItem))
        else:
            row_position = self.ui.tableWidget.rowCount()
            print('row pos1=',row_position )
            self.ui.tableWidget.insertRow(row_position)

            if (left_or_right == 'Right_palette'):
                chkBoxItem = QTableWidgetItem(left_or_right + ' - ' + f'layer{self.full_right_palet_number}')
                chkBoxItem.setCheckState(Qt.Unchecked)
                self.ui.tableWidget.setItem(row_position, 0, chkBoxItem)
            elif (left_or_right == 'Left_palette'):
                chkBoxItem = QTableWidgetItem(left_or_right + ' - ' + f'layer{self.full_left_palet_number}')
                chkBoxItem.setCheckState(Qt.Unchecked)
                self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(chkBoxItem))

        #adding image to the col1 and set the size
        label = QLabel()
        pixmap = QPixmap('darkPalet.png')
        label.setPixmap(pixmap)
        painter = QPainter(label.pixmap())

        self.ui.tableWidget.setCellWidget(row_position, 1, label)
        self.ui.tableWidget.setRowHeight(row_position, pixmap.height())

        if self.mode == "Standard":
            for item in mylist.values():
                for list_item in item:
                    if list_item[4] == 90 or list_item[4] == 270:
                        painter.drawPixmap(list_item[0], list_item[1], self.original_box.scaled(self.height,self.width))
                        painter.drawText(list_item[0] + int(self.height / 2),
                                          list_item[1] + int(self.width / 2), str(list_item[5]))


                    elif list_item[4] == 0 or list_item[4] == 180:
                        painter.drawPixmap(list_item[0], list_item[1], self.original_box.scaled(self.width,self.height))
                        painter.drawText(list_item[0] + int(self.width / 2),
                                          list_item[1] + int(self.height / 2), str(list_item[5]))
        elif self.mode == "Random":
            for item in mylist.values():
                for list_item in item:
                    print(list_item[4])
                    if list_item[4] == 0 or list_item[4] == 180:
                        painter.drawPixmap(list_item[0], list_item[1],  self.original_box.scaled(self.width,self.height))
                        painter.drawText(list_item[0] + int(self.width / 2),
                                         list_item[1] + int(self.height / 2), str(list_item[5]))
                    if list_item[4] == 90 or list_item[4] == 270:
                        painter.drawPixmap(list_item[0],list_item[1],  self.original_box.scaled(self.height,self.width))
                        painter.drawText(list_item[0] + int(self.height / 2),
                                         list_item[1] + int(self.width / 2), str(list_item[5]))

        self.table_counter += 1
        print('add to table exit')

    def retrieve_palet (self,index):
        print('iam in retrieve palet')
        self.double_clicked_flag=1
        self.row=index.row()
        col=index.column()

        #check the first col to know left or right and which layer
        table_item=self.ui.tableWidget.item(self.row,0)
        if table_item is not None:
            text_from_row=table_item.text()

        text_from_row=text_from_row.split()

        left_or_right=text_from_row[0]
        self.palette_layer = text_from_row[2]
        print('layer:',left_or_right,',,palette layer:',self.palette_layer)

        my_list=self.main_dic[left_or_right][self.palette_layer]


        print('mlist=',my_list)


        if ( left_or_right == 'Left_palette'):
            self.boxes1=[]
            self.rotate_when_rtrev1 = 1
            for item_list in list(self.main_dic[left_or_right][self.palette_layer].values()):
                for item in item_list:
                    self.boxes1.append(item)
                print("hahahah",left_or_right,self.palette_layer,self.boxes1)

                self.highlight1=len(self.boxes1)
                self.left_box_numbering=self.boxes1[-1][5]+1
                self.degree_check=self.boxes1[0][4]
                self.rotate()
                self.update()
        elif ( left_or_right == 'Right_palette'):
            self.boxes2 = []
            self.rotate_when_rtrev2 = 1
            for item_list in list(self.main_dic[left_or_right][self.palette_layer].values()):
                for item in item_list:
                    self.boxes2.append(item)
                print("hahahah", self.boxes2)
                self.highlight2 = len(self.boxes2)
                self.right_box_numbering = self.boxes2[-1][5]+1
                self.degree_check = self.boxes2[0][4]
                self.rotate()
                self.update()





    def undo_last_step(self):
        # hint check first flag to choose what to undo right or left palet
        if self.left_placement == 1:
            if self.boxes1:  # Check if there are any drawn boxes
                if self.highlight1 != 0:
                    self.highlight1 -= 1
                if self.left_box_numbering != 0:
                    self.left_box_numbering -= 1
                self.boxes1.pop()  # Remove the last drawn box
            self.update()  # Update the display to reflect the change

        elif self.left_placement == 0:
            if self.boxes2:  # Check if there are any drawn boxes
                if self.highlight2 != 0:
                    self.highlight2 -= 1
                if self.right_box_numbering != 0:
                    self.right_box_numbering -= 1
                self.boxes2.pop()  # Remove the last drawn box
            self.update()  # Update the display to reflect the change

    def repeate_palet(self):
        print('iam in repeat palet')
        self.repeat_flag = 1

        print('232232ps')
        #getting text from lineedit and convert it to numbers
        if '-' in self.ui.lineEdit.text():
            if (self.ui.lineEdit.text().split('-'))[1]=='':
                return
            elif len(self.ui.lineEdit.text().split('-'))==2:
                lower_edge= int((self.ui.lineEdit.text().split('-'))[0])
                higher_edge= int((self.ui.lineEdit.text().split('-'))[1])
                self.repeat_counter = lower_edge #to limit the loop of repetetion
        elif '-' not in self.ui.lineEdit.text():
            print('please enter a correct input and use ('-') to sepatrate')
            return
        else:
            print('please enter a correct input and use ('-') to sepatrate')
            return

        if '-' in self.ui.lineEdit2.text():
            lower_palet_to_repeat = int((self.ui.lineEdit2.text().split('-'))[0])
            higher_palet_to_repeat= int((self.ui.lineEdit2.text().split('-'))[1])
        elif '-' not in self.ui.lineEdit2.text():
            print(self.ui.lineEdit2.text().split()[0])
            lower_palet_to_repeat = int(self.ui.lineEdit2.text().split()[0])
            higher_palet_to_repeat=lower_palet_to_repeat
        else:
            print('please enter a correct input and use (' - ') to sepatrate')
            return

        #check if it exceeds the limits
        if higher_palet_to_repeat-1 > self.ui.tableWidget.rowCount():
            print('hhheheheh',higher_palet_to_repeat-1, ' ', self.ui.tableWidget.rowCount() )
            return

        if self.left_placement==1:
            left_or_right = 'Left_palette'
            if self.mode== 'Standard':
                for i in range(lower_edge, higher_edge + 1):
                    # boxes1_copy=[]
                    for layers in range(lower_palet_to_repeat, higher_palet_to_repeat + 1):
                        if self.repeat_counter > higher_edge:
                            break
                        palet_layer = f'layer{layers}'
                        for lines in self.main_dic[left_or_right][palet_layer].values():
                            for sub_line in lines:
                                self.boxes1.append(sub_line.copy())

                        for box in range(len(self.boxes1)):
                            print('main_while_repeat0 ', self.main_dic)
                            self.boxes1[box][5] = self.left_box_numbering
                            self.double_clicked_flag = 0
                            self.left_box_numbering += 1
                            print('repeat counter1', self.repeat_counter)
                        
                        # self.boxes1=boxes1_copy
                        print('main_while_repeat2 ', self.main_dic)

                        self.next_pallete()
                        self.repeat_counter += 1


                    if self.repeat_counter > higher_edge:
                        break

            elif self.mode=='Random':
                for i in range (lower_edge,higher_edge+1):
                    for layers in range( lower_palet_to_repeat,higher_palet_to_repeat+1):
                        if self.repeat_counter > higher_edge:
                            break
                        palet_layer = f'layer{layers}'
                        for lines in self.main_dic[left_or_right][palet_layer].values():
                            for sub_line in lines:
                                self.boxes1.append(sub_line.copy())
                        for box in range(len(self.boxes1)):
                            self.boxes1[box][5]=self.left_box_numbering
                            self.double_clicked_flag = 0
                            self.left_box_numbering+=1

                        self.next_pallete()
                        self.repeat_counter+=1

                    if self.repeat_counter > higher_edge:
                        break


        elif self.left_placement==0:
            left_or_right = 'Right_palette'
            if self.mode == 'Standard':
                for i in range(lower_edge, higher_edge + 1):
                    for layers in range(lower_palet_to_repeat, higher_palet_to_repeat + 1):
                        if self.repeat_counter > higher_edge:
                            break
                        palet_layer = f'layer{layers}'
                        for lines in self.main_dic[left_or_right][palet_layer].values():
                            for sub_line in lines:
                                self.boxes2.append(sub_line.copy())
                        for box in range(len(self.boxes2)):
                            self.boxes2[box][5] = self.right_box_numbering
                            self.right_box_numbering += 1
                        self.next_pallete()
                        self.repeat_counter += 1

                    if self.repeat_counter > higher_edge:
                        break

            elif self.mode == 'Random':
                for i in range(lower_edge, higher_edge + 1):
                    for layers in range(lower_palet_to_repeat, higher_palet_to_repeat + 1):
                        if self.repeat_counter > higher_edge:
                            break
                        palet_layer = f'layer{layers}'
                        for lines in self.main_dic[left_or_right][palet_layer].values():
                            for sub_line in lines:
                                self.boxes2.append(sub_line.copy())
                        for box in range(len(self.boxes2)):
                            self.boxes2[box][5] = self.right_box_numbering
                            self.right_box_numbering += 1
                        self.next_pallete()
                        self.repeat_counter += 1

                    if self.repeat_counter > higher_edge:
                        break
        print('main_dic_repeat', self.main_dic)

    def get_last_palet_number(self,palet_layer):
        print("ssss")
        palet_layer_number= int(re.findall(r'\d+', palet_layer)[0])
        print("hoola",palet_layer_number)
        return palet_layer_number

    def update_numbers(self):
        print('iam in update numbers')
        last_palet_retrved = self.palette_layer
        print('151215',last_palet_retrved)
        enter_flag=0
        if self.left_placement == 1:
            for layers in self.main_dic['Left_palette'].keys():
                if last_palet_retrved == layers:
                    enter_flag = 1
                    continue
                if enter_flag==1:
                    print('entered layer=',layers)
                    for lines in self.main_dic['Left_palette'][layers].keys():
                        for list in range(len(self.main_dic['Left_palette'][layers][lines])):
                            print('liiiiisyt',list)
                            self.main_dic['Left_palette'][layers][lines][list][5]=self.left_box_numbering
                            self.left_box_numbering+=1
                            print('updated list',self.main_dic['Left_palette'][layers][lines][list])


        elif self.left_placement == 0:
            for layers in self.main_dic['Right_palette'].keys():
                if last_palet_retrved == layers:
                    enter_flag = 1
                    continue
                if enter_flag == 1:
                    print('entered layer=', layers)
                    for lines in self.main_dic['Right_palette'][layers].keys():
                        for list in range(len(self.main_dic['Right_palette'][layers][lines])):
                            print('liiiiisyt', list)
                            self.main_dic['Right_palette'][layers][lines][list][5] = self.right_box_numbering
                            self.right_box_numbering += 1
                            print('updated list', self.main_dic['Right_palette'][layers][lines][list])

        #update palets in all the table
        if self.left_placement == 1:
            row_const=self.row
            for i in range(self.ui.tableWidget.rowCount()-row_const-1):
                print("holaaa")
                self.row+=1
                table_item = self.ui.tableWidget.item(self.row, 0)
                if table_item is not None:
                    text_from_row = table_item.text()

                text_from_row = text_from_row.split()

                left_or_right = text_from_row[0]
                if left_or_right=='Left_palette':
                    self.palette_layer = text_from_row[2]
                    print('layerr:', left_or_right, ',,palette layerrr:', self.palette_layer)

                    my_list = self.main_dic[left_or_right][self.palette_layer]
                    self.double_clicked_flag=1
                    self.add_to_table(my_list,left_or_right)
                    print('mlist6=', my_list)


        elif self.left_placement == 0:
            row_const = self.row
            for i in range(self.ui.tableWidget.rowCount() - row_const - 1):
                print("holaaa")
                self.row += 1
                table_item = self.ui.tableWidget.item(self.row, 0)
                if table_item is not None:
                    text_from_row = table_item.text()

                text_from_row = text_from_row.split()

                left_or_right = text_from_row[0]
                if left_or_right == 'Right_palette':
                    self.palette_layer = text_from_row[2]
                    print('layerr:', left_or_right, ',,palette layerrr:', self.palette_layer)

                    my_list = self.main_dic[left_or_right][self.palette_layer]
                    self.double_clicked_flag = 1
                    self.add_to_table(my_list, left_or_right)
                    print('mlist6=', my_list)




    def mousePressEvent(self, event):
        print('iam in mouse press event')
        if event.button() == Qt.LeftButton:
            # check if the mouse is pressed inside the box
            if (self.ui.box.rect().contains(self.ui.box.mapFromGlobal(event.globalPos()))):
                self.dragging = True
                self.offset = event.pos()
                self.firstMove = True
                # self.last_clicked = 0  #this means box has been pressed don't undo
                # print("Offset point", self.offset)
                print("Box position", self.ui.leftPalet.mapFromGlobal(
                    event.globalPos()))  # get the position of the box relative to left palet
            elif (self.ui.leftPalet.rect().contains(self.ui.leftPalet.mapFromGlobal(event.globalPos()))):
                # this means i (clicked) in the frame of the leftpalet label so i can make the commands(undo, new_palet) on it
                # self.last_clicked = 1
                # this means (the mouse is on) leftpalet
                self.firstFlag = 0
                # to make switch dark and flu according to the click
                self.ui.leftPalet.setPixmap(self.dark_palet)
                self.ui.rightPalet.setPixmap(self.flu_palet)
            elif (self.ui.rightPalet.rect().contains(self.ui.rightPalet.mapFromGlobal(event.globalPos()))):
                # this means i (clicked )(in the frame of the rightpalet) label so i can make the commands(undo, new_palet) on it
                # self.last_clicked = 2
                # this means the (mouse is on) rightpalet
                self.firstFlag = 2
            self.update()

    def mouseMoveEvent(self, event):
        print('iam in mouse move event')
        if self.dragging:
            # Sürüklenen box'ın merkezini güncelle
            self.offset = event.pos()
            # print(self.dark_palet.size())
            self.offset = self.ui.box.mapFromGlobal(event.globalPos()) + QPoint(520, 0)  # make it go out of the box

            if (self.offset.x() > 550):
                # iam in right palet
                self.firstFlag = 2
                self.offset = self.ui.box.mapFromGlobal(event.globalPos()) - QPoint(200, 0)

            elif (self.offset.x() > 450):
                # in the orinal box
                self.firstFlag = 1
                self.offset = self.ui.box.mapFromGlobal(event.globalPos())

            else:
                # iam in left palet
                self.offset = self.ui.box.mapFromGlobal(event.globalPos()) + QPoint(550, 0)
                self.firstFlag = 0

            print("Position:", self.offset)
            self.update()  # calls paintEvent
            print("out")

    def mouseReleaseEvent(self, event):
        print("iam in relesase")
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            print("RELEASE")
            self.relase = True
            #temp added
            if self.mode == "Random" and self.RelaseNotAllowed == 1:
                print("Dont let")
                self.RelaseNotAllowed = 0
                return

            if self.firstFlag == 0 and self.left_placement == 1:
                if self.mode == "Random":
                    print("new box")
                    if (int(self.offset.x() - self.original_box.width() / 2) < 0):
                        self.offset = QPoint(int(self.original_box.width() / 2), self.offset.y())
                    elif (int(self.offset.x() + self.original_box.width() / 2) > self.dark_palet.width()):
                        print("1sdsd")

                        self.offset = QPoint(self.dark_palet.width() - int(self.original_box.width() / 2),
                                             self.offset.y())
                        print(self.offset)
                    elif (int(self.offset.y() + self.original_box.height() / 2) > self.dark_palet.height()):
                        self.offset = QPoint(self.offset.x(),
                                             self.dark_palet.height() - int(self.original_box.height() / 2))
                    elif (int(self.offset.y() - self.original_box.height() / 2) < 0):
                        self.offset = QPoint(self.offset.x(),
                                             int(self.original_box.height() / 2))

                    new_box = [int(self.offset.x() - self.original_box.width() / 2),
                                    int(self.offset.y() - self.original_box.height() / 2),
                                    self.original_box.width(), self.original_box.height(),self.left_box_degree,self.left_box_numbering]
                    self.boxes1.append(new_box)
                    self.left_box_numbering += 1
                    print("BEfore release",self.boxes1)
                    self.update()
                elif self.mode == "Standard":
                    if len(self.boxes1) < len(self.grid_list_left):
                        new_box = [self.grid_list_left[self.highlight1][0],self.grid_list_left[self.highlight1][1],
                                        self.original_box.width(), self.original_box.height(),self.left_box_degree,self.left_box_numbering]

                        self.boxes1.append(new_box)
                        self.left_box_numbering += 1

                    if self.highlight1 < len(self.grid_list_left) - 1:
                        self.highlight1 += 1


            elif self.firstFlag == 2 and self.left_placement == 0:
                if (int(self.offset.x() - self.original_box.width() / 2) < 0):
                    print("HERE")
                    self.offset = QPoint(int(self.original_box.width() / 2), self.offset.y())
                elif (int(self.offset.x() + self.original_box.width() / 2) > self.dark_palet.width()):
                    print("1sdsd")
                    self.offset = QPoint(self.dark_palet.width() - int(self.original_box.width() / 2), self.offset.y())
                elif (int(self.offset.y() + self.original_box.height() / 2) > self.dark_palet.height()):
                    print("2sdsd")

                    self.offset = QPoint(self.offset.x(),
                                         self.dark_palet.height() - int(self.original_box.height() / 2))
                elif (int(self.offset.y() - self.original_box.height() / 2) < 0):
                    self.offset = QPoint(self.offset.x(),
                                         int(self.original_box.height() / 2))
                if self.mode == "Random" and self.RelaseNotAllowed == 1:
                    print("Dont let")
                    self.RelaseNotAllowed = 0
                    return

                if self.mode == "Random":
                    print("new box")
                    new_box = [int(self.offset.x() - self.original_box.width() / 2),
                                    int(self.offset.y() - self.original_box.height() / 2),
                                    self.original_box.width(), self.original_box.height(),self.right_box_degree,self.right_box_numbering]
                    self.boxes2.append(new_box)
                    self.right_box_numbering += 1
                    print("BEfore release", self.boxes2)
                    self.update()
                    # return

                if self.mode == "Standard":
                    if len(self.boxes2) < len(self.grid_list_right):
                        new_box = [self.grid_list_right[self.highlight2][0], self.grid_list_right[self.highlight2][1],
                                   self.original_box.width(), self.original_box.height(), self.right_box_degree,self.right_box_numbering]

                        self.boxes2.append(new_box)
                        self.right_box_numbering += 1
                    if self.highlight2 < len(self.grid_list_right) - 1:
                        self.highlight2 += 1
            self.update()
            print("iam out relesase")

    def generate_paletization(self, list):
        print("BEfore",list)
        print(self.dark_palet.width())
        print(self.dark_palet.height())
        # deepcopy
        my_list = copy.deepcopy(list)
        # my_list.append(list)
        print("Before",self.width,self.height)

        index = 0
        layerIndex = 0

        box_size = self.format_box_size(self.y, self.x, self.box_depth)
        palette_size = self.format_palette_size(self.palet_height, self.palet_width, self.palet_depth)

        if self.mode == "Random":
            for palet in my_list['Left_palette'].values():
                for item in palet['line10']:
                    print("before item",item[0],item[1],self.width)

                    if item[4] == 0 or item[4] == 180:
                        item[0] = self.dark_palet.width() - int((self.width)/2)-item[0] #sadece solsa bunu yapacağız.
                        item[1] = item[1]+ int(self.height/2)
                        item[0], item[1] = self.scale_box_center((self.dark_palet.width(), self.dark_palet.height()),
                                                                 (self.palet_width, self.palet_height)
                                                                 ,  (item[0], item[1]), )

                    if item[4] == 90 or item[4] == 270:
                        print("Angle 90")
                        item[0] = self.dark_palet.width() - int((self.height) / 2) - item[0]  # sadece solsa bunu yapacağız.
                        item[1] = item[1] + int(self.width / 2)

                        item[0], item[1] = self.scale_box_center((self.dark_palet.height(), self.dark_palet.width()),
                                                                 (self.palet_height, self.palet_width)
                                                                 , (item[0], item[1]), )



                        print(item[0],item[1])

            for palet2 in my_list['Right_palette'].values():
                for palet2 in my_list['Right_palette'].values():
                    for item in palet2['line10']:
                        if item[4] == 0 or item[4] == 180:
                            item[0] = item[0]+int(self.width/2)
                            item[1] = item[0]+int(self.height/2)
                            item[0], item[1] = self.scale_box_center(
                                (self.dark_palet.width(), self.dark_palet.height()),
                                (self.palet_width, self.palet_height)
                                , (item[0], item[1]), )
                        if item[4] == 90 or item[4] == 270:
                            item[0] = item[0] + int(self.height / 2)
                            item[1] = item[0] + int(self.width / 2)
                            item[0], item[1] = self.scale_box_center(
                                (self.dark_palet.height(), self.dark_palet.width()),
                                (self.palet_height, self.palet_width)
                                , (item[0], item[1]), )

                    # item[1] =self.dark_palet.height() - int(self.width)-item[1]


                        # print(newItem[0],newItem[1])
        if self.mode == "Standard":
            for palet in my_list['Left_palette'].values():
                print(palet)
                for line in palet.values():
                    for i, item in enumerate(line):
                        print(item[0], item[1])
                        if item[4] == 0 or item[4] == 180:
                            x = self.dark_palet.width() - int((self.width) / 2) - item[0]
                            y = item[1] + int(self.height / 2)
                            x, y = self.scale_box_center(
                                (self.dark_palet.width(), self.dark_palet.height()),
                                (self.palet_width, self.palet_height),
                                (x, y),
                            )
                            line[i] = (x, y, item[2], item[3], item[4])

                        if item[4] == 90 or item[4] == 270:
                            print("Angle 90")
                            x = self.dark_palet.width() - int((self.height) / 2) - item[0]
                            y = item[1] + int(self.width / 2)
                            x, y = self.scale_box_center(
                                (self.dark_palet.height(), self.dark_palet.width()),
                                (self.palet_height, self.palet_width),
                                (x, y),
                            )
                            line[i] = (x, y, item[2], item[3], item[4])




        left_palette_data = ""
        left_palette_data += f"Box_{box_size}\n"
        left_palette_data += f"Pallet_Size_{palette_size}\n"
        for layer_name, layer_data in my_list['Left_palette'].items():
            for line_name, coordinates in layer_data.items():
                left_palette_data += self.format_layer(layer_name, coordinates)
        self.write_to_file(left_palette_data, "left.txt")

        # Format and write right palette data (currently empty)
        right_palette_data = ""
        for layer_name, layer_data in my_list['Right_palette'].items():
            for line_name, coordinates in layer_data.items():
                right_palette_data += self.format_layer(layer_name, coordinates)
        self.write_to_file(right_palette_data, "right.txt")

        print("before",list)
        print("AFTER",my_list)

    def write_to_file(self,data, filename):
        with open(filename, 'w') as f:
            f.write(data)

    def format_box_size(self,height, width, depth):
        return f"{height:03d}x{width:03d}x{depth:03d}"

    def format_palette_size(self,height, width, depth):
        return f"{height:04d}x{width:04d}x{depth:04d}"

    def format_layer(self,layer_name, coordinates):
        layer_str = f"{layer_name}\n"
        for i, coord in enumerate(coordinates, start=1):
            x, y, r = coord[0], coord[1], coord[4]  # Koordinatları alırken iç içe geçmiş listeyi düzeltiyoruz
            layer_str += f"{i:02d}({x},{y},{r})\n"
        layer_str += "End_of_" + layer_name + "\n"
        return layer_str

    def calculate_scaling(self,old_size, old_position, new_size):
        print(old_size)
        # Calculate scaling factor
        scale_factor = (new_size[0] / old_size[0], new_size[1] / old_size[1])

        # Calculate new position
        new_position = (round(old_position[0] * scale_factor[0]), round(old_position[1] * scale_factor[1]))

        return new_position

    def scale_box_center(self,current_pallet_size, new_pallet_size, current_box_center):
        # Calculate scale factor
        scale_factor = (new_pallet_size[0] / current_pallet_size[0], new_pallet_size[1] / current_pallet_size[1])

        # Scale box size
        # scaled_box_size = int(current_box_size[0] * scale_factor[0], current_box_size[1] * scale_factor[1])

        # Scale box center position
        scaled_box_center = (round(current_box_center[0] * scale_factor[0]), round(current_box_center[1] * scale_factor[1]))

        return  scaled_box_center




if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
            QToolTip
{
     border: 1px solid black;
     background-color: #ffa02f;
     padding: 1px;
     border-radius: 3px;
     opacity: 100;
}

QWidget
{
    color: #b1b1b1;
    background-color: #3A3B3A;
}

QTreeView, QListView
{
    background-color: #B7B7B8;
    margin-left: 5px;
}

QWidget:item:hover
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ED1D24, stop: 1 #ED1D24);
    color: #000000;
}

QWidget:item:selected
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ED1D24, stop: 1 #ED1D24);
}

QMenuBar::item
{
    background: transparent;
}

QMenuBar::item:selected
{
    background: transparent;
    border: 1px solid #ffaa00;
}

QMenuBar::item:pressed
{
    background: #444;
    border: 1px solid #000;
    background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:1 #212121,
        stop:0.4 #343434/*,
        stop:0.2 #343434,
        stop:0.1 #ffaa00*/
    );
    margin-bottom:-1px;
    padding-bottom:1px;
}

QMenu
{
    border: 1px solid #000;
}

QMenu::item
{
    padding: 2px 20px 2px 20px;
}

QMenu::item:selected
{
    color: #000000;
}

QWidget:disabled
{
    color: #808080;
    background-color: #323232;
}

QAbstractItemView
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);
}

QWidget:focus
{
    /*border: 1px solid darkgray;*/
}

QLineEdit
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);
    padding: 1px;
    border-style: solid;
    border: 1px solid #1e1e1e;
    border-radius: 5;
}

QPushButton
{
    color: #FFFFFF;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ED1D24, stop: 0.9 #ED1D24, stop: 1 #000000);
    border-width: 0.5px;
    border-color: #000000;
    border-style: solid;
    border-radius: 6;
    padding: 3px;
    font-size: 14px;
    padding-left: 5px;
    padding-right: 5px;
    min-width: 40px;
}

QPushButton:pressed
{
    background-color:  #610C04;
}

QComboBox
{
    selection-background-color: #ED1D24;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
    border-style: solid;
    border: 1px solid #1e1e1e;
    border-radius: 5;
}

QComboBox:hover,QPushButton:hover
{
    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ff0000, stop: 1 #ff0000);
}


QComboBox:on
{
    padding-top: 3px;
    padding-left: 4px;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
    selection-background-color: #ffaa00;
}

QComboBox QAbstractItemView
{
    border: 2px solid darkgray;
    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QComboBox::drop-down
{
     subcontrol-origin: padding;
     subcontrol-position: top right;
     width: 15px;

     border-left-width: 0px;
     border-left-color: darkgray;
     border-left-style: solid; /* just a single line */
     border-top-right-radius: 3px; /* same radius as the QComboBox */
     border-bottom-right-radius: 3px;
 }

QComboBox::down-arrow
{
     image: url(:/dark_orange/img/down_arrow.png);
}

QGroupBox
{
    border: 1px solid darkgray;
    margin-top: 10px;
}

QGroupBox:focus
{
    border: 1px solid darkgray;
}

QTextEdit:focus
{
    border: 1px solid darkgray;
}

QScrollBar:horizontal {
     border: 1px solid #222222;
     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);
     height: 7px;
     margin: 0px 16px 0 16px;
}

QScrollBar::handle:horizontal
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);
      min-height: 20px;
      border-radius: 2px;
}

QScrollBar::add-line:horizontal {
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);
      width: 14px;
      subcontrol-position: right;
      subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);
      width: 14px;
     subcontrol-position: left;
     subcontrol-origin: margin;
}

QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal
{
      border: 1px solid black;
      width: 1px;
      height: 1px;
      background: white;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{
      background: none;
}

QScrollBar:vertical
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);
      width: 7px;
      margin: 16px 0 16px 0;
      border: 1px solid #222222;
}

QScrollBar::handle:vertical
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);
      min-height: 20px;
      border-radius: 2px;
}

QScrollBar::add-line:vertical
{
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
      height: 14px;
      subcontrol-position: bottom;
      subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical
{
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);
      height: 14px;
      subcontrol-position: top;
      subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
{
      border: 1px solid black;
      width: 1px;
      height: 1px;
      background: white;
}


QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
      background: none;
}

QTextEdit
{
    background-color: #242424;
}

QPlainTextEdit
{
    background-color: #242424;
}

QHeaderView::section
{
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);
    color: white;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
}

QCheckBox:disabled
{
color: #414141;
}

QDockWidget::title
{
    text-align: center;
    spacing: 3px; /* spacing between items in the tool bar */
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);
}

QDockWidget::close-button, QDockWidget::float-button
{
    text-align: center;
    spacing: 1px; /* spacing between items in the tool bar */
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);
}

QDockWidget::close-button:hover, QDockWidget::float-button:hover
{
    background: #242424;
}

QDockWidget::close-button:pressed, QDockWidget::float-button:pressed
{
    padding: 1px -1px -1px 1px;
}

QMainWindow::separator
{
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);
    color: white;
    padding-left: 4px;
    border: 1px solid #4c4c4c;
    spacing: 3px; /* spacing between items in the tool bar */
}

QMainWindow::separator:hover
{

    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);
    color: white;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
    spacing: 3px; /* spacing between items in the tool bar */
}

QToolBar::handle
{
     spacing: 3px; /* spacing between items in the tool bar */
     background: url(:/dark_orange/img/handle.png);
}

QMenu::separator
{
    height: 2px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);
    color: white;
    padding-left: 4px;
    margin-left: 10px;
    margin-right: 5px;
}

QProgressBar
{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center;
}

QProgressBar::chunk
{
    background-color: #d7801a;
    width: 2.15px;
    margin: 0.5px;
}

QTabBar::tab {
    color: #b1b1b1;
    border: 1px solid #444;
    border-bottom-style: none;
    background-color: #323232;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 2px;
    margin-right: -1px;
}

QTabWidget::pane {
    border: 1px solid #444;
    top: 1px;
}

QTabBar::tab:last
{
    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
    border-top-right-radius: 3px;
}

QTabBar::tab:first:!selected
{
 margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */


    border-top-left-radius: 3px;
}

QTabBar::tab:!selected
{
    color: #b1b1b1;
    border-bottom-style: solid;
    margin-top: 3px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);
}

QTabBar::tab:selected
{
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    margin-bottom: 0px;
}

QTabBar::tab:!selected:hover
{
    /*border-top: 2px solid #ffaa00;
    padding-bottom: 3px;*/
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);
}

QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{
    color: #b1b1b1;
    background-color: #323232;
    border: 1px solid #b1b1b1;
    border-radius: 6px;
}

QRadioButton::indicator:checked
{
    background-color: qradialgradient(
        cx: 0.5, cy: 0.5,
        fx: 0.5, fy: 0.5,
        radius: 1.0,
        stop: 0.25 #ffaa00,
        stop: 0.3 #323232
    );
}

QCheckBox::indicator{
    color: #b1b1b1;
    background-color: #323232;
    border: 1px solid #b1b1b1;
    width: 9px;
    height: 9px;
}

QRadioButton::indicator
{
    border-radius: 6px;
}

QRadioButton::indicator:hover, QCheckBox::indicator:hover
{
    border: 1px solid #ffaa00;
}

QCheckBox::indicator:checked
{
    image:url(:/dark_orange/img/checkbox.png);
}

QCheckBox::indicator:disabled, QRadioButton::indicator:disabled
{
    border: 1px solid #444;
}


QSlider::groove:horizontal {
    border: 1px solid #3A3939;
    height: 8px;
    background: #201F1F;
    margin: 2px 0;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
      stop: 0.0 silver, stop: 0.2 #a8a8a8, stop: 1 #727272);
    border: 1px solid #3A3939;
    width: 14px;
    height: 14px;
    margin: -4px 0;
    border-radius: 2px;
}

QSlider::groove:vertical {
    border: 1px solid #3A3939;
    width: 8px;
    background: #201F1F;
    margin: 0 0px;
    border-radius: 2px;
}

QSlider::handle:vertical {
    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 silver,
      stop: 0.2 #a8a8a8, stop: 1 #727272);
    border: 1px solid #3A3939;
    width: 14px;
    height: 14px;
    margin: 0 -4px;
    border-radius: 2px;
}

QAbstractSpinBox {
    padding-top: 2px;
    padding-bottom: 2px;
    border: 1px solid darkgray;

    border-radius: 2px;
    min-width: 50px;
}


        """)

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec_())


