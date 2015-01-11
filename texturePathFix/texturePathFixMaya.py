"""
export PYTHONPATH=$PYTHONPATH:"/Volumes/Macintosh\ HD/workspace4/mayaScript/texturePathFix"
"""

import os, sys

import maya.OpenMaya as OpenMaya
import pymel.core as pmc
import texturePathFixGui as tpfgui
import mayautils
import texturePathFix

_window = None


def show():
    global _window
    if _window is None:
        cont = tpfgui.pathFixController()
        parent = mayautils.get_maya_window()
        _window = tpfgui.create_window(cont, parent)

        def onrefresh():
            cont.listRefreshed.emit(texturePathFix.listPaths())
        _window.refreshClicked.connect(onrefresh)

        def onapply(paths, folder, prefix):
            print 'apply clicked! path:', paths
            texturePathFix.fixPaths(paths, folder, prefix)
            cont.fixApplied.emit(len(paths))
        _window.applyClicked.connect(onapply)

        def addPath():
            cont.addPath.emit(texturePathFix.getSceneDir())

        _window.addPathClicked.connect(addPath)

    _window.show()

if __name__ == "__main__":
    show()
