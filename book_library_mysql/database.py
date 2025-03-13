import mysql.connector
import pandas as pd

# Database connection function
def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mt",
        database="library_db"
    )
    return conn



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


        if user_selected == "Add a book":
            print("\n📖 Add a New Book to Your Library\n")

            title = input("Enter the book title : ")
            author = input("Enter the author : ")
            publication = input("Enter the publication year : ")
            genre = input("Enter the genre : ")
            read = input("Have you read this book? yes/no : ")

            read_status = None # is main 0 ya 1 aye ga
            if read.lower() == "yes": # agar read ky nadar yes aya to read_status main 1 aye ga wana 0
                read_status = 1
            else:
                read_status = 0  

            def add_book():
                conn = get_connection()  # Get database connection
                cursor = conn.cursor() # se ek cursor object milta hai, jo database pe SQL queries execute karne ke liye hota hai.

                # ye ek pory command hai mysql ki is command sy mysql ky andar ek row main value add hoti hai
                sql = "INSERT INTO books (title, author, publication, genre, read_status) VALUES (%s, %s, %s, %s, %s)"  # %s ky andar index ky zayeye "values" variable ki sary value arahe hai
                values = (title, author, publication, genre, read_status) # is ko tuple main dia hai q ky myaql tuple ko understand karta hai

                cursor.execute(sql,values) # mysql ky andar bata send kar raha ho
                conn.commit()  # ka kaam hai changes ko save karna
                cursor.close() # Cursor ko close kar deta hai.
                conn.close() # MySQL database connection close kar deta hai.

                print("\n📚 Book added successfully to Database!")

            if title and author and publication and genre and read:
                add_book()
            else:
                print("\n⚠️ Please fill in all details before saving!")



        if user_selected == "Remove a book":
            book_delete = input("\nEnter the title of the book you want to remove : ")

            def remove_book(title_to_remove):
                conn = get_connection() # Get database connection
                cursor = conn.cursor() # se ek cursor object milta hai, jo database pe SQL queries execute karne ke liye hota hai.
                
                # ye ek pory command hai mysql ki is command sy mysql ky jo abhi row main  title_to_remove match hoye ga us to delete kardy ta hai
                sql = "DELETE FROM books WHERE title = %s"   # %s ky andar index ky zayeye "values" variable ki  value arahe hai
                values = (title_to_remove,)  # is ko tuple main dia hai q ky mysql tuple ko understand karta hai or is ko , sy tuple bany ga

                cursor.execute(sql, values) # mysql ky andar bata send kar raha ho
                conn.commit() # ka kaam hai changes ko save karna
                
                rows_deleted = cursor.rowcount # check karega kitni rows delete hui hai
                cursor.close() # Cursor ko close kar deta hai.
                conn.close() # MySQL database connection close kar deta hai.

                return rows_deleted > 0  # agar value delete hoye hai to rows_deleted ky andar 1 hoye ga to ye return True karry ga wana rows_deleted ky andar 0 hoye go to ye False kary ga 

            if book_delete:
                success = remove_book(book_delete)
                if success:
                    print(f"\n✅ '{book_delete}' has been removed from your library!")
                else:
                    print(f"\n⚠️ No book found with the title '{book_delete}'.")
            else:
                print("\n⚠️ Please enter a book title to delete.")



        if user_selected == "Search for a book":
            find_book = input("\nEnter the title of the book you want to search: ")

            def search_book(search):
                conn = get_connection()  # Get database connection
                cursor = conn.cursor(dictionary=True) # database me query execute karna hai. or "dictionary=True" Jo data fetch hoga, wo dictionary format me aayega.
                # ye ek pory command hai mysql ki is command sy mysql ky andar sy tile ki madad sy q koye roe ni kal sak ty hai 
                sql = "SELECT * FROM books WHERE title = %s" # %s ky andar index ky zayeye "values" variable ki  value arahe hai
                values = (search,)# is ko tuple main dia hai q ky mysql tuple ko understand karta hai or is ko , sy tuple bany ga

                cursor.execute(sql, values) # mysql ky andar bata send kar raha ho
                book = cursor.fetchone()  # fetchone()  Sirf ek record return karega. Agar multiple books ho, to sirf pehla record fetch hoga.

                cursor.close() # Cursor ko close kar deta hai.
                conn.close() # MySQL database connection close kar deta hai.

                if book:
                    print(f"\n✅ Successfully found your book")
                    print(f"\nTitle: {book['title']}")
                    print(f"Author: {book['author']}")
                    print(f"Publication: {book['publication']}")
                    print(f"Genre: {book['genre']}")
                    print(f"Read: {'Yes' if book['read_status'] else 'No'}")
                else:
                    print("\n⚠️ No book found with this title!")

            if find_book:
                search_book(find_book)
            else:
                print("\n⚠️ Please enter a book title.")



        if user_selected == "Display all books":
            def all_books():
                conn = get_connection() # Get database connection
                cursor = conn.cursor(dictionary=True) # database me query execute karna hai. or "dictionary=True" Jo data fetch hoga, wo dictionary format me aayega.

                # ye ek pory command hai mysql ki is command sy mysql ky andar jitna bhi data hai us ko show kar ta hai 
                sql = "SELECT * FROM books"
                cursor.execute(sql) # mysql ky andar bata send kar raha ho
                books = cursor.fetchall() #fetchall()  Saari rows ek saath fetch karna. Agar book 1 sy zayeda ho to ye list of dictionaries return karega.

                cursor.close() # Cursor ko close kar deta hai.
                conn.close() # MySQL database connection close kar deta hai.

                if books:
                    df = pd.DataFrame(books)  # Pandas DataFrame me convert karna
                    print(f"\n{df}")
                else:
                    print("\n⚠️ No books found in the library!")

            all_books()



        if user_selected == "Display statistics":
            def read_statistics():
                conn = get_connection() # Get database connection
                cursor = conn.cursor() # se ek cursor object milta hai, jo database pe SQL queries execute karne ke liye hota hai.

                # ye ek pory command hai mysql ki is command sy mysql sy Yeh query total books ka count nikal rahi hai
                cursor.execute("SELECT COUNT(*) FROM books")
                total_books = cursor.fetchone()[0] # Ek single value fetch karega jo total books ki count hogi.

                # ye ek pory command hai mysql ki is command sy mysql ye sirf  read_status ky andar jis main 1 hoye ga us ko ye coun kary ga
                cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
                read_books = cursor.fetchone()[0] # Read books ka count fetch karega.

                # ye ek pory command hai mysql ki is command sy mysql ye sirf  read_status ky andar jis main 0 hoye ga us ko ye coun kary ga
                cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 0")
                unread_books = cursor.fetchone()[0] # Read books ka count fetch karega.

                cursor.close() # Cursor ko close kar deta hai.
                conn.close() # MySQL database connection close kar deta hai.

                if total_books > 0:
                    read_percentage = (read_books / total_books) * 100
                    unread_percentage = (unread_books / total_books) * 100
                else:
                    read_percentage = unread_percentage = 0

                print(f"\n📊 Library Statistics:")
                print(f"Total Books: {total_books}")
                print(f"Read Books: {read_books} ({read_percentage:.2f}%)")
                print(f"Unread Books: {unread_books} ({unread_percentage:.2f}%)")

            read_statistics()



        if user_selected == "Exit":
            print("\n👋 Thank you for using the Library Manager! Have a great day! 🚀")
            break


    except Exception as e:
        print("\n⚠️  Please enter a valid option number")
        