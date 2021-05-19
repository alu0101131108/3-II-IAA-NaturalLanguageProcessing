# Sebastián Daniel Tamayo Guzmán - alu0101131108
# Inteligencia Artifical Avanzada
# Proyecto PLN.
# Repo link: https://github.com/alu0101131108/IAA-language-model-ecommerce.git

import csv

# Load data from results file.
print('Loading data from resumen_alu0101131108.csv...')
with open('./resumen_alu0101131108.csv', 'r', encoding = 'utf-8-sig') as filehandle:
  reader = csv.reader(filehandle)
  result_data = list(reader)
  result_data.pop(0)  # Deletes first line which specifies the code.

# Load data from verification file.
print('Loading data from ecom-test-class.csv...')
with open('./ecom-test-classes.csv', 'r', encoding = 'utf-8-sig') as filehandle:
  reader = csv.reader(filehandle)
  verification_data = list(reader)

# Calculate error.
print('Error is being calculated...')
total = len(result_data)
wrong = 0
if total != len (verification_data):
  print('ERROR - Result and verification have diferent number of lines.')
else:
  for index in range(total):
    if result_data[index][0] != verification_data[index][0][0]:
      wrong += 1
  error = wrong / total
  print('Error: ', round(error * 100, 2), '%')