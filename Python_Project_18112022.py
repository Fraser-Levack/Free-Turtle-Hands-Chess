# Things to install to make work - pyttsx3 - speechRecognition - pyaudio - PIL

import random as rnd
import turtle as tt

copy = {}
Computer_get_out_of_check = []
using_libraries_test = False
user_test = input('Would you like to use speech recognition and other libraries? Please type "yes" :')
if 'yes' in user_test or 'Yes' in user_test:
    using_libraries_test = True

if using_libraries_test:

    import pyttsx3 as speech
    import pyaudio
    import speech_recognition as sr
    from PIL import Image

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    the_Recognizer = sr.Recognizer()
    the_Microphone = sr.Microphone()
    voice = speech.init()
else:
    voice = None


def initialize_text_to_speech(v, r):
    global voice
    voices = voice.getProperty('voices')
    voice.setProperty('volume', v)
    voice.setProperty('rate', r)
    voice.setProperty('voice', voices[0].id)
    # rate = voice.getProperty('rate')


def translate_mic_to_text():
    print('Listening now...')
    return_dictionary = {'completed': True,
                         'error_message': None,
                         'transcript': None}
    if using_libraries_test:

        with the_Microphone as source:
            the_Recognizer.adjust_for_ambient_noise(source, duration=0.3)
            source_audio = the_Recognizer.listen(source)
        try:
            return_dictionary['transcript'] = the_Recognizer.recognize_google(source_audio)
            print("Google Speech Recognition thinks you said:", return_dictionary['transcript'])
        except sr.RequestError:
            return_dictionary['completed'] = False
            return_dictionary['error_message'] = 'API error'
        except sr.UnknownValueError:
            return_dictionary['completed'] = False
            return_dictionary['error_message'] = 'unable to understand'

        return return_dictionary
    else:
        return_dictionary['transcript'] = input(':  ')
        return return_dictionary


def mic_error_checking(passed_dictionary):
    while not passed_dictionary['completed']:
        robot_speaking('Sorry i was {}. Please try again...'.format(passed_dictionary['error_message']))
        passed_dictionary = translate_mic_to_text()
    return passed_dictionary['transcript']


def get_dictionary_from_file(file_name, passed_dic):
    file = open('Project_textFiles/' + file_name)
    new_line = file.readline()
    while new_line != '':
        s_new_line = new_line[:-1].split(':::')
        dic_key = s_new_line[0]
        dic_value = s_new_line[1].split(',')
        passed_dic[dic_key] = dic_value
        new_line = file.readline()
    return passed_dic


def robot_speaking(text):
    print(text)
    if using_libraries_test:
        voice.say(text)
        voice.runAndWait()


def get_random_name():
    names_file = open('Project_textFiles/Names.txt')
    line_list = []
    new_line = names_file.readline()
    while new_line != '':
        line_list.append(new_line[:-1])
        new_line = names_file.readline()
    names_file.close()

    return rnd.choice(line_list)


def get_your_name():
    correct_name = False
    while not correct_name:

        translated_text = mic_error_checking(translate_mic_to_text())
        if 'my name' in translated_text or 'My name' in translated_text:
            extracted_name = translated_text[11:]
        else:
            extracted_name = translated_text
        robot_speaking('So your name is {}. Is this correct?'.format(extracted_name))
        yn_answer = mic_error_checking(translate_mic_to_text())
        if 'yes' in yn_answer or 'Yes' in yn_answer or 'correct' in yn_answer:
            return extracted_name
        elif 'no' in yn_answer or 'No' in yn_answer:
            robot_speaking('Sorry i will try to understand your name. Please try again.')
            voice.runAndWait()


def get_users_emotion():
    spoken_text = mic_error_checking(translate_mic_to_text())
    emotions_dic = {}
    emotions_dic = get_dictionary_from_file('Emotions.txt', emotions_dic)
    for neutral_emotion in emotions_dic['neutral']:
        if neutral_emotion in spoken_text:
            robot_speaking('I see that is good. Better to be just ok rather than sad')
            return 'neutral'
    for positive_emotion in emotions_dic['positive']:
        if positive_emotion in spoken_text:
            robot_speaking('That is great to hear you are feeling positive.')
            return 'positive'
    for negative_emotion in emotions_dic['negative']:
        if negative_emotion in spoken_text:
            robot_speaking('Oh no that is terrible to hear. I am very sorry.')
            return 'negative'


