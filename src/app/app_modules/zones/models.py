from flask import url_for
from app import db
from app.app_modules.base.models import BaseModel


class Zone(BaseModel):

    __tablename__ = 'Zone'

    ACTIVE = "active"
    INACTIVE = "inactive"
    
    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    )
    
    name            = db.Column(db.String(100), nullable=False)
    status          = db.Column(db.String(100), nullable=True)
    warehouse_id    = db.Column(db.Integer, db.ForeignKey('Warehouse.id'), nullable=True)
    warehouse       = db.relationship('Warehouse', backref=db.backref('warehouse_zone', lazy=True))

    def __repr__(self):
        return self.name
    
    @property
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, '')