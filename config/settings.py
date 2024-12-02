class Config:
    SECRET_KEY = 'sua_chave_secreta_supersegura'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/abex'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'sua_chave_secreta_jwt' 
