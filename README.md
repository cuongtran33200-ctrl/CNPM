# SBCB Shop — Website bán đồ điện tử & phụ kiện (Django)

Đồ án học phần CNPM-DAU · 24CT1-TRANVIETCUONG

## Phân quyền 3 cấp

Hệ thống dùng model `Profile` (gắn 1-1 với `User`) để lưu vai trò: `customer` / `staff` / `admin`.
Tài khoản mới đăng ký mặc định là **Khách hàng**. Superuser tạo bằng `createsuperuser` tự động có vai trò **Quản trị viên**.

### 👤 Khách hàng
- Đăng ký / đăng nhập / hồ sơ cá nhân (`/ho-so/`)
- Trang chủ, danh mục, tìm kiếm, chi tiết sản phẩm
- Giỏ hàng, thanh toán
- Lịch sử mua hàng, chi tiết đơn hàng, theo dõi trạng thái
- Đánh giá sản phẩm (chỉ với sản phẩm đã mua)
- Gửi yêu cầu hỗ trợ (`/ho-tro/`)

### 👨‍💼 Nhân viên (`/nhan-vien/...`)
- Quản lý bán hàng: danh sách đơn hàng, xác nhận, cập nhật trạng thái, xử lý giao hàng
- Quản lý kho: xem & cập nhật tồn kho, lọc sản phẩm sắp hết/hết hàng
- Hỗ trợ: xem thông tin khách hàng, xử lý yêu cầu hỗ trợ

### 👑 Admin (`/quan-tri/...`)
- Dashboard tổng quan (doanh thu, số đơn, khách hàng, sản phẩm sắp hết)
- Quản lý người dùng & phân quyền (đổi vai trò customer/staff/admin)
- Thống kê: doanh thu, sản phẩm bán chạy/tồn kho, khách hàng
- Quản lý Sản phẩm/Danh mục/Đơn hàng đầy đủ qua Django Admin (`/admin/`)

**Cách cấp quyền nhân viên/admin cho một tài khoản:** đăng nhập bằng tài khoản admin → vào menu 👑 Quản trị → Người dùng → chọn vai trò tương ứng → Lưu.

## Chức năng chung

- Trang chủ hiển thị sản phẩm theo danh mục, tìm kiếm sản phẩm
- Trang chi tiết sản phẩm
- Giỏ hàng (thêm / xoá / cập nhật số lượng) — lưu theo session
- Đăng ký / đăng nhập / đăng xuất
- Đặt hàng (checkout) — yêu cầu đăng nhập
- Xem lịch sử đơn hàng & chi tiết đơn hàng của bản thân
- Trang quản trị (Django Admin) để quản lý Danh mục, Sản phẩm, Đơn hàng

## Cấu trúc dự án

```
config/     -> settings, urls chính của project
home/       -> trang giới thiệu cũ (chuyển sang /about/)
shop/       -> app chính: models, views, cart, forms, templates, admin
```

## Cài đặt & chạy thử

```bash
# 1. Tạo và kích hoạt môi trường ảo
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Tạo database (SQLite mặc định)
python manage.py makemigrations shop
python manage.py migrate
# Lưu ý: nếu đã migrate từ trước khi có phần phân quyền,
# hãy chạy lại 2 lệnh trên để tạo bảng Profile/Review/SupportRequest mới.

# 4. Tạo dữ liệu mẫu (danh mục + sản phẩm điện tử)
python manage.py seed_data

# 5. Tạo tài khoản quản trị
python manage.py createsuperuser

# 6. Chạy server
python manage.py runserver
```

Sau đó truy cập:
- Trang chủ: http://127.0.0.1:8000/
- Trang quản trị: http://127.0.0.1:8000/admin/

## Giao diện

Thiết kế theo phong cách các sàn điện tử Việt Nam (Thế Giới Di Động / FPT Shop): tông đỏ thương hiệu + cam nhấn, thanh tìm kiếm nổi bật, sidebar danh mục, card sản phẩm có ribbon giảm giá.

Để hiện badge giảm giá (VD: "-15%"), vào admin → **Sản phẩm** → điền **Giá gốc (trước giảm)** cao hơn **Giá** hiện tại. Nếu để trống, sản phẩm hiển thị bình thường không có badge.

## Thêm hình ảnh sản phẩm

Vào trang admin (`/admin/`) → **Sản phẩm** → chọn sản phẩm → tải ảnh lên trường **Hình ảnh**.
Nếu sản phẩm chưa có ảnh, trang web sẽ hiển thị icon 📦 thay thế.

