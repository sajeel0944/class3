import os
import json
import pandas as pd

print("\n\t\t 📚 Welcome to Your Personal Library Manager")

while True:
    # is ky andar sary book ky optional hai
    select_options : list = ["Add a book", "Remove a book", "Search for a book", "Display all books", "Display statistics", "Exit"]
    count : int = 0

    print("\n")
    for options in select_options: # is main sary book ky option print hoye gy
        count += 1
        print(f"{count}. {options}")

    try:
        user_select_options : int = int(input("\nEnter Your Selection (Number) : ")) 

        user_selected = select_options[user_select_options -1]
        print(f"\n✅ Your Selecte This {user_selected}")

        library_file = "library.json" # jis file main sary book hai us ka naam

        # is ky andar sary show hoye gi jo  library.json ky andar hai
        def load_library():
            if os.path.exists(library_file):
                with open(library_file, "r") as file:
                    try:
                        return json.load(file)  # Load existing data
                    except json.JSONDecodeError:
                        return []  # Empty file case
            return []  # If file does not exist, return empty list
        
        # is ky andar library.json ky andar book add ho rahe hai
        def save_library(library):
            with open(library_file, "w") as file:
                json.dump(library, file, indent=4)


        if user_selected == "Add a book":
            print("\n📖 Add a New Book to Your Library\n")

            title = input("Enter the book title : ")
            author = input("Enter the author : ")
            publication = input("Enter the publication year : ")
            genre = input("Enter the genre : ")
            read = input("Have you read this book? yes/no : ")

            # is ky andar ko user ki book ad ho rahe library.json main
            def add_book():
                library = load_library() # is ky andar sary library.json ki book save hai
                new_book = {
                    "title" : title,
                    "author" : author,
                    "publication" : publication,
                    "genre" : genre,
                    "read" : read
                }

                library.append(new_book)
                save_library(library)
                print("\n📚 Book added successfully!")
            
            if title and author and publication and genre and read:
                add_book()
            else:
                print("\n⚠️ Please fill in all details before saving!")


        
        if user_selected == "Remove a book":
            # is sy book ko remove kar raha ho
            def remove_book(title_to_remove): # title_to_remove ky andar book ka title araha hai
                library = load_library() # is ky andar libary.json ki sary book save hai

                updated_library = []  # is main sary book aye gi lakin jo title_to_remove wali book is main nhi aye gi
                for book in library:
                    if book["title"].lower() != title_to_remove.lower(): # agar book or title_to_remove match hoye gy to ye condition false hojaye gi
                        updated_library.append(book)  # updated_library main sary book jaye gi lakin jo title_to_remove wali book is main nhi jaye gi
                                
                if len(updated_library) == len(library): # agar updated_library or library ki lenght same hoye gi to ye chly ga book delete nhi hoye gi
                    return False
                else:
                    save_library(updated_library) # sary book save_library ky nadat jara he hai lakin title_to_remove nhi jara he hai
                    return True
            
            book_delete = input("\nEnter the title of the book you want to remove : ")
            
            if book_delete :
                success = remove_book(book_delete) # remove_book function ky parameter main  book_delete ja raha hai
                if success:
                    print(f"\n✅ '{book_delete}' has been removed from your library!")
                else:
                    print(f"\n⚠️  No book found with the title '{book_delete}'.")
            else:
                print("\n⚠️ Please enter a book title to delete.")


        
        if user_selected == "Search for a book":
            def search_book(search): # is ky andar book ka title araha hai

                library = load_library() # is ky andar libary.json ki sary book save hai

                for book in library:
                    if book["title"].lower() == search.lower():
                        print(f"\n✅ successfully Find Your Book")
                        print(f"\ntitle :{book["title"]}")
                        print(f"uthor :{book["author"]}")
                        print(f"ublication :{book["publication"]}")
                        print(f"genre :{book["genre"]}")
                        print(f"read :{book["read"]}")

            find_book = input("\nEnter the title : ")
            if find_book:
                search_book(find_book) 
            else:
                print("\n⚠️ Please Inter Your Book Title.")



        if user_selected == "Display all books":
            def all_book():
                labrary = load_library() # is ky andar libary.json ki sary book save hai
                df : pd.DataFrame = pd.DataFrame(labrary) # is main pandas use ho raha hai
                print(f"\n{df}")
                
            all_book()



        if user_selected == "Display statistics":
            def read_book():
                library = load_library() # is ky andar libary.json ki sary book save hai

                find_read = [] # is ky andar read wali book aye gi
                find_unread = []  # is ky andar unread wali book aye gi

                for read in library:
                    if read["read"].lower() == "yes":
                        find_read.append(read)
                    elif read["read"].lower() == "no":
                        find_unread.append(read)


                count_read_book = len(find_read) / len(library) * 100 # read book ki percentage aye gi
                count_unread_book = len(find_unread) / len(library) * 100 #  unread book ki percentage aye gi

                print(f"\nTotal Book {len(library)}")
                print(f"\nRead Book {count_read_book:.2f}")
                print(f"\nUnread Book {count_unread_book:.2f}")

            read_book()



        if user_selected == "Exit":
            print("\n👋 Thank you for using the Library Manager! Have a great day! 🚀")
            break
            


    except Exception as e:
        print("\n⚠️  Please enter a valid option number")
        