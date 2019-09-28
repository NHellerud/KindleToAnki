import sqlite3
import sys
import argparse
import anki
from jisho import *
from timeleft import *
from bs4 import BeautifulSoup

def kindleExtractor(args):
	conn = sqlite3.connect(args.input) #connecting to sqlite server
	c = conn.cursor()

	

	if(args.a):
		c.execute("SELECT * FROM WORDS") 
	else:
		c.execute("SELECT * FROM WORDS WHERE category = 0")  

	words = c.fetchall()
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
			count += 1
			continue


		index = 1
		definition = ""
		for meanings in definitions:
			definition += str(index) + ". " + meanings.text + "<br>"
			index += 1
	
		anki.addNote(fullWord, noKanji, sentence, definition)
		count += 1


		timeLeft = getTimeLeft(time, stopwatch, count, numberOfElements)

		print("Progress: " + str(count) + "/" + str(numberOfElements) +  " " + timeLeft, end="\r")#printing the time remaining and the current progress

	if(not args.e):
		c.execute("UPDATE WORDS SET category = 100")#Setting all words to learned in the kindle database

	print("Summary")	
	print("Number of Words: " + str(count))
	print("Number of Words Skipped: " + str(numberOfElements - count))

	genanki.Package(anki.my_deck).write_to_file(args.output + '.apkg')

	conn.commit()
	conn.close()


def main():
	parser = argparse.ArgumentParser(description="Convert Kindle Database to Anki file.")
	parser.add_argument("-i", help="Location of the Kindles database file. Defaults to vocab.db otherwise.", dest="input", type=str, default="vocab.db")
	parser.add_argument("-o", help="Name of the .apkg file.", dest="output", type=str, default="Kindle_Vocab")
	parser.add_argument("-a", help="Tranfer everyword from Kindle including learned words.", action="store_true")
	parser.add_argument("-e", help="Does not edit the Kindle file to mark words as learned.", action="store_true")
	args = parser.parse_args()
	


	kindleExtractor(args)




if __name__=="__main__":
	main()