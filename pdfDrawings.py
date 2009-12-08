import glob
import string

filepaths = glob.glob('\\\\Sheffield\\SPD_Data\\Temporary\\TimBrowning\\Drawings\\*.pdf')

drawingsdb = {}

for filepath in filepaths:
    filename = filepath.split('\\')[-1:][0]
    item = filename[1:15]
    filename = filename.replace('[', '%5B').replace(']', '%5D').replace(' ', '%20').replace('&', '&amp;')
    drawingsdb[item] = filename
    
