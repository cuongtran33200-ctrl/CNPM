# 🛒 Shop SBCB – Website bán hàng công nghệ

## 📌 Giới thiệu

**Shop SBCB** là website bán các sản phẩm công nghệ được xây dựng bằng **Django Framework**.

Hệ thống hỗ trợ các chức năng chính:

* 👤 Đăng ký, đăng nhập và quản lý tài khoản
* 🛍️ Xem danh sách và chi tiết sản phẩm
* 🔎 Phân loại sản phẩm theo danh mục
* 🛒 Thêm sản phẩm vào giỏ hàng
* 📦 Đặt hàng và theo dõi đơn hàng
* ⭐ Đánh giá sản phẩm
* 💬 Gửi yêu cầu hỗ trợ
* 👨‍💼 Quản lý dành cho nhân viên
* 👑 Trang quản trị dành cho Admin
* ☁️ Lưu trữ hình ảnh sản phẩm bằng Cloudinary

---

## 🛠️ Công nghệ sử dụng

| Công nghệ    | Mục đích                     |
| ------------ | ---------------------------- |
| Python       | Ngôn ngữ lập trình           |
| Django       | Web Framework                |
| MySQL        | Hệ quản trị cơ sở dữ liệu    |
| Django ORM   | Kết nối và thao tác Database |
| Cloudinary   | Lưu trữ hình ảnh sản phẩm    |
| HTML / CSS   | Giao diện website            |
| WhiteNoise   | Phục vụ Static Files         |
| Git / GitHub | Quản lý mã nguồn             |

---

## 🗄️ Database – MySQL

Dự án sử dụng **MySQL** làm hệ quản trị cơ sở dữ liệu chính.

### Database

```text
MySQL
└── sbcb_shop
```

### Django Database Engine

```python
django.db.backends.mysql
```

Cấu hình Database chính nằm trong:

```text
config/settings.py
```

Ví dụ:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sbcb_shop',
        'USER': '...',
        'PASSWORD': '...',
        'HOST': '...',
        'PORT': '...',
    },
}
```

> **MySQL** là hệ quản trị cơ sở dữ liệu của dự án, còn **`sbcb_shop`** là tên Database.

---

## 📊 Database Models

Các model được định nghĩa trong:

```text
shop/models.py
```

Các model chính:

```text
MySQL
└── sbcb_shop
    ├── Profile
    ├── Category
    ├── Product
    ├── Order
    ├── OrderItem
    ├── Review
    └── SupportRequest
```

### Quan hệ chính

```text
User
 ├── Profile
 ├── Order
 ├── Review
 └── SupportRequest

Category
 └── Product

Product
 ├── OrderItem
 └── Review

Order
 └── OrderItem
```

---

## 📁 Cấu trúc project

```text
CNPM/
│
├── manage.py
├── requirements.txt
├── README.md
├── ca.pem
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── __init__.py
│
├── home/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│
└── shop/
    ├── admin.py
    ├── admin_views.py
    ├── apps.py
    ├── cart.py
    ├── context_processors.py
    ├── decorators.py
    ├── forms.py
    ├── models.py
    ├── staff_views.py
    ├── urls.py
    ├── views.py
    │
    ├── migrations/
    │   ├── 0001_initial.py
    │   └── 0002_alter_product_image.py
    │
    ├── management/
    │   └── commands/
    │       ├── create_admin.py
    │       └── seed_data.py
    │
    ├── static/
    │   └── shop/
    │       ├── css/
    │       │   └── style.css
    │       └── img/
    │
    ├── templates/
    │   ├── registration/
    │   │   ├── login.html
    │   │   └── register.html
    │   │
    │   └── shop/
    │       ├── base.html
    │       ├── cart_detail.html
    │       ├── checkout.html
    │       ├── order_detail.html
    │       ├── order_history.html
    │       ├── product_detail.html
    │       ├── product_list.html
    │       ├── profile.html
    │       ├── support.html
    │       │
    │       ├── admin_panel/
    │       └── staff/
    │
    └── templatetags/
        └── shop_filters.py
