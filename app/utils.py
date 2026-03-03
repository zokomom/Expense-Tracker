from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(received_pwd, hashed_pwd):
    return pwd_context.verify(received_pwd, hashed_pwd)
