# -*- coding: utf-8 -*-
"""latin-to-bulgarian-and-reverse.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qzgjHzbKiBD3mt3DGrn89GhKZ0uBJoc2
"""

# Imports

import csv
from googletrans import Translator
from OriginFinder import OriginFinder

class Transliterator:

    def __init__(self, originFinder):
        # Initialisations

        # +1
        self.onephtongsLatin = {
            "a": "а",
            "b": "б",
            "c": "к",
            "d": "д",
            "e": "е",
            "f": "ф",
            "g": "г",
            "h": "х",
            "i": "и",
            "j": "й",
            "k": "к",
            "l": "л",
            "m": "м",
            "n": "н",
            "o": "о",
            "p": "п",
            "q": "к",
            "r": "р",
            "s": "с",
            "t": "т",
            "u": "у",
            "v": "в",
            "x": "кс",
            "y": "и",
            "w": "в",
            "z": "з",  # Greek origin, otherwise in Latin origin - ц
        }

        # +2
        self.diphtongsLatin = {
            "ae": "е",
            "au": "ау",
            "ce": "це",
            "ch": "х",
            "ci": "ци",
            "cy": "ци",
            "eu": "еу",
            "gu": "гу",
            "ll": "л",
            "oe": "е",
            "ph": "ф",  # Greek origin, otherwise in Latin origin - пх
            "rh": "р",  # Greek origin, otherwise in Latin origin - рх
            "su": "су",
            "qu": "кв",
            "th": "т",
        }

        # +3
        self.triphtongsLatin = {
            "cae": "цае",
            "coe": "цое",
            "sch": "сх",
            "sua": "сва",
            "sue": "све",
            "sui": "суи"
        }

        self.vowelsLatin = [ "a", "e", "o", "i", "u" ]
        self.vowelsBulgarian = [ "а", "е", "о", "и", "у" ]

        # Initialisations

        # +1
        self.onephtongsBulgarian = {
            "а": "a",
            "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",  # oe, ae също
            "з": "z",  # за гръцки думи ; s също може да е
            "и": "i",  # може и y
            "й": "j",
            "к": "c",  # k в чужди думи
            "л": "l",  # ll понякога
            "м": "m",
            "н": "n",
            "о": "o",
            "п": "p",
            "р": "r",  # rh в гръцки думи
            "с": "s",
            "т": "t",  # th също
            "у": "u",
            "ф": "f",  # ph в думи от гръцки произход
            "х": "ch",  # h
            "ц": "z",  # за гръцки думи
        }

        # +2
        self.diphtongsBulgarian = {
            "гу": "gu",
            "еу": "eu",
            "кв": "qu",
            "кс": "x",
            "сх": "sch",
            "су": "su",
            "ци": "ci",  # cy
            "це": "ce"
        }

        # +3
        self.triphtongsBulgarian = {
            "сва": "sua",
            "све": "sue",
            "суи": "sui",
            "цае": "cae",
            "цое": "coe"
        }

        self.originFinder = originFinder

    def indexes(self, i, j, len):
        if i >= 0 and j < len:
            return True
        else:
            return False

    def translateInEnglish(self, word):
        translator = Translator()
        wordEnglish = translator.translate(word, src = 'la', dest = 'en').text
        wordEnglish = wordEnglish.lower()
        return wordEnglish

    # Transliteration of Latin language terms to Bulgarian letters

    def latinToBulgarian(self, wordLatin):
        wordBulgarian = ""

        i = 0
        word0 = wordLatin
        word1 = wordBulgarian

        word0 = word0.lower()
        wordLatin = word0

        lenWord = len(word0)
        wordEnglish = "" # self.translateInEnglish(word0)
        origin = self.originFinder.extractOrigin(wordLatin, wordEnglish)

        while i < lenWord:
            # Triphtong rules, +3

            # ngu + Vowel = "нгв"
            if (self.indexes(i, i + 3, lenWord) and wordLatin[i:i + 3] == "ngu" and wordLatin[i + 3] in self.vowelsLatin):
                wordBulgarian += "нгв"
                i += 3
                continue

            # Diphtong rules, +2

            # ns + Vowel = "нз"
            if (self.indexes(i, i + 2, lenWord) and wordLatin[i:i + 2] == "ns" and wordLatin[i + 2] in self.vowelsLatin):
                wordBulgarian += "нз"
                i += 2
                continue

            # sm + Vowel = "зм"
            if (self.indexes(i, i + 2, lenWord) and wordLatin[i:i + 2] == "sm" and wordLatin[i + 2] in self.vowelsLatin):
                wordBulgarian += "зм"
                i += 2
                continue

            # rs + Vowel = "рз"
            if (self.indexes(i, i + 2, lenWord) and wordLatin[i:i + 2] == "rs" and wordLatin[i + 2] in self.vowelsLatin):
                wordBulgarian += "рз"
                i += 2
                continue

            # !(s|x|t) + "ti" + Vowel = "ци"
            if (self.indexes(i - 1, i + 2, lenWord) and (not (wordLatin[i-1:i] in ["s", "x", "t"]))
                    and wordLatin[i:i + 2] == "ti" and (wordLatin[i + 2] in self.vowelsLatin)):
                wordBulgarian += "ци"
                i += 2
                continue

            # Triphtongs, +3
            if (self.indexes(i, i + 2, lenWord) and wordLatin[i:i + 3] in self.triphtongsLatin.keys()):
                wordBulgarian += self.triphtongsLatin[wordLatin[i:i + 3]]
                i += 3
                continue

            # Diphtongs, +2
            context = wordLatin[i:i + 2]
            if (self.indexes(i, i + 1, lenWord) and context in self.diphtongsLatin.keys()):
                if context == "rh":
                    wordBulgarian += "р" if origin == "Greek" else "р" # it should have been "рx" if origin finding was correct
                    # print(i)
                    i += 2
                    continue
                if context == "ph":
                    wordBulgarian += "ф" if origin == "Greek" else "ф" # it should have been "пx" if origin finding was correct
                    # print(i)
                    i += 2
                    continue
                wordBulgarian += self.diphtongsLatin[context]
                i += 2
                continue

            # Onephtong rules, +1
            # "x" + Vowel = "кз"
            if (self.indexes(i, i + 1, lenWord) and wordLatin[i:i + 1] == "x" and (wordLatin[i + 1] in self.vowelsLatin)):
                wordBulgarian += "кз"
                i += 1
                continue

            # Vowel + s + Vowel -> "з"
            if (self.indexes(i - 1, i + 1, lenWord) and (wordLatin[i - 1] in self.vowelsLatin) and wordLatin[i] == 's' and (
                    wordLatin[i + 1] in self.vowelsLatin)):
                wordBulgarian += "з"
                i += 1
                continue

            # Onephtongs, +1
            context = wordLatin[i: i+1]
            if (context in self.onephtongsLatin.keys()):
                if context == "z":
                    wordBulgarian += "ц" if origin == "Latin" else "з"
                    i += 1
                    continue
                wordBulgarian += self.onephtongsLatin[context]
                i += 1
                continue

            # Other type of symbol
            wordBulgarian += word0[i]
            i += 1

        return wordBulgarian

    # Restoring Bulgarian transliterations of Latin terms back to Latin language
    def bulgarianToLatin(self, wordBulgarian):

        wordLatin = ""

        i = 0
        word0 = wordBulgarian
        word1 = wordLatin
        lenWord = len(word0)

        while i < lenWord:
            # Triphtong rules, +3
            # нгв + Vowel = "ngu"
            if (self.indexes(i, i + 3, lenWord) and word0[i:i+3] == "нгв" and (word0[i + 3] in self.vowelsBulgarian)):
                word1 += "ngu"
                i += 3
                continue

            # Diphtong rules, +2
            # нз + Vowel = "ns"
            if (self.indexes(i, i + 2, lenWord) and word0[i:i+2] == "нз" and (word0[i + 2] in self.vowelsBulgarian)):
                word1 += "ns"
                i += 2
                continue

            # зм + Vowel = "sm"
            if (self.indexes(i, i + 2, lenWord) and word0[i:i+2] == "зм" and (word0[i + 2] in self.vowelsBulgarian)):
                word1 += "sm"
                i += 2
                continue

            # рз + Vowel = "rs"
            if (self.indexes(i, i + 2, lenWord) and word0[i:i+2] == "рз" and (word0[i + 2] in self.vowelsBulgarian)):
                word1 += "rs"
                i += 2
                continue

            # !(s|x|t) + "ци" + Vowel = "ti"
            if (self.indexes(i - 1, i + 2, lenWord) and (not (word1[-1:] in ["s", "x", "t"]))
                    and word0[i:i+2] == "ци" and (word0[i+2] in self.vowelsBulgarian)):
                word1 += "ti"
                i += 2
                continue

            # "кз" + Vowel = "x"
            if (self.indexes(i, i + 2, lenWord) and word0[i:i+2] == "кз" and (word0[i+2] in self.vowelsBulgarian)):
                word1 += "x"
                i += 2
                continue

            # Triphtongs, +3
            if (self.indexes(i, i + 2, lenWord) and word0[i:i+3] in self.triphtongsBulgarian.keys()):
                word1 += self.triphtongsBulgarian[word0[i:i+3]]
                i += 3
                continue

            # Diphtongs, +2
            if (self.indexes(i, i + 1, lenWord) and word0[i:i+2] in self.diphtongsBulgarian.keys()):
                word1 += self.diphtongsBulgarian[word0[i:i+2]]
                i += 2
                continue

            # Onephtong rules, +1
            # Vowel + s + Vowel -> "з"
            if (self.indexes(i - 1, i + 1, lenWord) and (word0[i - 1] in self.vowelsBulgarian) and word0[i] == 'з'
                    and (word0[i + 1] in self.vowelsBulgarian)):
                word1 += "s"
                i += 1
                continue

            # Onephtongs, +1
            if (word0[i:i + 1] in self.onephtongsBulgarian.keys()):
                word1 += self.onephtongsBulgarian[ word0[i:i + 1] ]
                i += 1
                continue

            # Other type of symbol
            word1 += word0[i]
            i += 1

        wordLatin = word1
        return wordLatin

    def test(self, words_latin):
        words_bulgarian = []
        reverse_to_latin = []

        for wordInLatin in words_latin:
            transliteratedWord = self.latinToBulgarian(wordInLatin)
            # based on reverse rules
            wordInEnglish = "" # self.translateInEnglish(wordInLatin)
            wordOrigin = self.originFinder.extractOrigin(wordInLatin, wordInEnglish)
            reverseToBulgarian = self.bulgarianToLatin(transliteratedWord)

            words_bulgarian.append(transliteratedWord)
            reverse_to_latin.append(reverseToBulgarian)
            print('{0}, {1}, {2}, {3}, {4}'.
                  format(wordInLatin, wordInEnglish, wordOrigin, transliteratedWord,
                         reverseToBulgarian))

    def checkIfRomanNumeral(self, numeral):
        """ Controls that the numeral only contains valid Roman numerals. """
        numeral = numeral.upper()
        validRomanNumerals = [ "M", "D", "C", "L", "X", "V", "I" ]
        for letter in numeral:
            if letter not in validRomanNumerals:
                return False
        return True

    def exportFromCSV(self):
        cnt = 0
        with open('icd10_3sign_latin_clean.csv', 'r') as read_file:
            with open('icd10_3sign_latin_clean_2.csv', 'w', encoding="utf-8", newline='') as write_file:
                reader = csv.reader(read_file)
                writer = csv.writer(write_file)
                for row in reader:
                    cnt += 1
                    disease_name = row[1]
                    subwords = disease_name.split(' ')
                    # print(subwords)
                    transliterated_subwords = ""
                    for word in subwords:
                        if (self.checkIfRomanNumeral(word)):
                            transliterated_subwords += word
                            transliterated_subwords += " "
                            continue
                        transliterated_subwords += self.latinToBulgarian(word)
                        transliterated_subwords += " "
                    transliterated_subwords = transliterated_subwords[:-1]

                    # print([row[0], row[1], transliterated_subwords])
                    writer.writerow([row[0], row[1], transliterated_subwords])
                    '''
                    if (cnt == 20):
                        break
                    '''