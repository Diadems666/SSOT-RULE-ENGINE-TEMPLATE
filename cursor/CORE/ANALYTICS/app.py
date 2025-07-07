from flask import Flask, render_template
from .api.kg_routes import kg_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(kg_bp)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True) 