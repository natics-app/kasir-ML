

class TextProcessor:
    def __init__(self):
        pass

    def text_processing(self, dictionary, taggedArray, newLabel):
        tagging_arr = taggedArray

        sentence = []
        for tag in tagging_arr:
            sentence.append(tag[0])

        location_arr = dictionary

        locationArr_index = 0
        location_index = 0
        sentence_index = 0
        tagging_index = 0
        success_count = 0
        check = []
        while_count = 0

        for word in sentence:
            for location in location_arr:
                if word == location[0]:
                    checking_arr = []
                    checking_arr.append(word)
                    for _ in range(len(location) - 1):
                        sentence_index += 1
                        checking_arr.append(sentence[sentence_index])
                    sentence_index -= (len(location) - 1)

                    if checking_arr == location:
                        for _ in range(len(location) - 1):
                            tagging_arr[sentence_index][0] = tagging_arr[sentence_index][0] + ' ' + \
                                                             tagging_arr[tagging_index + 1][0]
                            tagging_arr[tagging_index + 1][0] = ''
                            tagging_index += 1
                        tagging_arr[sentence_index][1] = newLabel
                        tagging_index -= len(location) - 1
            sentence_index += 1
            tagging_index += 1

        new_arr = []

        for tag in tagging_arr:
            if tag[0] != '':
                new_arr.append(tag)

        return new_arr