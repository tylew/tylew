def filter_story_words(story_file, words_file, output_file):
    # Read the list of words from the words file
    with open(words_file, 'r') as file:
        words_list = file.read().splitlines()
    
    # Create a set for faster lookup
    words_set = set(words_list)

    # Read the story from the story file
    with open(story_file, 'r') as file:
        story_words = file.read().lower().split()
    
    # Filter the words from the story that are in the words list
    filtered_words = [word for word in story_words if word in words_set]
    
    # Sort the filtered words based on their order in the words list
    sorted_filtered_words = sorted(filtered_words, key=lambda word: words_list.index(word))
    
    # Write the filtered and sorted words to the output file
    with open(output_file, 'w') as file:
        for word in sorted_filtered_words:
            file.write(word + '\n')

# Example usage
filter_story_words('story.txt', 'bip39_word_list.txt', 'filtered_story_words.txt')
