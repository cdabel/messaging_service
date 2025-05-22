from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MessageSchema(BaseModel):
    """
    This schema represents a single message sent or received by Hatch's API.
    - from_:       The sender (either SaaS customer or end-user contact)
    - to:          The recipient
    - type:        Messaging channel (e.g., 'sms', 'email', 'mms')
    - attachments: Optional list of attachment URLs
    - timestamp:   UTC datetime when the message was sent
    - provider_id: Optional id for inbound payloads only
    TODO: Assign message to a conversation once grouping logic is defined.
    """
    from_: str
    to: str
    type: str
    body: str
    attachments: Optional[List[str]] = None
    timestamp: Optional[datetime] = None
    provider_id: Optional[str] = None
