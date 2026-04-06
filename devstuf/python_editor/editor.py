from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QLabel, QGridLayout, QTextEdit, QScrollArea, QMessageBox
)
from pyqt6_multiselect_combobox import MultiSelectComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from copy import deepcopy
from enum import Enum
import sys

save_location = 'saved_list.txt'
export_location = '../../src/assets/projectlist.json'
data_length = 8

curr_save_indx = 0

tagsList = [
    ['class_project', 'Class Project', "false"],
    ['game_jam', 'Game Jam', "true"],
    ['group', 'Group Project', "true"],
    ['solo', 'Solo', "true"],
    ['program', 'Program', "true"],
    ['godot', 'Godot', "true"],
    ['unity', 'Unity', "true"],
    ['python', 'Python', "true"],
    ['cpp', 'C++', "true"],
    ['cs', 'C#', "true"],
    ['java', 'Java', "true"],
    ['vue', 'Vue.js', "true"],
    ['postgres', 'PostgreSQL', "true"],
    ['nim', 'Nim', "true"],
    ['vhdl', 'VHDL', "true"]
]

# load save data
save_data = open(save_location).readlines()
for line in range(len(save_data)):
    if (save_data[line].endswith('\n')):
        save_data[line] = save_data[line][:-1]

# save current data
def save_curr_data():
    # rewrite save file
    with open(save_location, "w") as f:
        for datum in save_data:
            print(datum, file=f)

# ADDING A NEW CATEGORY
def expand_save_data():
    global data_length
    curr_len = int(len(save_data)/data_length)
    for i in range(curr_len):
        save_data.insert((i+1)*data_length + i, "")
    data_length += 1
    print("NEW LENGTH: ", data_length)


# export current data
def export_curr_data():
    # rewrite save file
    with open(export_location, "w") as f:
        size = int(len(save_data)/data_length)
        print("{\n\t\"size\": \"", size, "\",\n\t\"0\": \"",end='',sep='', file=f)
        tagOrder = [tagname[0] for tagname in tagsList]
        for datum in range(len(save_data)):

            # check if tag (SPECIAL CASE)
            if (datum % data_length == 3):
                tags = save_data[datum].split(" ")
                for tag in tags:
                    tag = tag.strip()
                    if tag in tagOrder:
                        # print id number
                        print(tagOrder.index(tag),end='',file=f)
                        # space separation
                        if (tag != tags[-1]):
                            print(' ',end='', file=f)
                print("\\n",end="",file=f)
                continue

            # check if fav (SPECIAL CASE)
            if (datum % data_length == 7):
                continue


            # otherwise print line
            print(save_data[datum],end='',file=f)
            # separate every project
            if (datum % data_length == data_length-2 and datum < len(save_data)-3):
                print("\",\n\t\"", int((datum/data_length)+1), "\": \"",end="",sep="", file=f)
            else:
                print("\\n",end='', file=f)
        
        # print the tagslist
        print("\",\n\t\"tagslist\": [", end="", file=f)
        for tag in tagsList:
            print("[\"", tag[0], "\", \"", tag[1], "\", ", tag[2], "]", sep="",end="", file=f)
            if (tagsList.index(tag) < len(tagsList)-1):
                print(",\n\t\t", end="", file=f)
        
        print("]",end='', file=f)

        favs = []
        for i in range(size):
            if (save_data[i*data_length + 7] == "T"):
                favs.append(i)

        print(",\n\t\"favs\": [",end='',sep='', file=f)
        for fav in favs:
            print("\"", fav, "\"", sep="",end="", file=f)
            if (favs.index(fav) < len(favs)-1):
                print(",", end="", file=f)
        print("]\n}",end='', file=f)


        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Successfully exported")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


# FORMAT PREVIEW:
# [Title]
# [Source Code URL]
# [Run URL]
# [Tags]
# [Preview IMG Name]
# [date; description]
# [Notable mention: notable mention]


class ProjectEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setWindowTitle("Edit Project")
 
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ADD THE TITLE EDITOR
        layout.addWidget(QLabel("Title:"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.title = QLineEdit()
        self.title.setFixedWidth(200)
        self.title.textEdited.connect(self.textUpdated)
        layout.addWidget(self.title, alignment= Qt.AlignmentFlag.AlignCenter)
        
        # ADD THE SOURCE CODE URL INPUT
        layout.addWidget(QLabel("\nSource Code URL:"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.src_url = QLineEdit()
        self.src_url.setFixedWidth(300)
        self.src_url.textEdited.connect(self.textUpdated)
        layout.addWidget(self.src_url, alignment= Qt.AlignmentFlag.AlignCenter)
        
        # ADD THE RUN URL INPUT
        layout.addWidget(QLabel("\nRun URL:"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.run_url = QLineEdit()
        self.run_url.setFixedWidth(300)
        self.run_url.textEdited.connect(self.textUpdated)
        layout.addWidget(self.run_url, alignment= Qt.AlignmentFlag.AlignCenter)

        # ADD THE TAGS INPUT
        layout.addWidget(QLabel("\nTags:"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.tags = MultiSelectComboBox()
        for tag in tagsList:
            self.tags.addItem(tag[1], tag[0])
        self.tags.setFixedWidth(300)
        self.tags.currentTextChanged.connect(self.textUpdated)
        layout.addWidget(self.tags, alignment= Qt.AlignmentFlag.AlignCenter)
 
        # ADD THE IMG URL INPUT
        layout.addWidget(QLabel("\nIMG Name:"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.img_url = QLineEdit()
        self.img_url.setFixedWidth(200)
        self.img_url.textEdited.connect(self.textUpdated)
        layout.addWidget(self.img_url, alignment= Qt.AlignmentFlag.AlignCenter)

        # ADD THE DESCRIPTION INPUT
        layout.addWidget(QLabel("\nDescription (and Date):"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.desc = QTextEdit()
        self.desc.setFixedWidth(400)
        self.desc.textChanged.connect(self.textUpdated)
        layout.addWidget(self.desc, alignment= Qt.AlignmentFlag.AlignCenter)
        
        # ADD THE NOTABLE MENTION INPUT
        layout.addWidget(QLabel("\nNotable Mention:"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.mention = QTextEdit()
        self.mention.setFixedWidth(400)
        self.mention.textChanged.connect(self.textUpdated)
        layout.addWidget(self.mention, alignment= Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(QLabel("\n"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.button = QPushButton("\nS A V E\n")
        self.button.clicked.connect(self.update_data)
        self.button.setStyleSheet("")
        self.button.setFont(QFont("Impact", pointSize=20))
        layout.addWidget(self.button)
    
    def set_to_index(self, indx):
        self.index = indx*data_length
        self.title.setText(save_data[self.index])
        self.setWindowTitle("Edit Project \""+save_data[self.index]+"\"")
        self.src_url.setText(save_data[self.index+1])
        self.run_url.setText(save_data[self.index+2])
        # parse the tags
        tag_list = save_data[self.index+3].split(' ')
        indices_list = []
        for tag in tag_list:
            tag = tag.strip()
            success = False
            for idx in range(len(tagsList)):
                if (tag in tagsList[idx]):
                    indices_list.append(idx)
                    success = True
            if not success: print("ERROR: could not find tag \"", tag, "\"")
        self.tags.setCurrentIndexes(indices_list)

        self.img_url.setText(save_data[self.index+4])
        self.desc.setText(save_data[self.index+5])
        self.mention.setText(save_data[self.index+6])
        
        # reset button
        self.button.setStyleSheet("")

 
    def update_data(self):
        # get curr data
        thislist = self.grab_data()
        # remove save prompt
        self.button.setStyleSheet("")
        self.setWindowTitle("Edit "+thislist[0])
        # update vals
        for i in range(data_length):
            if (i != 7): # skip fav because fav isnt here
                save_data[self.index+i] = thislist[i]
        # save and refresh
        save_curr_data()

        refresh()
    
    # verify the text was updated, and show green save button
    def textUpdated(self):
        # CHECK IF WAS ACTUALLY UPDATED
        thislist = self.grab_data()

        for i in range(data_length):
            if (thislist[i] != save_data[self.index+i]):
                #print("\"", thislist[i], "\" IS NOT \"", save_data[self.index+i], "\"")
                # FOUND A DIFF FROM LAST SAVE; CHANGE COLOR AND GET OUTTA HERE
                self.setWindowTitle("Edit "+thislist[0]+"*")
                self.button.setStyleSheet("background-color:#0d4;color:#000")
                return
        self.setWindowTitle("Edit "+thislist[0])
        self.button.setStyleSheet("")

 
    # grab the data from the inputs
    def grab_data(self):
        # format everything
        thislist = ['']*data_length
        thislist[0] = self.title.text()
        thislist[1] = self.src_url.text()
        thislist[2] = self.run_url.text()
        thislist[3] = ''
        for tag in self.tags.currentData():
            thislist[3] += tag + ' '
        thislist[3] = thislist[3][:-1]
        thislist[4] += self.img_url.text()
        thislist[5] += self.desc.toPlainText()
        thislist[6] += self.mention.toPlainText()
        return thislist

class ProjectManager(QWidget):
    favbuttons = []

    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        self.setWindowTitle("Project List")

        self.editWindow = None
 
        layout = QGridLayout()
        self.setLayout(layout)

        item = QLabel("Projects")
        layout.addWidget(item, 0, 0)

        # Add project
        item = QPushButton("Add New Project")
        item.clicked.connect(self.addNewProject)
        item.setStyleSheet("""QPushButton {background-color:#0d4;color:#000}
                           QPushButton:pressed {background-color:#0b2}""")
        item.setFont(QFont("Impact", 12))
        layout.addWidget(item, 0, 1)

        # Export List to JSON
        item = QPushButton("Export to JSON")
        item.clicked.connect(export_curr_data)
        item.setStyleSheet("""QPushButton {background-color:#ff0;color:#000}
                           QPushButton:pressed {background-color:#bb0;color:#fff}""")
        layout.addWidget(item, 0, 2)

        # add scroll region
        scrollarea = QScrollArea()
        scrollarea.setWidgetResizable(True)
        layout.addWidget(scrollarea, 1, 0, 1, 3)

        self.scroll_region = QGridLayout()
        container_widget = QWidget()
        container_widget.setLayout(self.scroll_region)
        scrollarea.setWidget(container_widget)


        self.refreshProjects()

    def refreshProjects(self):
        layout = self.scroll_region

        # CLEAR ALL WIDGETS
        for i in reversed(range(layout.count())):
            widget = layout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.favbuttons = []

        # LIST THE PROJECTS
        for i in range(0, len(save_data), data_length):
            # BREAK OUT IF INVALID
            if i+data_length-1 > len(save_data): break

            levelIndx = int(round(i/data_length) + 1)

            button = QPushButton("*")
            button.setFixedWidth(30)
            button.clicked.connect(lambda state, x=levelIndx-1:self.setFav(x))
            if (save_data[i+7]=="T"):
                button.setStyleSheet("""QPushButton {background-color:#ff0;color:#000}
                                QPushButton:hover {background-color:#bb0;color:#000}
                                QPushButton:pressed {background-color:#990;color:#000}""")
            else: button.setStyleSheet("")
            layout.addWidget(button, levelIndx, 0)
            self.favbuttons.append(button)

            button = QPushButton(save_data[i])
            button.clicked.connect(lambda state, x=levelIndx-1:self.editProject(x))
            layout.addWidget(button, levelIndx, 1)
            button = QLabel(save_data[i+5].split(";")[0])
            button.setFixedWidth(100)
            layout.addWidget(button, levelIndx, 2)
            button = QPushButton("v")
            button.setFixedWidth(40)
            button.clicked.connect(lambda state, x=levelIndx:swapPrev(x))
            layout.addWidget(button, levelIndx, 3)
            button = QPushButton("^")
            button.setFixedWidth(40)
            button.clicked.connect(lambda state, x=levelIndx-1:swapPrev(x))
            layout.addWidget(button, levelIndx, 4)

            button = QPushButton("DEL")
            button.setStyleSheet("""QPushButton {background-color:#f00;color:#fff}
                            QPushButton:hover {background-color:#b00;color:#fff}
                            QPushButton:pressed {background-color:#900;color:#fff}""")
            button.setFixedWidth(40)
            button.clicked.connect(lambda state, x=levelIndx-1:self.delProject(x))
            layout.addWidget(button, levelIndx, 5)
    
    def editProject(self, index):
        if (self.editWindow is None):
            self.editWindow = ProjectEditor()
        
        self.editWindow.set_to_index(index)

        self.editWindow.show()
    
    def addNewProject(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Confirm Project Creation")
        msgBox.setText("Are you sure you want to create a new project?")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msgBox.setDefaultButton(QMessageBox.StandardButton.No)
        result = msgBox.exec()

        if (result != QMessageBox.StandardButton.Yes): return

        thislist = ['']*data_length
        thislist[0] = 'New Project'

        global save_data
        save_data = deepcopy(thislist + save_data)
        self.refreshProjects()

        self.editProject(0)

    def delProject(self, index):
        global save_data
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Confirm Project DELETION")
        msgBox.setText("Are you sure you want to DELETE this project?\n"+save_data[index])
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msgBox.setDefaultButton(QMessageBox.StandardButton.No)
        result = msgBox.exec()

        if (result != QMessageBox.StandardButton.Yes): return
        for i in range(data_length):
            save_data.pop(index)
        self.refreshProjects()
        save_curr_data()
    
    def setFav(self, index):
        sav_indx = (index*data_length)+7

        if (save_data[sav_indx] == "T"):
            save_data[sav_indx] = ""
        else:
            save_data[sav_indx] = "T"

        self.refreshProjects()
        save_curr_data()




app = QApplication(sys.argv)
window = ProjectManager()
window.show()


def refresh():
    window.refreshProjects()

def swapPrev(indx):
    indx2 = indx-1
    if (indx2 < 0 or indx*data_length > len(save_data)):
        return
    item1 = indx*data_length
    item2 = (indx-1)*data_length
    for i in range(data_length):
        temp = save_data[item1+i]
        save_data[item1+i] = save_data[item2+i]
        save_data[item2+i] = temp
    
    # update details window
    if (window.editWindow is not None):
        subwindow_index = window.editWindow.index
        if (subwindow_index == item1):
            window.editWindow.index -= data_length
        if (subwindow_index == item2):
            window.editWindow.index += data_length

    # refresh main window
    refresh()
    

sys.exit(app.exec())