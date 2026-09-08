import json
import re
import uuid
from datetime import datetime

from backend.search import MODEL


UPLOADS = {}
MAX_UPLOAD_BYTES = 10 * 1024 * 1024

WHATSAPP_PATTERNS = (
    re.compile(r"^\[?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),?\s+(\d{1,2}:\d{2}(?:\s?[APMapm]{2})?)\]?\s*[-:]\s*([^:]+):\s*(.*)$"),
    re.compile(r"^(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),\s*(\d{1,2}:\d{2})\s*-\s*([^:]+):\s*(.*)$"),
)


def _parse_timestamp(date_text, time_text):
    date_text = date_text.replace("/", "-")
    for date_format in ("%d-%m-%Y", "%m-%d-%Y", "%d-%m-%y", "%m-%d-%y"):
        for time_format in ("%H:%M", "%I:%M %p", "%I:%M%p"):
            try:
                return datetime.strptime(
                    f"{date_text} {time_text.upper().replace('  ', ' ')}",
                    f"{date_format} {time_format}",
                ).isoformat()
            except ValueError:
                continue
    raise ValueError(f"Unsupported date format: {date_text} {time_text}")


def _normalise_messages(items):
    messages = []
    for item in items:
        sender = str(item.get("sender", item.get("author", ""))).strip()
        text = str(item.get("message", item.get("text", ""))).strip()
        timestamp = item.get("timestamp", item.get("date"))
        if not sender or not text or not timestamp:
            continue
        try:
            timestamp = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00")).replace(tzinfo=None).isoformat()
        except ValueError:
            continue
        messages.append({"id": len(messages) + 1, "sender": sender, "timestamp": timestamp, "message": text})
    return messages


def parse_chat_file(filename, raw_content):
    decoded = raw_content.decode("utf-8-sig", errors="replace")
    if filename.lower().endswith(".json"):
        try:
            payload = json.loads(decoded)
        except json.JSONDecodeError as error:
            raise ValueError("That JSON file could not be read.") from error
        items = payload if isinstance(payload, list) else payload.get("messages", [])
        messages = _normalise_messages(items)
    else:
        messages = []
        for line in decoded.splitlines():
            match = next((pattern.match(line) for pattern in WHATSAPP_PATTERNS if pattern.match(line)), None)
            if not match:
                if messages and line.strip():
                    messages[-1]["message"] += f"\n{line.strip()}"
                continue
            date_text, time_text, sender, text = match.groups()
            try:
                timestamp = _parse_timestamp(date_text, time_text)
            except ValueError:
                continue
            messages.append({"id": len(messages) + 1, "sender": sender.strip(), "timestamp": timestamp, "message": text.strip()})

    if not messages:
        raise ValueError("No readable messages were found. Upload a WhatsApp .txt export or a messages JSON file.")
    return messages


def create_upload(messages, user_id):
    chat_id = uuid.uuid4().hex
    embeddings = MODEL.encode(
        [message["message"] for message in messages],
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    UPLOADS[chat_id] = {
        "messages": messages,
        "embeddings": embeddings,
        "user_id": user_id,
        "created_at": datetime.utcnow(),
    }
    return chat_id


def get_upload(chat_id, user_id):
    upload = UPLOADS.get(chat_id)
    return upload if upload and upload["user_id"] == user_id else None