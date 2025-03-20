import streamlit as st
import json
import os

filename = 'library.txt'

# Load library data from file if exists
def load_library():
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

# Save library data to file
def save_library(library):
    with open(filename, 'w') as file:
        json.dump(library, file)

# Main Streamlit App
st.title("📚 Personal Library Manager")

# Session State for Library
if 'library' not in st.session_state:
    st.session_state.library = load_library()

menu = st.sidebar.radio("Menu", ("Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics"))

if menu == "Add Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Enter Book Title")
    author = st.text_input("Enter Author Name")
    year = st.number_input("Enter Publication Year", min_value=0, max_value=2100, step=1)
    genre = st.text_input("Enter Genre")
    read = st.checkbox("Have you read this book?")

    if st.button("Add Book"):
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read
        }
        st.session_state.library.append(new_book)
        save_library(st.session_state.library)
        st.success("Book added successfully!")

elif menu == "Remove Book":
    st.header("🗑 Remove a Book")
    titles = [book['title'] for book in st.session_state.library]
    selected_title = st.selectbox("Select the book to remove", titles)

    if st.button("Remove Book"):
        st.session_state.library = [book for book in st.session_state.library if book['title'] != selected_title]
        save_library(st.session_state.library)
        st.success("Book removed successfully!")

elif menu == "Search Book":
    st.header("🔍 Search a Book")
    search_by = st.radio("Search by", ("Title", "Author"))
    query = st.text_input(f"Enter {search_by}")

    if st.button("Search"):
        found = False
        for book in st.session_state.library:
            if query.lower() in book[search_by.lower()].lower():
                st.write(f"✅ **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
                found = True
        if not found:
            st.warning("No matching books found!")

elif menu == "Display All Books":
    st.header("📖 All Books in Your Library")
    if not st.session_state.library:
        st.info("Library is empty.")
    else:
        st.table(st.session_state.library)

elif menu == "Statistics":
    st.header("📊 Library Statistics")
    total_books = len(st.session_state.library)
    if total_books == 0:
        st.info("Library is empty.")
    else:
        read_books = sum(1 for book in st.session_state.library if book['read'])
        percentage_read = (read_books / total_books) * 100
        st.write(f"**Total Books:** {total_books}")
        st.write(f"**Books Read:** {read_books}")
        st.write(f"**Percentage Read:** {percentage_read:.2f}%")
