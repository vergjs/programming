import unittest
import os
from src.lab4.Task_film import MovieRepository, HistoryRepository, Recommender

class RecommenderTest(unittest.TestCase):
    """
    Модульные тесты для системы рекомендаций фильмов.
    """

    def setUp(self):
        """
        Создание временных файлов с фильмами и историей просмотров
        для каждого теста.
        """
        # Файл с фильмами
        self.movies_file = "test_movies.txt"
        with open(self.movies_file, "w", encoding="utf-8") as f:
            f.write("1,Мстители: Финал\n")
            f.write("2,Хатико\n")
            f.write("3,Дюна\n")
            f.write("4,Унесенные призраками\n")

        # Файл с историей просмотров
        self.history_file = "test_history.txt"
        with open(self.history_file, "w", encoding="utf-8") as f:
            f.write("2,1,3\n")
            f.write("1,4,3\n")
            f.write("2,2,2,2,2,3\n")

        # Репозитории и рекомендатель
        self.movie_repo = MovieRepository(self.movies_file)
        self.history_repo = HistoryRepository(self.history_file)
        self.recommender = Recommender(self.movie_repo, self.history_repo)

    def tearDown(self):
        """
        Удаление временных файлов после каждого теста.
        """
        os.remove(self.movies_file)
        os.remove(self.history_file)

    def test_recommend_basic(self):
        """Проверка стандартной рекомендации [2,4] → Дюна"""
        result = self.recommender.recommend([2, 4])
        self.assertEqual(result, "Дюна")

    def test_recommend_single_movie(self):
        """Проверка рекомендации для одного фильма [4]"""
        result = self.recommender.recommend([4])
        self.assertIn(result, ["Мстители: Финал", "Дюна"])

    def test_recommend_no_matches(self):
        """Проверка, когда нет похожих пользователей [1,2,3,4]"""
        result = self.recommender.recommend([1, 2, 3, 4])
        self.assertEqual(result, "Нет рекомендаций")

    def test_overlap_weight(self):
        """Проверка метода вычисления веса совпадения"""
        w_full = self.recommender.overlap_weight({1,2}, {1,2})
        w_half = self.recommender.overlap_weight({1,2}, {2,3})
        w_none = self.recommender.overlap_weight({1,2}, {3,4})

        self.assertEqual(w_full, 1.0)
        self.assertEqual(w_half, 0.5)
        self.assertEqual(w_none, 0.0)

    def test_recommend_multiple_candidates_weighted(self):
        """Проверка суммарного веса кандидатов [2] → Дюна"""
        result = self.recommender.recommend([2])
        self.assertEqual(result, "Дюна")


if __name__ == "__main__":
    unittest.main()
