from domain.user_car_client import get_users_and_cars, create_relation_user_cars

from flask.views import MethodView


class UserCar(MethodView):
    """
    The class represents a group of endpoints dealing with owner_user relation
    """

    def get(self):
        """
        get all users and their cars
        """
        return get_users_and_cars()

    def post(self, user_id):
        """
        Create a relation between a user and cars
        """
        return create_relation_user_cars(user_id)

    def patch(self, user_id):
        """
        Update a relation between a user and cars
        """
        return update_relation_user_cars(user_id)
