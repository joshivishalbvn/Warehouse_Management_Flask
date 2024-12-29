from app import create_app
from flask import redirect,url_for
from app.celery_config import celery_init_app

app = create_app()
celery = celery_init_app(app)

@app.route('/')
def dashboard():
    # return redirect(url_for('auth_bp.login')) if not current_user.is_authenticated else render_template("index.html")
    return redirect(url_for('dashboard_bp.dashboard')) 

if __name__ == "__main__":
    app.run(port=5001)
