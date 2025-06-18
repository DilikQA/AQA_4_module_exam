import pytest
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT


class TestMoviesAPI:

    def test_get_movies(self, api_manager):
        """
        Получение фильмов с параметрами по умолчанию.
        """
        response = api_manager.movies_api.get_movies()
        data = response.json()

        assert response.status_code == 200
        assert "movies" in data


    def test_create_movie(self, api_manager, movie_data):
        """
        Тест на создание нового фильма.
        """
        response = api_manager.movies_api.create_movie(data=movie_data)
        response_data = response.json()

        assert response.status_code == 201
        assert response_data["name"] == movie_data["name"]
        assert "id" in response_data


    def test_update_movie(self, api_manager, movie_data, updated_data):
        """
        Обновление существующего фильма.
        """
        response = api_manager.movies_api.create_movie(data=movie_data)

        assert response.status_code == 201

        created_movie = response.json()
        response = api_manager.movies_api.update_movie(movie_id=created_movie['id'],data=updated_data)

        assert response.status_code == 200

        updated_movie = response.json()

        assert created_movie ["name"] != updated_movie['name']
        assert created_movie ["genreId"] != updated_movie["genreId"]
        assert created_movie ["price"] != updated_movie["price"]

    def test_get_movie_by_id(self, api_manager, movie_data):
        """
        Создаем фильм и получаем его по ID.
        """
        created= api_manager.movies_api.create_movie(data=movie_data).json()
        movie_id = created["id"]
        response = api_manager.movies_api.get_movie_by_id(movie_id)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["id"] == movie_id



    def test_delete_movie(self, api_manager, movie_data):
        """
        Удаление фильма.
        """
        created = api_manager.movies_api.create_movie(data=movie_data).json()
        movie_id = created["id"]

        response = api_manager.movies_api.delete_movie(movie_id)

        assert response.status_code in [200, 204]

        # Повторная попытка получения фильма должна вернуть 404
        response = api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)

        assert response.status_code == 404

    def test_get_movies_with_filters(self, api_manager):
        """
        Проверка фильтрации по жанру и локации.
        """
        response = api_manager.movies_api.get_movie_by_id(14)
        data = response.json()

        assert response.status_code == 200
        assert data["location"] == "MSK"
        assert data["name"] == "Зеленая миля"

    def test_get_movies_invalid_location(self, api_manager):
        """
        Негативный тест: передаем недопустимую локацию.
        """
        params = {
            "locations": "LA"  # допустимы только MSK, SPB
        }

        response = api_manager.movies_api.get_movies(params=params, expected_status=400)
        data = response.json()

        assert response.status_code == 400
        assert data["error"] == "Bad Request"



