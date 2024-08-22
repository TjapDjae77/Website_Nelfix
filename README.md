# Website_Nelfix
 NAMA: RAJENDRA FARRAS RAYHAN
 NIM: 18222105

 Untuk menjalankan websitenya:
 1. Jalankan Env\Scripts\activate.bat untuk masuk ke environment
 2. Lalu masuk ke cd website-project dan lakukan python manage.py runserver

 Design pattern yang saya gunakan adalah Template Method, Factory, Decorator, dan Strategy. 
 1. Template method dipakai untuk mendefinisikan alur umum dari suatu proses dalam superclass, sedangkan detail dari implementasinya bisa diubah sama subclass tanpa mengubah struktur algoritmanya, contohnya di FilmListView bisa definisiin get_query() dan filter_queryset() di subclass.
 2. Factory dipakai buat mengelola pembuatan objek Profile di view tanpa menentukan kelas yang tepat dari objek yang dibuat 
 3. Strategy dipakai untuk mendefinisikan rangkaian algoritma yang bisa diganti antar satu sama lain. Dalam FilmListView bisa punya berbagai strategi filter tergantung query yang diberikan
 4. Decorator dipakai buat menambah fungsionalitas tambahan ke suatu objek secara dinamis tanpa mengubah strukturnya, contohnya @login_required.


 Saya menggunakan technology stack untuk frontend yaitu framework Tailwind CSS. Lalu untuk backend menggunakan frameworke Django. Untuk database saya menggunakan MySQL.

 Endpoint yang saya buat sebagai berikut:
 1. Monolith:
    a. / = Landing page (Browse film)
    b. /user/register/ = Register account
    c. /user/login/ = Login
    d. /user/profile/ = Profile account
    e. /my-list/ = My List (Film-film yang sudah dibeli oleh account)
    f. /films/:id/ = Films Details Page

 2. REST API:
    a. POST /films = api/films/
    b. GET /films = api/films/
    c. GET /films/:id = api/films/<int:pk>/
    d. PUT /films/:id = api/films/<int:pk>/
    e. DELETE /films/:id = api/films/<int:pk>/
    f. POST /login = api/login/
    g. GET /self = api/self/
    h. GET /users = api/users/
    i. GET /users/:id = api/users/<int:pk>/
    j. POST /users/:id/balance = api/users/<int:pk>/balance/
    k. DELETE /users/:id = api/users/<int:pk>/
    
Bonus: Responsive Design, namun tidak seluruhnya terbuat Responsivenya

