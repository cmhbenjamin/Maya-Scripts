from qtshim import QtGui, QtCore, Signal
import sys


class pathFixController(QtCore.QObject):
    listRefreshed = Signal(list)
    fixApplied = Signal(int)
    addPath = Signal(str)


class pathFixWindow(QtGui.QMainWindow):
    refreshClicked = Signal()
    applyClicked = Signal(list, str, str)
    addPathClicked = Signal()


def create_window(controller, parent=None):
    window = pathFixWindow(parent)
    window.setWindowTitle('Texture Path Fix')
    # change this line
    statusbar = QtGui.QStatusBar()

    container = QtGui.QWidget(window)
    folderLabel = QtGui.QLabel("Parent folder:", container)
    prefixLabel = QtGui.QLabel('Prefix:', container)
    listwid = QtGui.QListWidget(container)
    refreshbutton = QtGui.QPushButton('Refresh', container)
    folderTextbox = QtGui.QLineEdit(container, 'sourceimages')
    prefixTextbox = QtGui.QLineEdit(container, '/.')
    pathbutton = QtGui.QPushButton('Use Maya file path')
    applybutton = QtGui.QPushButton('Apply', container)

    listwid.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

    def updateMessage():
        selections = len(listwid.selectedItems())
        pathCount = listwid.count()
        statusbar.showMessage(
            "broken file path(s): {}, selected file paths: {}"
            .format(pathCount, selections)
            )
    listwid.itemSelectionChanged.connect(updateMessage)

    def refreshonclick():
        window.refreshClicked.emit()
    refreshbutton.clicked.connect(refreshonclick)

    pathbutton.clicked.connect(window.addPathClicked)

    def applyonclick():
        # return the select items on the list
        #window.applyClicked.emit(["test"])
        selected_paths = listwid.selectedItems()
        new_paths = [p.data(QtCore.Qt.UserRole) for p in selected_paths]
        folder = folderTextbox.text()
        prefix = prefixTextbox.text()
        if len(new_paths) == 0 or folder == "":
            msgBox = QtGui.QMessageBox()
            msgBox.setText("please select path and input folder name")
            msgBox.exec_()
        else:
            window.applyClicked.emit(
                new_paths, folder, prefix)
    applybutton.clicked.connect(applyonclick)

    def updateList(path_list):
        # list the current file paths in the list
        pathCount = 0
        pathLength = 0
        width = 1
        for p in path_list:
            pathLength += len(p[0])
            pathCount += 1
        if pathCount:
            width = pathLength/pathCount
        listwid.clear()
        statusbar.showMessage("broken file path(s): {}".format(pathCount))
        for p in path_list:
            #dText = unicode("%5s:\t%s" % (p[0], p[1]))
            dText = '{0:{fill}}: \t{1}'.format(
                p[0], p[1], fill=width)
            item = QtGui.QListWidgetItem(view=listwid)
            item.setText(dText)
            item.setData(QtCore.Qt.UserRole, p)
            #listwid.addItem(item)
    controller.listRefreshed.connect(updateList)

    def addPath(path):
        prefixTextbox.setText(path)
    controller.addPath.connect(addPath)

    def updatestatus(num):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("updated %d path(s)" % (num))
        msgBox.exec_()
        window.refreshClicked.emit()

    controller.fixApplied.connect(updatestatus)

    layout = QtGui.QGridLayout(container)
    container.setLayout(layout)
    layout.addWidget(listwid, 0, 0, 2, 3)
    layout.addWidget(refreshbutton, 2, 0, 1, 3)

    layout.addWidget(folderLabel, 3, 0, 1, 1)
    layout.addWidget(folderTextbox, 3, 1, 1, 2)
    layout.addWidget(prefixLabel, 4, 0, 1, 1)
    layout.addWidget(prefixTextbox, 4, 1, 1, 1)
    layout.addWidget(pathbutton, 4, 2, 1, 1)

    layout.addWidget(applybutton, 5, 0, 1, 3)
    window.setCentralWidget(container)
    # add this line
    window.setStatusBar(statusbar)

    return window


def _pytest():
    #import random

    controller = pathFixController()

    def nextsel():
        return [
            ('apple_COL_file',
             """C:/Users/ben/Documents/maya/projects/LightingYourShot_workshop/
             /sourceimages/fruit_bowl_textures/apple/apple_COL.jpg"""),
            ('apple_BMP_file',
             """C:/Users/ben/Documents/maya/projects/LightingYourShot_workshop/
             /sourceimages/fruit_bowl_textures/apple/apple_BMP.jpg"""),
            ('apple_REFL_file',
             """C:/Users/ben/Documents/maya/projects/LightingYourShot_workshop/
             /sourceimages/fruit_bowl_textures/apple/apple_SPEC.jpg""")
        ]

    def onapply(paths):
        print 'apply clicked! path:', paths
        controller.fixApplied.emit(len(paths), "folder", "prefix")

    def onrefresh():
        print 'list refreshed'
        controller.listRefreshed.emit(nextsel())

    app = QtGui.QApplication([])
    win = create_window(controller)
    win.refreshClicked.connect(onrefresh)
    win.applyClicked.connect(onapply)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    _pytest()
