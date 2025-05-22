from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from httpx import RequestError, HTTPStatusError
from tenacity import RetryError
from app.schemas.message import MessageSchema
from app.services.provider import send_to_provider
from app.services.messaging import save_message


router = APIRouter(
    prefix="/messages",
    tags=["messages"],
)


@router.post(
    "/send",
    response_model=MessageSchema,
    status_code=status.HTTP_201_CREATED,
)
async def send_message(payload: MessageSchema):
    """
    Accepts an outbound message payload, validates it,
    sends it to the provider, and persists it in the database.
    """
    try:
        result = await send_to_provider(payload)
    except HTTPStatusError as exc:
        if exc.response.status_code == 429:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded; please retry later."
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Upstream error {exc.response.status_code}"
        ) from exc
    except RetryError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Upstream provider retry failed: {exc}"
        ) from exc
    except RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Network error communicating with provider."
        ) from exc

    try:
        save_message(payload)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Something went wrong while saving your message. "
                "Please check your input — the recipient or content "
                "may be invalid or already used.")
        ) from exc
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while saving message."
        ) from exc

    return result
