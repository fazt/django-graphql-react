import graphene
from graphene_django import DjangoObjectType
from books.models import Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "desc")

class Query(graphene.ObjectType):
    books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.Int())

    def resolve_books(self, info):
        return Book.objects.all()

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)

class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return DeleteBook(message="Book deleted")

class Mutation(graphene.ObjectType):
    create_book = graphene.Field(BookType, title=graphene.String(), desc=graphene.String())
    update_book = graphene.Field(BookType, id=graphene.Int(), title=graphene.String(), desc=graphene.String())
    deleteBook = DeleteBook.Field()

    def resolve_create_book(self, info, title, desc):
        book = Book(title=title, desc=desc)
        book.save()
        return book

    def resolve_update_book(self, info, id, title, desc):
        book = Book.objects.get(pk=id)
        book.title = title
        book.desc = desc
        book.save()
        return book

schema = graphene.Schema(query=Query, mutation=Mutation)