import logging

# Jaro-Winkler distance function
def jaro_winkler(s1, s2):
    # Calculate the Jaro distance
    def jaro_distance(s1, s2):
        if s1 == s2:
            return 1.0

        len_s1, len_s2 = len(s1), len(s2)
        max_dist = max(len_s1, len_s2) // 2 - 1
        match = 0

        # Flags to mark matches
        s1_matches = [False] * len_s1
        s2_matches = [False] * len_s2

        # Count matches
        for i in range(len_s1):
            start = max(0, i - max_dist)
            end = min(i + max_dist + 1, len_s2)
            for j in range(start, end):
                if s1[i] == s2[j] and not s2_matches[j]:
                    s1_matches[i] = True
                    s2_matches[j] = True
                    match += 1
                    break

        if match == 0:
            return 0.0

        # Count transpositions
        t = 0
        point = 0
        for i in range(len_s1):
            if s1_matches[i]:
                while not s2_matches[point]:
                    point += 1
                if s1[i] != s2[point]:
                    t += 1
                point += 1
        t /= 2

        # Jaro distance formula
        return (match / len_s1 + match / len_s2 + (match - t) / match) / 3.0

    # Apply the Jaro-Winkler adjustment
    jaro_dist = jaro_distance(s1, s2)
    prefix = 0
    max_prefix_length = 4  # Maximum length of common prefix
    for i in range(min(len(s1), len(s2))):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break
        if prefix == max_prefix_length:
            break

    # Jaro-Winkler formula
    winkler_adjustment = 0.1 * prefix * (1 - jaro_dist)
    return jaro_dist + winkler_adjustment

# Function to suggest a similar word from the list
def suggest_similar_word(input_word, word_list, threshold=0.8):
    suggestions = [(word, jaro_winkler(input_word, word)) for word in word_list]
    # Filter out suggestions below the threshold
    suggestions = [s for s in suggestions if s[1] >= threshold]
    # Sort by similarity score in descending order
    suggestions.sort(key=lambda x: x[1], reverse=True)
    return suggestions[0][0] if suggestions else None

# Main interaction function
def interact_and_update_list(input_word, word_list):
    # Check for an exact match first
    if input_word in word_list:
        print(f"The word '{input_word}' is already in the list.")
        return

    # Get the suggestion if no exact match is found
    suggested_word = suggest_similar_word(input_word, word_list)
    if suggested_word:
        print(f"Did you mean '{suggested_word}'? (yes/no): ")
        user_response = input().strip().lower()
        if user_response == 'yes':
            print(f"Great! '{input_word}' will be treated as '{suggested_word}' for future suggestions.")
            return
        else:
            print(f"Okay, you chose not to use the suggestion. Would you like to add '{input_word}' to the list? (yes/no): ")
            user_response = input().strip().lower()
            if user_response == 'yes':
                word_list.append(input_word)
                print(f"Word '{input_word}' has been added to the list.")
            else:
                print(f"No changes have been made to the list.")
    else:
        print(f"No similar words found for '{input_word}'.")
        print("Would you like to add it to the list? (yes/no): ")
        user_response = input().strip().lower()
        if user_response == 'yes':
            word_list.append(input_word)
            print(f"Word '{input_word}' has been added to the list.")
        else:
            print("No changes have been made to the list.")

# Predefined list of words
word_list = ["apple", "application", "appetizer", "phone", "iphonex", "iphone", "app", "application"]

# Get user input
user_input = input("Enter a word: ").strip().lower()

# Suggest a similar word and possibly update the list
interact_and_update_list(user_input, word_list)