```

---

## 👥 Phân quyền người dùng

Hệ thống có 3 vai trò chính:

### 👤 Customer

Khách hàng có thể:

* Xem sản phẩm
* Thêm sản phẩm vào giỏ hàng
* Đặt hàng
* Xem lịch sử đơn hàng
* Đánh giá sản phẩm
* Gửi yêu cầu hỗ trợ

### 👨‍💼 Staff

Nhân viên có thể:

* Quản lý đơn hàng
* Quản lý khách hàng
* Quản lý tồn kho
* Xử lý yêu cầu hỗ trợ

### 👑 Admin

Admin có quyền quản lý toàn bộ hệ thống và tài khoản người dùng.

---

## 🛍️ Các chức năng chính

### Sản phẩm

* Danh mục sản phẩm
* Thông tin sản phẩm
* Giá bán
* Giá gốc
* Số lượng tồn kho
* Cảnh báo sắp hết hàng
* Hình ảnh sản phẩm
* Đánh giá và xếp hạng

### Giỏ hàng

```text
Product
   ↓
Cart
   ↓
Checkout
   ↓
Order
   ↓
OrderItem
```

### Đơn hàng

Các trạng thái đơn hàng:

```text
pending
   ↓
confirmed
   ↓
shipping
   ↓
completed
```

Ngoài ra đơn hàng có thể chuyển sang:

```text
cancelled
```

---

## ☁️ Cloudinary

Hình ảnh sản phẩm được lưu trữ thông qua **Cloudinary**.

Model `Product` sử dụng:

```python
CloudinaryField
```

Ảnh sản phẩm được lưu trong thư mục:

```text
shop-sbcb/products
```

---

## ⚙️ Cài đặt project

### 1. Clone repository

```bash
git clone https://github.com/cuongtran33200-ctrl/CNPM.git
cd CNPM
```

### 2. Tạo virtual environment

Windows:

```bash
python -m venv venv
```

Kích hoạt:

```bash
venv\Scripts\activate
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 4. Cấu hình biến môi trường

Tạo file:

```text
.env
```

Các biến môi trường cần thiết:

```text
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=sbcb_shop
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=your_mysql_host
DB_PORT=your_mysql_port

CLOUDINARY_URL=your_cloudinary_url
```

### 5. Chạy migration

```bash
python manage.py migrate
```

### 6. Tạo dữ liệu mẫu

```bash
python manage.py seed_data
```

### 7. Tạo tài khoản Admin

```bash
python manage.py create_admin
```

### 8. Chạy server

```bash
python manage.py runserver
```

Truy cập:

```text
http://127.0.0.1:8000/
```

---

## 🚀 Deployment

Project có thể triển khai Django trên nền tảng cloud.

Database sử dụng:

```text
MySQL
```

Database production:

```text
sbcb_shop
```

Hình ảnh sản phẩm:

```text
Cloudinary
```

---

## 🔗 Repository

GitHub:

https://github.com/cuongtran33200-ctrl/CNPM

GitDiagram:

https://gitdiagram.com/cuongtran33200-ctrl/cnpm

---

## 👨‍💻 Thông tin dự án

**Tên dự án:** Shop SBCB
**Framework:** Django
**Database:** MySQL
**Database name:** sbcb_shop
**Project:** CNPM
**Lớp:** 24CT1

---

## 📌 Kiến trúc tổng quát

```text
                    SHOP SBCB
                        │
                        ▼
                  Django Framework
                        │
                 ┌──────┴──────┐
                 │             │
                 ▼             ▼
              Shop App      Home App
                 │
                 ▼
              Django ORM
                 │
                 ▼
              MySQL
                 │
                 ▼
             sbcb_shop
                 │
      ┌──────────┼───────────┐
      ▼          ▼           ▼
  Category    Product      Order
                 │           │
                 ▼           ▼
             Review       OrderItem
```
