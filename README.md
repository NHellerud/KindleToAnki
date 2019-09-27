# KindleToAnki
This python scipt is used to convert Kindle's vocab builder into an Anki deck. It does this by reading in the Kindle's vocab builder database, Combining it with definitions from Jisho.com and then creating an anki deck from the results. This program uses beautifulsoup to read in and parse the html and genanki to create the apkg file(Anki's format).

There are two cards created or each word.
The format is as follows.

Card 1 Front:
Word
  
Card 1 Back:
Word
------------
Kana          --This is how to pronounce each word
Sentence      --Taken in context from the Kindle's database
Definitions   --All definitions from Jisho.com
  
  
Card 2 front:
Definition
  
Card 2 Back:
Definition
------------
Word - Kana
Sentence