def counting_to_number(user_speech):
    number = int(user_speech[9:])
    print('Going to count to {}'.format(number))
    robot_speaking('Ok here we go.   ')
    for n in range(0, number + 1):
        robot_speaking(str(n))


def compute_expression(user_speech):
    expression_invalid = user_speech[10:]
    expression = (expression_invalid.replace('x', '*').replace('÷', '/').replace('over', '/').
                  replace('squared', '** 2').replace('to the power of', '**').replace('^', '**'))
    evaluation = str(eval(expression))
    robot_speaking('The answer to this problem is.    ' + evaluation)


def get_inspire():
    if using_libraries_test:
        random_number = rnd.randint(1, 10)
        random_file_location = 'Project_images/inspire/' + str(random_number) + '.png'
        im = Image.open(r'{}'.format(random_file_location))
        im.show()
        im.close()
    else:
        print('Sorry unable to get inspirational quote as imported libraries are turned off.')
        print('Here is a joke instead.')
        get_joke()


def get_joke():
    file = open('Project_textFiles/Jokes.txt')
    all_jokes = file.readlines()
    random_joke = all_jokes[rnd.randint(0, 170)]
    robot_speaking('Ok here is a funny joke.  {}'.format(random_joke))
    if 3 == rnd.randint(1, 3):
        robot_speaking('Hahaha I can not believe it that joke was too funny {}!'.format(data['user_name']))


