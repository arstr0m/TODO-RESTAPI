from jose import jwt, JWTError
import consts

#
def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, consts.SECRET_KEY, algorithms=[consts.ALGORITHM])
        return payload
    except JWTError:
        return None
