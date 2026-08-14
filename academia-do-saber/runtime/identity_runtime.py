import hashlib


def generate_learning_identity(payload: dict):
    raw = (
        f"{payload.get('email')}:"
        f"{payload.get('document')}:"
        f"{payload.get('university')}"
    )

    federation_id = hashlib.sha256(raw.encode()).hexdigest()

    trust_score = 50

    if payload.get("document"):
        trust_score += 20

    if payload.get("email"):
        trust_score += 10

    if payload.get("university"):
        trust_score += 20

    return {
        "federation_id": federation_id,
        "trust_score": min(trust_score, 100),
        "runtime": "academia-do-saber",
    }