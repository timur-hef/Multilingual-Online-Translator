import requests
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="huipstion")
parser.add_argument("from_lang")
parser.add_argument("to_lang")
parser.add_argument("word")
args = parser.parse_args()

from_lang = args.from_lang
to_lang = args.to_lang
word = args.word
user_agent = 'Mozilla/5.0'
languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish',
             'portuguese', 'romanian', 'russian', 'turkish']


def get_response(first, second, w):
    url = f'https://context.reverso.net/translation/{first.lower()}-{second.lower()}/{w}'
    return requests.get(url, headers={'User-Agent': user_agent})


def translate(language, words, type):
    original = [x.text.strip() for x in soup.find_all("div", {'class': 'src ltr'})]
    translated = [x.text.strip() for x in soup.find_all('div', {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]})]
    if type == "all":
        print(f"\n{language.capitalize()} Translations:")
        print(words[0])
        print(f"\n{language.capitalize()} Examples:")
        print(original[0])
        print(translated[0])
        print()
        with open(f'{word}.txt', 'a', encoding='utf-8') as my_file:
            my_file.write(f"\n{language.capitalize()} Translations:\n")
            my_file.write(words[0] + "\n")
            my_file.write(f"\n{language.capitalize()} Examples:\n")
            my_file.write(original[0] + "\n")
            my_file.write(translated[0]+ "\n")
            my_file.write("\n")
    if type == "one":
        with open(f'{word}.txt', 'a', encoding='utf-8') as my_file:
            print(f"\n{language.capitalize()} Translations:")
            my_file.write(f"\n{language.capitalize()} Translations:\n")
            for x in range(5):
                print(words[x])
                my_file.write(words[x] + "\n")
            print(f"\n{language.capitalize()} Examples:")
            my_file.write(f"\n{language.capitalize()} Examples:\n")
            for y in range(5):
                print(original[y])
                my_file.write(original[y] + "\n")
                print(translated[y])
                my_file.write(translated[y] + "\n")
                print()
                my_file.write("\n")


if to_lang == "all":
    if from_lang not in languages:
        print(f"Sorry, the program doesn't support {from_lang}")
    else:
        for i in languages:
            to_lang = i
            if from_lang == i:
                continue
            r = get_response(from_lang, to_lang, word)
            soup = BeautifulSoup(r.content, 'html.parser')
            temp = soup.find_all("a", {'class': 'translation'}) + soup.find_all("div", {'class': 'translation'})
            translations = [x.text.strip() for x in temp]
            translations.pop(0)
            if not translations:
                print(f"Sorry, unable to find {word}")
                break
            elif r.status_code != 200:
                print("Something wrong with your internet connection")
                break
            else:
                translate(to_lang, translations, "all")
else:
    if from_lang not in languages:
        print(f"Sorry, the program doesn't support {from_lang}")
    elif to_lang not in languages:
        print(f"Sorry, the program doesn't support {to_lang}")
    else:
        r = get_response(from_lang, to_lang, word)
        soup = BeautifulSoup(r.content, 'html.parser')
        temp = soup.find_all("a", {'class': 'translation'}) + soup.find_all("div", {'class': 'translation'})
        translations = [x.text.strip() for x in temp]
        translations.pop(0)
        if not translations:
            print(f"Sorry, unable to find {word}")
        elif r.status_code != 200:
            print("Something wrong with your internet connection")
        else:
            translate(to_lang, translations, "one")