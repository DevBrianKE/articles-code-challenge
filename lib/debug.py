from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database

def debug_session():
    print("Starting debug session...")
    print("Seeding database...")
    seed_database()
    
    print("\nSample queries:")
    
    # Get all authors
    authors = Author.find_by_name("John Doe")
    print(f"Authors named John Doe: {authors.name if authors else 'None'}")
    
    # Get all magazines
    magazines = Magazine.find_by_category("Technology")
    print(f"Technology magazines: {[m.name for m in magazines]}")
    
    # Get articles by author
    author = Author.find_by_name("John Doe")
    if author:
        articles = author.articles()
        print(f"Articles by John Doe: {[a.title for a in articles]}")
    
    # Get magazines by author
    if author:
        magazines = author.magazines()
        print(f"Magazines John Doe writes for: {[m.name for m in magazines]}")
    
    # Get contributing authors for a magazine
    magazine = Magazine.find_by_name("Science Weekly")
    if magazine:
        contributors = magazine.contributors()
        print(f"Contributors to Science Weekly: {[a.name for a in contributors]}")
    
    print("\nDebug session complete.")

if __name__ == '__main__':
    debug_session()