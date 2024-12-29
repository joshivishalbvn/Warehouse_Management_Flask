from flask import Blueprint
from .views import DashboardView

dashboard_bp = Blueprint('dashboard_bp', __name__)

dashboard_bp.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))
