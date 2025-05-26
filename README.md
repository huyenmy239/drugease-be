# Drugease Backend - Hệ Thống Quản Lý Đơn Thuốc

Drugease là một hệ thống webservice giúp quản lý đơn thuốc trong các bệnh viện, nhằm theo dõi và quản lý đơn thuốc từ khi bác sĩ kê đơn đến khi bệnh nhân nhận thuốc và theo dõi tình trạng điều trị.

## Mô Tả Đề Tài

Đề tài này phát triển một hệ thống webservice để giúp quản lý đơn thuốc, cải thiện hiệu quả trong việc kê đơn và phát thuốc, đồng thời giảm thiểu sai sót trong quá trình quản lý thuốc và chăm sóc bệnh nhân.

## Các Tính Năng Chính

### 1. Đăng Nhập và Quản Lý Tài Khoản
- **Đăng Nhập/Đăng Xuất:** Cho phép bác sĩ, dược sĩ và nhân viên y tế đăng nhập vào hệ thống bằng tài khoản cá nhân.
- **Quản Lý Tài Khoản:** Quản lý quyền truy cập và thông tin cá nhân của người dùng.

### 2. Kê Đơn Thuốc
- **Kê Đơn:** Bác sĩ có thể tạo đơn thuốc cho bệnh nhân với các thông tin về bệnh nhân, thuốc kê, liều lượng, và thời gian sử dụng.
- **Lưu và Cập Nhật:** Lưu lại đơn thuốc và có thể cập nhật nếu có sự thay đổi.

### 3. Quản Lý Đơn Thuốc
- **Danh Sách Đơn Thuốc:** Xem danh sách đơn thuốc của bệnh nhân, với trạng thái (chưa phát, đã phát). Dược sĩ chịu trách nhiệm cấp phát thuốc cho bệnh nhân.
- **Chi Tiết Đơn Thuốc:** Xem chi tiết đơn thuốc, thông tin thuốc và hướng dẫn sử dụng.

### 4. Quản Lý Kho Thuốc
- **Cập Nhật Tình Trạng Thuốc:** Quản lý số lượng thuốc trong kho và nhận cảnh báo khi thuốc gần hết.
- **Nhập/Xuất Thuốc:** Theo dõi việc nhập và xuất thuốc từ kho.

### 5. Quản Lý Bệnh Nhân
- **Thông Tin Bệnh Nhân:** Lưu trữ và quản lý thông tin bệnh nhân và lịch sử khám chữa bệnh.
- **Lịch Sử Đơn Thuốc:** Xem lịch sử đơn thuốc của bệnh nhân, bao gồm các đơn thuốc trước đó.

### 6. Báo Cáo và Thống Kê
- **Báo Cáo Đơn Thuốc:** Tạo báo cáo thống kê về số lượng đơn thuốc, loại thuốc và tình trạng sử dụng.

### 7. Giao Diện Người Dùng
- **Giao Diện Đơn Giản:** Cung cấp giao diện người dùng dễ sử dụng cho bác sĩ, dược sĩ và nhân viên y tế.

## Công Nghệ Sử Dụng

- **Web Framework:** Django.
- **Cơ Sở Dữ Liệu:** MySQL.
- **Web Service:** RESTful API.
- **Bảo Mật:** Xác thực người dùng, mã hóa dữ liệu nhạy cảm và bảo mật API.

## Cài Đặt

### 1. Yêu Cầu Hệ Thống
- Python 3.x
- Django
- MySQL

### 2. Cài Đặt Môi Trường

