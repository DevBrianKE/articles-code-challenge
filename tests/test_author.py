import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture
def setup_db():
    # Setup database connection
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        );
        
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;
    """)
    
    # Create test data
    author = Author.create(name="Test Author")
    magazine = Magazine.create(name="Test Magazine", category="Test")
    Article.create("Test Article", author, magazine)
    
    yield
    
    # Clean up
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_author_creation(setup_db):
    author = Author.create(name="New Author")
    assert author.id is not None
    assert author.name == "New Author"

def test_find_author_by_id(setup_db):
    author = Author.create(name="Find Me")
    found = Author.find_by_id(author.id)
    assert found.id == author.id
    assert found.name == author.name

def test_author_articles(setup_db):
    author = Author.find_by_name("Test Author")
    articles = author.articles()
    assert len(articles) >= 1
    assert any(a.title == "Test Article" for a in articles)

def test_author_magazines(setup_db):
    author = Author.find_by_name("Test Author")
    magazines = author.magazines()
    assert len(magazines) >= 1
    assert any(m.name == "Test Magazine" for m in magazines)