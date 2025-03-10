import streamlit as st
import json
import os

st.title("📚 Welcome to Your Personal Library Manager")

# ✅ Store User Inputs in Session State to Prevent Reload Issue
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

if "book_data" not in st.session_state:
    st.session_state.book_data = {"title": "", "author": "", "publication": "", "genre": "", "read": ""}

if "book_added" not in st.session_state:
    st.session_state.book_added = False  # ✅ Track if book was added successfully

# ✅ Options List
select_options : list[str] = ["Add a book", "Remove a book", "Search for a book", "Display all books", "Display statistics", "Exit"]
count : int = 0

for selecte in select_options:
    count += 1
    st.write(f"{count}. **{selecte}** ")


# ✅ User Selection Input
user_input = st.text_input("Enter Your Selection (Number)")

if st.button("Selete"):
    try:
        user_option = int(user_input)
        st.session_state.selected_option = select_options[user_option - 1]
        st.session_state.book_added = False  # ✅ Reset book added status
        st.success(f"✅ You Selected: **{st.session_state.selected_option}**")
    except ValueError:
        st.warning("⚠️ Please enter a valid option number!")




# ✅ File Handling Functions
LIBRARY_FILE = "library.json"

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            try:
                return json.load(file)  # Load existing data
            except json.JSONDecodeError:
                return []  # Empty file case
    return []  # If file does not exist, return empty list

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)




# ✅ If User Selects "Add a Book", Show Form
if st.session_state.selected_option == "Add a book":
    st.subheader("📖 Add a New Book to Your Library")

    # ✅ Use Session State for Form Fields (so values remain after clicking)
    st.session_state.book_data["title"] = st.text_input("Enter the book title", value=st.session_state.book_data["title"], key="title")
    st.session_state.book_data["author"] = st.text_input("Enter the author", value=st.session_state.book_data["author"], key="author")
    st.session_state.book_data["publication"] = st.text_input("Enter the publication year", value=st.session_state.book_data["publication"], key="publication")
    st.session_state.book_data["genre"] = st.text_input("Enter the genre", value=st.session_state.book_data["genre"], key="genre")
    st.session_state.book_data["read"] = st.selectbox("Have you read this book?", ["yes", "no"], index=0 if st.session_state.book_data["read"] == "yes" else 1, key="read")

    def add_book():
        """Add a new book to the library"""
        library = load_library()
        new_book = {
            "title": st.session_state.book_data["title"],
            "author": st.session_state.book_data["author"],
            "publication": st.session_state.book_data["publication"],
            "genre": st.session_state.book_data["genre"],
            "read": st.session_state.book_data["read"]
        }
        library.append(new_book)
        save_library(library)
        st.session_state.book_added = True  # ✅ Mark book as added
        st.success("📚 Book added successfully!")

    # ✅ Button to Add Book (Page Reload Problem Fixed)
    if st.button("📥 Save Book"):
        if all(st.session_state.book_data.values()):
            add_book()
            # ✅ Reset form only if book added
            st.session_state.book_data = {"title": "", "author": "", "publication": "", "genre": "", "read": ""}
        else:
            st.warning("⚠️ Please fill in all details before saving!")





if st.session_state.selected_option == "Remove a book":
    def remove_book(title_to_remove):
        """Remove a book by title."""
        library = load_library()
        updated_library = [book for book in library if book["title"].lower() != title_to_remove.lower()]
        
        if len(updated_library) == len(library):
            return False  # No book was removed (book not found)
        
        save_library(updated_library)
        return True  # Book was successfully removed
    
    # ✅ User Input to Remove Book
    book_to_delete = st.text_input("Enter the title of the book you want to remove")

    if st.button("🗑️ Delete Book"):
        if book_to_delete:
            success = remove_book(book_to_delete)
            if success:
                st.success(f"✅ '{book_to_delete}' has been removed from your library!")
            else:
                st.warning(f"⚠️ No book found with the title '{book_to_delete}'.")
        else:
            st.warning("⚠️ Please enter a book title to delete.")





if st.session_state.selected_option == "Search for a book":
    def search_book(search):
        library = load_library()
        for book in library:
            if book["title"].lower() == search.lower():
                st.markdown(f"""
                ### 📖 Book Details  
                - **📚 Title:** {book["title"]}  
                - **✍️ Author:** {book["author"]}  
                - **📅 Publication Year:** {book["publication"]}  
                - **📖 Genre:** {book["genre"]}  
                - **✅ Read Status:** {book["read"]}
                """)
                st.success(f"✅  Your Book successfully Find!")

            
    
    user_search = st.text_input("Enter the title")
    if st.button("Search"):
        if user_search:
            search_book(user_search)
        else:
            st.warning("⚠️ Please Inter Your Book Title.")





if st.session_state.selected_option == "Display all books":
    try:
        def all_book():
            library = load_library()
            count_2 = 0
            st.subheader("****📚 All Book****")
            for book in library:
                count_2 += 1
                st.write(f"""**{count_2}: 📚 Title:** {book["title"]} **✍️ Author:** {book["author"]} **📅 Publication Year:** {book["publication"]} **📖 Genre:** {book["genre"]} **✅ Read Status:** {book["read"]}""")

        all_book()
    except Exception as e:
        st.warning("⚠️ No Book")





if st.session_state.selected_option == "Display statistics":
    # ✅ Count Read Books
    def count_read_books():
        """Count how many books have been read."""
        library = load_library()
        read_books = [book for book in library if book.get("read", "").lower() == "yes"]
        total_books = len(library)
        read_count = len(read_books)
        
        # ✅ Calculate Percentage
        read_percentage = (read_count / total_books * 100) if total_books > 0 else 0
        
        return read_count, total_books, read_percentage

    # ✅ Show Results in Streamlit
    st.title("📊 Library Statistics")

    read_count, total_books, read_percentage = count_read_books()

    st.write(f"📚 **Total Books in Library:** {total_books}")
    st.write(f"✅ **Books Read:** {read_count}")
    st.write(f"📊 **Percentage Read:** {read_percentage:.2f}%")





if st.session_state.selected_option == "Exit":
     # ✅ If user selects Exit, show exit message
    st.warning("👋 Thank you for using the Library Manager! Have a great day! 🚀")
    st.stop()  # Stop execution so nothing else runs