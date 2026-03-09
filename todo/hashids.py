from hashids import Hashids

from django.conf import settings


hashids = Hashids(
    salt=settings.HASHID_KEY,
    min_length=settings.HASHID_MIN_LENGTH
)


def encode_id(id: int) -> str:
    """
    id to hashid
    """

    return hashids.encode(id)


def decode_id(hashid: str) -> int | None:
    """
    hashid to id
    """

    decoded = hashids.decode(hashid)
    return decoded[0] if decoded else None
