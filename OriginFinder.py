import pandas as pd
import googletrans as gt
import numpy as np

class OriginFinder:

    def __init__(self):
        self.typeMorphems = {"prefix": [], "root": [], "suffix": []}

        # pd.set_option("display.max_column", None)
        data = pd.read_excel('greek_and_latin_roots.xlsx', index_col = 0)
        newIndex = -1

        originMorphems = {"Latin": {
            "prefix": [],
            "root": [],
            "suffix": []
        },
            "Greek": {
                "prefix": [],
                "root": [],
                "suffix": []
            }
        }

        allMorphems = []

        for index, row in data.iterrows():
            values = list(row.values)
            prefixes = index
            if ("Origin language" in values):
                rootColumn = values.index("Root") if "Root" in values else None
                newIndex = values.index("Origin language")
            elif (newIndex > -1):
                if (pd.isnull(prefixes) and (not pd.isnull(rootColumn))):
                    prefixes = values[rootColumn]
                origin = values[newIndex]
                if (not (pd.isnull(prefixes) or pd.isnull(origin))):
                    prefixes = prefixes.split(",")
                    prefixes = list(map(lambda x: x.strip("\n "), prefixes))
                    if (origin == "Latin" or origin == "Greek"):
                        # print("{0}, {1}".format(prefixes, origin))
                        for word in prefixes:
                            type = self.prefixOrRoot(word)
                            if (type != "out"):
                                wordStripped = word.strip("-")
                                originMorphems[origin][type].append(wordStripped)
                                self.typeMorphems[type].append((wordStripped, origin))
                                allMorphems.append((wordStripped, type, origin))

            for type in self.typeMorphems:
                self.typeMorphems[type].sort(key=lambda x: (-len(x[0]), x[0]))
            # allMorphems.sort( key = lambda x: ( -len(x[0]), x[0]) )

            '''
            for origin in originMorphems:
                for morphem in originMorphems[origin]:
                    originMorphems[origin][morphem].sort(key = lambda x: (- len(x), x))

            print(row.values)
            cnt += 1
            print("New line")
            if (cnt == 10):
               break
            '''

    def prefixOrRoot(self, word):
        if word.startswith("-") and word.endswith("-"):
            return "root"
        if word.endswith("-"):
            return "prefix"
        if word.startswith("-"):
            return "suffix"
        return "out"

    def extractOrigin(self, wordLatin, wordEnglish):
        counts = {
            "prefix": { "Latin": 0, "Greek": 0 },
            "root": { "Latin": 0, "Greek": 0 },
            "suffix": { "Latin": 0, "Greek": 0 }
        }

        # prefix
        prefixesByOrigin = self.typeMorphems["prefix"]
        for pref in prefixesByOrigin:
            if (wordLatin.startswith(pref[0])):
                counts["prefix"][pref[1]] += 1
                break

        # root
        # use WordNet Lematizer - skipped up to now

        rootsByOrigin = self.typeMorphems["root"]
        for root in rootsByOrigin:
            if (wordLatin.find(root[0]) != -1 and
                not wordLatin.startswith(root[0]) and
                not wordLatin.endswith(root[0])):
                counts["root"][root[1]] += 1
                break

        if (wordLatin == "rhaphe"):
            pass

        # suffix
        suffixesOrigin = self.typeMorphems["suffix"]
        for suf in suffixesOrigin:
            if (wordLatin.endswith(suf[0])):
                counts["suffix"][suf[1]] += 1
                break

        latins = counts["prefix"]["Latin"] + counts["suffix"]["Latin"] + counts["root"]["Latin"]
        greeks = counts["prefix"]["Greek"] + counts["suffix"]["Greek"] + counts["root"]["Greek"]

        return "Latin" if latins >= greeks else "Greek"