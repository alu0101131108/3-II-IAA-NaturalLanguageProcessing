# Sebastián Daniel Tamayo Guzmán - alu0101131108
# Inteligencia Artifical Avanzada
# Proyecto PLN.
# Repo link: https://github.com/alu0101131108/IAA-language-model-ecommerce.git

import csv

# Load data from ecom-train.
print('Loading data from ecom-train.csv...')
with open('./../ecom-train.csv', 'r', encoding = 'utf-8-sig') as filehandle:
  reader = csv.reader(filehandle)
  data = list(reader)

print('Generating test file...')
with open('ecom-test-descriptions.csv', 'w') as filehandle:
  for index, row in enumerate(data):
    textline = str(index) + ';' + row[1]
    filehandle.write('%s\n' % textline)

print('Generating verification file...')
with open('ecom-test-classes.csv', 'w') as filehandle:
  for row in data:
    filehandle.write('%s\n' % row[0])
