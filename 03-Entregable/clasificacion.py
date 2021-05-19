# Sebastián Daniel Tamayo Guzmán - alu0101131108
# Inteligencia Artifical Avanzada
# Proyecto PLN.
# Repo link: https://github.com/alu0101131108/IAA-language-model-ecommerce.git

import csv
import re
import math
import nltk

classes = ['Household', 'Books', 'Clothing & Accessories', 'Electronics']
learningFiles = ['aprendizajeH.txt','aprendizajeB.txt','aprendizajeC.txt','aprendizajeE.txt']
whitelist = set('abcdefghijklmnopqrstuvwxyz ')
stopwords = ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at',
'be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever',
'every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if',
'in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my',
'neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say',
'says','she','should','since','so','some','than','that','the','their','them','then','there','these',
'they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while',
'who','whom','why','will','with','would','yet','you','your']

# Load data from corpus test input.
print('Loading data from ecom-train.csv...')
with open('./corpus_test.csv', newline='') as filehandle:
  reader = csv.reader(filehandle)
  data = list(reader)


# Corpus data storage.
corpus_datas = {}
for i in range(4):
  corpus_datas[classes[i]] = {
    'documentsN': 0,
    'wordsN': 0,
    'words': {}
  }

# Load corpus data from learning files.
print('Loading data from learning files...')
for i in range(4):
  with open('./../02-Entregable/' + learningFiles[i], 'r', encoding='utf8', errors='ignore') as filehandle:
    corpus = corpus_datas[classes[i]] 
    corpus['documentsN'] = int((filehandle.readline()).split()[-1])
    corpus['wordsN'] = int(filehandle.readline().split()[-1])
    words = corpus['words']

    while True:
      line = filehandle.readline().split()

      if not line or len(line) < 6:
        break

      words[line[1]] = {
        'frecuency': line[3],
        'lprob': float(line[5]),
      }


# Description probability storage.
total_descriptions = 0
for category in classes:
  total_descriptions += corpus_datas[category]['documentsN']

class_lprob = {}
for category in classes:
  class_lprob[category] = corpus_datas[category]['documentsN'] / total_descriptions


# Preprocess descriptions and compute their probabilities.
print('Computating description probabilities...')
descriptions = []
for row in data:
  description = row[0]

  # Lower case all words.
  description = description.lower()

  # Filter non whitelisted characters.
  description = ''.join(filter(whitelist.__contains__, description))

  # Use Regex to remove URLs.
  description = re.sub(r'(www|http)(.)*', '', description)

  # Tokenization.
  descriptionTokens = nltk.word_tokenize(description)

  # Also filter stopwords.
  stopwordsSet = set(stopwords)
  descriptionTokens = [item for item in descriptionTokens if item not in stopwordsSet]

  # Description probability computation.
  container = {
    'description': description,
    'lprobs': {}
  }
  for category in classes:
    description_lprob = 0
    for token in descriptionTokens:
      corpus_words = corpus_datas[category]['words']
      word = corpus_words.get(token, None)
      if word is not None:
        description_lprob += word['lprob'] 
      else:
        description_lprob += corpus_words['<UNK>']['lprob']

    description_lprob += class_lprob[category]
    container['lprobs'][category] = round(description_lprob, 2)

  best_lprob = max([
    container['lprobs']['Household'], 
    container['lprobs']['Books'], 
    container['lprobs']['Clothing & Accessories'], 
    container['lprobs']['Electronics']
  ])

  if best_lprob == container['lprobs']['Household']:
    container['prediction'] = 'H'
  elif best_lprob == container['lprobs']['Books']:
    container['prediction'] = 'B'
  elif best_lprob == container['lprobs']['Clothing & Accessories']:
    container['prediction'] = 'C'
  elif best_lprob == container['lprobs']['Electronics']:
    container['prediction'] = 'E'
  else:
    print('WARNING - Prediction could not be found')

  descriptions.append(container)

# output results
print('Writing results in output files...')

with open('clasificacion_alu0101131108.csv', 'w') as filehandle:
  for description in descriptions:
    textline = description['description'] + ','
    for category in classes:
      textline += str(description['lprobs'][category]) + ','
    textline += description['prediction'] + '.'
    filehandle.write('%s\n' % textline)

with open('resumen_alu0101131108.csv', 'w') as filehandle:
  user_code = input('Enter the code for resumen_alu0101131108.csv: ')
  textline = 'codigo: ' + str(user_code)
  filehandle.write('%s\n' % textline)
  for description in descriptions:
    textline = description['prediction']
    filehandle.write('%s\n' % textline)