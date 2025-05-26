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

def test_article_creation(setup_db):
    author = Author.find_by_name("Test Author")
    magazine = Magazine.find_by_name("Test Magazine")
    article = Article.create("New Article", author, magazine)
    assert article.id is not None
    assert article.title == "New Article"
    assert article.author_id == author.id
    assert article.magazine_id == magazine.id

def test_find_article_by_id(setup_db):
    author = Author.find_by_name("Test Author")
    magazine = Magazine.find_by_name("Test Magazine")
    article = Article.create("Find Me", author, magazine)
    found = Article.find_by_id(article.id)
    assert found.id == article.id
    assert found.title == article.title

def test_article_author(setup_db):
    articles = Article.find_by_title("Test Article")
    assert len(articles) > 0
    article = articles[0]
    author = article.author()
    assert author.id is not None
    assert author.name == "Test Author"

def test_article_magazine(setup_db):
    articles = Article.find_by_title("Test Article")
    assert len(articles) > 0
    article = articles[0]
    magazine = article.magazine()
    assert magazine.id is not None
    assert magazine.name == "Test Magazine"