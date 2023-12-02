from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable =False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):

        if not name:
            raise ValueError("Name can't be empty")
        elif Author.query.filter_by(name = name).first():
            raise ValueError("Author already exists")
    
        
    

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be exactly ten digits")
        
        else:
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
            raise ValueError ("Post must have a title")
        

        to_title = ["Won't Believe", "Secret", "Top", "Guess"]

        if not any (substring in title for substring in to_title):
            
            raise ValueError("No clickbait found")
        
        return title
    
    
  
        
    @validates('content', 'summary')
    def validate_length(self, key, string):

        if (key == 'content'):
            if len(string) < 250:
                raise ValueError("Post content must be greater than 250 characters")
        
        if (key == 'summary'):
            if len(string) > 250:
                raise ValueError("Post must not be more than 250 characters")
            
        
        return string
        
        
    @validates('category')
    def validate_category(self, key, category):
        
        allowed_category = ['Fiction', 'Non-Fiction']

        if category not in allowed_category:
            raise ValueError ("Category not found")
        
        else:
            return category
        


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
