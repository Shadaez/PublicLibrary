"""Use object-oriented Python to model a public library
(w/ three classes: Library, Shelf, & Book). 
The library should be aware of a number of shelves. 
Each shelf should know what books it contains. 
Make the book object have "enshelf" and "unshelf" 
methods that control what shelf the book is sitting on. 
The library should have a method to report all books it contains."""

#shelf is a really weird word when you retype it 50 times, especially when you're writing self.shelf 

class Library(object):
	unshelved_books = []
	shelf = []
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return self.list_books()

	def add_shelf(self, *args): #arg is optional if you want to add an existing shelf to library
		if len(args) == 0:
			Shelf(self)
		else:
			self.shelf.append(args[0])
			self.shelf[-1].library = self
		if len(self.unshelved_books) > 0:
			for book in self.unshelved_books:
				self.shelf[-1].enshelf(book)
				self.unshelved_books = []
		return self.shelf[-1]

	def list_books(self):
		unshelved_string = ''
		if len(self.unshelved_books) >= 1:
			unshelved_string = ', ' + ', '.join([str(x) for x in self.unshelved_books])
		return (','.join([str(x) for x in self.shelf]) + unshelved_string) 
		
	def remove_shelf(self, shelf):
		books = shelf.books
		i = 0
		for book in books:
			self.unshelved_books.append(book)  
			book.shelf = None
		self.shelf.remove(shelf) #python will delete the shelves instance itself when it garbage collects (i think) when there are no references to it
		if len(self.shelf) > 1:
			for book in self.unshelved_books:
				book.reshelve(self.shelf[i%(len(self.shelf)-1)]) #puts an even number of books in each remaining shelf
				i += 1 
			else:
				self.unshelved_books = []

class Shelf(object):
	def __init__(self, *args): #arg0 should be lib, arg 1 should be a list any books you want added on creation. Both are optional.
		self.books = []
		self.library = None
		if len(args) > 0:
			self.library = args[0]
			if len(args) > 1:
				for book in args[1]:
					self.books.append(book)
			if self.library.shelf.count(self) < 1:
				self.library.shelf.append(self)

	def __str__(self):
		return ', '.join(str(x) for x in self.books)

	def enshelf(self, book):
		self.books.append(book)

	def unshelf(self, book):
		self.books.remove(book)

class Book(object):
	def __init__(self, title, author, *args): #args[0] is shelf, optional.
		self.title = str(title)
		self.author = str(author)
		self.shelf = None
		if len(args) > 0:
			self.shelf = args[0]
			self.shelf.books.append(self)

	def __str__(self):
		return '"'+self.title+'"' + ' by ' + self.author

	def unshelf(self):
		if self.shelf != None:
			self.shelf.unshelf(self)
		self.shelf = None

	def enshelf(self, shelf):
		if self.shelf != None: #to make sure the book isn't accidentally shelved twice!
			self.unshelf()
		self.shelf = shelf
		self.shelf.enshelf(self)

	def reshelve(self, shelf): #unshelves then enshelves
		self.unshelf()
		self.enshelf(shelf)

port_orchard_library = 	Library("Port Orchard Library")

#you can add shelves like:
shelf = Shelf(port_orchard_library)
#or:
port_orchard_library.add_shelf() #this one's just a reference (i think thats the word?) in the shelf list
#or
shelf2 = Shelf(port_orchard_library)
#they all created a new shelf in the port orchard library, one's just a reference in the port_orchard_library.shelf list, though.
#you can also make a shelf that doesn't belong to any library
shelf3 = Shelf()
#and then you can add it to a library
port_orchard_library.add_shelf(shelf3)

#same with books, you can make a book that doesn't belong to a shelve
enders_game = Book("Ender's Game", "Orson Scott Card")
#and add it to a shelf
enders_game.enshelf(shelf3)
#and now it's in the shelf
print str(shelf3)
#you can also add books directly to shelves
print str(shelf) #no books
Book("The Hunger Games", "Suzanne Collins", shelf)
print str(shelf) #omg a book

#and if a shelf gets thrown out, the books will repopulate the rest of the shelves
port_orchard_library.remove_shelf(shelf3)
print str(shelf) #now shelf has both books.

#lets add a bunch of books to demonstrate that the library will print out all books

Book("Catching Fire","Suzanne Collins", shelf)
Book("Mockingjay","Suzanne Collins", shelf2)
Book("Harry Potter and the Philosopher's Stone","J. K. Rowling", shelf)
Book("Harry Potter and the Chamber of Secrets","J. K. Rowling", shelf2)
Book("Harry Potter and the Prisoner of Azkaban","J. K. Rowling", shelf2)
Book("Harry Potter and the Goblet of Fire","J. K. Rowling", shelf2)
Book("Harry Potter and the Order of the Phoenix","J. K. Rowling", shelf)
Book("Harry Potter and the Half-Blood Prince","J. K. Rowling", shelf2)
Book("Harry Potter and the Deathly Hallows","J. K. Rowling", shelf)

print "should have all"
print port_orchard_library.list_books()

#oops we threw away all the shelves
tempshelf = port_orchard_library.shelf[:]
for x in tempshelf:
	port_orchard_library.remove_shelf(x)
#but all the books are OK
print ', '.join([str(x) for x in port_orchard_library.unshelved_books])
#and if we get a new shelf
port_orchard_library.add_shelf()
#they will all populate it
print str(port_orchard_library.shelf[0])
print port_orchard_library.list_books()

#Hope this is OK! I think I debugged it all but who knows.