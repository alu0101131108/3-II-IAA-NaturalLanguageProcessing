# Sebastián Daniel Tamayo Guzmán - alu0101131108
# Inteligencia Artifical Avanzada
# Proyecto PLN.
# Repo link: https://github.com/alu0101131108/IAA-language-model-ecommerce.git

import csv
import re
import math
import nltk
# nltk.download('punkt')

# Size found with code from part 01.
vocabularySize = 78604

# Read each row from csv as a list.
with open('./../ecom-train.csv', newline='') as filehandle:
  reader = csv.reader(filehandle)
  data = list(reader)

# Preprocessing.
whitelist = set('abcdefghijklmnopqrstuvwxyz ')
stopwords = ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at',
'be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever',
'every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if',
'in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my',
'neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say',
'says','she','should','since','so','some','than','that','the','their','them','then','there','these',
'they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while',
'who','whom','why','will','with','would','yet','you','your']

# Name data
outputs = ['aprendizajeH.txt', 'aprendizajeB.txt', 'aprendizajeC.txt', 'aprendizajeE.txt']
classes = ['Household', 'Books', 'Clothing & Accessories', 'Electronics']

# Corpus data storage.
corpus_datas = {}
for i in range(4):
  corpus_datas[classes[i]] = {
    'documents': 0,
    'words': 0,
    'frecuency': {}
  }

for row in data:
  # Lower case all words.
  row[1] = row[1].lower()

  # Filter non whitelisted characters.
  row[1] = ''.join(filter(whitelist.__contains__, row[1]))

  # Use Regex to remove URLs.
  row[1] = re.sub(r'(www|http)(.)*', '', row[1])

  # Tokenization.
  rowTokens = nltk.word_tokenize(row[1])

  # Corpus data filling.
  if (corpus_datas.get(row[0], 0) != 0):
    corpus = corpus_datas.get(row[0], 0)
    corpus['documents'] += 1
    corpus['words'] += len(rowTokens)
    frecuencies = corpus['frecuency']

    for token in rowTokens:
      if (token not in stopwords):
        if (frecuencies.get(token, 0) == 0):
          frecuencies[token] = 1
        else:
          frecuencies[token] += 1

# Output results
for i in range(4):
  with open(outputs[i], 'w') as filehandle:
    # Headers.
    corpus = corpus_datas[classes[i]]
    filehandle.write('Numero de documentos del corpus: %s\n' % corpus['documents'])
    filehandle.write('Numero de palabras del corpus: %s\n' % corpus['words'])
   
    # Word info.
    corpusVocabulary = list(corpus['frecuency'].keys())
    corpusVocabulary.sort()
    
    for token in corpusVocabulary:
      # Compute probabilty logarithm
      logProb = math.log((corpus['frecuency'][token] + 1) / (corpus['words'] + vocabularySize))
      filehandle.write('Palabra: %s ' % token)
      filehandle.write('Frec: %s ' % corpus['frecuency'][token])
      filehandle.write('LogProb: %s\n' % logProb)