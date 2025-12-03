"""
Программа для генерации рекомендаций фильмов на основе истории просмотров других пользователей.
Использует простой алгоритм коллаборативной фильтрации, который определяет,
на каких пользователей текущий пользователь похож, и рекомендует фильмы, которые эти пользователи смотрели,
но текущий — ещё нет.

Основная логика работы:
1. Загружается список фильмов (ID и названия).
2. Загружается история просмотров многих пользователей.
3. Пользователь вводит ID фильмов, которые он уже смотрел.
4. Программа ищет пользователей с похожей историей просмотров (совпадение >= 50%).
5. Собираются фильмы, которые похожие пользователи смотрели, а текущий — нет.
6. Формируется рекомендация: выбирается фильм с максимальным суммарным "весом" совпадений.
7. Выводится название рекомендованного фильма.

Программа разделена на несколько классов:
- Movie — сущность фильма.
- MovieRepository — загрузка и хранение фильмов.
- HistoryRepository — загрузка истории просмотров.
- Recommender — алгоритм рекомендаций.
- main() — точка входа, работа с вводом пользователя.
"""




from typing import List, Dict, Set

MOVIES_FILE = "movies.txt"
HISTORY_FILE = "history.txt"


class Movie:
    """
    Класс для хранения информации о фильме.

    Атрибуты:
        movie_id (int): Уникальный идентификатор фильма.
        title (str): Название фильма.
    """
    def __init__(self, movie_id: int, title: str):
        """
        Инициализация объекта Movie.

        Аргументы:
            movie_id (int): Уникальный идентификатор фильма.
            title (str): Название фильма.
        """
        self.movie_id = movie_id
        self.title = title

    def __repr__(self):
        """
        Строковое представление объекта Movie.

        Возвращает:
            str: Строка вида Movie(id, title)
        """
        return f"Movie({self.movie_id}, {self.title})"


class MovieRepository:
    """
    Репозиторий для хранения и получения фильмов.

    Методы позволяют загружать фильмы из файла и получать название фильма по ID.
    """
    def __init__(self, path: str = MOVIES_FILE):
        """
        Загружает фильмы из текстового файла.

        Аргументы:
            path (str): Путь к файлу с фильмами.
        """
        self.movies: Dict[int, Movie] = {}
        self._load(path)

    def _load(self, path: str):
        """
        Внутренний метод для чтения файла фильмов.

        Каждая строка должна быть в формате:
            <movie_id>,<title>

        Аргументы:
            path (str): Путь к файлу с фильмами.
        """
        with open(path, encoding="utf-8") as f:
            for line in f:
                movie_id, title = line.strip().split(",", 1)
                self.movies[int(movie_id)] = Movie(int(movie_id), title)

    def get_title(self, movie_id: int) -> str:
        """
        Возвращает название фильма по его ID.

        Аргументы:
            movie_id (int): Идентификатор фильма.

        Возвращает:
            str: Название фильма.

        Исключения:
            KeyError: Если фильма с таким ID нет в репозитории.
        """
        return self.movies[movie_id].title


class HistoryRepository:
    """
    Репозиторий истории просмотров пользователей.

    Методы позволяют загружать истории просмотров из файла и получать их для рекомендаций.
    """
    def __init__(self, path: str = HISTORY_FILE):
        """
        Загружает историю просмотров из текстового файла.

        Каждая строка файла — это список идентификаторов фильмов
        просмотренных одним пользователем, разделённые запятыми.

        Аргументы:
            path (str): Путь к файлу с историей просмотров.
        """
        self.history: List[List[int]] = []
        self._load(path)

    def _load(self, path: str):
        """
        Внутренний метод для чтения файла истории просмотров.

        Аргументы:
            path (str): Путь к файлу истории просмотров.
        """
        with open(path, encoding="utf-8") as f:
            for line in f:
                ids = [int(x) for x in line.strip().split(",") if x]
                self.history.append(ids)

    def get_all(self) -> List[List[int]]:
        """
        Возвращает список всех просмотров пользователей.

        Возвращает:
            List[List[int]]: Список списков идентификаторов фильмов.
        """
        return self.history


class Recommender:
    """
    Класс для генерации рекомендаций фильмов.

    Алгоритм рекомендаций основан на user-user collaborative filtering:
        1. Находит пользователей с похожими просмотрами (>=50% совпадения).
        2. Исключает фильмы, которые пользователь уже видел.
        3. Суммирует веса совпадений для оставшихся фильмов.
        4. Выбирает фильм с максимальным суммарным весом.
    """
    def __init__(self, movie_repo: MovieRepository, history_repo: HistoryRepository):
        """
        Инициализация класса рекомендаций.

        Аргументы:
            movie_repo (MovieRepository): Репозиторий фильмов.
            history_repo (HistoryRepository): Репозиторий истории просмотров.
        """
        self.movie_repo = movie_repo
        self.history_repo = history_repo

    def overlap_weight(self, user_movies: Set[int], other_movies: Set[int]) -> float:
        """
        Вычисляет "вес совпадения" между двумя пользователями.

        Вес = доля фильмов текущего пользователя, которые встречаются у другого пользователя.

        Аргументы:
            user_movies (Set[int]): Множество фильмов текущего пользователя.
            other_movies (Set[int]): Множество фильмов другого пользователя.

        Возвращает:
            float: Вес совпадения (0.0 - 1.0)
        """
        if not user_movies:
            return 0
        overlap = len(user_movies & other_movies)
        return overlap / len(user_movies)

    def recommend(self, user_input: List[int]) -> str:
        """
        Формирует рекомендацию фильма для пользователя.

        Алгоритм:
            1. Преобразует введённый список фильмов в множество.
            2. Проходит по истории всех пользователей.
            3. Выбирает пользователей с весом совпадения >=0.5.
            4. Формирует кандидатов (фильмы, которых пользователь ещё не видел).
            5. Суммирует веса для каждого кандидата.
            6. Возвращает фильм с максимальным суммарным весом.

        Аргументы:
            user_input (List[int]): Список идентификаторов фильмов, которые посмотрел пользователь.

        Возвращает:
            str: Рекомендованный фильм или "Нет рекомендаций", если подходящих нет.
        """
        user_set = set(user_input)
        history = self.history_repo.get_all()

        weighted_candidates: Dict[int, float] = {}

        for record in history:
            record_set = set(record)

            weight = self.overlap_weight(user_set, record_set)
            if weight < 0.5:
                continue

            candidates = record_set - user_set

            for movie_id in candidates:
                weighted_candidates[movie_id] = weighted_candidates.get(movie_id, 0) + weight

        if not weighted_candidates:
            return "Нет рекомендаций"

        best = max(weighted_candidates.items(), key=lambda x: x[1])[0]
        return self.movie_repo.get_title(best)


def main():
    """
    Основная функция для запуска программы.

    Пользователь вводит список просмотренных фильмов через запятую,
    программа выводит рекомендацию фильма.
    """
    user_input = input("Введите фильмы через запятую: ").strip()
    user_movies = [int(x) for x in user_input.split(",")]

    movie_repo = MovieRepository()
    history_repo = HistoryRepository()
    recommender = Recommender(movie_repo, history_repo)

    print(recommender.recommend(user_movies))


if __name__ == "__main__":
    main()
