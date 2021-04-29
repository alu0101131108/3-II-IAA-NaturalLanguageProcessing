import csv
import re
import nltk

# Read each row from csv as a list.
with open('ecom-train.csv', newline='') as filehandle:
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
tokens = []


for row in data:
  # Use Regex to remove URLs 
  row[1] = re.sub(r'^(http|www)', '', row[1], flags=re.MULTILINE)

  # Lower case all words.
  row[1] = row[1].lower()

  # Filter non whitelisted characters.
  row[1] = ''.join(filter(whitelist.__contains__, row[1]))

  # Tokenization.
  rowTokens = nltk.word_tokenize(row[1])
  for token in rowTokens:
    tokens.append(token)

# Preserve only unique values.
token_set = set(tokens)

# Filter stop words
for stopword in stopwords:
  token_set.discard(stopword)

clean_tokens = list(token_set)
clean_tokens.sort()

with open('vocabulario.txt', 'w') as filehandle:
  filehandle.write('Numero de palabras: %s\n' % len(clean_tokens))
  for token in clean_tokens:
    filehandle.write('%s\n' % token)