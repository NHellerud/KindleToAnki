import requests
import sys
from bs4 import BeautifulSoup


def getDictionaryWebpage(word):
	###Gets the html for the webpage of the given word
	###

	source = requests.get("https://jisho.org/search/" + word).text #searching for the definitions

	soup = BeautifulSoup(source, "lxml")

	return soup



def getWordSearched(soup):
	"""Gets the word for the dictionary sort result. This is important because the word given to the getDictionaryWebpage might
	not always be the same as the result
	"""
	
	word = soup.find("div", class_="concept_light-representation")
	word = word.find("span", class_="text").text
	
	
	return word.strip()



def getFurigana(soup):
	"""Gets the furigana of the word searched. 


	In japanese there are multiple alphabets. Kanji(Chinese characters) and the two phonic
	alphabets hiragana and katakana. In order to know how to read the words the 
	kanji have to be translated into furigana,
	 """
	
	furigana = soup.find("span", class_='furigana')
	furigana = furigana.findAll("span") 


	return furigana



def getNoKanjiWord(soup):
	"""Gets the word that was searched with the kanji replaced with kana(shows how to pronounce the word)
	"""
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
	###Gets the dictionary definition for the current webpage
	###

	definitionText = soup.find("div", class_ = "concept_light-meanings medium-9 columns")
	definitionText = definitionText.find_all("span", class_ = "meaning-meaning")
	return definitionText










