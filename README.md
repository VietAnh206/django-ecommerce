# Django E-commerce API

Dự án backend e-commerce xây dựng theo tài liệu *Django ecommerce tutorial v5*
(Django + Django REST Framework + JWT/Djoser + Cloudinary + Swagger + deploy Vercel/Render).

## Cấu trúc

| App | Chức năng |
|---|---|
| `backend_ecommerce/` | settings, urls, `helpers.py` (response chung, base CRUD view, permission) |
| `user/` | `UserAccount` (custom user), profile API, đăng ký/đăng nhập qua Djoser + JWT |
| `products/` | Category, Product, ProductImage, ProductComment (có comment cha-con) |
| `upload/` | Upload nhiều ảnh lên Cloudinary |
| `orders/` | Order, OrderDetail, tự động tính `total` bằng signal |

## Chạy trên máy (Windows cmd)

```bat
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
copy .env.example .env        :: rồi điền thông tin Cloudinary (DATABASE_URL để trống = sqlite3)
python manage.py makemigrations user products upload orders
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- API: http://127.0.0.1:8000/api/v1/
- Swagger: http://127.0.0.1:8000/swagger/
- Admin: http://127.0.0.1:8000/admin/
- Test: `python manage.py test`

## Endpoints (prefix `/api/v1/`)

| Nhóm | Endpoint | Quyền |
|---|---|---|
| Auth | `POST users/` (đăng ký), `POST jwt/create/`, `POST jwt/refresh/`, `POST jwt/verify/` | public |
| Profile | `GET/PUT users/profile/` | đăng nhập |
| Category | `GET/POST category/`, `GET/PUT/DELETE category/<id>/` | đọc: public, ghi: admin |
| Product | `GET/POST product/` (`?category=<id>&search=<text>`), `GET/PUT/DELETE product/<id>/` | đọc: public, ghi: admin |
| Images | `GET/POST product/<pid>/images/`, `GET/PUT/DELETE product/<pid>/images/<id>/` | đọc: public, ghi: admin |
| Comments | `GET/POST product/<pid>/comments/`, `GET/PUT/DELETE product/<pid>/comments/<id>/` | đọc: public, ghi: đăng nhập (chủ comment/admin) |
| Upload | `GET/POST upload-images/` (form-data, key `uploadImages`) | đọc: public, ghi: admin |
| Order | `GET/POST orders/`, `GET/PUT/DELETE orders/<id>/` | đăng nhập (user chỉ thấy đơn của mình) |
| Order detail | `GET/POST orders/<oid>/detail/`, `GET/PUT/DELETE orders/<oid>/detail/<id>/` | đăng nhập |

Header cho route cần đăng nhập: `Authorization: Bearer <access_token>`

Response thống nhất:
```json
{ "status_code": 200, "status": "Success", "message": "...", "data": { } }
```

## Deploy
1. **Database (Render):** tạo PostgreSQL, copy *External Database URL* vào `DATABASE_URL` trong `.env`, chạy `python manage.py migrate`.
2. **Vercel:** push lên GitHub, import project, khai báo các biến môi trường trong `.env.example`
   (đặt `DEBUG=False`, `CORS_ALLOWED_ORIGINS=<url frontend>`), rồi redeploy.
   Nếu Vercel báo không hỗ trợ runtime, chỉnh `runtime` trong `vercel.json` cho khớp phiên bản Python Vercel đang hỗ trợ.

## Những chỗ đã sửa so với slide
- `imprort` → `import`; `UserAccountView` → `UserProfileView`; thiếu `from datetime import timedelta`, `permissions`, `cloudinary.uploader`.
- Serializer: `images`/`comments` dùng `source=` đúng `related_name` (`product_images`, `product_comments`).
- Dùng `AUTH_USER_MODEL` ngay từ đầu nên **không cần comment `admin/`** hay xóa migrations.
- `DEFAULT_PERMISSION_CLASSES` chỉ để `IsAuthenticated` (slide liệt kê cả 3 quyền → tương đương AllowAny).
- `users/profile/` đặt trước `djoser.urls` để không bị nhầm với `users/<id>/`.
- Phân quyền thực tế: user chỉ xem/sửa đơn của mình, `user_id` lấy từ token (không nhận từ body), `total` chỉ đọc.
- URL dùng `<int:pk>`; DELETE trả 200 kèm body (204 không có body).
- Signal tính total không lỗi khi order bị xóa cascade; `OrderDetail.price` tự lấy giá sản phẩm nếu không gửi.

## Kết hợp Firebase Hosting (giao diện) + Django (API)

```
Trình duyệt ──▶ Firebase Hosting (firebase/public: HTML tĩnh)
                    │  fetch(API)
                    ▼
              Django API (Vercel/Render) ──▶ PostgreSQL + Cloudinary
```

1. Deploy Django lên Vercel/Render (xem chương 7), lấy địa chỉ API, vd `https://xxx.vercel.app`.
2. Sửa `firebase/public/config.js`: `API: "https://xxx.vercel.app/api/v1/"`.
3. Sửa `firebase/.firebaserc`: thay `TEN-PROJECT-FIREBASE` bằng Project ID trên Firebase Console.
4. Deploy giao diện:
   ```bash
   npm install -g firebase-tools
   firebase login
   cd firebase
   firebase deploy --only hosting
   ```
5. Cho phép CORS: trong biến môi trường của backend đặt
   `CORS_ALLOWED_ORIGINS=https://<project-id>.web.app,https://<project-id>.firebaseapp.com` rồi redeploy.

Khi chạy local, Django vẫn phục vụ giao diện ở `/` (dùng `templates/index.html`, gọi API cùng domain).
`templates/index.html` và `firebase/public/index.html` chỉ khác nhau một dòng nạp `config.js`.
