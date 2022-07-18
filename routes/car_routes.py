from flask.views import MethodView

from domain.car_client import create_car, get_one_car, get_cars, update_car, delete_car
from utils.authentication import check_token


class Cars(MethodView):
    """
    The class represents a group of endpoints dealing with cars
    """
    decorators = [check_token]

    def post(self):
        """
        Create car
        """
        return create_car()

    def get(self, car_id=None):
        """
        Get cars
        """
        if car_id is None:
            return get_cars()
        return get_one_car(car_id)

    def patch(self, car_id):
        """
        Update a car
        """
        return update_car(car_id)

    def delete(self, car_id):
        """
        Delete a car
        """
        return delete_car(car_id)
