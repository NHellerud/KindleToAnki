import genanki

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


def addNote(fullWord, noKanji, sentence, definition):

	my_note = genanki.Note(
		model = my_model,
		fields=[fullWord, noKanji, sentence, definition])

	my_deck.add_note(my_note)


