import glob

filepaths = glob.glob('\\\\Sheffield\\SPD_Data\\Temporary\\TimBrowning\\Drawings\\*.pdf')

for filepath in filepaths:
    filename = filepath.split('\\')[-1:]
    item = filename[1:14]
    print item, filename