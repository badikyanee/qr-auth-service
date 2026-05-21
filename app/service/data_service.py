from app.repository.data_repository import DataRepository

class DataService:
    def __init__(self, repo: DataRepository):
        self.repo = repo

    def create_data(self, text: str, user_id: int):
        return self.repo.create(text, user_id)

    def get_user_data(self, user_id: int):
        return self.repo.get_by_user(user_id)