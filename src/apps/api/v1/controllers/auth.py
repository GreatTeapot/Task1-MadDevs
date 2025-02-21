
from fastapi import APIRouter
from starlette.responses import Response

from api.dependencies.dependencies import AuthUOWDep, AuthServiceDep, RefreshDep, UserDep
from core.constants import REFRESH
from core.security import Security
from modules.responses.users import auth_res as responses
from modules.schemas.users.auth_schemas import TokenInfoSchema, LogoutResponseSchema, LoginRequestSchema

auth = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@auth.post(
    path="/login",
    summary="Login to user account (Authentication).",
    responses=responses.LOGIN_RESPONSES)
async def login(
        body: LoginRequestSchema,
        uow: AuthUOWDep,
        service: AuthServiceDep,
        response: Response,
) -> TokenInfoSchema:
    """
    Controller for logging into a user's account.

    Required arguments:
    * *`username`* or *`email`* *.

    * *`password`* - password input.
    """
    user = await service.user_authenticate(uow, body.credentials, body.password)
    access_token = Security.create_access_token(str(user.id))
    refresh_token = Security.create_refresh_token(str(user.id))

    response.set_cookie(key=REFRESH,
                        value=refresh_token,
                        httponly=True,
                        secure=False, )  # if https set to True
    return TokenInfoSchema(access_token=access_token)



# @auth.post(
#     path="/refresh",
#     summary="Get a new access token.",
#     responses=responses.REFRESH_RESPONSES,
# )
# async def get_new_access_token(
#     uow: AuthUOWDep,
#     service: AuthServiceDep,
#     refresh: RefreshDep,
# ) -> TokenInfoSchema:
#     """
#     Controller for renewing the access token.
#
#     Arguments:
#     * *`refresh_token`* - refresh token (*hidden*).
#     """
#     login = await service.get_user_for_update_tokens(uow, refresh)
#     access_token = Security.create_access_token(login)
#     return TokenInfoSchema(access_token=access_token)
#
#
#
# @auth.post(path="/logout", summary="Logout from user account.")
# async def logout_user(
#     current_user: UserDep,
#     response: Response,
# ) -> LogoutResponseSchema:
#     """Controller for logging out of a user account."""
#     # Later need to add a method that will log out all active sessions on this account
#     response.delete_cookie(REFRESH, httponly=True, secure=False)
#     return LogoutResponseSchema()