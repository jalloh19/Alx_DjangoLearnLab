
**update.md**
```markdown
# Update Book

```python
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.save()
book
# <Book: Nineteen Eighty-Four by George Orwell (1949)>
