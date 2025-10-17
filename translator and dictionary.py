import nltk
nltk.download('wordnet')
import sys
from googletrans import Translator, LANGUAGES
from nltk.corpus import wordnet as wn

class DictionaryTranslator:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text, dest_language='en'):
        try:
            translation = self.translator.translate(text, dest=dest_language)
            return translation.text
        except Exception as e:
            print(f"خطا در ترجمه: {e}")
            return None

    def get_meaning(self, word):
        try:
            synsets = wn.synsets(word)
            meanings = {}
            for synset in synsets:
                meanings[synset.name()] = synset.definition()
            return meanings
        except Exception as e:
            print(f"خطا در دریافت معنی: {e}")
            return None

    def display_languages(self):
        print("\nزبان‌های قابل پشتیبانی:")
        for lang_code, lang_name in LANGUAGES.items():
            print(f"{lang_code}: {lang_name}")

def main():
    dt = DictionaryTranslator()

    while True:
        print("\n--- دیکشنری و مترجم ---")
        print("1. ترجمه متن")
        print("2. دریافت معنی کلمه")
        print("3. نمایش زبان‌های قابل پشتیبانی")
        print("4. خروج")

        choice = input("انتخاب کنید: ")

        if choice == '1':
            text = input("متن را وارد کنید: ")
            lang = input("زبان مقصد (مثلاً 'en' برای انگلیسی): ")
            translated = dt.translate_text(text, lang)
            if translated:
                print(f"ترجمه: {translated}")

        elif choice == '2':
            word = input("کلمه را وارد کنید: ")
            meanings = dt.get_meaning(word)
            if meanings:
                for synset, definition in meanings.items():
                    print(f"\nمعنی '{synset}': {definition}")
            else:
                print(f"متاسفم، معنی برای '{word}' پیدا نشد.")

        elif choice == '3':
            dt.display_languages()

        elif choice == '4':
            print("خروج از برنامه.")
            sys.exit()

        else:
            print("لطفاً گزینه صحیحی را انتخاب کنید.")

if __name__ == "__main__":
    main()
