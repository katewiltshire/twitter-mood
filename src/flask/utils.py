import re
import string


'''
Strips links from string
'''
def strip_links_from_text(text):
  link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
  links         = re.findall(link_regex, text)
  for link in links:
      text = text.replace(link[0], ', ')    
  return text

'''
Strips links, @ and # from text
'''
def strip_all_entities(text):
  text = strip_links_from_text(text)

  entity_prefixes = ['@','#']
  for separator in  string.punctuation:
      if separator not in entity_prefixes :
          text = text.replace(separator,' ')
  words = []
  for word in text.split():
      word = word.strip()
      if word:
          if word[0] not in entity_prefixes:
              words.append(word)

  return ' '.join(words)
