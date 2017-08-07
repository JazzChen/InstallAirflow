import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'yourname'
user.email = 'jazz.chen@xxx.com'
user.password = 'yourpasswd'
session = settings.Session()
session.add(user)
session.commit()
session.close()
