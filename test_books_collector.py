import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()

@pytest.mark.parametrize(
    "attribute,expected",
    [
        ("books_genre", {}),
        ("favorites", []),
        ("genre", ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']),
        ("genre_age_rating", ['Ужасы', 'Детективы'])
    ]
)
def test_collector_init_fields(collector, attribute, expected):
    value = getattr(collector, attribute)
    assert value == expected

def test_add_new_book_adds_book(collector):
    collector.add_new_book('Хоббит, или Туда и обратно')
    assert 'Хоббит, или Туда и обратно' in collector.books_genre

@pytest.mark.parametrize('name', ['', 'a' * 41])
def test_add_new_book_wrong_length_not_added(collector, name):
    collector.add_new_book(name)
    assert name not in collector.books_genre

def test_add_new_book_same_book_not_added_twice(collector):
    collector.add_new_book('Война и Мир')
    collector.add_new_book('Война и Мир')
    assert len(collector.get_books_genre()) == 1

def test_set_book_genre_sets_genre(collector):
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')
    assert collector.get_book_genre('Оно') == 'Ужасы'

def test_get_book_genre_returns_genre(collector):
    collector.add_new_book('Дюна')
    collector.set_book_genre('Дюна', 'Фантастика')
    assert collector.get_book_genre('Дюна') == 'Фантастика'

def test_get_books_with_specific_genre_returns_books(collector):
    collector.add_new_book('Дюна')
    collector.add_new_book('1984')
    collector.set_book_genre('Дюна', 'Фантастика')
    collector.set_book_genre('1984', 'Фантастика')
    books = collector.get_books_with_specific_genre('Фантастика')
    assert 'Дюна' in books and '1984' in books

def test_get_books_with_specific_genre_no_books(collector):
    collector.add_new_book('Ревизор')
    collector.set_book_genre('Ревизор', 'Комедии')
    books = collector.get_books_with_specific_genre('Фантастика')
    assert books == []

def test_get_books_genre_returns_dict(collector):
    collector.add_new_book('Грозовой перевал')
    assert type(collector.get_books_genre()) == dict

def test_get_books_for_children_exclude_age_rating(collector):
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')
    books = collector.get_books_for_children()
    assert 'Оно' not in books

def test_add_book_in_favorites_adds_book(collector):
    collector.add_new_book('Степной волк')
    collector.add_book_in_favorites('Степной волк')
    assert 'Степной волк' in collector.favorites

def test_add_book_in_favorites_not_added_twice(collector):
    collector.add_new_book('Война и Мир')
    collector.add_book_in_favorites('Война и Мир')
    collector.add_book_in_favorites('Война и Мир')
    assert len(collector.get_list_of_favorites_books()) == 1

def test_delete_book_from_favorites_removes_book(collector):
    collector.add_new_book('Оно')
    collector.add_book_in_favorites('Оно')
    collector.delete_book_from_favorites('Оно')
    assert 'Оно' not in collector.favorites

def test_get_list_of_favorites_books_returns_list(collector):
    collector.add_new_book('1984')
    collector.add_book_in_favorites('1984')
    favorites = collector.get_list_of_favorites_books()
    assert favorites[0] == '1984'
