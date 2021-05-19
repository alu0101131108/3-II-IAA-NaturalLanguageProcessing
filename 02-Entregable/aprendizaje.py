# Sebastián Daniel Tamayo Guzmán - alu0101131108
# Inteligencia Artifical Avanzada
# Proyecto PLN.
# Repo link: https://github.com/alu0101131108/IAA-language-model-ecommerce.git

import csv
import re
import math
import nltk
# nltk.download('punkt')

# Read each row from csv as a list.
print('Loading data from ecom-train.csv...')
with open('./../ecom-train.csv', newline='') as filehandle:
  reader = csv.reader(filehandle)
  data = list(reader)

# Preprocessing.
print('Data structures setting...')
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
# corpus_outputs = ['corpusH.txt', 'corpusB.txt', 'corpusC.txt', 'corpusE.txt']
learn_outputs = ['aprendizajeH.txt', 'aprendizajeB.txt', 'aprendizajeC.txt', 'aprendizajeE.txt']
classes = ['Household', 'Books', 'Clothing & Accessories', 'Electronics']

# Vocabulary set.
vocabulary = set()

# Corpus data storage.
corpus_datas = {}
for i in range(4):
  corpus_datas[classes[i]] = {
    'documents': 0,
    'words': 0,
    'frecuency': {}
  }

# Preprocess and create corpus data structures.
print('Preprocessing data and computing vocabulary and class corpuses...')
for row in data:
  # Lower case all words.
  row[1] = row[1].lower()

  # Filter non whitelisted characters.
  row[1] = ''.join(filter(whitelist.__contains__, row[1]))

  # Use Regex to remove URLs.
  row[1] = re.sub(r'(www|http)(.)*', '', row[1])

  # Tokenization.
  rowTokens = nltk.word_tokenize(row[1])

  # Also filter stopwords.
  stopwordsSet = set(stopwords)
  cleanRowTokens = [item for item in rowTokens if item not in stopwordsSet]

  # Vocabulary filling.
  vocabulary.update(cleanRowTokens)

  # Corpus data filling.
  if (corpus_datas.get(row[0], 0) != 0):  # Ensures the class is known.
    corpus = corpus_datas.get(row[0], 0)
    corpus['documents'] += 1
    corpus['words'] += len(cleanRowTokens)
    frecuencies = corpus['frecuency']
    for token in cleanRowTokens:
      if (frecuencies.get(token, 0) == 0):
        frecuencies[token] = 1
      else:
        frecuencies[token] += 1


# Setting unknown word addition.
print('Setting <UNK> word tag...')
kUNK = 0
vocabulary.add('<UNK>')
unkownWords = set()
for category in classes:
  corpus = corpus_datas.get(category)
  frecuencies = corpus['frecuency']
  frecuencies['<UNK>'] = 0
  for word in frecuencies:
    if (frecuencies[word] <= kUNK and word != '<UNK>'):
      frecuencies['<UNK>'] += frecuencies[word]
      unkownWords.add(word)
  for word in unkownWords:
    frecuencies.pop(word, 0)   

# Vocabulary size.
vocabularySize = len(vocabulary)
  
# Create learn result files.
for i in range(4):
  print('Creating learning file for class ' + str(classes[i]) + '...')
  with open(learn_outputs[i], 'w') as filehandle:
    # Headers.
    corpus = corpus_datas[classes[i]]
    filehandle.write('Numero de documentos del corpus: %s\n' % corpus['documents'])
    filehandle.write('Numero de palabras del corpus: %s\n' % corpus['words'])
   
    # Word info.
    corpusVocabulary = list(corpus['frecuency'].keys())
    corpusVocabulary.sort()
    for token in corpusVocabulary:
      # Compute probabilty logarithm with Laplace softener and considering kUNK value. 
      if (kUNK == 0):
        if (token == '<UNK>'):
          logProb = math.log(1 / (corpus['words'] + vocabularySize + 1))
        else:
          logProb = math.log((corpus['frecuency'][token] + 1) / (corpus['words'] + vocabularySize + 1))
      else:
        logProb = math.log((corpus['frecuency'][token] + 1) / (corpus['words'] + vocabularySize))

      # Write data for current token.
      filehandle.write('Palabra: %s ' % token)
      filehandle.write('Frec: %s ' % corpus['frecuency'][token])
      filehandle.write('LogProb: %s\n' % logProb)