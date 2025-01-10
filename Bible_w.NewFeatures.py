import os
import json
import random
import tkinter as tk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tkinter import Toplevel, Scrollbar, Button, Label, Text, OptionMenu, StringVar, messagebox

# Ordered list of Old Testament and New Testament books
OLD_TESTAMENT = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges",
    "Ruth", "1Samuel", "2Samuel", "1Kings", "2Kings", "1Chronicles", "2Chronicles",
    "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "SongofSolomon",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"
]

NEW_TESTAMENT = [
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1Corinthians", "2Corinthians",
    "Galatians", "Ephesians", "Philippians", "Colossians", "1Thessalonians", "2Thessalonians",
    "1Timothy", "2Timothy", "Titus", "Philemon", "Hebrews", "James", "1Peter", "2Peter",
    "1John", "2John", "3John", "Jude", "Revelation"
]

ALL_BOOKS = OLD_TESTAMENT + NEW_TESTAMENT

def show_about():
    """
    Display information about the author and application.
    """
    messagebox.showinfo(
        "About Bible Viewer",
        "Bible Viewer Application\n\n"
        "Author: @o5341V\n"
        "Date: January 2025\n\n"
        "A Python application for browsing, searching, and analyzing the Bible."
    )

def load_bible(folder_path):
    """
    Load all Bible books from JSON files in the specified folder.
    """
    bible = {}
    try:
        for book in ALL_BOOKS:
            file_name = f"{book}.json"
            file_path = os.path.join(folder_path, file_name)
            if os.path.exists(file_path):  # Check if the file exists
                with open(file_path, 'r', encoding='utf-8') as file:
                    bible[book] = json.load(file)
        print("Bible successfully loaded!")
    except Exception as e:
        print(f"Error: {e}")
    return bible

def get_random_verse(bible):
    """
    Get a random verse from the entire Bible.
    """
    book = random.choice(list(bible.keys()))  # Random book
    chapters = bible[book].get("chapters", [])
    chapter_data = random.choice(chapters)  # Random chapter
    chapter = chapter_data["chapter"]
    verses = chapter_data.get("verses", [])
    verse_data = random.choice(verses)  # Random verse
    verse_num = verse_data["verse"]
    verse_text = verse_data["text"]
    return book, chapter, verse_num, verse_text

def show_random_verse():
    """
    Display a random Bible verse in a pop-up window.
    """
    book, chapter, verse_num, verse_text = get_random_verse(bible)
    verse_display = f"{book} {chapter}:{verse_num}\n\n{verse_text}"
    messagebox.showinfo("Random Bible Verse", verse_display)

