
class PostProcessing:

    def __init__(self) -> None:
        pass

    def combineSeparatedNumber(self, text):
        words = text.split()
        start_end_list = []
        flags = [False for _ in words]
        for index, word in enumerate(words):
            if word.isdecimal() and flags[index] is False:
                index_decimal = index
                index_start = index_decimal
                start_end = []
                while words[index_decimal].isdecimal():
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

app = PostProcessing()

text = app.combineSeparatedNumber("1 tôi cần số điện 1 2 3 1 4 2 thoại 0 9 8 7 1 2 3 4 1 3 2 với số tiền 1 3 5 7 8 hiện tại tôi đang cần kiểm tra một số điện thoại 0 9 8 3 1 2 2 3")
print(text)