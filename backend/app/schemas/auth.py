from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    Authentication token response.
    """

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class LoginResponse(TokenResponse):
    """
    Login response.
    """

    pass


class RefreshRequest(BaseModel):
    """
    Refresh token request.
    """

    refresh_token: str


class LogoutRequest(BaseModel):
    """
    Logout request.
    """

    refresh_token: str