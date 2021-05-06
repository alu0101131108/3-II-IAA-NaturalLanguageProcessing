# Sebastián Daniel Tamayo Guzmán - alu0101131108
# Inteligencia Artifical Avanzada
# Proyecto PLN.
# Repo link: https://github.com/alu0101131108/IAA-language-model-ecommerce.git

import csv
import re
import nltk
# nltk.download('punkt')

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
tokens = set()


for row in data:

  # Lower case all words.
  row[1] = row[1].lower()

  # Filter non whitelisted characters.
  row[1] = ''.join(filter(whitelist.__contains__, row[1]))

  # Use Regex to remove URLs 
  row[1] = re.sub(r'(www|http)(.)*', '', row[1])

  # Tokenization.
  rowTokens = nltk.word_tokenize(row[1])
  for token in rowTokens:
    # Also filter stopwords
    if (token not in stopwords):
      tokens.add(token)

# Sort tokens.
clean_tokens = list(tokens)
clean_tokens.sort()

# Output results to file.
with open('vocabulario.txt', 'w') as filehandle:
  filehandle.write('Numero de palabras: %s\n' % len(clean_tokens))
  for token in clean_tokens:
    filehandle.write('%s\n' % token)