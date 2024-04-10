# Server Resource Monitoring Application

This web application is designed to monitor the resource usage of different programs on a server. It allows users to create accounts, log in, and view resource usage data. Admin users have additional privileges to manage user accounts.

## Features

- User authentication system with standard and admin roles.
- Real-time monitoring of server resource usage, including CPU, memory, and disk.
- Historical data analysis and visualization.
- Admin dashboard for advanced monitoring control.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Clone the repository to your local machine:```bash
git clone https://github.com/LunaBarrett/Server-program-resource-manager-QA.git
cd Server-program-resource-manager-QA 
```2. Create a virtual environment and activate it:```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```3. Install the required packages:```bash
pip install -r requirements.txt
```4. Set up the environment variables:

Create a `.env` file in the root directory of the project and add the following content:```env
SECRET_KEY=your_secret_key
```Replace `your_secret_key` with a strong, random key.

5. Initialize the database:```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```6. Run the application:```bash
flask run
```The application will be accessible at `http://127.0.0.1:5000/`.

## Running the Tests

Explain how to run the automated tests for this system (if applicable).

## Deployment

Add additional notes about how to deploy this on a live system.

## Built With

- Flask - The web framework used
- SQLite - Database engine
- SQLAlchemy - ORM and database toolkit


## License

This project is licensed under the MIT License - see the <LICENSE.md|LICENSE.md> file for details.## 
