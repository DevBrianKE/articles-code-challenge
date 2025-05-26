import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture
def setup_db():
    # Setup database schema
    conn = get_connection()
    cursor = conn.cursor()
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
    """)
    
    # Create test data
    author1 = Author.create(name="Author 1")
    author2 = Author.create(name="Author 2")
    magazine = Magazine.create(name="Test Magazine", category="Test")
    Article.create("Article 1", author1, magazine)
    Article.create("Article 2", author1, magazine)
    Article.create("Article 3", author2, magazine)
    
    yield
    
    # Clean up
    cursor.execute("DROP TABLE IF EXISTS articles")
    cursor.execute("DROP TABLE IF EXISTS authors")
    cursor.execute("DROP TABLE IF EXISTS magazines")
    conn.commit()
    conn.close()

def test_magazine_creation(setup_db):
    magazine = Magazine.create(name="New Magazine", category="New")
    assert magazine.id is not None
    assert magazine.name == "New Magazine"
    assert magazine.category == "New"

def test_magazine_articles(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    articles = magazine.articles()
    assert len(articles) == 3
    titles = [a.title for a in articles]
    assert "Article 1" in titles
    assert "Article 2" in titles
    assert "Article 3" in titles

def test_magazine_contributors(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    contributors = magazine.contributors()
    assert len(contributors) == 2
    names = [a.name for a in contributors]
    assert "Author 1" in names
    assert "Author 2" in names

def test_magazine_article_titles(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    titles = magazine.article_titles()
    assert len(titles) == 3
    assert "Article 1" in titles
    assert "Article 2" in titles
    assert "Article 3" in titles