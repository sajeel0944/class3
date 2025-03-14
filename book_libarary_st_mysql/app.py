import mysql.connector
import pandas as pd
import streamlit as st


API_KEY_TOKEN = st.secrets["HOST_NAME"]
# Database connection function
def get_connection():
    conn = mysql.connector.connect(
        host=f"{API_KEY_TOKEN}",
        user="root",
        password="mt",
        database="library_db"
    )
    return conn




# 🟢 Sidebar ka background color change karne ke liye CSS
st.markdown("""
    <style>
        /* Sidebar background color */
        [data-testid="stSidebar"] {
            background-color: #2E4053;  /* Dark Blue/Gray Shade */
        }

        /* Sidebar ke text ka color white */
        [data-testid="stSidebar"] * {
            color: white;
        }

        /* Sidebar ke radio buttons */
        div[data-testid="stSidebar"] label {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)



st.title("\n\t\t 📚 Welcome to Your Personal Library Manager")

st.sidebar.title("Navigation")
# is ky andar sary book ky optional hai
select_options : list = st.sidebar.radio("Select an option:",["Add a book", "Remove a book", "Search for a book", "Display all books", "Display statistics", "Exit"])
    
    

try:
  
    st.sidebar.write(f"✅ Your Selecte This {select_options}")


    if select_options == "Add a book":
        st.subheader("📖 Add a New Book to Your Library")

        title = st.text_input("Enter the book title")
        author = st.text_input("Enter the author")
        publication = st.text_input("Enter the publication year")
        genre = st.text_input("Enter the genre")
        read = st.text_input("Have you read this book? yes/no")

        read_status = None # is main 0 ya 1 aye ga
        if read.lower() == "yes": # agar read ky nadar yes aya to read_status main 1 aye ga wana 0
            read_status = 1
        else:
            read_status = 0  

        if st.button("Add Book"):
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

                st.success("📚 Book added successfully to Database!")

            if title and author and publication and genre and read:
                add_book()
            else:
                st.warning("⚠️ Please fill in all details before saving!")



    elif select_options == "Remove a book":
        st.subheader("📖 Remove a book to Your Library")
        book_delete = st.text_input("\nEnter the title of the book you want to remove")

        if st.button("Delete"):
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
                    st.success(f"✅ '{book_delete}' has been removed from your library!")
                else:
                    st.warning(f"⚠️ No book found with the title '{book_delete}'.")
            else:
                st.warning("⚠️ Please enter a book title to delete.")



    elif select_options == "Search for a book":
        st.subheader("📖 Search for a book to Your Library")
        find_book = st.text_input("\nEnter the title of the book you want to search: ")

        if st.button("Search"):
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
                    new_book = pd.DataFrame([[book['title'], book['author'], book['publication'], book['genre'], 'Yes' if book['read_status'] else 'No']], 
                                            columns=['Title', 'Author', 'Publication Year', 'Genre', 'Read Status'])
                    st.write(new_book)
                else:
                    st.warning("⚠️ No book found with this title!")

            if find_book:
                search_book(find_book)
            else:
                st.warning("⚠️ Please enter a book title.")



    elif select_options == "Display all books":
        st.subheader("📖 Display all books to Your Library")

        if st.button("Display All Book"):
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
                    df = pd.DataFrame(books)

                    # Column names better kar diye
                    df.rename(columns={'title': 'Title', 
                                    'author': 'Author', 
                                    'publication': 'Publication Year', 
                                    'genre': 'Genre', 
                                    'read_status': 'Read Status'}, inplace=True)

                    # Read Status ko "Yes/No" format me convert kiya
                    df['Read Status'] = df['Read Status'].apply(lambda x: 'Yes' if x else 'No')

                    # Streamlit me properly dataframe dikhane ka tarika
                    st.dataframe(df)  
                else:
                    st.warning("⚠️ No books found in the library!")

            all_books()



    elif select_options == "Display statistics":
        st.subheader("📖 Display statistics to Your Library")

        if st.button("Check Book Read States"):
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

                st.write(f"📊 **Library Statistics:**")
                st.write(f"**Total Books**: {total_books}")
                st.write(f"**Read Books**: ({read_percentage:.2f}%)")
                st.write(f"**Unread Books**: ({unread_percentage:.2f}%)")

            read_statistics()



    elif select_options == "Exit":
        st.write("👋 Thank you for using the Library Manager! Have a great day! 🚀")
      

except Exception as e:
    st.warning("\n⚠️ Somethink Was Wrong ")
        



        