from Transliterator import Transliterator
from OriginFinder import OriginFinder

originFinder = OriginFinder()

words_latin = [
    "basis",
    "crisis", "khrusos",
    "dorsalis",
    "kephale",
    "lingua",
    "neoplasma",
    "rhigos", "rhaphe", "rhabdos", "rhachis", "rhein", "rhiza", "rhodon", "rhombos",
    "ruptus",
    "sanguis", "sensibilis", "suavis", "suillus", "sphaira",
    "taxis", "trapez", "trapeza",
    "thanatos",
    "vulpis", "vicesimus", "viceni",
    "xantos", "xiphos",
    "zona", "zester", "zincum"
]

transliterator = Transliterator(originFinder)
# transliterator.test(words_latin)
transliterator.exportFromCSV()