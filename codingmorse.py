"""
import requests
from string import ascii_lowercase
from bs4 import BeautifulSoup

# Souping through wiki to get information of translating from english to morse and back

header = {
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
}

wiki_link = requests.get('https://en.wikipedia.org/wiki/Morse_code', headers=header).text
soup = BeautifulSoup(wiki_link, 'html.parser')


# Getting english letters and symbols to the list

x = soup.select('tbody tr td b a')
symbols_not_ready = [i.text for i in x[26:-1]]


# Getting morse-english code to the list

z = soup.select('tbody tr td div div a')
symbols_morse_not_ready = [i.text for i in z[2:]]


#Moddifying english letters and symbols list

english_symbols = []
for i in symbols_not_ready:
    if i == 'Period [.]':
        i = '.'
    elif i == 'Comma [,]':
        i = ','
    elif i == 'Question Mark [?]':
        i = '?'
    elif i == "Apostrophe [']":
        i = "'"
    elif i == 'Exclamation Point [!]':
        i = '!'
    elif i == 'Slash':
        i = '/'
    elif i == 'Parenthesis (Open)':
        i = '('
    elif i == ' Ampersand (or "Wait") [&]':
        i = '&'
    elif i == ' Colon [:] ':
        i = ':'
    elif i == ' Semicolon [;] ':
        i = ':'
    elif i == ' Double Dash [=] ':
        i = '='
    elif i == ' Plus sign [+] ':
        i = '+'
    elif i == 'Hyphen':
        i = '-'
    elif i == 'Underscore [_]':
        i = '_'
    elif i == 'Quotation mark ["] ':
        i = '"'
    elif i == 'Dollar sign [$] ':
        i = '$'
    elif i == 'At Sign [@] ':
        i = '@'
    elif i == ' Minus Sign [-] ':
        continue
    elif i == 'Parenthesis (Close)':
        i = ')'
    elif i == 'Fraction Bar [/]':
        continue
    english_symbols.append(i)

letters = [i for i in ascii_lowercase]
for letter in letters[::-1]:
    number = 0
    if number < 27:
        english_symbols.insert(number, letter)
        number += 1


# Modifying morse code

morse_code_with_spaces = [i for i in symbols_morse_not_ready[:54]]
morse_code_with_spaces += symbols_morse_not_ready[61:]
morse_code_without_spaces = [i.replace(' ', '') for i in morse_code_with_spaces]
morse_code_without_spaces2 = [i.replace(' ', '') for i in morse_code_without_spaces]
morse_code = [i.replace('·', '.') for i in morse_code_without_spaces2]
morse_clear = [i.replace('−', '-') for i in morse_code]
with open('english_letters.txt', mode='w', encoding='utf-8') as eng_words:
    for i in english_symbols:
        eng_words.write(f'{i}|')
with open('morse_symbols.txt', mode='w', encoding='utf-8') as morse_symbols:
    for i in morse_clear:
        morse_symbols.write(f'{i}|')
"""

# GETTING SYMBOLS FROM FILE

with open('english_letters.txt', mode='r', encoding='utf-8') as english:
    en_symbols = []
    for symb in english.read().split('|'):
        en_symbols.append(symb)
with open('morse_symbols.txt', mode='r', encoding='utf-8') as morse_code:
    morse_symb = []
    for symb in morse_code.read().split('|'):
        morse_symb.append(symb)


# Creating class to translate our text

class Translate:
    def __init__(self, text: str, symbols=en_symbols, morse=morse_symb):
        self.text = text.lower()
        self.symbols = symbols
        self.morse = morse
        self.translate_english = False
        self.check_translate()
        self.translate = None

# Checking if typed sentence consists of english and symbols or morse code

    def check_translate(self):
        splitted_text = [i for i in self.text]
        for i in splitted_text:
            if i in self.symbols[:36] or i in self.symbols[37:41] or i in self.symbols[42:49] or i in self.symbols[50:]:
                self.translate_english = True
                break
            else:
                continue
        if self.translate_english:
            self.translate_to_morse()
        else:
            self.translate_to_english()

    def translate_to_morse(self):
        morse_list = []
        try:
            for word in self.text:
                if word in self.symbols:
                    morse_symbol = self.morse[self.symbols.index(word)]
                    morse_list.append(f'{morse_symbol} ')
                elif word == ' ':
                    morse_list.append('/ ')
                else:
                    print(f'{word} not in morse code')
            self.translate = ''.join(morse_list)
            print(f'Translated text: {self.translate}')
        except ValueError:
            print('You used not english words')

    def translate_to_english(self):
        english_list = []
        splitted_text = self.text.split()
        try:
            for morse in splitted_text:
                if morse == '/':
                    english_list.append(' ')
                else:
                    english_word = self.symbols[self.morse.index(morse)]
                    english_list.append(f'{english_word}')
            self.translate = ''.join(english_list)
            print(f'Translated text: {self.translate.upper()}')
        except ValueError:
            print('You typed not morse code')
