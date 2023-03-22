#!/opt/homebrew/bin/python3

import sys
import time
import random
import argparse

NUM_STRINGS = 6
STRING_NAMES = ['e', 'B', 'G', 'D', 'A', 'E']
THICK_STRINGS = ['E','A','D']
NOTE_ORDER = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
NOTE_ORDER_FLATS = ['Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D','Eb', 'E', 'F', 'Gb', 'G']

def get_answer(user_in):
    notes = user_in.split(' ')[:NUM_STRINGS]
    return [f'{n[0].upper()}{n[1:]}' if len(n) > 1 and n[1] == 'b' else n.upper() for n in notes]
    
def draw_string(string_name, fret):
    line = f'{("=" if string_name in THICK_STRINGS else "-") * 11}'
    return f'{string_name} {line}  {fret} {line}*'
    
def draw_string_answer(string_name, note):
    line = f'{("=" if string_name in THICK_STRINGS else "-") * 11}'
    return f'{string_name} {line}  {note} {line}*'

def draw_string_result(string_name, note, result):
    line = f'{("=" if string_name in THICK_STRINGS else "-") * 11}'
    check = '✓' if result else 'X'
    note_str = f' {note}' if len(note) == 1 else f'{note}'
    return f'{string_name} {line}  {note_str} {check} {line}*'

def draw_riddle(frets):
    fret_strs = [f' {fret}' if fret < 10 else f'{fret}' for fret in frets]
    guitar_strings = [draw_string(string_name, fret) for string_name, fret in zip(STRING_NAMES, fret_strs)]
    print('\n'.join(guitar_strings))

def draw_answer(answer):
    notes = []
    for note in answer:
        if is_sharp(note):
            notes.append(f'{note}/{sharp_to_flat(note)}')
        elif is_flat(note):
            notes.append(f'{note}/{flat_to_sharp(note)}')
        else:
            notes.append(note)

    note_strs = [f'  {note}  ' if len(note) == 1 else f'{note}' for note in notes]
    guitar_strings = [draw_string(STRING_NAMES[i], note_strs[i]) for i in range(len(answer))]
    print('\n'.join(guitar_strings))

def draw_result(result, answer, correct_answer):
    print('\nYour answer is:')
    # print(f'result={result}, answer={answer}, correct_answer={correct_answer}')
    notes = [correct_answer[i] if result[i] else answer[i] for i in range(len(result))]
    note_strs = [f'{note} ' if len(note) == 1 else f'{note}' for note in notes]
    guitar_strings = [draw_string_result(STRING_NAMES[i], note_strs[i], result[i]) for i in range(len(result))]
    print('\n'.join(guitar_strings))

def get_correct_answer(frets):
    return [get_note(string_index, fret) for string_index, fret in enumerate(frets)]

def check_answer(answer, frets):
    print(f'\nEvaluating answer: {" ".join(answer)}...')
    time.sleep(1)
    return [check_single_note(string_index, frets[string_index], note_answer) for string_index, note_answer in enumerate(answer[:NUM_STRINGS])]
    
def check_single_note(string_index, fret, note_answer):
    correct_note = get_note(string_index, fret)
    if (correct_note == note_answer):
        return True
    if 'b' in note_answer:
        note_order = get_note_order(note_answer)
        sharp = NOTE_ORDER[note_order - 1]
        return sharp == correct_note
    return False

def flat_to_sharp(flat):
    note_order = get_note_order(flat)
    return NOTE_ORDER[note_order - 1]

def sharp_to_flat(sharp):
    note_order = get_note_order(sharp)
    return NOTE_ORDER_FLATS[( note_order + 1 ) % len(NOTE_ORDER_FLATS)]

def is_flat(note):
    return 'b' in note

def is_sharp(note):
    return '#' in note

def get_note(string_index, fret):
    string_name = STRING_NAMES[string_index]
    base_note_index = get_note_order(string_name.upper())
    return NOTE_ORDER[(base_note_index + fret) % len(NOTE_ORDER)]

def get_note_order(note):
    if (note in NOTE_ORDER):
        return NOTE_ORDER.index(note)
    if (note in NOTE_ORDER_FLATS):
        return NOTE_ORDER_FLATS.index(note)
    raise ValueError(f'Invalid note {note}')

def run_game(args):
    frets = list(range(0,args.neck_length + 1))
    sample = random.sample(frets, NUM_STRINGS)
    draw_riddle(sample)

    user_in = input('Enter the names of all notes separated by spaces: ')
    answer = get_answer(user_in)
    try:
        result = check_answer(answer, sample)
    except ValueError as e:
        print('Something went wrong: ', e)
        exit(1)
    is_answer_correct = all(result)
    correct_answer = get_correct_answer(sample)
    if (is_answer_correct):
        print('You Are Correct!')
    else:
        print('\nWrong! the correct answer is:')
        draw_answer(correct_answer)
    draw_result(result, answer, correct_answer)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sharps', action='store_true')
    parser.add_argument('-flats', action='store_true')
    parser.add_argument('--neck-length', type=int, action='store', default=12)
    return  parser.parse_args()

def main():
    args = get_args()
    user_choice = None
    while user_choice != 'q':
        run_game(args)
        user_choice = input('\nfor more press "RETURN", to exit enter "q": ')

if __name__ == '__main__':
    main()
