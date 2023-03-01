from googletrans import Translator


translator = Translator()
translation = translator.translate("i like sucking cocks", dest='en')
print(translation.text)