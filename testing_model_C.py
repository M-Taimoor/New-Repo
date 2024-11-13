import logging

# Define the Jaro-Winkler distance function
def jaro_winkler(s1, s2):
    # ... (Jaro-Winkler function code from previous snippets goes here)
    # Example implementation (ensure you include the full function code as well)
    def jaro_distance(s1, s2):
        # ... (Jaro distance sub-function code)
        pass

    # Step 1: Calculate the Jaro distance using the sub-function
    jaro_dist = jaro_distance(s1, s2)
    
    # Step 2: Apply the Jaro-Winkler adjustment
    prefix = 0
    max_prefix_length = 4
    for i in range(min(len(s1), len(s2))):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break
        if prefix == max_prefix_length:
            break
    winkler_adjustment = 0.1 * prefix * (1 - jaro_dist)

    # Return the Jaro-Winkler distance
    return jaro_dist + winkler_adjustment

# Function to suggest a similar word from the list
def suggest_similar_word(input_word, word_list, threshold=0.8):
    # Filter out suggestions below the threshold
    suggestions = [(word, jaro_winkler(input_word, word)) for word in word_list]
    # Sort by similarity score in descending order
    suggestions.sort(key=lambda x: x[1], reverse=True)
    # Get the most similar word if it exists above the threshold
    return suggestions[0][0] if suggestions and suggestions[0][1] >= threshold else None

# Function to interact with the user and update the word list if necessary
def interact_and_update_list(input_word, word_list):
    # Check if the input word matches any word in the list
    if input_word in word_list:
        print(f"The word '{input_word}' is in the list.")
        return
    # Suggest a similar word from the list
    suggested_word = suggest_similar_word(input_word, word_list)
    if suggested_word:
        print(f"Did you mean '{suggested_word}'? (yes/no): ", end="")
        user_response = input().strip().lower()
        if user_response == 'yes':
            print(f"Great! Using '{suggested_word}' as the correct word.")
        else:
            print("No similar word found.")
    else:
        # Ask the user if they want to add the new word to the list
        print(f"No similar word found. Would you like to add '{input_word}' to the list for future suggestions? (yes/no): ", end="")
        add_word_response = input().strip().lower()
        if add_word_response == 'yes':
            word_list.append(input_word)
            print(f"Word '{input_word}' added to the list.")
            # Save the updated list to a file (optional)
            with open('word_list.txt', 'w') as file:
                file.writelines(f"{word}\n" for word in word_list)
            print("The word list has been updated.")

# Main program loop to interact with the user
if __name__ == "__main__":
    word_list = ["apple", "application", "appetizer", "phone", "iphonex", "iphone", "app", "application"]
    while True:
        user_input = input("Enter a word (or type 'exit' to quit): ").strip().lower()
        if user_input == 'exit':
            break
        interact_and_update_list(user_input, word_list)