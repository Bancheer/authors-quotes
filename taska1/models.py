from mongoengine import connect, Document, StringField, DateTimeField, ReferenceField, ListField
import json

connect(db='my_mongodb', host='mongodb://localhost:27017')

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)

def load_data():
    with open('authors.json', 'r', encoding='utf-8') as f:
        authors_data = json.load(f)
        for author_data in authors_data:
            author = Author(**author_data)
            author.save()

    with open('quotes.json', 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            quote = Quote(tags=quote_data['tags'], author=author, quote=quote_data['quote'])
            quote.save()

    for author_info in authors_data:
        author = Author(
            fullname=author_info['fullname'],
            born_date=author_info['born_date'],
            born_location=author_info['born_location'],
            description=author_info['description']
        )
        author.save()

    for quote_info in quotes_data:
        author_name = quote_info['author']
        author = Author.objects(fullname=author_name).first()
        if author:
            quote = Quote(
                tags=quote_info['tags'],
                author=author,
                quote=quote_info['quote']
            )
            quote.save()

def search_quotes():
    while True:
        command = input("Введіть команду: ").strip()

        if command.startswith('name:'):
            author_name = command.split(':')[1].strip()
            author = Author.objects(fullname=author_name).first()
            if author:
                quotes = Quote.objects(author=author)
                for q in quotes:
                    print(f"{q.quote}")
            else:
                print("Автор не знайдений.")

        elif command.startswith('tag:'):
            tag = command.split(':')[1].strip()
            quotes = Quote.objects(tags=tag)
            for q in quotes:
                print(f"{q.quote}")

        elif command.startswith('tags:'):
            tags = command.split(':')[1].strip().split(',')
            quotes = Quote.objects(tags__in=tags)
            for q in quotes:
                print(f"{q.quote}")

        elif command == 'exit':
            break

        else:
            print("Невірна команда. Спробуйте ще раз.")

if __name__ == "__main__":
    load_data()
    search_quotes() 