#### Cài Đặt Các Thư Viện Khác
Đảm bảo rằng tất cả các thư viện phụ thuộc được cài đặt đúng bằng cách sử dụng tệp `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 3. Cấu Hình Cơ Sở Dữ Liệu
- Cấu hình kết nối MySQL trong tệp `settings.py` của Django:
  - Mở tệp `settings.py` trong thư mục dự án Django.
  - Tìm phần cấu hình cơ sở dữ liệu và thay đổi các giá trị sau:
    - `NAME`: Tên cơ sở dữ liệu bạn sẽ sử dụng.
    - `USER`: Tên người dùng MySQL.
    - `PASSWORD`: Mật khẩu của người dùng MySQL.
    - `HOST`: Địa chỉ máy chủ MySQL (thường là `localhost` nếu chạy trên máy của bạn).
    - `PORT`: Cổng kết nối MySQL (thường là `3306`).

### 4. Migrate Cơ Sở Dữ Liệu
Đứng trên folder drugease. Chạy lệnh migrate trong Django để tạo các bảng cần thiết trong cơ sở dữ liệu.
```bash
python manage.py migrate
```

### 5. Chạy Server
Tương tự, khởi động server phát triển Django bằng cách chạy lệnh để bắt đầu server và truy cập ứng dụng thông qua trình duyệt.
```bash
python manage.py runserver
```

### 6. kết nối với Frontend

- **Backend Link:** [Drugease Frontend](https://github.com/huyenmy239/drugease-fe)

## API

### Tài Khoản
- **GET/POST/PUT** `/api/accounts/`  
  Thực hiện các tính năng năng đăng nhập, đăng ký và quản lý người dùng (vai trò Người quản lý/Admin).

### Đơn Thuốc và Bệnh Nhân
- **GET/POST/PUT/DELETE** `/api/prescriptions/`  
  Thực hiện các tính năng thao tác với thuốc, đơn thuốc và bệnh nhân (vai trò Bác sĩ/Doctor và Dược sĩ/Pharmacist).

### Kho Thuốc
- **GET/POST/PUT/DELETE** `/api/warehouses/`  
  Thực hiện các tính năng quản lý kho thuốc (vai trò Nhân viên/Staff).

### Báo Cáo
- **GET** `/api/reports/`  
  Xem các báo cáo liên quan của hệ thống (vai trò Người quản lý/Admin).

## Các Thành Viên Thực Hiện

| Thành Viên                  | Tính Năng Được Giao                                                         | Tài Khoản GitHub                  | Avatar                                |
|------------------------------|----------------------------------------------------------------------------|-----------------------------------|---------------------------------------|
| **Tô Phan Kiều Thương**      | Quản lý kho thuốc: Quản lý số lượng thuốc trong kho, nhập xuất thuốc, cập nhật tình trạng thuốc. | [ThuongPhan662003](https://github.com/ThuongPhan662003) | <img src="https://avatars.githubusercontent.com/ThuongPhan662003" width="50" height="50" /> |
| **Trần Huỳnh Trung Hiếu**    | Quản lý bệnh nhân và thuốc: Thêm, xóa, sửa thông tin bệnh nhân và thuốc trong hệ thống. | [ththieu2412](https://github.com/ththieu2412) | <img src="https://avatars.githubusercontent.com/ththieu2412" width="50" height="50" /> |
| **Nguyễn Thị Thanh Huyến**   | Quản lý việc xuất thuốc: Quản lý phiếu xuất thuốc, thêm, sửa, xóa các chi tiết phiếu xuất thuốc khi chưa duyệt. | [zethro](https://github.com/zethro) | <img src="https://avatars.githubusercontent.com/zethro" width="50" height="50" /> |
| **Nguyễn Thị Huyền My**      | Quản lý tài khoản người dùng, thực hiện các thao tác với đơn thuốc. | [huyenmy239](https://github.com/huyenmy239) | <img src="https://avatars.githubusercontent.com/huyenmy239" width="50" height="50" /> |



## Kết Luận

Hệ thống Drugease sẽ giúp tối ưu hóa quy trình kê đơn, phát thuốc và quản lý kho thuốc tại các bệnh viện. Việc sử dụng các tính năng như kê đơn thuốc, quản lý kho thuốc và báo cáo thống kê sẽ giúp cải thiện hiệu quả điều trị và giảm thiểu sai sót trong quá trình quản lý thuốc.
