# KindleToAnki
This python scipt is used to convert Kindle's vocab builder into an Anki deck.
It does this by reading in the Kindle's vocab builder database,
 Combining it with definitions from Jisho.com and then creating an anki deck 
from the results. This program uses beautifulsoup to read in and parse the html
 and genanki to create the apkg file(Anki's format).

There are two cards created or each word.
The format is as follows.

<h2>Card 1</h2>
<h4>Front</h4>
Word
  
<h4>Back</h4>
Word<br>
------------<br>
Kana          --This is how to pronounce each word<br>
Sentence      --Taken in context from the Kindle's database<br>
Definitions   --All definitions from Jisho.com<br>
  
<h2>Card 2</h2>
<h4>Front</h4>
Definition
  
<h4>Back</h4>
Definition<br>
------------<br>
Word - Kana<br>
Sentence<br>
