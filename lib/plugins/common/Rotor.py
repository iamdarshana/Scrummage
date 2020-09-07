# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Homograph Enumerator v2.0 (A.K.A Punycode Domain Fuzzer)

import itertools, datetime, logging, string, sys

def Date():
    return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def List_Formatter(English_Upper, Numbers, Special_Characters, Asian, Phoenetic, Middle_Eastern, Phoenetic_Alternatives, Comprehensive):
    Lists = {}
    Cyrillic = False
    Greek = False
    Lao = False
    Thai = False
    Korean = False
    Armenian = False
    Arabic = False
    Amharic = False
    Hebrew = False
    Georgian = False
    Khmer = False
    Burmese = False
    Vietnamese = False

    if Asian:
        Middle_Eastern = False
        Phoenetic = False
        Phoenetic_Alternatives = False
        English_Upper = False
        Lao = True
        Thai = True
        Korean = True
        Khmer = True
        Burmese = True
        Vietnamese = True

    if Middle_Eastern:
        Asian = False
        Phoenetic = False
        Phoenetic_Alternatives = False
        English_Upper = False
        Armenian = True
        Arabic = True
        Amharic = True
        Hebrew = True
        Georgian = True

    if Phoenetic:
        Middle_Eastern = False
        Asian = False
        Phoenetic_Alternatives = True
        Greek = True
        Cyrillic = True

    for Alphabet_Letter in list(string.ascii_lowercase):
        Lists[Alphabet_Letter] = [Alphabet_Letter]

        if English_Upper:
            Lists[Alphabet_Letter].append(Alphabet_Letter.upper())

    if Numbers:
        Lists["a"].append("4")
        Lists["b"].append("8")
        Lists["e"].extend(["3", u"з", u"З", u"Ӡ", u"ဒ", u"ვ", u"ჳ"])
        Lists["i"].append("1")
        Lists["l"].append("1")
        Lists["o"].extend(["0", u"θ", u"០", u"៙"])
        Lists["s"].append("5")
        Lists["t"].append("7")
        Lists["z"].extend(["2", u"ㄹ"])

    if Special_Characters:
        Lists["a"].append("@")
        Lists["s"].append("$")
        Lists["l"].extend(["|", "[", "]"])
        Lists["t"].append("+")

    if Cyrillic and Comprehensive:
        Lists["a"].extend([u"а", u"д"])
        Lists["b"].append(u"в")
        Lists["c"].append(u"с")
        Lists["e"].extend([u"е", u"є"])
        Lists["h"].extend([u"һ", u"Һ", u"ʜ"])
        Lists["i"].append(u"і")
        Lists["k"].append(u"к")
        Lists["m"].append(u"м")
        Lists["n"].extend([u"п", u"и", u"й", u"л"])
        Lists["o"].append(u"о")
        Lists["p"].append(u"р")
        Lists["r"].extend([u"г", u"я"])
        Lists["s"].append(u"ѕ")
        Lists["t"].append(u"т")
        Lists["w"].extend([u"ш", u"щ"])
        Lists["x"].extend([u"х", u"ж"])
        Lists["y"].extend([u"у", u"ү"])

    elif Cyrillic and not Comprehensive:
        Lists["a"].append(u"а")
        Lists["c"].append(u"с")
        Lists["e"].append(u"е")
        Lists["h"].extend([u"һ", u"Һ"])
        Lists["i"].append(u"і")
        Lists["k"].append(u"к")
        Lists["m"].append(u"м")
        Lists["n"].append(u"п")
        Lists["o"].append(u"о")
        Lists["p"].append(u"р")
        Lists["r"].append(u"г")
        Lists["s"].append(u"ѕ")
        Lists["t"].append(u"т")
        Lists["w"].append(u"ш")
        Lists["x"].append(u"х")
        Lists["y"].extend([u"у", u"ү"])

    if Greek and Comprehensive:
        Lists["i"].extend([u"ί", u"ι"])
        Lists["k"].append(u"κ")
        Lists["n"].extend([u"η", u"π"])
        Lists["o"].extend([u"ο", u"σ"])
        Lists["p"].append(u"ρ")
        Lists["t"].append(u"τ")
        Lists["u"].append(u"υ")
        Lists["v"].extend([u"ν", u"υ"])
        Lists["w"].append(u"ω")
        Lists["x"].append(u"χ")
        Lists["y"].append(u"γ")

    elif Greek and not Comprehensive:
        Lists["k"].append(u"κ")
        Lists["n"].append(u"η")
        Lists["o"].extend([u"ο", u"σ"])
        Lists["p"].append(u"ρ")
        Lists["u"].append(u"υ")
        Lists["v"].append(u"ν")
        Lists["w"].append(u"ω")
        Lists["y"].append(u"γ")

    if Armenian:
        Lists["d"].append(u"ժ")
        Lists["g"].append(u"ց")
        Lists["h"].extend([u"հ" u"ի"])
        Lists["n"].extend([u"ր", u"ռ", u"ո", u"ղ"])
        Lists["o"].append(u"օ")
        Lists["p"].extend([u"թ", u"բ", u"ք"])
        Lists["q"].extend([u"գ", u"զ"])
        Lists["u"].extend([u"ս", u"ն", u"մ"])
        Lists["w"].extend([u"ա", u"պ"])

    if Amharic:
        Lists["h"].extend([u"ከ", u"ኩ", u"ኪ", u"ካ", u"ኬ", u"ክ", u"ኮ", "ዘ", u"ዙ", u"ዚ", u"ዛ", u"ዜ", u"ዝ", u"ዞ", u"ዟ", u"ዠ", u"ዡ", u"ዢ", u"ዣ", u"ዤ", u"ዥ", u"ዦ", u"ዧ"])
        Lists["l"].extend([u"ገ", u"ጉ", u"ጊ", u"ጋ", u"ጌ", u"ግ", u"ጎ"])
        Lists["m"].extend([u"ጠ", u"ጡ", u"ጢ", u"ጣ", u"ጤ", u"ጦ", u"ጧ"])
        Lists["n"].extend([u"ሰ", u"ሱ", u"ሲ", u"ሳ", u"ሴ", u"ስ", u"ሶ", u"በ", u"ቡ", u"ቢ", u"ባ", u"ቤ", u"ብ", u"ቦ"])
        Lists["o"].extend([u"ዐ", u"ዑ", u"ዕ", u"ፀ", u"ፁ"])
        Lists["p"].extend([u"የ", u"ዩ", u"ዪ", u"ያ", u"ዬ", u"ይ", u"ዮ"])
        Lists["t"].extend([u"ፐ", u"ፑ", u"ፒ", u"ፓ", u"ፔ", u"ፕ", u"ፖ", u"ፗ"])
        Lists["u"].extend([u"ሀ", u"ሁ", u"ሆ", u"ህ"])
        Lists["v"].extend([u"ሀ", u"ሁ", u"ሆ"])
        Lists["w"].extend([u"ሠ", u"ሡ"])
        Lists["y"].extend([u"ሂ", u"ሃ"])

    if Arabic:
        Lists["j"].append(u"ز")
        Lists["l"].extend([u"ا", u"أ", u"آ"])

    if Hebrew:
        Lists["i"].extend([u"ו", u"נ", u"ו"])
        Lists["l"].append(u"ן")
        Lists["n"].extend([u"ח", u"ת", u"ה", u"תּ"])
        Lists["o"].extend([u"ס", u"ם"])
        Lists["u"].append(u"ט")
        Lists["v"].append(u"ע")
        Lists["w"].extend([u"ש", u"שׂ", u"שׁ"])
        Lists["x"].extend([u"א", u"ɣ"])
        Lists["y"].extend([u"צ", u"ץ"])

    if Burmese:
        Lists["c"].append(u"င")
        Lists["h"].append(u"꧵")
        Lists["n"].append(u"ဂ")
        Lists["o"].append(u"ဝ")
        Lists["u"].append(u"ပ")
        Lists["w"].append(u"ယ")

    if Khmer:
        Lists["h"].append(u"អ")
        Lists["m"].extend([u"ញ", u"៣"])
        Lists["n"].extend([u"ក", u"ព", u"ត", u"ភ", u"ឥ"])
        Lists["s"].append(u"ន")
        Lists["u"].extend([u"ឋ", u"ប", u"ឞ"])
        Lists["w"].extend([u"ឃ", u"យ", u"ដ", u"ផ"])

    if Korean:
        Lists["c"].append(u"ㄷ")
        Lists["e"].append(u"ㅌ")
        Lists["l"].extend([u"ㅣ", u"ㄴ"])
        Lists["o"].extend([u"ㅁ", u"ㅇ"])
        Lists["t"].extend([u"ㅜ", u'ㅊ'])

    if Thai:
        Lists["n"].extend([u"ก", u"ค", u"ฅ", u"ฑ", u"ด", u"ต", u"ถ", u"ท", u"ห", u"ภ"])
        Lists["u"].extend([u"ข", u"ฃ", u"น", u"บ", u"ป"])
        Lists["w"].extend([u"ผ", u"ฝ", u"พ", u"ฟ", u"ฬ"])

    if Lao:
        Lists["m"].extend([u"ຕ", u"໘"])
        Lists["n"].extend([u"ດ", u"ກ", u"ຄ", u"ຖ"])
        Lists["o"].append(u"໐")
        Lists["s"].extend([u"ຣ", u"ຮ"])
        Lists["u"].extend([u"ນ", u"ບ", u"ປ", u"ມ"])
        Lists["w"].extend([u"ຜ", u"ຝ", u"ພ", u"ຟ", u"໖"])

    if Georgian:
        Lists["b"].extend([u"ხ", u"წ", u"Ⴆ"])
        Lists["d"].append(u"ძ")
        Lists["h"].extend([u"Ⴙ", u"ⴌ", u"ⴡ", u"ჩ"])
        Lists["m"].extend([u"ⴅ", u"ⴜ", u"ო", u"რ"])
        Lists["n"].extend([u"ⴄ", u"ⴈ", u"ი"])
        Lists["t"].append([u"ⴕ"])
        Lists["w"].extend([u"ⴍ", u"ⴓ"])
        Lists["x"].append(u"ⴟ")
        Lists["y"].extend([u"ⴁ", u"ⴗ", u"ⴞ", u"ⴤ", u"ყ"])

    if Vietnamese or (Phoenetic_Alternatives and Comprehensive):
        Lists["a"].extend([u"ắ", u"ậ", u"ả", u"ạ", u"ắ", u"ằ", u"ẳ", u"ẵ", u"ặ", u"ấ", u"ầ", u"ẩ", u"ẫ", u"ă", u"ą"])
        Lists["d"].extend([u"đ", u"d̪"])
        Lists["i"].extend([u"ị", u"ĩ", u"ỉ"])
        Lists["e"].extend([u"ệ", u"ế", u"ẻ", u"ẽ", u"ẹ", u"ề", u"ể", u"ễ", u"ĕ", u"ė", u"ę", u"ě"])
        Lists["g"].extend([u"ġ", u"ğ"])
        Lists["n"].extend([u"n̪", u"ŋ", u"ɲ"])
        Lists["o"].extend([u"ơ", u"ớ", u"ỏ", u"ố", u"ồ", u"ổ", u"ỗ", u"ộ", u"ờ", u"ở", u"ỡ", u"ŏ", u"ợ"])
        Lists["s"].extend([u"ş", u"s̠", u"ʂ"])
        Lists["t"].append(u"t̪")
        Lists["u"].extend([u"ư", u"ự", u"ữ", u"ủ", u"ụ", u"ứ", u"ừ", u"ử", u"ŭ", u"ů", u"ư"])
        Lists["y"].extend([u"ỹ", u"ỳ", u"ỷ", u"ỵ", u"ý"])

    if Phoenetic_Alternatives:
        Lists["a"].extend([u"à", u"á", u"â", u"ã", u"ä", u"å", u"ā"])
        Lists["b"].append(u"þ")
        Lists["c"].extend([u"ç", u"ć", u"ĉ", u"ċ", u"č"])
        Lists["d"].append(u"ð")
        Lists["e"].extend([u"ē", u"è", u"é", u"ê", u"ë"])
        Lists["h"].append(u"ɦ")
        Lists["i"].extend([u"ì", u"í", u"î", u"ï"])
        Lists["m"].append("rn")
        Lists["o"].extend([u"ø", u"ó", u"ò", u"ô", u"õ", u"ö", u"ō", u"ɸ"])
        Lists["s"].extend([u"š", u"ś"])
        Lists["u"].extend([u"ù", u"ú", u"û", u"ü", u"ũ", u"ū"])
        Lists["v"].extend([u"ʋ", u"ʊ"])
        Lists["y"].append(u"ÿ")

    return Lists

