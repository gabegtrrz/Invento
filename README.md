###Project Name:
**Inventó**
Your Inventory Management Made Quick & Easy

###Members:
Gutierrez, Gabriel Louis (23000782010)
Pacardo, John Christopher (22015347710)

###What is Invento?
Inventó is a web-based inventory management system designed to streamline
inventory tracking, reduce manual errors, and provide valuable insights to businesses.
By automating inventory processes, the system aims to improve efficiency, reduce costs,
and enhance decision-making.

It is in it's prototype phase, and this current version is its MVP.
We are excited to deliver enhanced features that are most relevant and most useful to the
target market.


###Installation Instructions:

1. Clone this repo.
2. Install requirements file.
3. Make sure to create your MySQL connection, and configure the project's
   settings.py and __init__.py accordingly:

   **settings.py**
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',  # Or your database server's IP
        'PORT': '3306',  # Default MySQL port
                }
    }
    **init.py**
    
    import pymysql
    pymysql.install_as_MySQLdb()


4. Apply Migrations.
5. Run the development server.


##_Hope it's not too bad :)_


   

