from nemo_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer
import regex as re

inverse_normalizer = InverseNormalizer(lang='vi', cache_dir="fst_model", overwrite_cache=False)

f = open("regexDatabase.txt", "r", encoding="utf8")
type_regexs = [" ".join((regex.replace("\n", "").split("=>")[0]).split()) for regex in f.readlines()]
f = open("regexDatabase.txt", "r", encoding="utf8")
regexs = [" ".join((regex.replace("\n", "").replace("\\\\", "\\").split("=>")[1]).split()) for regex in f.readlines()]

def reformatDate(text):
    text = " " + text + " "
    for i, regex in enumerate(regexs):
        _matches = re.findall(regex, text)
        if _matches:
            for _match in _matches:
                matches = re.search(_match, text)
                if matches:
                    start = matches.span()[0]
                    stop = matches.span()[1]
                    string_21 = text[:start]
                    string_22 = text[stop:]
                    entity = text[start:stop]
                    if type_regexs[i] == "DAY_MONTH":
                        entity = entity.replace("ngày", "")
                        entity = entity.replace("tháng", "/")
                        entity = entity.replace(" ", "")
                        entity = " " + entity + " "
                    elif type_regexs[i] == "MONTH_YEAR":
                        entity = entity.replace("tháng", "")
                        entity = entity.replace("năm", "/")
                        entity = entity.replace(" ", "")
                        entity = " " + entity + " "
                    elif type_regexs[i] == "DAY_MONTH_YEAR":
                        entity = entity.replace("ngày", "")
                        entity = entity.replace("tháng", "/")
                        entity = entity.replace("năm", "/")
                        entity = entity.replace(" ", "")
                        entity = " " + entity + " "
                    text = string_21 + entity + string_22
    return " ".join(text.split())

print(reformatDate(" ngày 12 tháng 2 năm 2021 "))