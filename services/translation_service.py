import json
import os

class TranslationManager:
    def __init__(self, default_lang='uz'):
        self.current_lang = default_lang
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        trans_dir = 'd:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/translations'
        for lang_file in os.listdir(trans_dir):
            if lang_file.endswith('.json'):
                lang_code = lang_file.split('.')[0]
                with open(os.path.join(trans_dir, lang_file), 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)

    def get_text(self, key):
        return self.translations.get(self.current_lang, {}).get(key, key)

    def set_language(self, lang_code):
        if lang_code in self.translations:
            self.current_lang = lang_code
            return True
        return False
