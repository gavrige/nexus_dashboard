from app import create_app

app = create_app()

if __name__ == '__main__':
    # Note: debug=True is for development only.
    # In production, use a proper WSGI server like Gunicorn.
    app.run(debug=True)