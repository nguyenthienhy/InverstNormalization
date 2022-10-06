from convert_number import NumberToText
from nemo_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer
import regex as re

class PostProcessing:

    def __init__(self) -> None:
        
        self.num2text = NumberToText()
        f = open("regexDatabase.txt", "r", encoding="utf8")
        self.type_regexs = [" ".join((regex.replace("\n", "").split("=>")[0]).split()) for regex in f.readlines()]
        f.close()
        f = open("regexDatabase.txt", "r", encoding="utf8")
        self.regexs = [" ".join((regex.replace("\n", "").replace("\\\\", "\\").split("=>")[1]).split()) for regex in f.readlines()]
        f.close()
        self.inverse_normalizer = InverseNormalizer(lang='vi', cache_dir="fst_model", overwrite_cache=False)

    def reformatDate(self, text):
        text = " " + text + " "
        for i, regex in enumerate(self.regexs):
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
                        if self.type_regexs[i] == "DAY_MONTH":
                            entity = entity.replace("ngày", "")
                            entity = entity.replace("tháng", "/")
                            entity = entity.replace(" ", "")
                            entity = " " + entity + " "
                        elif self.type_regexs[i] == "MONTH_YEAR":
                            entity = entity.replace("tháng", "")
                            entity = entity.replace("năm", "/")
                            entity = entity.replace(" ", "")
                            entity = " " + entity + " "
                        elif self.type_regexs[i] == "DAY_MONTH_YEAR":
                            entity = entity.replace("ngày", "")
                            entity = entity.replace("tháng", "/")
                            entity = entity.replace("năm", "/")
                            entity = entity.replace(" ", "")
                            entity = " " + entity + " "
                        text = string_21 + entity + string_22
        return " ".join(text.split())

    def reformatNumber(self, text):
        money_unit = ["tỷ", "triệu", "nghìn", "trăm"]
        words = text.split()
        for index, word in enumerate(words):
            if word in money_unit:
                if index >= 1:
                    if words[index-1].isdecimal():
                        words[index-1] = self.num2text.getFullText(words[index-1])
                if word == "trăm":
                    if index + 1 < len(words):
                        if words[index+1].isdecimal():
                            words[index+1] = self.num2text.getFullText(words[index+1])
        return " ".join(words)

    def isSurplusNumber(self, word):
        if len(word) == 2:
            if word[0] == "0" and word[1].isdecimal():
                return 0
        if len(word) == 3:
            if word[0] == "0" and word[1] == "0" and word[2].isdecimal():
                return 1
        return 2

    def revertSurplusNumber(self, text):
        words = text.split()
        for i, word in enumerate(words):
            if self.isSurplusNumber(word) == 0:
                words[i] = "linh " + self.num2text.getFullText(str(words[i][-1]))
            elif self.isSurplusNumber(word) == 1:
                words[i] = "không trăm linh " + self.num2text.getFullText(str(words[i][-1]))
        return " ".join(words)

    def revertDate2Num(self, text):
        words = text.split()
        for index, word in enumerate(words):
            if word == "năm" and words[index-1].isdecimal() and words[index+1].isdecimal():
                words[index] = "5"
                words[index+1] = self.num2text.getFullText(words[index+1], character=True, number=True)
        return " ".join(words)

    def combineSeparatedNumber(self, text):
        words = text.split()
        start_end_list = []
        flags = [False for _ in words]
        for index, word in enumerate(words):
            if word.isdecimal() and len(word) == 1 and flags[index] is False:
                index_decimal = index
                index_start = index_decimal
                start_end = []
                while words[index_decimal].isdecimal() and len(words[index_decimal]) == 1:
                    flags[index_decimal] = True
                    start_end.append(words[index_decimal])
                    index_decimal += 1
                    if index_decimal >= len(words):
                        break
                index_end = index_decimal - 1
                separatedNumber = " ".join(words[index_start:index_end+1])
                combineNumber = "".join(words[index_start:index_end+1])
                text = text.replace(separatedNumber, combineNumber)
                start_end_list.append(start_end)
                if index_decimal == len(words):
                    break
        return " ".join(text.split())

    def postProcess(self, text):
        text = self.reformatDate(text)
        text = self.revertDate2Num(text)
        text = self.combineSeparatedNumber(text)
        text = self.revertSurplusNumber(text)
        text = self.reformatNumber(text)
        text = self.inverse_normalizer.inverse_normalize(text, verbose=False)
        return text

if __name__ == "__main__":

    app = PostProcessing()

    text = app.postProcess("tôi vừa mới chuyển cho số điện thoại 0 9 8 1 2 3 4 5 6 số tiền là 1 trăm 20 nghìn đồng vào ngày 12 tháng 3 năm 2022 lúc 16 giờ 31 phút")

    print(text)