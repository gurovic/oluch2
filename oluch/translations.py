from modeltranslation.translator import translator, TranslationOptions
from models import Contest

class ContestTranslationOptions(TranslationOptions):
    fields = ('title', )

translator.register(Contest, ContestTranslationOptions)