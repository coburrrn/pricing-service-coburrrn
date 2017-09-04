import uuid

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User: {}".format(self.email)

    @staticmethod
    def login_valid(email, password):
        """
        This method verifies that an email/pw combo is valid
        :param email: user's email
        :param password: a sha512 hashed password
        :return: true if valid else false
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            raise UserErrors.UserNotExistError("Your user does not exist")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was wrong")
        return True

    @staticmethod
    def register_user(email, password):
        """
        register a user using email and password
        :param email:
        :param password:
        :return: true if regsiters successfully
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("Email already exists")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email address is invalid")
        User(email, Utils.hash_password(password)).save()
        return True

    def save(self):
        Database.insert(collection=UserConstants.COLLECTION,
                        data=self.json())

    def json(self):
        return {
            "_id": self.password,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**(Database.find_one(collection=UserConstants.COLLECTION, query={"email": email})))

    def get_alerts(self):
        return Alert.find_by_email(self.email)