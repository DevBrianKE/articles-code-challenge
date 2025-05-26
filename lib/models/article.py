from lib.db.connection import get_connection

class Article:
    def __init__(self, id=None, title=None, author_id=None, magazine_id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        if self.title is None or self.author_id is None or self.magazine_id is None:
            raise ValueError("Article title, author_id, and magazine_id cannot be None")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute(
                """INSERT INTO articles (title, author_id, magazine_id) 
                   VALUES (?, ?, ?) RETURNING id""",
                (self.title, self.author_id, self.magazine_id)
            )
            self.id = cursor.fetchone()[0]
        else:
            cursor.execute(
                """UPDATE articles SET title = ?, author_id = ?, magazine_id = ? 
                   WHERE id = ?""",
                (self.title, self.author_id, self.magazine_id, self.id)
            )
        conn.commit()
        conn.close()
    
    @classmethod
    def create(cls, title, author, magazine):
        article = cls(title=title, author_id=author.id, magazine_id=magazine.id)
        article.save()
        return article
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            return None
        return cls(id=row['id'], title=row['title'], 
                  author_id=row['author_id'], magazine_id=row['magazine_id'])
    
    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(id=row['id'], title=row['title'], 
                author_id=row['author_id'], magazine_id=row['magazine_id']) 
                for row in rows]
    
    @classmethod
    def find_by_author(cls, author):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author.id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(id=row['id'], title=row['title'], 
                author_id=row['author_id'], magazine_id=row['magazine_id']) 
                for row in rows]
    
    @classmethod
    def find_by_magazine(cls, magazine):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine.id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(id=row['id'], title=row['title'], 
                author_id=row['author_id'], magazine_id=row['magazine_id']) 
                for row in rows]
    
    def author(self):
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)
    
    def magazine(self):
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)