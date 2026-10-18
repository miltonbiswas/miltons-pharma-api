import os
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed


@dataclass(frozen=True)
class SupabaseUser:
    id: str
    email: str

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


class SupabaseTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = get_authorization_header(request).split()

        if not header:
            return None

        if len(header) != 2 or header[0].lower() != b"bearer":
            raise AuthenticationFailed("Invalid authorization header.")

        token = header[1].decode("utf-8")

        supabase_url = os.getenv("SUPABASE_URL", "").rstrip("/")
        publishable_key = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")

        parsed_url = urlparse(supabase_url)

        if parsed_url.scheme != "https" or not parsed_url.hostname or not publishable_key:
            raise AuthenticationFailed("Authentication service is not configured.")

        try:
            response = httpx.get(
                f"{supabase_url}/auth/v1/user",
                headers={
                    "apikey": publishable_key,
                    "Authorization": f"Bearer {token}",
                },
                timeout=5.0,
            )
        except httpx.RequestError as exc:
            raise AuthenticationFailed("Authentication service is temporarily unavailable.") from exc

        if response.status_code in (401, 403):
            raise AuthenticationFailed("Invalid or expired access token.")

        if response.status_code != 200:
            raise AuthenticationFailed("Could not verify the access token.")

        try:
            data = response.json()
            user_id = data.get("id")
            email = data.get("email")
        except ValueError as exc:
            raise AuthenticationFailed("Invalid authentication response.") from exc

        if not user_id or not email:
            raise AuthenticationFailed("The authenticated account has no valid identity.")

        return SupabaseUser(id=user_id, email=email), token

    def authenticate_header(self, request):
        return "Bearer"