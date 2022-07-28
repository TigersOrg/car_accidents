from models.car_model import CarSchema

from domain.user_client import get_all_users, get_one_user, create_user, update_user, delete_user
from utils.authentication import check_token

from flask.views import MethodView


car_schema = CarSchema()


class Users(MethodView):
    """
    The class represents a group of endpoints dealing with users
    """
    decorators = [check_token]

    def get(self, user_id=None):
        """
        Get users
        """
        if not user_id:
            return get_all_users()
        return get_one_user(user_id)

    def post(self):
        """
        create a user
        """
        return create_user()

    def patch(self, user_id):
        """
        Update an existing user
        """
        return update_user(user_id)

    def delete(self, user_id):
        """
         Delete an existing user
        """
        return delete_user(user_id)

