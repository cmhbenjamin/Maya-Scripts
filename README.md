This script fixes the broken texture paths in a Maya file

For example:
The 'apple_COL_file' in a downloaded scene uses a absolute path in the computer of creator:
"C:/Users/foo/Documents/maya/projects/fruit_bowl
//sourceimages/fruit_bowl_textures/apple/apple_COL.jpg"

We can use the script to reset the path to:
./sourceimages/fruit_bowl_textures/apple/apple_COL.jpg
by entering the folder "sourceimages" and prefix "./"