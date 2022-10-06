import regex as re

numberFormatValidator = r"^\d+$"
largeUnitsBase = ['nghìn ', 'triệu ', 'tỉ ']
basicNumberToWord = {
        '0': 'không',
        '1': 'một',
        '2': 'hai',
        '3': 'ba',
        '4': 'bốn',
        '5': 'năm',
        '6': 'sáu',
        '7': 'bảy',
        '8': 'tám',
        '9': 'chín'
}

HUNDRED_PLACE_INDEX = 0
TENS_PLACE_INDEX = 1
ONES_PLACE_INDEX = 2

class NumberToText:
    @staticmethod
    def breakIntoGroupOfThree(string):
        groups = []
        remainder = len(string) % 3
        if len(string) > 3 and remainder != 0:
            groups.append(string[0:remainder])
            string = string[remainder:]
        return groups + re.findall (r"\d{1,3}", string)
    @staticmethod
    def mapGroupsToUnits(groups):
        reversedGroups = list(reversed(groups))
        reversedUnits = []
        reversedGroupsWithIndex = [{'value' : x, 'index' : i} for i, x in enumerate(reversedGroups)]
        for item in reversedGroupsWithIndex:
            if item['index'] == 0:
                reversedUnits.append('')
            else:
                reversedUnits.append(largeUnitsBase[(item['index'] - 1 ) % 3]) 

        return list(reversed(reversedUnits))

    @staticmethod
    def translateThreeDigitsNumberToWords(number):
        number = str(number)
        if len(number) > 3 or len(number) < 0 or not re.findall(numberFormatValidator, number):
            print("Type error")
        digitsLength = len(number)
        numbers = list(number)
        numbersWithIndex = [{'value' : x, 'index' : i} for i, x in enumerate(numbers)]
        result = []
        for item in numbersWithIndex:
            placeIndex = item['index']
            if digitsLength < 3:
                placeIndex = placeIndex + (3 - digitsLength)
            if placeIndex == HUNDRED_PLACE_INDEX:
                result.append(basicNumberToWord[item['value']] + ' trăm ')
            if (placeIndex == TENS_PLACE_INDEX):
                if (item['value'] == '0'):
                    nextDigest = number[item['index'] + 1]

                    if (nextDigest == '0'):
                        result.append('')
                    else:
                        result.append('lẻ')
                elif (item['value'] == '1'):
                    result.append('mười')
                else:
                    result.append(basicNumberToWord[item['value']] + ' mươi')
            if (placeIndex == ONES_PLACE_INDEX):
                if (item['value'] == '5' and digitsLength > 1):
                    result.append('lăm')
                elif (item['value'] == '1' and digitsLength > 1):
                    nextDigest = number[item['index'] - 1]
                    if (nextDigest != '0'  and nextDigest != '1'):
                        result.append('mốt')
                    else:
                        result.append('một')
                elif (item['value'] == '0' and digitsLength > 1):
                    result.append('')
                else:
                    result.append(basicNumberToWord[item['value']])
        s = ' '
        return s.join(list(filter(lambda n: n != '', result)))   

    @staticmethod
    def mapGroupsToWords(groups):
        groupsWithIndex = [{'value' : x, 'index' : i} for i, x in enumerate(groups)]
        result = []
        for i, item in enumerate(groupsWithIndex):
            t = NumberToText.translateThreeDigitsNumberToWords(item['value'])
            if i == len(groupsWithIndex) - 1:
                if t.strip() == 'không trăm':
                    continue
            result.append(t)
        return result

    def getBasisNumber(self, numberOrString):
        number = str(numberOrString)
        return basicNumberToWord[number[0]]

    def convert_phonenumber(self, numberOrString):
        number = str(numberOrString)
        text_number = number.replace('+', 'cộng').replace('-', ' ').replace('.', ' ')
        str_number = text_number.replace('cộng', '').replace(' ', '').strip()
        n = len(str_number)
        if str_number[0] == '0' and n not in [10, 11]:
            return str_number
        if str_number[0] == '8' and n not in [11, 12]:
            return str_number
        for k, v in basicNumberToWord.items():
            text_number = text_number.replace(k, v)
        return text_number

    def convert_cardserial(self, numberOrString):
        number = str(numberOrString)
        text_number = number.replace('-', ' ').replace('.', ' ')
        str_number = text_number.replace(' ', '').strip()
        n = len(str_number)
        if n != 13 and n != 16:
            return str_number
        text_number = ' '.join(list(text_number))
        for k, v in basicNumberToWord.items():
            text_number = text_number.replace(k, v)
        return text_number


    def getFullText(self, numberOrString, character=False, number=False):
        number = str(numberOrString)
        if number[0] == '0' or character is True:
            if number is False:
                for k, v in basicNumberToWord.items():
                    number = number.replace(k, " " + v + " ")
                number = " ".join(number.split())
                return number
            else:
                for k, v in basicNumberToWord.items():
                    number = number.replace(k, " " + k + " ")
                number = " ".join(number.split())
                return number
        groups = NumberToText.breakIntoGroupOfThree(number)
        groupsToUnits = NumberToText.mapGroupsToUnits(groups)
        groupsToWords = NumberToText.mapGroupsToWords(groups)
        groupsToWordsWithIndex = [{'value' : x, 'index' : i} for i, x in enumerate(groupsToWords)]
        result = ''
        for item in groupsToWordsWithIndex:
            if groupsToUnits[item['index']] == '':
                result += item['value']
            else:
                result += item['value'] + ' ' + groupsToUnits[item['index']]
        return " ".join(result.split())

if __name__ == '__main__':
   num2text = NumberToText()
   print(num2text.getFullText("2021"))
