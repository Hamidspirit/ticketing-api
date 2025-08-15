from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import db, Ticket
from ..utils.validators import (
    require_json_keys,
    validate_status,
    validate_priority
    )
from ..utils.errors import InvalidInputError

ticket_bp = Blueprint("ticket", __name__)

@ticket_bp.post("/ticket")
@jwt_required
def create_ticket():
    data = request.get_json(silent=True) or {}
    require_json_keys(data, ["title", "description", "priority"])

    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()
    priority = (data.get("priority") or "").strip().lower()

    if not title:
        raise InvalidInputError("Title is required")
    
    if not description:
        raise InvalidInputError("Description is required")
    
    validate_priority(priority)

    user_id = get_jwt_identity()
    ticket = Ticket(title=title, description=description, priority=priority, user_id=user_id)
    db.session.add(ticket)
    db.session.commit()
    return jsonify({"ticket_id": ticket.id, "created_at": ticket.created_at.isoformat()})

@ticket_bp.get("/ticket")
@jwt_required
def list_tickets():
    # filter via query params: ?status=open&priority=high
    user_id = get_jwt_identity()
    status = (request.args.get("status") or "").strip().lower()
    priority = (request.args.get("priority") or "").strip().lower()

    query = Ticket.query.filter_by(user_id=user_id)

    if status:
        validate_status(status)
        query.filter(Ticket.status == status)
    
    if priority:
        validate_priority(priority)
        query.filter(Ticket.priority == priority)
    
    tickets = query.order_by(Ticket.created_at.desc()).all()
    return jsonify({"tickets": [t.to_dict() for t in tickets]}), 200