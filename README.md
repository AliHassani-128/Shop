
# Shop with Python/Django
![alt text](https://github.com/AliHassani-128/Shop/blob/main/media/shop_test_img.png?raw=true)

## Short description:
This is an E-Commerce website that is made with python and it's popular framework Django.

![alt text](https://github.com/AliHassani-128/Shop/blob/main/media/shop_test_image.png?raw=true)
## How to run this project

This project has been dockerized and you should have docker in your system to run it easily.


1.cd to root directory

2.open terminal and type

```http
  docker-compose up --build
```

3.After this command you should wait to download images and requirements for project

When download has finished open another terminal and type:

```http
  docker ps
```

Then copy your web container id (web container) from list and then in terminal type:

```http
  docker exec -t -i your-container-id bash
```

Now in your terminal you should have your container sh.
type this command to make database tables:


```http
  python manage.py makemigrations
```
then :

```http
  python manage.py migrate
```

after these you should make a super user for your django site:

```http
  python manage.py createsuperuser
```
then you should fill information of the super user.

4.Now you should open a terminal and type this command:
```http
  docker-compose up
```
now your site should be run .
open a browser and type http://127.0.0.1.8000/ to visit shop.


## Demo of Project :
If you want to see the demo of my project you can visit this site:

```http
  https://ali128-shop.herokuapp.com/
```









