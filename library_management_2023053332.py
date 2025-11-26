import json
import os
from datetime import datetime
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.widget import Widget 

## CONFIGURATION

DATA_FILE = 'library_records.json'

## KIVYMD UI DEFINITION (KV Language)

KV = """
MDBoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        id: toolbar
        title: "ROCKVIEW LIBRARY MANAGEMENT SYSTEM"
        md_bg_color: app.theme_cls.primary_color
        specific_text_color: 1, 1, 1, 1
        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]
        elevation: 10
        right_action_items: [] 

    MDNavigationLayout:
        
        MDScreenManager:
            id: screen_manager
            
            ## Screen 1: Book List Screen (Main View)
            
            MDScreen:
                name: 'list'
                on_enter: app.current_screen_name = 'list' 
                MDBoxLayout:
                    orientation: 'vertical'
                    MDLabel:
                        text: "Book Collection"
                        font_style: 'H5'
                        halign: 'center'
                        size_hint_y: None
                        height: dp(50)
                        padding: dp(10), dp(10)
                    
                    MDTextField:
                        id: search_input
                        hint_text: "Search by ID, Title, or Author..."
                        mode: "round"
                        pos_hint: {'center_x': 0.5}
                        size_hint_x: 0.95
                        on_text: app.search_books_ui(self.text)
                        
                    ScrollView:
                        MDList:
                            id: book_list_container
                            padding: dp(10)
                            
            ## Screen 2: Add Book Screen (Scrollable)
            
            MDScreen:
                name: 'add'
                on_enter: app.current_screen_name = 'add' 
                
                ScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(15)
                        size_hint_y: None
                        height: self.minimum_height 
                        
                        MDLabel:
                            text: "Add New Book Record"
                            font_style: 'H5'
                            size_hint_y: None
                            height: dp(50)
                        
                        MDTextField:
                            id: add_id
                            hint_text: "Book ID (e.g., L001)"
                            helper_text: "Must be unique. Will be converted to uppercase."
                            required: True
                        MDTextField:
                            id: add_title
                            hint_text: "Title"
                            required: True
                        MDTextField:
                            id: add_author
                            hint_text: "Author"
                            required: True
                        MDTextField:
                            id: add_year
                            hint_text: "Year Published (e.g., 2023)"
                            input_type: 'number'
                            required: True
                        
                        MDRaisedButton:
                            text: "Add Book"
                            on_release: app.add_book_ui()
                            md_bg_color: app.theme_cls.accent_color
                        
                        Widget:
                            size_hint_y: None
                            height: dp(30)

            ## Screen 3: Transaction Screen
            
            MDScreen:
                name: 'actions'
                on_enter: app.current_screen_name = 'actions'
                
                ScrollView:
                    GridLayout:
                        cols: 1 
                        padding: dp(20)
                        spacing: dp(20) 
                        size_hint_y: None
                        height: self.minimum_height
                        
                        MDLabel:
                            text: "Library Transactions"
                            font_style: 'H5'
                            halign: 'center'
                            size_hint_y: None
                            height: dp(50)
                            padding: dp(10), dp(10)
                            
                        ## 4. BORROW BOOK
                        
                        MDCard:
                            orientation: 'vertical'
                            padding: dp(15)
                            spacing: dp(15)
                            radius: [dp(15)]
                            elevation: 8
                            size_hint_y: None
                            height: self.minimum_height
                            
                            MDLabel:
                                text: "Borrow Book"
                                font_style: 'H6'
                                bold: True
                                theme_text_color: "Primary"
                                size_hint_y: None
                                height: self.texture_size[1]
                                
                            MDTextField:
                                id: borrow_id
                                hint_text: "Book ID to Borrow"
                                required: True
                                mode: "rectangle"
                            
                            MDTextField:
                                id: borrower_name
                                hint_text: "Borrower's Name"
                                required: True
                                mode: "rectangle"
                                
                            MDRaisedButton:
                                text: "Record Borrowing"
                                on_release: app.borrow_book_ui()
                                size_hint_x: 1
                                md_bg_color: app.theme_cls.primary_color

                        ## 5. RETURN BOOK
                        
                        MDCard:
                            orientation: 'vertical'
                            padding: dp(15)
                            spacing: dp(15)
                            radius: [dp(15)]
                            elevation: 8
                            size_hint_y: None
                            height: self.minimum_height
                            
                            MDLabel:
                                text: "Return Book"
                                font_style: 'H6'
                                bold: True
                                theme_text_color: "Primary"
                                size_hint_y: None
                                height: self.texture_size[1]
                                
                            MDTextField:
                                id: return_id
                                hint_text: "Book ID to Return"
                                required: True
                                mode: "rectangle"
                                
                            MDRaisedButton:
                                text: "Record Return"
                                on_release: app.return_book_ui()
                                size_hint_x: 1
                                md_bg_color: app.theme_cls.accent_color

                        ## 6. DELETE BOOK
                        
                        MDCard:
                            orientation: 'vertical'
                            padding: dp(15)
                            spacing: dp(15)
                            radius: [dp(15)]
                            elevation: 8
                            size_hint_y: None
                            height: self.minimum_height
                            
                            MDLabel:
                                text: "Delete Book"
                                font_style: 'H6'
                                bold: True
                                theme_text_color: "Error"
                                size_hint_y: None
                                height: self.texture_size[1]
                                
                            MDTextField:
                                id: delete_id
                                hint_text: "Book ID to Delete"
                                required: True
                                mode: "rectangle"
                                
                            MDRaisedButton:
                                text: "Permanently Delete"
                                on_release: app.delete_book_confirmation()
                                size_hint_x: 1
                                md_bg_color: app.theme_cls.error_color
                                
                        Widget:
                            size_hint_y: None
                            height: dp(30) # Final buffer space

        ## Navigation Drawer Layout
        
        MDNavigationDrawer:
            id: nav_drawer
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20), dp(10), dp(10), dp(10)
                spacing: dp(10)
                size_hint_y: 1
                
                MDLabel:
                    text: "Navigation"
                    font_style: 'H6'
                    size_hint_y: None
                    height: self.texture_size[1]
                
                MDList:
                    id: nav_list_container 
                    OneLineIconListItem:
                        text: "Book List (View All)"
                        on_release:
                            app.root.ids.screen_manager.current = 'list'
                            nav_drawer.set_state("close")
                        IconLeftWidget:
                            icon: "book-multiple"
                    
                    OneLineIconListItem:
                        text: "Add New Book"
                        on_release:
                            app.root.ids.screen_manager.current = 'add'
                            nav_drawer.set_state("close")
                        IconLeftWidget:
                            icon: "book-plus"
                    
                    OneLineIconListItem:
                        text: "Transactions"
                        on_release:
                            app.root.ids.screen_manager.current = 'actions'
                            nav_drawer.set_state("close")
                        IconLeftWidget:
                            icon: "book-sync"

                    ## Exit Button
                    OneLineIconListItem:
                        text: "Exit App"
                        theme_text_color: "Error" 
                        on_release: app.stop() 
                        IconLeftWidget:
                            icon: "exit-to-app"

                ## Flexible spacer: Pushes content above to the top and content below to the bottom
                Widget:
                    size_hint_y: 1

                ## Footer Label: Placed at the end to be pushed to the bottom
                MDLabel:
                    text: "POWERED BY SINAI DIVINE"
                    halign: 'center'
                    size_hint_y: None
                    height: dp(30)
                    font_style: 'Caption'
                    theme_text_color: "Secondary"
                    pradding: dp(10), dp(10)


"""


