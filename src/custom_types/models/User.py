from .mongo_model.MongoModel import MongoModel


class User(MongoModel):
  username: str
  mail_password: str
  full_name: str
  
  def get_cleaned(self):
    return {
      "username": self.username,
      "full_name": self.full_name
    }
  
  @staticmethod
  def collection() -> str:
    return "users"
