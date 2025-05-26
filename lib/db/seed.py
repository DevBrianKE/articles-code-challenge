from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

# Clear and reseed DB logic here if needed (optional)

author1 = Author("Alice")
author1.save()

mag1 = Magazine("Tech World", "Technology")
mag1.save()

article1 = Article("Future of AI", author_id=author1.id, magazine_id=mag1.id)
article1.save()
