import os
import pandas as pd
from lxml import etree

tax_tuple = (
    '7413', '7430', '7424', '7455', '7456', '7457', '7458', '7459', '7460', '7415', '7454', '7404', '7447', '7448',
    '7449',
    '7451', '7452', '7453')

# Folder with xml
folder_path = '/folder/path'

# File csv
csv_file = 'file.csv'

data = []

for filename in os.listdir(folder_path):
    if filename.endswith('.xml'):
        xml_file = os.path.join(folder_path, filename)
        tree = etree.parse(xml_file)
        root = tree.getroot()

        row_data = {}

        # Go through the elements of the XML file
        for element in root.iter():

            if row_data.get('КодРегион'):
                row_data = {}

            # Extract data from element attributes
            for key, value in element.items():
                row_data[key] = value

            # Extract data from item text
            if element.text:
                row_data[element.tag] = element.text

            # Add to dict if 'КодРегион' is "74"
            if row_data.get('КодРегион') == '74':
                if 'ИННФЛ' in row_data:
                    data.append(row_data['ИННФЛ'])
                elif 'ИННЮЛ' in row_data:
                    data.append(row_data['ИННЮЛ'])

# Make dataframe
df = pd.DataFrame(data)

df.to_csv(csv_file, index=False)
