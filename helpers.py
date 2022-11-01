from PIL import ImageGrab
from time import sleep
from pytesseract import pytesseract
from nltk.corpus import wordnet
from pyautogui import click, moveTo
import webbrowser


def open_freerice_and_focus():
    """
    Opens freerice.com and focuses the window in firefox.

    :return: None.
    """

    webbrowser.open('https://freerice.com')
    sleep(10)  # Let the webpage open/load fully first
    return None


def grab_question_and_answers(debug=False):
    """
    Grabs the "_____ means:" prompt, along with each possible answer.

    :param debug: Whether we're debugging or not.
    :return: A list of PIL image grabs, in the format [question, ans1, ans2, ans3, ans4].
    """

    question = ImageGrab.grab(bbox=(795, 200, 1110, 250))
    ans1 = ImageGrab.grab(bbox=(800, 260, 1105, 300))
    ans2 = ImageGrab.grab(bbox=(800, 320, 1105, 360))
    ans3 = ImageGrab.grab(bbox=(800, 380, 1105, 416))
    ans4 = ImageGrab.grab(bbox=(800, 437, 1105, 472))

    qalist = [question, ans1, ans2, ans3, ans4]
    if debug:
        i = 0
        for im in qalist:
            im.save(f'B:\\Data_Storage\\hokahoka\\debug\\{str(i)}.png')
            i += 1
    return qalist


def read_question_and_answers(qa_list):
    """
    Reads the question and answer image list, and returns the english words in a list.

    :param qa_list: A list of PIL.Image objects from grab_questions_and_answers().
    :return: A list of strs, corresponding to the input list of images.
    """

    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    strlist = [pytesseract.image_to_string(qa_list[0], config=f"--psm 7 -c tessedit_char_whitelist='abcdefghijklmnopqr stuvwxyz'").strip().split(' ')[0]]
    for im in qa_list[1:]:
        strlist.append(pytesseract.image_to_string(im, config=f"--psm 7 -c tessedit_char_whitelist='abcdefghijklmnopqr stuvwxyz'").strip())

    print(f'The question word is: {strlist[0]}')
    print(f'The answers are: {strlist[1:]}')
    return strlist


def get_answer_number(qa_str_list, debug=False):
    """
    Finds the most related word to the question word. It stops looking after the first answer that looks good,
    so no multiple answer situations (just hope that it's right). If it can't find an answer, we just say
    that the first one is correct (easier to just skip to the next question).

    :param qa_str_list: The list of strings from read_question_and_answers().
    :param debug: Whether we're debugging or not.
    :return: An int where 1 <= x <= 4, corresponding to the correct answer.
    """

    synonyms = set()

    for syn in wordnet.synsets(qa_str_list[0]):
        for wordobj in syn.lemmas():
            synonyms.add(wordobj.name().replace('_', ' ', -1))

    if debug:
        print(synonyms)

    i = 1
    for ans in qa_str_list[1:]:
        if ans in synonyms:
            print(f'I think the answer word is: {qa_str_list[1:][i-1]}')
            return i
        i += 1

    print(f"I'm confused and don't know the answer :(")
    return 0


def click_answer(ans_int):
    """
    Actually does the clicking.

    :param ans_int: An int where 1 <= x <= 4, corresponding to the correct answer.
    :return: None.
    """

    coord_dict = {1: (800, 260, 1105, 300),
                  2: (950, 340),
                  3: (950, 396),
                  4: (950, 455)}

    if ans_int == 0:
        ans_int = 1

    x_coord = coord_dict[ans_int][0]
    y_coord = coord_dict[ans_int][1]
    click(x_coord, y_coord)
    moveTo(100, 100)
    return None


def analyse_result(answer_int, debug):
    """
    Checks whether we were right or not.

    :param answer_int: The answer number that we chose.
    :param debug: Whether we're debugging or not.
    :return: True if correct, False otherwise.
    """

    coord_dict = {1: (800, 260, 1105, 300),
                  2: (800, 320, 1105, 360),
                  3: (800, 380, 1105, 416),
                  4: (800, 437, 1105, 472)}

    if answer_int == 0:
        answer_int = 1

    if not debug:
        ans = ImageGrab.grab(bbox=coord_dict[answer_int]).load()
    else:
        ans = ImageGrab.grab(bbox=coord_dict[answer_int])
        ans.show()
        ans = ans.load()

    if ans[1, 1][:3][0] < 140 and ans[1, 1][:3][1] > 200 and ans[1, 1][:3][2] > 101:
        return True
    else:
        if debug:
            print(f'RGB: {ans[1, 1][:3]}')
        return False



