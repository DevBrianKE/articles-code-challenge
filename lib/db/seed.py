from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_database():
    # Clear existing data
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

    # Create authors
    author1 = Author.create(name="John Doe")
    author2 = Author.create(name="Jane Smith")
    author3 = Author.create(name="Bob Johnson")

    # Create magazines
    magazine1 = Magazine.create(name="Tech Today", category="Technology")
    magazine2 = Magazine.create(name="Science Weekly", category="Science")
    magazine3 = Magazine.create(name="Business Insights", category="Business")

    # Create articles
    Article.create("Python Programming", author1, magazine1)
    Article.create("Machine Learning", author1, magazine1)
    Article.create("Quantum Physics", author2, magazine2)
    Article.create("Neuroscience", author2, magazine2)
    Article.create("Stock Market", author3, magazine3)
    Article.create("Startup Funding", author3, magazine3)
    Article.create("AI Ethics", author1, magazine2)  # Cross-category
    Article.create("Tech Startups", author3, magazine1)  # Cross-category

    print("Database seeded successfully.")

if __name__ == '__main__':
    from lib.db.connection import get_connection
    seed_database()