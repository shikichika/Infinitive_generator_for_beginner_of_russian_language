import streamlit as st
import pymorphy2
import pandas as pd
import requests
import json

st.title("""ロシア語原型メーカー""")
st.header("""Генератор инфинитива""")

st.write("\n")
st.write("\n")
st.write("\n")

st.write("""
    これはロシア語学習者向けの単語の原型検索ツールです\n
    翻訳は無料の外部リソースのDeepLを使っているので月の利用上限を超えると止まります\n
    個別の単語の翻訳は目も当てられないほど悲惨な出来だったのでやめました\n
    Это приложение для тех, кто начинает изучать русский язык\n
    Используя бесплатный перевочик DeepL, это остановится когда поиск превышает лимит\n
    Это генератор не переводит каждый слово из-за того, как перевод ужасный 
""")

st.write("\n")
st.write("\n")
st.write("\n")

search_words = st.text_input("検索 (Поиск слов)", "検索したい単語を入れてください Напишите слова")


with open("auth.json") as json_open:
    json_load = json.load(json_open)

API_KEY = "3237dd9b-f637-dabd-af60-64ad5eae28da:fx"
# API_KEY = json_load["api_key"]


target_lang = "ja"

def translation(words):

    params = {
                'auth_key' : API_KEY,
                'text' : words,
                "target_lang": target_lang
            }
    request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
    result = request.json()

    return result['translations'][0]['text']

parts_of_speech ={

    "NOUN" : "名詞　Сущ",
    "ADJF" : "形容詞　П.При",
    "ADJS" : "形容詞短縮形　К.При",
    "COMP" : "比較詞　Компаратив",
    "VERB" : "動詞　Глагол",
    "INFN" : "不定形　Инфинитив",
    "PRTF" : "形動詞　П.Причастие",
    "PRTS" : "短縮形動詞　К.Причастие",
    "GRND" : "副動詞　Деепричасте",
    "NUMR" : "数詞　Числительное",
    "ADVB" : "副詞　Наречие",
    "NPRO" : "代名詞　Мест",
    "PRED" : "否定代名詞　Предикатив",
    "PREP" : "前置詞　Предлог",
    "PREP" : "接続詞　Союз",
    "PRCL" : "不変化詞　Частица",
    "INTJ" : "Междометие",
    "<NA>" : " "
}

def lemmatize(words):

    words = words.replace(".", "").replace(",", "").replace("!", "").replace("?", "").replace("'", "").replace("\"", "")
    words = words.split(" ")
    lemma_words = []
    word_types = []
    #trans_words = []

    for word in words:
        
        analyzer = pymorphy2.MorphAnalyzer()
        lemma_word = analyzer.parse(word)[0].normal_form
        lemma_words.append(lemma_word)
        word_type = analyzer.parse(word)[0].tag.POS

        try:
            word_types.append(parts_of_speech[word_type])
        except:
            word_types.append("")
        # try:
        #     if lemma_word == "я" or lemma_word == "меня" or lemma_word == "мне" or lemma_word == "мной":
        #         trans_words.append("わたし")
        #         continue
        #     trans_words.append(translation(lemma_word))
        # except:
        #     st.error('今月の翻訳上限超えました (Лимит поиска закончен в этом месяце)', icon="🚨")      

    return words, lemma_words, word_types#, trans_words


lemma_df = pd.DataFrame(lemmatize(search_words), index=["元の単語 (Предыдущее слово)", "原型 (Инфинитив)", "タイプ (Часть речи)"]).T

try:
    translation_all = translation(search_words)
except:
    st.error('今月の翻訳上限超えました (Лимит поиска закончен в этом месяце)', icon="🚨")      

st.write(lemma_df)

st.text_input(""" 全訳 (Перевод всех слов)""", translation_all)



def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

csv = convert_df(lemma_df)

st.download_button(
     label="Download (Скачать резурьтат)",
     data=csv,
     file_name='result.csv',
     mime='text/csv',
 )

st.caption("@shiki_yoshida")
st.caption("問い合わせ・要望などはDMでお願いします　https://twitter.com/anya_ruski")