def play_chess():
    tt.speed(0)
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    pieces = {'Pawn': '\u2659',
              'Rook': '\u2656',
              'Knight': '\u2658',
              'Bishop': '\u2657',
              'Queen': '\u2655',
              'King': '\u2654'}

    def initialize_turtle(color):
        tt.shape('turtle')
        tt.color(color)
        tt.pencolor('black')

    def draw_square():
        tt.begin_fill()
        for s in range(4):
            tt.forward(30)
            tt.right(90)
        tt.end_fill()

    def colour_set_square(piece_location):
        x = letters.index(piece_location[:1]) * 30
        y = (int(piece_location[1:]) - 1) * 30
        tt.goto(x, y)
        set_location_colour(x, y)
        tt.pd()
        draw_square()
        tt.pu()

    def set_location_colour(a, b):
        if (a / 30) % 2 != 0 and ((b / 30) % 2 != 0):
            initialize_turtle('grey50')
        elif (a / 30) % 2 == 0 and ((b / 30) % 2 != 0):
            initialize_turtle('green')
        elif (a / 30) % 2 != 0 and ((b / 30) % 2 == 0):
            initialize_turtle('green')
        elif (a / 30) % 2 == 0 and ((b / 30) % 2 == 0):
            initialize_turtle('grey50')

    def increment_direction_dic(piece_location, direction_distance):
        increments = {'forward': [],
                      'backward': [],
                      'left': [],
                      'right': [],
                      'diagonal_north_east': [],
                      'diagonal_south_east': [],
                      'diagonal_south_west': [],
                      'diagonal_north_west': [],
                      }

        for inc_x in range(8):
            if inc_x < letters.index(piece_location[:1]):
                increments['left'].append(str(letters[inc_x]) + piece_location[1:])
                increments['left'].reverse()
            if inc_x > letters.index(piece_location[:1]):
                increments['right'].append(str(letters[inc_x]) + piece_location[1:])

        for inc_y in range(8):
            if inc_y + 1 < int(piece_location[1:]):
                increments['backward'].append(piece_location[:1] + str(inc_y + 1))
                increments['backward'].reverse()
            elif inc_y + 1 > int(piece_location[1:]):
                increments['forward'].append(piece_location[:1] + str(inc_y + 1))

        unit_location = [letters.index(piece_location[:1]), int(piece_location[1:]) - 1]

        while unit_location[0] != 7 and unit_location[1] != 7:
            unit_location[0] += 1
            unit_location[1] += 1
            increments['diagonal_north_east'].append(letters[unit_location[0]] + str(int(unit_location[1]) + 1))
        unit_location = [letters.index(piece_location[:1]), int(piece_location[1:]) - 1]

        while unit_location[0] != 7 and unit_location[1] != 0:
            unit_location[0] += 1
            unit_location[1] -= 1
            increments['diagonal_south_east'].append(letters[unit_location[0]] + str(int(unit_location[1]) + 1))

        unit_location = [letters.index(piece_location[:1]), int(piece_location[1:]) - 1]

        while unit_location[0] != 0 and unit_location[1] != 0:
            unit_location[0] -= 1
            unit_location[1] -= 1
            increments['diagonal_south_west'].append(letters[unit_location[0]] + str(int(unit_location[1]) + 1))

        unit_location = [letters.index(piece_location[:1]), int(piece_location[1:]) - 1]

        while unit_location[0] != 0 and unit_location[1] != 7:
            unit_location[0] -= 1
            unit_location[1] += 1
            increments['diagonal_north_west'].append(letters[unit_location[0]] + str(int(unit_location[1]) + 1))

        return_list = []
        for key in direction_distance:
            if direction_distance[key] == 'MAX':
                for item in increments[key]:
                    if len(increments[key]) != 0:
                        return_list.append(item)
                    else:
                        return_list.append('EMPTY')
            else:
                for index in range(direction_distance[key]):
                    if len(increments[key]) != 0:
                        return_list.append(increments[key][index])
                    else:
                        return_list.append('EMPTY')
        return return_list

    def draw_board():

        def write_letters_numbers():

            for colum in range(8):
                tt.goto(colum * 30 + 10, -60)
                tt.write(letters[colum], font=("Comic Sans MS", 15, "normal"))
                tt.goto(-30, colum * 30 - 25)
                tt.write(str(colum + 1), font=("Comic Sans MS", 15, "normal"))

        def line_row(begin, end):

            for row_number in range(8):

                if row_number % 2 != 0:
                    colour = end
                else:
                    colour = begin

                initialize_turtle(colour)
                draw_square()
                tt.forward(30)

        for colum_number in range(8):
            if colum_number % 2 != 0:
                line_row('green', 'grey50')
            else:
                line_row('grey50', 'green')
            tt.pu()
            tt.goto(0, 30 * colum_number + 30)
            tt.pd()
        tt.pu()
        write_letters_numbers()
        tt.goto(30, 230)
        tt.write('{0} VS {1}'.format(data['user_name'], data['robot_name']), font=("Comic Sans MS", 15, "normal"))
        tt.goto(10, 240)

    def get_possible_moves(piece, colour, piece_location):
        possible_locations = []

        def get_other_colour(switch):
            if colour == 'W' and not switch:
                return 'W'
            elif colour == 'B' and not switch:
                return 'B'
            elif colour == 'W' and switch:
                return 'B'
            elif colour == 'B' and switch:
                return 'W'

        def distance_checking_just_w(direction, distance):

            angle_direction = increment_direction_dic(piece_location, {direction: distance})
            if len(angle_direction) != 0 and angle_direction[0] != 'EMPTY':
                for loc in angle_direction:
                    if board_state[loc][0] == get_other_colour(False):
                        break
                    else:
                        possible_locations.append(loc)

        def distance_checking_both_wb(direction, distance):

            angle_direction = increment_direction_dic(piece_location, {direction: distance})
            if len(angle_direction) != 0 and angle_direction[0] != 'EMPTY':
                for loc in angle_direction:
                    if board_state[loc][0] == get_other_colour(False) or board_state[loc][0] == get_other_colour(True):
                        break
                    else:
                        possible_locations.append(loc)

        def distance_checking_w_one_b(direction, distance):

            angle_direction = increment_direction_dic(piece_location, {direction: distance})

            if len(angle_direction) != 0 and angle_direction[0] != 'EMPTY':
                for loc in angle_direction:
                    if board_state[loc][0] == get_other_colour(False):
                        break
                    elif board_state[loc][0] == get_other_colour(True):
                        possible_locations.append(loc)
                        break
                    else:
                        possible_locations.append(loc)

        def all_horizontal_vertical():

            distance_checking_w_one_b('forward', 'MAX')

            distance_checking_w_one_b('right', 'MAX')

            distance_checking_w_one_b('backward', 'MAX')

            distance_checking_w_one_b('left', 'MAX')

        def all_diagonal():

            distance_checking_w_one_b('diagonal_north_east', 'MAX')

            distance_checking_w_one_b('diagonal_south_east', 'MAX')

            distance_checking_w_one_b('diagonal_south_west', 'MAX')

            distance_checking_w_one_b('diagonal_north_west', 'MAX')

        if piece == 'Pawn' and colour == 'W' and piece_location[1:] == '2':

            north_east = increment_direction_dic(piece_location, {'diagonal_north_east': 1})[0]
            if north_east != 'EMPTY' and board_state[north_east][0] == 'B':
                possible_locations.append(north_east)

            north_west = increment_direction_dic(piece_location, {'diagonal_north_west': 1})[0]
            if north_west != 'EMPTY' and board_state[north_west][0] == 'B':
                possible_locations.append(north_west)

            distance_checking_both_wb('forward', 2)

        elif piece == 'Pawn' and colour == 'W':

            north_east = increment_direction_dic(piece_location, {'diagonal_north_east': 1})[0]
            if north_east != 'EMPTY' and board_state[north_east][0] == 'B':
                possible_locations.append(north_east)

            north_west = increment_direction_dic(piece_location, {'diagonal_north_west': 1})[0]
            if north_west != 'EMPTY' and board_state[north_west][0] == 'B':
                possible_locations.append(north_west)

            distance_checking_both_wb('forward', 1)

        elif piece == 'Pawn' and colour == 'B' and piece_location[1:] == '7':

            south_east = increment_direction_dic(piece_location, {'diagonal_south_east': 1})[0]
            if south_east != 'EMPTY' and board_state[south_east][0] == 'W':
                possible_locations.append(south_east)

            south_west = increment_direction_dic(piece_location, {'diagonal_south_west': 1})[0]
            if south_west != 'EMPTY' and board_state[south_west][0] == 'W':
                possible_locations.append(south_west)

            distance_checking_both_wb('backward', 1)

        elif piece == 'Pawn' and colour == 'B':

            south_east = increment_direction_dic(piece_location, {'diagonal_south_east': 1})[0]
            if south_east != 'EMPTY' and board_state[south_east][0] == 'W':
                possible_locations.append(south_east)

            south_west = increment_direction_dic(piece_location, {'diagonal_south_west': 1})[0]
            if south_west != 'EMPTY' and board_state[south_west][0] == 'W':
                possible_locations.append(south_west)

            distance_checking_both_wb('backward', 1)

        elif piece == 'King':

            distance_checking_just_w('forward', 1)

            distance_checking_just_w('diagonal_north_east', 1)

            distance_checking_just_w('right', 1)

            distance_checking_just_w('diagonal_south_east', 1)

            distance_checking_just_w('backward', 1)

            distance_checking_just_w('diagonal_south_west', 1)

            distance_checking_just_w('left', 1)

            distance_checking_just_w('diagonal_north_west', 1)

        elif piece == 'Rook':

            all_horizontal_vertical()

        elif piece == 'Bishop':

            all_diagonal()

        elif piece == 'Queen':

            all_horizontal_vertical()
            all_diagonal()

        elif piece == 'Knight' and colour == 'W':
            i_location = [letters.index(piece_location[:1]), int(piece_location[1:]) - 1]
            knight_move_list = [[2, 1], [1, 2], [2, -1], [-2, 1], [-2, -1], [-1, -2], [-1, 2], [1, -2]]
            for cords in knight_move_list:
                position = [i_location[0] + cords[0], i_location[1] + cords[1]]
                if 8 > position[0] > -1 and 8 > position[1] > -1:
                    new_location = letters[position[0]] + str(position[1] + 1)
                    if board_state[new_location][0] != 'W':
                        possible_locations.append(new_location)

        return possible_locations

    def board_update(before_copy):

        for key in board_state:
            if key[1:] == '8' and board_state[key] == ['W', 'Pawn']:
                board_state[key] = ['W', 'Queen']
            elif key[1:] == '1' and board_state[key] == ['B', 'Pawn']:
                board_state[key] = ['B', 'Queen']

        if before_copy == 'reset':
            for key in board_state:
                if board_state[key][0] != '':
                    x = letters.index(key[:1]) * 30
                    y = (int(key[1:]) - 1) * 30 - 34
                    tt.goto(x, y)
                    tt.pencolor(str(board_state[key][0]).replace('W', 'white').replace('B', 'black'))
                    uni = pieces[board_state[key][1]]

                    tt.write(uni, font=("Comic Sans MS", 20, "normal"))

            tt.goto(10, 240)
        else:
            for key in board_state:
                if board_state[key][0] != '' and board_state[key] != before_copy[key]:
                    x = letters.index(key[:1]) * 30
                    y = (int(key[1:]) - 1) * 30 - 30
                    tt.goto(x, y)
                    tt.pencolor(str(board_state[key][0]).replace('W', 'white').replace('B', 'black'))
                    uni = pieces[board_state[key][1]]

                    tt.write(uni, font=("Verdana", 20, "normal"))

            tt.goto(10, 240)

    def create_copy():
        global copy
        for key in board_state:
            copy[key] = board_state[key]

    def computer_moves(given_start_location='NONE', given_end_location='NONE'):
        all_black_locations = []
        for key in board_state:
            if board_state[key][0] == 'B':
                all_black_locations.append(key)
        if given_start_location == 'NONE':
            random_location = rnd.choice(all_black_locations)
        else:
            random_location = given_start_location

        random_piece = board_state[random_location][1]

        if given_end_location == 'NONE':
            all_possible_moves = get_possible_moves(random_piece, 'B', random_location)
        else:
            all_possible_moves = [given_end_location]

        if len(all_possible_moves) != 0:

            create_copy()
            move_location = rnd.choice(all_possible_moves)
            robot_speaking('I am going to move ' + random_location + ' to ' + move_location)
            colour_set_square(random_location)
            board_state[random_location] = ['']
            colour_set_square(move_location)
            board_state[move_location] = ['B', random_piece]
            board_update(copy)

        else:
            computer_moves()
            return

    def make_a_move(user_input):
        print(user_input, len(user_input))

        if using_libraries_test:
            initialize_text_to_speech(1.0, 250)

        create_copy()
        absent_alphabet = ['I', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'U', 'V', 'X', 'Y', 'Z', 'i',
                           'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 'u', 'v', 'x', 'y', 'z']

        new_user_string = user_input.replace('alpha ', 'A').replace('bravo ', 'B'). \
            replace('charlie ', 'C').replace('delta ', 'D').replace('echo ', 'E'). \
            replace('foxtrot ', 'F').replace('golf ', 'G').replace('hotel ', 'H'). \
            replace('Alpha ', 'A').replace('Bravo ', 'B'). \
            replace('Charlie ', 'C').replace('Delta ', 'D').replace('Echo ', 'E'). \
            replace('Foxtrot ', 'F').replace('Golf ', 'G').replace('Hotel ', 'H'). \
            replace('for', '4').replace('12', '1 to').replace('22', '2 to').replace('32', '3 to'). \
            replace('42', '4 to').replace('52', '5 to').replace('62', '6 to').replace('72', '7 to'). \
            replace('82', '8 to')

        print(new_user_string, len(new_user_string))

        replaced_input = new_user_string.replace('12', '1 to').replace('22', '2 to').replace('32', '3 to'). \
            replace('42', '4 to').replace('52', '5 to').replace('62', '6 to').replace('72', '7 to'). \
            replace('82', '8 to').replace('fh', 'F').replace('c', 'C')

        print(replaced_input, len(replaced_input))

        start_location = replaced_input[:2]
        end_location = replaced_input[6:]
        print(end_location)

        if len(replaced_input) == 8 and not any(x in user_input for x in absent_alphabet):
            if board_state[start_location][0] == 'W':
                piece_user_wants_to_move = board_state[start_location][1]
                print(piece_user_wants_to_move)
                all_possible_moves = get_possible_moves(piece_user_wants_to_move, 'W', start_location)
                print(all_possible_moves)

                if end_location in all_possible_moves:
                    colour_set_square(start_location)
                    board_state[start_location] = ['']
                    colour_set_square(end_location)
                    board_state[end_location] = ['W', piece_user_wants_to_move]
                    board_update(copy)
                else:
                    robot_speaking('This is an illegal move. Please try again:')
                    make_a_move(mic_error_checking(translate_mic_to_text()))

            else:
                robot_speaking('Piece is either not your colour or not a piece at all. Please try again:')
                make_a_move(mic_error_checking(translate_mic_to_text()))
        else:
            robot_speaking('Try again:')
            make_a_move(mic_error_checking(translate_mic_to_text()))

    def look_for_check_position():
        all_white_locations = []
        w_found = False
        for key in board_state:
            if board_state[key][0] == 'W' and board_state[key][1] == 'King':
                w_found = True
                all_white_locations.append(key)
            elif board_state[key][0] == 'W':
                all_white_locations.append(key)

        all_black_locations = []
        b_found = False
        for key in board_state:
            if board_state[key][0] == 'B' and board_state[key][1] == 'King':
                b_found = True
                all_black_locations.append(key)
            elif board_state[key][0] == 'B':
                all_black_locations.append(key)

        if not w_found:
            print('White in checkmate, I win!')
            return 'B'

        if not b_found:
            print('Black in checkmate, You win!')
            return 'W'

        all_w_moves = []
        for each in all_white_locations:
            all_w_moves = get_possible_moves(board_state[each][1], 'W', each)

        all_b_moves = []
        for each in all_black_locations:
            all_b_moves = get_possible_moves(board_state[each][1], 'B', each)

        count = 0
        for move_w in all_w_moves:
            if board_state[move_w][0] == 'B' and board_state[move_w][1] == 'King':
                b_kings_moves = get_possible_moves(board_state[move_w][1], 'B', move_w)
                for b_k in b_kings_moves:
                    if b_k in all_w_moves:
                        count += 1
                if count == len(b_kings_moves) and move_w not in all_b_moves:
                    robot_speaking('Black in checkmate, You win!')
                    return 'W'
                else:
                    robot_speaking('Black in Check')
                    global Computer_get_out_of_check

                    for b_k in b_kings_moves:
                        if b_k not in all_w_moves:
                            Computer_get_out_of_check = [move_w, b_k]
                            return ''

                    for each in all_black_locations:
                        protection_moves = get_possible_moves(board_state[each][1], 'B', each)
                        for protection_move in protection_moves:
                            if move_w == protection_move:
                                Computer_get_out_of_check = [each, protection_moves]
                                return ''

        count = 0
        for move_b in all_b_moves:
            if board_state[move_b][0] == 'W' and board_state[move_b][1] == 'King':
                w_kings_moves = get_possible_moves(board_state[move_b][1], 'W', move_b)
                for w_k in w_kings_moves:
                    if w_k in all_b_moves:
                        count += 1
                if count == len(w_kings_moves) and move_b not in all_w_moves:
                    robot_speaking('White in checkmate, I win!')
                    return 'B'
                else:
                    robot_speaking('White in Check')
                    return ''
        return ''

    draw_board()
    robot_speaking('Lets play. You go first.')
    board_state = {}
    win = ''
    global Computer_get_out_of_check
    board_state = get_dictionary_from_file('Chess.txt', board_state)
    print(board_state)
    board_update('reset')

    while win == '':
        win = look_for_check_position()
        print(win)

        robot_speaking('Your move!')
        make_a_move(mic_error_checking(translate_mic_to_text()))

        win = look_for_check_position()

        if len(Computer_get_out_of_check) == 0 and win == '':
            computer_moves()
        elif win == '':
            computer_moves(Computer_get_out_of_check[0], Computer_get_out_of_check[1])
            Computer_get_out_of_check = []
        else:
            robot_speaking('Well done {}! Click on the chess board to continue.'.format(data['user_name']))

    tt.exitonclick()


def initialize_introduction():
    func_data = {'robot_name': get_random_name(), 'user_name': None, 'user_feeling': None}

    robot_speaking('Hello my name is {}. What is your name?'.format(func_data['robot_name']))

    func_data['user_name'] = get_your_name()

    robot_speaking('Good to meet you {}. How are you?'.format(func_data['user_name']))

    func_data['user_feeling'] = get_users_emotion()

    robot_speaking('As a program I do not have emotions like you. This is because I can not feel. '
                   'However I can perform tasks. '
                   'Such as doing calculations and organising data. '
                   'What would you like me to do?')

    return func_data


def check_commands():
    while True:
        robot_speaking('What is the next command you would like me to perform?')
        command_spoken = mic_error_checking(translate_mic_to_text())
        cmd_dic = {}
        cmd_dic = get_dictionary_from_file('Commands.txt', cmd_dic)
        for word_counting in cmd_dic['count']:
            if word_counting in command_spoken:
                counting_to_number(command_spoken)
                break
        for word_cal in cmd_dic['calculate']:
            if word_cal in command_spoken:
                compute_expression(command_spoken)
                break
        for word_off in cmd_dic['powerDown']:
            if word_off in command_spoken:
                return
        for word_inspire in cmd_dic['inspireQuotes']:
            if word_inspire in command_spoken:
                get_inspire()
                break
        for word_joke in cmd_dic['joke']:
            if word_joke in command_spoken:
                get_joke()
                break
        for word_chess in cmd_dic['chess']:
            if word_chess in command_spoken:
                play_chess()
                if using_libraries_test:
                    initialize_text_to_speech(1.0, 175)
                break


if __name__ == '__main__':

    if using_libraries_test:
        initialize_text_to_speech(1.0, 175)

    data = initialize_introduction()
    check_commands()

    robot_speaking('Good bye ' + data['user_name'] + '!')

    if using_libraries_test:
        voice.stop()
