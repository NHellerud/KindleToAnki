import sqlite3
import datetime
import requests
import sys
import time
import genanki
from bs4 import BeautifulSoup



def getDictionaryWebpage(word):
	###Gets the html for the webpage of the given word###

	source = requests.get("https://jisho.org/search/" + word).text #searching for the definitions

	soup = BeautifulSoup(source, "lxml")

	return soup



def getWordSearched(soup):
	"""Gets the word for the dictionary sort result. This is important because the word given to the getDictionaryWebpage might
	not always be the same as the result"""
	
	word = soup.find("div", class_="concept_light-representation")
	word = word.find("span", class_="text").text
	
	
	return word.strip()



def getFurigana(soup):
	"""Gets the furigana of the word searched. In japanese there are multiple alphabets. Kanji(Chinese characters) and the two phonic alphabets hiragana and katakana.
	 In order to know how to read the words the kanji have to be translated into furigana,"""
	
	furigana = soup.find("span", class_='furigana')
	furigana = furigana.findAll("span") 


	return furigana



def getNoKanjiWord(soup):
	"""Gets the word that was searched with the kanji replaced with kana(shows how to pronounce the word)"""


	furigana = getFurigana(soup)
	kana = getWordSearched(soup)

	word = ""
	for symbol in furigana:

		if(symbol.text == ''):
			word += kana[0]
			
		else:
			word += symbol.text
		kana = kana[1:len(kana)]	


	word += str(kana)
	return word





def getDictionaryDefinition(soup):
	###Gets the dictionary definition for the current webpage###

	definitionText = soup.find("div", class_ = "concept_light-meanings medium-9 columns")
	definitionText = definitionText.find_all("span", class_ = "meaning-meaning")
	return definitionText





def getTimeLeft(time, stopwatch, count, numberOfElements):
	currentTime = time.time() - stopwatch
	estimatedTime = round(currentTime * (numberOfElements - count) / count)
	estimatedHours = int(estimatedTime / 3600)
	estimatedMinutes = int((estimatedTime - (estimatedHours * 3600)) / 60)
	estimatedSeconds = estimatedTime - (estimatedHours * 3600) - (estimatedMinutes * 60)
	estimatedTime = str(estimatedTime)
	if(estimatedHours < 10):
		estimatedHours = "0" + str(estimatedHours)
	else:
		estimatedHours = str(estimatedHours)

	if(estimatedMinutes < 10):
		estimatedMinutes = "0" + str(estimatedMinutes)
	else:
		estimatedMinutes = str(estimatedMinutes)

	if(estimatedSeconds < 10):
		estimatedSeconds = "0" + str(estimatedSeconds)
	else:
		estimatedSeconds = str(estimatedSeconds)
	return "Estimated Time Left : " + estimatedHours + ":" + estimatedMinutes + ":" + estimatedSeconds










conn = sqlite3.connect('vocab.db') #connecting to sqlite server
c = conn.cursor()




ts = str(datetime.datetime.now()) #get the time to label the created file
date = ts[0:10]


my_deck = genanki.Deck(
	1807823766,
	'Kindle_Vocab')

my_model = genanki.Model(
	1083202559,
	'Recognize',
	fields=[
		{'name': 'Word'},
		{'name': 'Kana'},
		{'name': 'Sentence'},
		{'name': 'Definition'}
	],
	templates=[
		{
			'name': 'Card 1',
			'qfmt': '{{Word}}',
			'afmt': '{{FrontSide}}<hr id="answer">{{Kana}}<br>{{Sentence}}<br>{{Definition}}',
		},
		{
			'name': 'Card 1',
			'qfmt': '{{Definition}}',
			'afmt': '{{FrontSide}}<hr id="answer">{{Word}} - {{Kana}}<br>{{Sentence}}',
		},
	])


#f = open("Kindle_Vocab" + date + ".txt", "w+", encoding="utf-8") #opens the kindle database using default name in same directory
c.execute("UPDATE WORDS SET category = 0") #Testing Only

c.execute("SELECT * FROM WORDS WHERE category = 0")  #select all words under learning

words = c.fetchall() #preparing the words
numberOfElements = len(words)
count = 0

stopwatch = time.time() #starting timer

for word in words:
	c.execute("SELECT * FROM LOOKUPS WHERE (word_key = ? )", (word[0],)) #grabing the sentence that the word comes from
	lookup = c.fetchone()


	#Getting all of the information to be writen to the file
	try:
		soup = getDictionaryWebpage(str(word[0]))
		fullWord = getWordSearched(soup)
		noKanji = getNoKanjiWord(soup)
		definitions = getDictionaryDefinition(soup)	
		sentence = lookup[5]
	except:
		continue


	index = 1
	definition = ""
	for meanings in definitions:
		definition += str(index) + ". " + meanings.text + "<br>"
		index += 1


	
	my_note = genanki.Note(
		model = my_model,
		fields=[fullWord, noKanji, sentence, definition])

	my_deck.add_note(my_note)
	count += 1


	timeLeft = getTimeLeft(time, stopwatch, count, numberOfElements)

	print("Progress: " + str(count) + "/" + str(numberOfElements) +  " " + timeLeft, end="\r")#printing the time remaining and the current progress

	


c.execute("UPDATE WORDS SET category = 100")#Setting all words to learned in the kindle database

print("Summary")	
print("Number of Words: " + str(count))
print("Number of Words Skipped: " + str(numberOfElements - count))

genanki.Package(my_deck).write_to_file("Kindle_Vocab" + date + '.apkg')

conn.commit()
conn.close()