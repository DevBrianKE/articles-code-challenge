import pytest
from lib.models.author import Author

def test_author_save_and_find():
    author = Author("Test Author")
    author.save()
    found = Author.find_by_id(author.id)
    assert found.name == "Test Author"
