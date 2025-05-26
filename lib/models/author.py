from lib.db.connection import get_connection

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def save(self):
        if self.name is None:
            raise ValueError("Author name cannot be None")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute(
                "INSERT INTO authors (name) VALUES (?) RETURNING id",
                (self.name,)
            )
            self.id = cursor.fetchone()[0]
        else:
            cursor.execute(
                "UPDATE authors SET name = ? WHERE id = ?",
                (self.name, self.id)
            )
        conn.commit()
        conn.close()
    
    @classmethod
    def create(cls, name):
        author = cls(name=name)
        author.save()
        return author
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            return None
        return cls(id=row['id'], name=row['name'])
    
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            return None
        return cls(id=row['id'], name=row['name'])
    
    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Article(id=row['id'], title=row['title'], 
                       author_id=row['author_id'], magazine_id=row['magazine_id']) 
                for row in rows]
    
    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        
        from lib.models.magazine import Magazine
        return [Magazine(id=row['id'], name=row['name'], category=row['category']) 
                for row in rows]
    
    def add_article(self, magazine, title):
        from lib.models.article import Article
        return Article.create(title, self, magazine)
    
    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT category FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [row['category'] for row in rows]