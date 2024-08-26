# FastApi4

FastAPI Tutorial 4 dars

# 4-dars: Authentication va Authorization

Bu darsda siz FastAPI da autentifikatsiya va avtorizatsiya tushunchalari bilan tanishasiz. Ayniqsa, token-based
authentication (JWT) va OAuth2 with Password (Bearer) flow ni o‘rganasiz. Shuningdek, foydalanuvchi autentifikatsiyasi
va himoyalangan endpointlarni qanday yaratishni ham ko‘rib chiqasiz.

### Dars mavzulari:

* Token-based Authentication (JWT) ga Kirish
* OAuth2 with Password (Bearer) Flow
* Foydalanuvchi Autentifikatsiyasi
* Himoyalangan Endpointlarni Yaratish

1. Token-based Authentication (JWT) ga Kirish
   JSON Web Token (JWT) - bu foydalanuvchini identifikatsiyalash va ma'lumotlarni xavfsiz tarzda uzatish uchun
   ishlatiladigan tokenlar. Bu tokenlar odatda foydalanuvchini autentifikatsiya qilish uchun ishlatiladi va har bir
   so‘rovda serverga uzatiladi.

### JWT Ishlash Tizimi:

* Foydalanuvchi tizimga kiradi va login uchun API chaqiradi.
* Server foydalanuvchini tekshiradi va JWT tokenni yaratadi.
* JWT token foydalanuvchiga qaytariladi.
* Foydalanuvchi JWT tokenni barcha so‘rovlar bilan birga yuboradi.
* Server JWT tokenni tekshiradi va foydalanuvchiga kirish imkoniyatini beradi.

2. OAuth2 with Password (Bearer) Flow
   FastAPI OAuth2 yordamida foydalanuvchini autentifikatsiya qilishni qo‘llab-quvvatlaydi. OAuth2 with Password (Bearer)
   flow - bu foydalanuvchi foydalanuvchi nomi va parol orqali tizimga kirganda foydalaniladigan eng keng tarqalgan flow.

Misol:

```shell
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}

def fake_hash_password(password: str):
    return "fakehashed" + password

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    # Bu yerda tokenni dekodlash va userni olish ishlari amalga oshiriladi
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

```

Yuqoridagi kodda:

* OAuth2PasswordBearer - bu foydalanuvchi tokenni yuborganida autentifikatsiya qilish uchun ishlatiladigan security
  schema.
* tokenUrl="token" - bu foydalanuvchi tizimga kirganda ishlatiladigan endpoint.
* get_current_user funksiyasi token orqali foydalanuvchini olish va uni autentifikatsiya qilish uchun ishlatiladi.

3. Foydalanuvchi Autentifikatsiyasi
   Foydalanuvchini autentifikatsiya qilish uchun parolni hashlash va token yaratish jarayonlarini qo‘shishimiz kerak. Bu
   misolda biz fake_hash_password va fake_decode_token funksiyalaridan foydalanmoqdamiz, lekin amalda bcrypt va JWT
   yordamida real parolni hashlash va token yaratish amalga oshiriladi.

4. Himoyalangan Endpointlarni Yaratish
   Yuqoridagi kodda @app.get("/users/me") himoyalangan endpoint bo‘lib, u faqat autentifikatsiyadan o‘tgan
   foydalanuvchilar uchun mo‘ljallangan. Himoyalangan endpointlarni yaratish uchun Depends() yordamida get_current_user
   funksiyasini in'ektsiya qilamiz.

## Yakuniy Qo'shimchalar:

* Token-based authentication (JWT) - foydalanuvchini identifikatsiyalash uchun ishlatiladi.
* OAuth2 with Password (Bearer) Flow - tizimga kirish uchun foydalaniladigan xavfsizlik flow.
* Foydalanuvchi autentifikatsiyasi - foydalanuvchini tizimga kiritish va ularning kirish huquqlarini boshqarish.
* Himoyalangan endpointlar - faqat autentifikatsiyadan o‘tgan foydalanuvchilar uchun mo‘ljallangan API yo‘llari.
  Bu darsda siz FastAPI da autentifikatsiya va avtorizatsiya tizimlarini yaratish bo‘yicha muhim tushunchalarni
  o‘rgangansiz. Bu tushunchalar sizning API xavfsizligingizni ta'minlashda muhim ahamiyatga ega.

-------------------------------------------------------------------------------------------

# SQLAlchemy bilan ishlash

Bu darsda siz SQLAlchemy va FastAPI ni integratsiya qilishni o‘rganasiz. SQLAlchemy - bu Python’da eng ko‘p
ishlatiladigan ORM (Object-Relational Mapper) vositasi bo‘lib, u ma’lumotlar bazasi bilan ishlashni osonlashtiradi.
Ushbu darsda ma’lumotlar bazasi modeli va schema yaratish, shuningdek, CRUD (Create, Read, Update, Delete)
operatsiyalarini qanday amalga oshirishni ko‘rib chiqamiz.

