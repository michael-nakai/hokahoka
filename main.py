from helpers import *
import pandas as pd
import os


def main(report_folder_loc: str, num_of_loops: str | int = 'tons of rice', debug: bool = False):
    """
    The main loop for hokahoka.

    :param report_folder_loc: The location to the folder where reports should be saved. Should end with a slash or backslash.
    :param num_of_loops: Determines whether the loop should be infinite or not. Use 'tons of rice' for infinite, or an int for a specific number of loops.
    :param debug: Whether we're debugging or not.
    """

    # Initialize reporting
    qwords = []
    a1s = []
    a2s = []
    a3s = []
    a4s = []
    ans_int_chosen = []
    myans = []
    correct = []

    # Reporting function
    def add_to_reporting(qa_list_str, answer_int, what_i_thought, was_it_right):
        nonlocal qwords, a1s, a2s, a3s, a4s, ans_int_chosen, myans, correct
        qwords.append(qa_list_str[0])
        a1s.append(qa_list_str[1])
        a2s.append(qa_list_str[2])
        a3s.append(qa_list_str[3])
        a4s.append(qa_list_str[4])
        ans_int_chosen.append(answer_int)
        myans.append(what_i_thought)
        correct.append(was_it_right)
        return None

    # Main
    def mainloop(debug_setting=False):
        qas = grab_question_and_answers(debug=debug_setting)
        qa_list = read_question_and_answers(qas)
        ans = get_answer_number(qa_list, debug=debug_setting)
        click_answer(ans)

        j = 0
        tf = False
        while j != 3:
            sleep(0.5)
            tf = analyse_result(ans, debug=debug_setting)
            if tf:
                print('I was right!')
                break
            j += 1
        if not tf:
            print('I was wrong.')

        add_to_reporting(qa_list, ans, qa_list[ans], tf)
        print()
        sleep(4)

    # Execution
    open_freerice_and_focus()

    if debug:
        mainloop(debug_setting=True)

    elif num_of_loops == 'tons of rice':
        while True:
            mainloop()

    else:
        i = 0
        while i != num_of_loops:
            mainloop()
            i += 1

    # Final reporting
    report = pd.DataFrame(data={'Query': qwords,
                                'Option_1': a1s,
                                'Option_2': a2s,
                                'Option_3': a3s,
                                'Option_4': a4s,
                                'Answer_Chosen': myans,
                                'Answer_Number': ans_int_chosen,
                                'Correct': correct})

    filelist = os.listdir(report_folder_loc)
    if filelist:
        used_nums = [int(x.split('.')[0][-4:]) for x in filelist if x.split('.')[0][-4:].isnumeric()]
        run_num = f'{used_nums.sort()[-1] + 1:04d}'
    else:
        run_num = '0001'
    report.to_csv(report_folder_loc + 'run_' + run_num + '.csv', index=False)


if __name__ == '__main__':

    report_folder = r'B:\Data_Storage\hokahoka\reports\\'

    main(report_folder, 5, debug=True)
