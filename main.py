"""Solver for LetterBoxed game"""
from typing import Set, List, Tuple


def load_word_set() -> Set:
    """Returns a set of words > 3 letters from words.txt file"""
    words = set()
    with open("words.txt", "r", encoding="utf-8") as file:
        for line in file:
            if len(line.strip()) >= 3 and line.strip().isalpha():
                words.add(line.lower().strip())
    return words


def get_puzzle_setup() -> List[List[str]]:
    """Returns a list of lists representing the puzzle"""
    sides = []
    response = input("Enter the puzzle layout (ex: 'abc,def,ghi,jkl'): ")
    for side in response.split(","):
        sides.append([letter for letter in side])
    return sides


def filter_possible_words(puzzle_layout: List[List[str]], word_set: Set) -> List[str]:
    """Returns a list of words that are possible based on the puzzle layout"""
    possible_words = []

    all_letters = [letter for side in puzzle_layout for letter in side]

    for word in word_set:
        if not all(letter.lower() in all_letters for letter in word):
            continue
        word_letters = list(word)
        for i, letter in enumerate(word_letters):
            letter_options = []
            current_letter = letter
            if i == len(word_letters) - 1:
                possible_words.append(word)
                continue
            letter_options = [
                letter
                for side in puzzle_layout
                if current_letter not in side
                for letter in side
            ]
            if word_letters[i + 1] not in letter_options:
                break
    return possible_words


def select_next_word(
    possible_words: List[str], unused_letters: List[str], starting_letter: str
) -> Tuple[str, List[str]]:
    """Returns the next word to be used"""
    if starting_letter == "":
        word_choices = possible_words
    else:
        word_choices = [word for word in possible_words if word[0:1] == starting_letter]
    # Checks if there is a word that uses all the remaining letters (1 word solution)
    for word in word_choices:
        if all(letter in word for letter in unused_letters):
            return word, []

    # Checks if there is a word that leaves unused letters another word can use (2 word solution)
    for word in word_choices:
        remaining_letters = [letter for letter in unused_letters if letter not in word]
        new_word_choices = [
            new_word for new_word in possible_words if new_word[0:1] == word[-1:]
        ]
        for new_word in new_word_choices:
            if all(letter in new_word for letter in remaining_letters):
                return word, remaining_letters

    # Picks the word that uses the most unused letters
    max_tracker = 0
    for word in word_choices:
        val = sum(letter in word for letter in unused_letters)
        if val > max_tracker:
            max_tracker = val
            selected_word = word
        if val == max_tracker:
            if len(word) < len(selected_word):
                selected_word = word
    return selected_word, [
        letter for letter in unused_letters if letter not in selected_word
    ]


def find_solution(puzzle_layout: List[List[str]], word_set: Set) -> List[str]:
    """Returns a list of words that solve the puzzle"""
    unused_letters = [letter for side in puzzle_layout for letter in side]

    possible_words = filter_possible_words(
        puzzle_layout=puzzle_layout, word_set=word_set
    )

    # if all([letter in unused_letters for letter in word]):
    #     possible_words.append(word)
    solution_words = []
    selected_word = None
    starting_letter = ""
    while len(unused_letters) != 0:
        selected_word, unused_letters = select_next_word(
            possible_words=possible_words,
            unused_letters=unused_letters,
            starting_letter=starting_letter,
        )
        solution_words.append(selected_word)
        starting_letter = selected_word[-1:]

    return solution_words


def remove_problem_word(word: str) -> None:
    """Removes a word from the word list"""
    with open("words.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    with open("words.txt", "w", encoding="utf-8") as file:
        for line in lines:
            if line.lower().strip() != word.lower():
                file.write(line)


if __name__ == "__main__":
    puzzle_layout_input = get_puzzle_setup()
    while True:
        full_word_set = load_word_set()
        solution = find_solution(puzzle_layout_input, full_word_set)
        print("\nTo Solve:\n" + " -> ".join(word.upper() for word in solution))
        if (
            input(
                "\nPress Enter to Exit, Enter '1' if there is an issue with the solution: "
            )
            == "1"
        ):
            for index, solution_word in enumerate(solution):
                print(f"{index+1}: {solution_word.upper()}")
            problem_word = input("Which word is the issue? Enter the number: ")
            remove_problem_word(solution[int(problem_word) - 1])
        else:
            print("Thanks for using the solver!")
            break