def Rotor_Combinations(Rotor_Wordlist):

    if (len(Rotor_Wordlist) <= 15):
        Altered_URLs = list(map(''.join, list(itertools.product(*Rotor_Wordlist))))
        return Altered_URLs

    else:
        logging.warning(f"{Date()} [-] The word entered was either over 15 characters in length or had no characters, this function only permits words with character lengths between 1 and 15.")
        return None

def Search(Query, English_Upper, Numbers, Special_Characters, Asian, Phoenetic, Middle_Eastern, Phoenetic_Alternatives, Comprehensive):
    Rotor_Wordlist = []
    URL_Allowed_Characters_List = ['$', '-', '_', '.', '+', '!', '*', '\'', '(', ')', ',']

    if type(Query) == str:
        Query = list(Query)

    elif type(Query) != str and type(Query) != list:
        logging.error(f"{Date()} [-] Invalid query type.")
        return None

    Lists = List_Formatter(English_Upper, Numbers, Special_Characters, Asian, Phoenetic, Middle_Eastern, Phoenetic_Alternatives, Comprehensive)

    for Letter in Query:

        for List_Key, List_Value in Lists.items():

            if Letter == List_Key:
                Rotor_Wordlist.append(List_Value)

        for Character in URL_Allowed_Characters_List:

            if Letter == Character:
                Rotor_Wordlist.append(Character)

    return Rotor_Combinations(Rotor_Wordlist)