### Dars mavzulari:

* SQLAlchemy va FastAPI ni Integratsiya qilish
* Database model va schema yaratish
* CRUD operatsiyalarni amalga oshirish

1. SQLAlchemy va FastAPI ni Integratsiya qilish
   Avvalo, FastAPI va SQLAlchemy ni birgalikda ishlatish uchun kerakli kutubxonalarni o‘rnatishimiz kerak:

```shell
pip install fastapi sqlalchemy sqlite3 uvicorn
```

Keyin, database.py faylida ma'lumotlar bazasiga ulanish va sessiyalarni boshqarish uchun konfiguratsiya yaratiladi.

database.py

```shell
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

6-dars: SQLAlchemy bilan ishlash

Bu darsda siz SQLAlchemy va FastAPI ni integratsiya qilishni o‘rganasiz. SQLAlchemy - bu Python’da eng ko‘p
ishlatiladigan ORM (Object-Relational Mapper) vositasi bo‘lib, u ma’lumotlar bazasi bilan ishlashni osonlashtiradi.
Ushbu darsda ma’lumotlar bazasi modeli va schema yaratish, shuningdek, CRUD (Create, Read, Update, Delete)
operatsiyalarini qanday amalga oshirishni ko‘rib chiqamiz.

Dars mavzulari:
SQLAlchemy va FastAPI ni Integratsiya qilish
Database model va schema yaratish
CRUD operatsiyalarni amalga oshirish

1. SQLAlchemy va FastAPI ni Integratsiya qilish
   Avvalo, FastAPI va SQLAlchemy ni birgalikda ishlatish uchun kerakli kutubxonalarni o‘rnatishimiz kerak:

bash
Copy code
pip install fastapi sqlalchemy sqlite3 uvicorn
Keyin, database.py faylida ma'lumotlar bazasiga ulanish va sessiyalarni boshqarish uchun konfiguratsiya yaratiladi.

database.py
python
Copy code
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

### Bu kodda:

* create_engine yordamida SQLite bilan ulanish yaratildi.
* SessionLocal SQLAlchemy sessiyalarini boshqarish uchun ishlatiladi.
* Base barcha modellarning asosiy sinfidir.

2. Database model va schema yaratish
   SQLAlchemy yordamida ma'lumotlar bazasining modelini yaratish uchun models.py faylidan foydalanamiz. Pydantic
   yordamida schema yaratish uchun schemas.py fayli kerak bo‘ladi.

models.py: Database model yaratish

```shell
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
    image = Column(String)

```

### Bu yerda Product sinfi SQLAlchemy modeli bo‘lib, u products jadvaliga mos keladi. U quyidagi ustunlarni o‘z ichiga oladi:

* id: Mahsulotning ID si.
* title: Mahsulotning nomi.
* description: Mahsulotning ta’rifi.
* price: Mahsulotning narxi.
* image: Mahsulotning rasmi (URL).

schemas.py: Pydantic schema yaratish

```shell
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

```

Bu yerda ProductBase va ProductCreate sinflari Pydantic schema bo‘lib, ular orqali ma’lumotlarni validatsiya qilish va
serializatsiya qilish amalga oshiriladi. Product sinfi esa ProductBase dan meros oladi va id ustunini qo‘shadi.

3. CRUD operatsiyalarni amalga oshirish
   Endi biz CRUD operatsiyalarini yozishimiz mumkin. Buning uchun main.py faylida kerakli endpointlarni yaratamiz.

main.py: CRUD operatsiyalar

```shell
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

```

Bu yerda CRUD operatsiyalari uchun kerakli API endpointlar yaratildi:

* POST /products/: Yangi mahsulot yaratish.
* GET /products/: Barcha mahsulotlarni ko‘rish.
* GET /products/{product_id}: ID bo‘yicha mahsulotni ko‘rish.
* PUT /products/{product_id}: ID bo‘yicha mahsulotni yangilash.
* DELETE /products/{product_id}: ID bo‘yicha mahsulotni o‘chirish.

## Yakuniy Qo'shimchalar:

* SQLAlchemy va FastAPI ni integratsiya qilish orqali ma'lumotlar bazasi bilan ishlash osonlashadi.
* Database model va schema yaratish orqali ma'lumotlarni modellashtirish va validatsiya qilishni amalga oshirasiz.
* CRUD operatsiyalari bilan API orqali ma'lumotlar bazasida yaratilish, o'qish, yangilash va o'chirish kabi amallarni
  amalga oshirishingiz mumkin.
  Ushbu darsda siz SQLAlchemy va FastAPI yordamida backend ilovalari uchun asosiy CRUD operatsiyalarini yaratish va
  boshqarish bo‘yicha muhim tushunchalarni o‘rgandingiz.