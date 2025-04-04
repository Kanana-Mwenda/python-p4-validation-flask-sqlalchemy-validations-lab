from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validates_name(self,key,name):
        if not name:
            raise ValueError ("Author must have a name.")
        author = db.session.query(Author.id).filter_by(name=name).first()
        if author is not None:
            raise ValueError("Author name already exists.")
        return name

    @validates('phone_number')
    def validates_phone_number(self,key,phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be 10 digits.")
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validates_content(self,key,content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters.")
        return content

    @validates('summary')
    def validates_summary(self,key,summary):   
        if len(summary) > 250:
            raise ValueError("Summary must be at most 250 characters.")
        return summary

    @validates('category')
    def validates_category(self,key,category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("Category must be either Fiction or NonFiction.")
        return category

    @validates ('title')
    def validates_title(self,key,title):
        if not title:
            raise ValueError("Title must not be empty.")
        clickbait = ["Won't Believe", "Secret","Top","Guess"]
        if not any(word in title for word in clickbait):
            raise ValueError("No clickbait found")
        return title




    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
