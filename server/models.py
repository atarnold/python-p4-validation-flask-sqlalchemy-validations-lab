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
    def validate_name(self, key, name):
        if not name:
            raise ValueError("name field required.")
        author = db.session.query(Author.id).filter_by(name=name).first()
        if author is not None:
            raise ValueError("Name must be unique")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
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
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title field required.")
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any (bait in title for bait in clickbait):
            raise ValueError("No clickbait in title.")
        return title
        
    @validates('category')
    def validate_Category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("category must be either fiction or non-fiction.")
        return category

    @validates('content', 'summary')
    def validate_content(self, key, string):
        if key == 'content':
            if len(string) < 250:
                raise ValueError("Post content must be atleast 250 characters long.") 
        if key == 'summary':
            if len(string) > 250:
                raise ValueError("Post summary must not e greater than 250 characters")
            return string


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
    