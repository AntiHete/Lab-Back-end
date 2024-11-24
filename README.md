# Backend-labs

### *Need installed:* 
- Python
- Flask (pip install flask)
- psycopg2-binary (pip install psycopg2-binary)
- Flask-SQLAlchemy (pip install flask-sqlalchemy)
- Flask-Migrate (pip install Flask-Migrate)
- Flask-Smorest (pip install flask-smorest)

### *Use these commands in cmd:*
1. Create a virtual environment:
   - `.\env\Scripts\activate`
2. Create a directory for your project:
   - `mkdir my_flask_app`
   - `cd my_flask_app`
3. Clone the repository:
   - `git clone https://github.com/AntiHete/Lab-Back-end.git`
4. Navigate to the cloned repository:
   - `cd Lab-Back-end` 
5. Install dependencies:
   - `pip install -r requirements.txt`
6. Set up the database container with Docker (if needed):
   - `docker-compose up db` (to run PostgreSQL container)
7. Initialize migrations (create the migrations folder):
   - `flask db init`
8. Run the Flask application:
   - `flask --app app run --host 0.0.0.0 --port 5000` 

### Testing the API
You can test the API endpoints using Postman or similar tools by sending requests to:

- `http://localhost:5000/healthcheck` - to check if the server is running.
- `POST http://localhost:5000/user` - to create a new user.
- `GET http://localhost:5000/users` - to get all users.
- `GET http://localhost:5000/user/<int:user_id>` - to get a user by ID.
- `DELETE http://localhost:5000/user/<int:user_id>` - to delete a user by ID.
- `POST http://localhost:5000/category` - to create a new category.
- `GET http://localhost:5000/category` - to get all categories.
- `DELETE http://localhost:5000/category/<int:category_id>` - to delete a category by ID.
- `POST http://localhost:5000/record` - to create a new record (expense).
- `GET http://localhost:5000/record/<int:record_id>` - to get a record by ID.
- `DELETE http://localhost:5000/record/<int:record_id>` - to delete a record by ID.

### Database Configuration
The project uses PostgreSQL as the database, configured in `docker-compose.yaml`. Make sure the database container is running to connect with the app.

### Additional Information
- **Migrations**: We use Flask-Migrate for handling database migrations. After updating models, run `flask db migrate` and `flask db upgrade` to apply changes to the database schema.
- **Environment variables**: Use `.env` or configure environment variables like `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` for proper database connection.

###### Окрошко Ярослав ІО-26