def contents_gui():
    """
    Open a standalone window showing all books divided by Old and New Testaments.
    """
    contents_window = Toplevel(root)
    contents_window.title("Contents")
    contents_window.geometry("400x600")

    canvas = tk.Canvas(contents_window)
    scrollbar = Scrollbar(contents_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((200, 0), window=scrollable_frame, anchor="n")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add Old Testament books
    Label(scrollable_frame, text="Old Testament", font=("Arial", 14, "bold")).pack(pady=10)
    for book in OLD_TESTAMENT:
        Button(
            scrollable_frame,
            text=book,
            command=lambda b=book: read_bible_gui(book=b),
            font=("Arial", 12),
            width=20
        ).pack(pady=2)

    # Add New Testament books
    Label(scrollable_frame, text="New Testament", font=("Arial", 14, "bold")).pack(pady=10)
    for book in NEW_TESTAMENT:
        Button(
            scrollable_frame,
            text=book,
            command=lambda b=book: read_bible_gui(book=b),
            font=("Arial", 12),
            width=20
        ).pack(pady=2)

def search_bible_gui():
    """
    Open a search window to input the keyword/phrase.
    Results are shown in a separate window with stats.
    """
    def perform_search():
        """
        Perform the search and display results in a new window.
        """
        keyword = search_entry.get().strip().lower()
        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword or phrase to search.")
            return

        # Perform the search
        matches = []
        books_with_matches = set()
        chapters_with_matches = set()
        verse_frequencies = {}

        for book, content in bible.items():
            for chapter_data in content.get("chapters", []):
                chapter = chapter_data["chapter"]
                for verse in chapter_data.get("verses", []):
                    verse_text = verse["text"]
                    if keyword in verse_text.lower():  # Check if keyword is in the verse text
                        matches.append(f"{book} {chapter}:{verse['verse']} - {verse_text}")
                        books_with_matches.add(book)
                        chapters_with_matches.add((book, chapter))
                        verse_frequencies[book] = verse_frequencies.get(book, 0) + 1

        # Display results in a new window
        show_results_window(keyword, matches, books_with_matches, chapters_with_matches, verse_frequencies)

    def show_results_window(keyword, matches, books_with_matches, chapters_with_matches, verse_frequencies):
        """
        Display the search results in a new pop-up window with stats.
        """
        results_window = Toplevel(root)
        results_window.title(f"Search Results for '{keyword}'")
        results_window.geometry("700x500")

        # Stats section
        stats_frame = tk.Frame(results_window)
        stats_frame.pack(fill=tk.X, pady=10)

        Label(stats_frame, text=f"Search Term: '{keyword}'", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
        Label(stats_frame, text=f"Total Matches: {len(matches)}", font=("Arial", 12)).pack(anchor="w", padx=10)
        Label(stats_frame, text=f"Books with Matches: {len(books_with_matches)}", font=("Arial", 12)).pack(anchor="w", padx=10)
        Label(stats_frame, text=f"Chapters with Matches: {len(chapters_with_matches)}", font=("Arial", 12)).pack(anchor="w", padx=10)

        # Cross-references (Top 5 Books with Most Matches)
        Label(stats_frame, text="Top Books with Matches:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)
        sorted_books = sorted(verse_frequencies.items(), key=lambda x: x[1], reverse=True)
        for book, count in sorted_books[:5]:
            Label(stats_frame, text=f"{book}: {count} matches", font=("Arial", 12)).pack(anchor="w", padx=20)

        # Results section
        results_frame = tk.Frame(results_window)
        results_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        results_text = Text(results_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        results_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=results_text.yview)

        # Display matches with highlighting
        for match in matches:
            start_idx = results_text.index(tk.END)
            results_text.insert(tk.END, match + "\n\n")
            end_idx = results_text.index(tk.END)
            highlight_text(results_text, keyword, start_idx, end_idx)

        results_text.tag_config("highlight", background="yellow", foreground="black")

        if not matches:
            results_text.insert(tk.END, "No matches found.")

    def highlight_text(widget, keyword, start_idx, end_idx):
        """
        Highlight the searched keyword in the Text widget.
        """
        idx = start_idx
        while True:
            idx = widget.search(keyword, idx, stopindex=end_idx, nocase=True)
            if not idx:
                break
            widget.tag_add("highlight", idx, f"{idx}+{len(keyword)}c")
            idx = f"{idx}+{len(keyword)}c"

    # Create the search window
    search_window = Toplevel(root)
    search_window.title("Search the Bible")
    search_window.geometry("400x200")

    Label(search_window, text="Enter keyword/phrase:", font=("Arial", 14)).pack(pady=10)
    search_entry = tk.Entry(search_window, font=("Arial", 14), width=30)
    search_entry.pack(pady=10)

    search_button = Button(search_window, text="Search", font=("Arial", 14), command=perform_search)
    search_button.pack(pady=10)

def read_bible_gui(book=None):
    """
    Open a new window to display the selected book of the Bible with a dropdown for book navigation.
    """
    def display_chapter():
        text_box.delete(1.0, tk.END)
        chapters = book_content.get("chapters", [])
        if not chapters:
            text_box.insert(tk.END, "This book has no chapters.", "error")
            return

        chapter_data = chapters[current_chapter.get() - 1]
        chapter = chapter_data["chapter"]
        text_box.insert(tk.END, f"Chapter {chapter}\n\n", "chapter_header")
        for verse in chapter_data.get("verses", []):
            first_word, rest_of_text = verse["text"].split(" ", 1)
            text_box.insert(tk.END, f"{verse['verse']} ", "verse_number")
            text_box.insert(tk.END, f"{first_word} ", "first_word")
            text_box.insert(tk.END, f"{rest_of_text}\n")

    def next_chapter():
        if current_chapter.get() < len(book_content.get("chapters", [])):
            current_chapter.set(current_chapter.get() + 1)
            display_chapter()

    def previous_chapter():
        if current_chapter.get() > 1:
            current_chapter.set(current_chapter.get() - 1)
            display_chapter()

    def change_book(selected_book):
        nonlocal book_content
        nonlocal current_chapter
        book_content = bible.get(selected_book, {})
        current_chapter.set(1)
        display_chapter()

    read_window = Toplevel(root)
    read_window.title("Read the Bible")
    read_window.geometry("600x600")

    book_content = bible.get(book, {})
    current_chapter = tk.IntVar(value=1)

    top_frame = tk.Frame(read_window)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    # Dropdown for selecting a book
    selected_book = StringVar(read_window)
    selected_book.set(book or ALL_BOOKS[0])  # Default to the selected or first book
    book_dropdown = OptionMenu(top_frame, selected_book, *ALL_BOOKS, command=change_book)
    book_dropdown.pack(side=tk.LEFT, padx=10, pady=5)

    Button(top_frame, text="CloseWindow", command=read_window.destroy, font=("Arial", 10)).pack(side=tk.RIGHT, padx=10, pady=5)

    navigation_frame = tk.Frame(read_window)
    navigation_frame.pack(side=tk.TOP, fill=tk.X)

    Button(navigation_frame, text="Previous Chapter", command=previous_chapter, font=("Arial", 10)).pack(side=tk.LEFT, padx=10, pady=10)
    Button(navigation_frame, text="Next Chapter", command=next_chapter, font=("Arial", 10)).pack(side=tk.RIGHT, padx=10, pady=10)

    scrollbar = Scrollbar(read_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_box = Text(read_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text_box.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=text_box.yview)

    # Configure text formatting
    text_box.tag_config("chapter_header", font=("Arial", 14, "bold"))
    text_box.tag_config("verse_number", font=("Arial", 10, "bold"))
    text_box.tag_config("first_word", font=("Arial", 10, "bold"))
    text_box.tag_config("error", foreground="red", font=("Arial", 12, "italic"))

    display_chapter()

def generate_word_cloud(text, max_words):
    """
    Generate and display a word cloud from the given text.
    """
    wordcloud = WordCloud(
        width=800, height=400,
        max_words=max_words,
        background_color="white",
        colormap="viridis"
    ).generate(text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Word Cloud (Top {max_words} Words)", fontsize=16)
    plt.show()

def word_cloud_gui():
    """
    Open a GUI window to allow users to generate a word cloud.
    """
    def perform_word_cloud():
        max_words = int(max_words_var.get())
        selected_book = book_var.get()

        if selected_book == "Entire Bible":
            # Combine text from all books
            combined_text = " ".join(
                verse["text"] for book_content in bible.values()
                for chapter in book_content.get("chapters", [])
                for verse in chapter.get("verses", [])
            )
            generate_word_cloud(combined_text, max_words)
        else:
            # Generate for a specific book
            book_content = bible.get(selected_book, {})
            if not book_content:
                messagebox.showerror("Error", f"The book '{selected_book}' is unavailable.")
                return
            combined_text = " ".join(
                verse["text"] for chapter in book_content.get("chapters", [])
                for verse in chapter.get("verses", [])
            )
            generate_word_cloud(combined_text, max_words)

    # Create the GUI window
    word_cloud_window = Toplevel(root)
    word_cloud_window.title("Generate Word Cloud")
    word_cloud_window.geometry("400x200")

    Label(word_cloud_window, text="Select a Book:", font=("Arial", 12)).pack(pady=5)
    book_var = StringVar(word_cloud_window)
    book_var.set("Entire Bible")  # Default option
    book_options = ["Entire Bible"] + ALL_BOOKS
    OptionMenu(word_cloud_window, book_var, *book_options).pack(pady=5)

    Label(word_cloud_window, text="Number of Words:", font=("Arial", 12)).pack(pady=5)
    max_words_var = StringVar(word_cloud_window)
    max_words_var.set("50")  # Default value
    OptionMenu(word_cloud_window, max_words_var, *[str(x) for x in range(10, 101, 10)]).pack(pady=5)

    Button(word_cloud_window, text="Generate Word Cloud", command=perform_word_cloud).pack(pady=10)


def create_gui():
    """
    Create the main GUI for the Bible Viewer.
    """
    global root
    root = tk.Tk()
    root.title("Bible Viewer")
    root.geometry("500x400")

    Button(root, text="Table of Contents", command=contents_gui, font=("Arial", 14)).pack(pady=10)
    Button(root, text="Holy Bible", command=lambda: read_bible_gui(book=ALL_BOOKS[0]), font=("Arial", 14), width=13).pack(pady=10)
    Button(root, text="Random Verse", command=show_random_verse, font=("Arial", 14)).pack(pady=10)
    Button(root, text="Word Cloud", command=word_cloud_gui, font=("Arial", 14)).pack(pady=10)
    Button(root, text="Search", command=search_bible_gui, font=("Arial", 14)).pack(pady=10)
    Button(root, text="About", command=show_about, font=("Arial", 14)).pack(pady=10)

    root.mainloop()
    

    root.mainloop()

# Download the folder I provided 'kjv_bible', specify below the filepath where you downloaded that to
# You can right click the folder and copy/paste into here
# Example: r'c:\User\Desktop\Bible-kjv-master\kjv_bible'

bible_folder = r"c:\\Users\\User\\Desktop\\USB\\Bible-kjv-master\\kjv_bible"  # Replace with the correct folder path
bible = load_bible(bible_folder)
create_gui()
