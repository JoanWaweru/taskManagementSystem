from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
# run the Flask application in debug mode on port 5000 by default
