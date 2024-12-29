from flask import Blueprint
from .views import CreateZoneView, ZoneUpdateView, ZoneDataTableView, DeleteZone , GetZoneAjax

zone_bp = Blueprint('zone_bp', __name__)

zone_bp.add_url_rule('/create-zone', view_func=CreateZoneView.as_view('create_zone'))
zone_bp.add_url_rule('/<int:id>/update-zone', view_func=ZoneUpdateView.as_view('update_zone'))
zone_bp.add_url_rule('/<int:id>/delete-zone/', view_func=DeleteZone.as_view('delete_zone'))
zone_bp.add_url_rule('/api/zone', view_func=ZoneDataTableView.as_view('zone_data_table'))
zone_bp.add_url_rule('/api/get-zone', view_func=GetZoneAjax.as_view('get_zone_ajax'))

