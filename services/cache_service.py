import time
from threading import Lock
from models import User

class AppCache:
    def __init__(self) -> None:
        self.logged_in_users = {}
        self.logged_in_ttl = 600 # expired in 600s
        self.lock = Lock()

    def add_user(self, user_id, user: User):
        with self.lock:
            self.logged_in_users[user_id] = {
                "last_login_time": time.time() + self.logged_in_ttl,
                "user": user
            }

    def remove_user(self, user_id):
        with self.lock:
            if user_id in self.logged_in_users:
                del self.logged_in_users[user_id]

    def is_user_logged_in(self, user_id):
        with self.lock:
            if user_id in self.logged_in_users:
                if self.logged_in_users[user_id].get("last_login_time", 0) > time.time():
                    return True
                else:
                    del self.logged_in_users[user_id]
            return False
        
    def is_user_manager(self, user_id):
        if not self.is_user_logged_in(user_id):
            return False
        user = self.logged_in_users[user_id].get("user", None)
        if user:
            return user.permission == 1
        return False
    
    def is_user_customer(self, user_id):
        if not self.is_user_logged_in(user_id):
            return False
        user = self.logged_in_users[user_id].get("user", None)
        if user:
            return user.permission == 0
        return False

app_cache = AppCache()
