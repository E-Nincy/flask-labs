from blogger import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create tables if they don’t exist
    app.run(debug=True)
