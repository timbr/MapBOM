import yaml

namedata={}
matdata={}

Ire_prefix = "  **IRE**"

yamlfile = "\\\\Sheffield\\SPD_Data\\Temporary\\TimBrowning\\IrelandBOMs\\IrelandBOM.yaml"
try:
    yamldata = open(yamlfile, 'r').read()
except:
    from IrelandBOM import yamldata

for assy in yaml.load_all(yamldata):
    if assy['Assembly'] not in namedata:
        namedata[assy['Assembly']] = assy['Description'] + Ire_prefix
    for part in assy['Items']:
        print assy['Assembly'], assy['Description'], part['Part Number'], part['Description'], part['Qty']
        if part['Part Number'] not in namedata:
            namedata[part['Part Number']] = part['Description']
        if assy['Assembly'] not in matdata:
            matdata[assy['Assembly']] = [[part['Part Number'], part['Qty']]]
        else:
            matdata[assy['Assembly']].append([part['Part Number'], part['Qty']])
