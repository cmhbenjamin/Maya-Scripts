import pymel.core as pmc
import os
""" Remove the front part of file texture path in a downloaded model"""


def _find(list, s):
    # case in-sensitive compare two strings
    def comparator(str1, str2):
        return str(str1).lower() == str(str2).lower()
    for i, p in enumerate(list):
        if(comparator(p, s)):
            return i
    return -1


def listPaths():
    # return a list path with broken texture path
    files = pmc.ls(type='file')
    brokenPaths = []
    for f in files:
        path_str = pmc.getAttr("%s.fileTextureName" % f)
        if not os.path.isfile(path_str):
            brokenPaths.append((str(f), path_str))
    return brokenPaths


def fixPaths(brokenPaths, folder, prefix):
    # fix the file texture paths
    # convert absolute paths into relative paths
    # brokenPaths in a list of (#filename, #filepath)
    count = 0
    for bp in brokenPaths:
        path = bp[1].split(os.sep)
        ind = _find(path, folder)
        # if (ind == -1):
        #     print("word not found")
        #     sys.exit()
        if ind != -1:
            newPath = os.path.join(*path[ind:])
            newPath = os.path.join(prefix, newPath)
            pmc.setAttr("%s.fileTextureName" % bp[0], newPath, type="string")
            count += 1


def getSceneDir():
    return os.path.dirname(pmc.sceneName())


if __name__ == '__main__':
    fixPaths(listPaths(), "fruit_bowl_textures", getSceneDir())