class BookManagerApp(MDApp):
    """
    Main application class for the KivyMD Library Management System.
    Handles the GUI, in-memory data, and JSON file handling.
    """
    
    ## In-memory storage for all book records
    books = []
    
    db_status = StringProperty("Initializing Data...")
    current_screen_name = StringProperty('list') 
    dialog = None

    def build(self):
        """Initializes the theme, loads the KV layout, and loads data from JSON."""
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        
        self.load_data() # Load data from JSON file
        
        root_widget = Builder.load_string(KV)
        self.bind(current_screen_name=self.update_toolbar_actions)
        
        return root_widget
    
    def on_stop(self):
        """Saves all book data to the JSON file when the application closes."""
        self.save_data()
        print(f"[INFO] Application stopped. Data saved to {DATA_FILE}")

    def go_back(self, instance):
        """Called by the back button to navigate to the 'list' screen."""
        self.root.ids.screen_manager.current = 'list'

    def update_toolbar_actions(self, instance, screen_name):
        """Dynamically sets the right action items of the toolbar based on the screen."""
        if not self.root or 'toolbar' not in self.root.ids:
            return

        toolbar = self.root.ids.toolbar
        
        if screen_name == 'list':
            toolbar.right_action_items = []
        else:
            back_action = ['arrow-left', self.go_back, 'Back']
            toolbar.right_action_items = [back_action]


    ## Data Persistence (JSON File Handling)

    def load_data(self):
        """Loads book data from the JSON file into the in-memory 'books' list."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    self.books = json.load(f)
                self.db_status = "Data Loaded (JSON)"
                print(f"[INFO] Loaded {len(self.books)} books from {DATA_FILE}.")
            except Exception as e:
                self.books = []
                self.db_status = "Data Error (New File Created)"
                print(f"[ERROR] Failed to load data from JSON: {e}. Starting with empty list.")
        else:
            self.books = []
            self.db_status = "New Data File Initialized"
            print(f"[INFO] {DATA_FILE} not found. Starting with empty list.")
        
        self.load_books() 

    def save_data(self):
        """Saves the current in-memory 'books' list to the JSON file."""
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.books, f, indent=4)
            print(f"[INFO] Successfully saved {len(self.books)} books to {DATA_FILE}.")
        except Exception as e:
            print(f"[ERROR] Failed to save data to JSON: {e}")


    ## Utility: Dialog Management (Replaces alert/confirm)

    def show_dialog(self, title, text, buttons=None):
        """Displays a modal dialog for alerts or confirmations."""
        if not buttons:
            buttons = [MDFlatButton(text="OK", on_release=self.close_dialog)]
            
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=buttons,
            radius=[dp(20), dp(7), dp(20), dp(7)],
        )
        self.dialog.open()

    def close_dialog(self, instance):
        """Closes the currently open dialog."""
        if self.dialog:
            self.dialog.dismiss()


    ## 1. ADD BOOK RECORD (Logic)

    def add_book_ui(self):
        """Handles data collection from the Add Book screen and adds the book to the list."""
        ids = self.root.ids
        
        book_id = ids.add_id.text.strip().upper()
        title = ids.add_title.text.strip()
        author = ids.add_author.text.strip()
        year_str = ids.add_year.text.strip()
        
        try:
            year = int(year_str)
            if not (1000 <= year <= datetime.now().year + 5):
                 raise ValueError("Invalid year range.")
        except ValueError:
            self.show_dialog("Input Error", "Please enter a valid year (e.g., 2023).")
            return
            
        if not all([book_id, title, author]):
            self.show_dialog("Input Error", "All fields are required.")
            return

        ## Check for duplicate ID in the in-memory list
        if any(book['book_id'] == book_id for book in self.books):
            self.show_dialog("Error", f"Book ID '{book_id}' already exists. Use a different ID.")
            return

        ## Create new book dictionary
        new_book = {
            'book_id': book_id,
            'title': title,
            'author': author,
            'year_published': year,
            'availability': 'Available',
            'borrower_name': '',
            'date_borrowed': ''
        }
        
        self.books.append(new_book)
        self.save_data() # Save change immediately
            
        ## Clear fields
        ids.add_id.text = ""
        ids.add_title.text = ""
        ids.add_author.text = ""
        ids.add_year.text = ""
        
        self.show_dialog("Success", f"Book '{title}' added successfully!")
        self.root.ids.screen_manager.current = 'list' 
        self.load_books() 


    ## 2. VIEW ALL BOOKS & 3. SEARCH BOOK (Logic)

    @mainthread
    def load_books(self, search_term=''):
        """Filters the in-memory list based on search term and updates the UI."""
        
        container = self.root.ids.book_list_container
        container.clear_widgets() 
        
        # Sort books by title before filtering
        sorted_books = sorted(self.books, key=lambda b: b['title'])
        
        filtered_books = []
        term_lower = search_term.strip().lower()

        if not term_lower:
            filtered_books = sorted_books
        else:
            for book in sorted_books:
                if (term_lower in book['title'].lower() or
                    term_lower in book['book_id'].lower() or
                    term_lower in book['author'].lower()):
                    filtered_books.append(book)

        if not filtered_books:
            no_books_item = OneLineIconListItem(
                text="No books found." if search_term else "No books in the library.",
                bg_color=self.theme_cls.bg_normal
            )
            no_books_item.add_widget(IconLeftWidget(icon="information-outline"))
            container.add_widget(no_books_item)
            return

        for book in filtered_books:
            is_borrowed = book['availability'] == "Borrowed"
            icon_name = "book-lock" if is_borrowed else "book-check"
            secondary_text = f"ID: {book['book_id']} | Author: {book['author']} | Year: {book['year_published']}"
            
            if is_borrowed:
                secondary_text += f" | Borrowed by {book['borrower_name']}"
            
            list_item = OneLineIconListItem(
                text=book['title'],
                secondary_text=secondary_text,
                
                ## Theme colors for borrowed books
                theme_text_color="Primary" if is_borrowed else "Custom",
                text_color=(0.9, 0.4, 0.4, 1) if is_borrowed else (0.2, 0.6, 0.2, 1),
                bg_color=self.theme_cls.bg_normal,
            )
            list_item.add_widget(IconLeftWidget(icon=icon_name))
            container.add_widget(list_item)
            
    
    def search_books_ui(self, search_term):
        """Called by the search input field to filter the list."""
        self.load_books(search_term)


    ## 4. BORROW BOOK (Logic)
    
    def borrow_book_ui(self):
        """Handles borrowing a book by updating the in-memory list."""
        ids = self.root.ids
        book_id = ids.borrow_id.text.strip().upper()
        borrower_name = ids.borrower_name.text.strip()

        if not book_id or not borrower_name:
            self.show_dialog("Input Error", "Book ID and Borrower Name are required.")
            return

        book_found = None
        for book in self.books:
            if book['book_id'] == book_id:
                book_found = book
                break
        
        if not book_found:
            self.show_dialog("Error", f"Book ID '{book_id}' not found.")
            return

        if book_found['availability'] == "Borrowed":
            self.show_dialog("Error", f"Book is already borrowed by {book_found['borrower_name']}.")
            return

        ## Update the book record
        book_found['availability'] = "Borrowed"
        book_found['borrower_name'] = borrower_name
        book_found['date_borrowed'] = datetime.now().strftime("%Y-%m-%d")
        
        self.save_data() ## Save change
        
        ids.borrow_id.text = ""
        ids.borrower_name.text = ""
        self.show_dialog("Success", f"Book '{book_found['title']}' borrowed successfully by {borrower_name}.")
        self.load_books()


    ## 5. RETURN BOOK (Logic)

    def return_book_ui(self):
        """Handles returning a book by updating the in-memory list."""
        ids = self.root.ids
        book_id = ids.return_id.text.strip().upper()

        if not book_id:
            self.show_dialog("Input Error", "Book ID is required for return.")
            return

        book_found = None
        for book in self.books:
            if book['book_id'] == book_id:
                book_found = book
                break
                
        if not book_found:
            self.show_dialog("Error", f"Book ID '{book_id}' not found.")
            return

        if book_found['availability'] == "Available":
            self.show_dialog("Error", f"Book is already marked as available.")
            return

        ## Update the book record
        book_found['availability'] = "Available"
        book_found['borrower_name'] = ""
        book_found['date_borrowed'] = ""
        
        self.save_data() ## Save change
        
        ids.return_id.text = ""
        self.show_dialog("Success", f"Book '{book_found['title']}' returned successfully.")
        self.load_books()


    ## 6. DELETE BOOK (Logic)

    def delete_book_confirmation(self):
        """Shows confirmation dialog before deleting."""
        book_id = self.root.ids.delete_id.text.strip().upper()
        if not book_id:
            self.show_dialog("Input Error", "Book ID is required for deletion.")
            return
            
        def delete_confirmed(instance):
            self.close_dialog(instance)
            self._execute_delete(book_id)

        self.show_dialog(
            "Confirm Deletion",
            f"Are you sure you want to PERMANENTLY delete book ID '{book_id}'? This cannot be undone.",
            [
                MDFlatButton(text="CANCEL", on_release=self.close_dialog),
                MDRaisedButton(text="DELETE", on_release=delete_confirmed, md_bg_color=self.theme_cls.error_color),
            ]
        )

    def _execute_delete(self, book_id):
        """Performs the actual deletion by removing the book from the in-memory list."""
        book_to_delete = None
        
        ## Find the book and its index
        for i, book in enumerate(self.books):
            if book['book_id'] == book_id:
                book_to_delete = book
                book_index = i
                break

        if not book_to_delete:
            self.show_dialog("Error", f"Book ID '{book_id}' not found.")
            return

        if book_to_delete['availability'] == "Borrowed":
            self.show_dialog("Error", f"Book is currently borrowed and cannot be deleted.")
            return

        ## If found and available, remove it
        del self.books[book_index]
        self.save_data() ## Save change
        
        self.root.ids.delete_id.text = ""
        self.show_dialog("Success", f"Book '{book_to_delete['title']}' deleted successfully.")
        self.load_books()


if __name__ == '__main__':
    BookManagerApp().run()
