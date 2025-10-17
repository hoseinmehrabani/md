def search_in_text(text, keyword):
    occurrences = []
    index = text.lower().find(keyword.lower())

    while index != -1:
        occurrences.append((index, text[index:index + len(keyword)]))
        index = text.lower().find(keyword.lower(), index + 1)

    return occurrences


def main():
    file_name = input("Please enter the name of the text file (with the extension .txt): ")

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print("File not found. Please enter the correct file name.")
        return

    keyword = input("Please enter the keyword you want to search for: ")

    occurrences = search_in_text(text, keyword)

    if occurrences:
        print(f"Found {len(occurrences)} occurrences of the word '{keyword}':")
        for index, word in occurrences:
            print(f"Word '{word}' found at index {index}.")
        output_file_name = "search_results.txt"
        with open(output_file_name, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Occurrences of the word '{keyword}':\n")
            for index, word in occurrences:
                output_file.write(f"Word '{word}' found at index {index}.\n")

        print(f"Results saved to {output_file_name}.")
    else:
        print(f"The word '{keyword}' was not found in the text.")


if __name__ == "__main__":
    main()
