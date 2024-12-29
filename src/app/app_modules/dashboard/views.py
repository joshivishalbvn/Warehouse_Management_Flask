from app.app_modules.base.base_views import BaseListView

class DashboardView(BaseListView):
    template_name = 'dashboard/dashboard.html' 

    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["name"] = "Hello"
        return ctx
    