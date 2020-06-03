# 手把手Django+Vue前后端分离开发入门(附demo)

众所周知，Django对于网站快速开发非常友好，这得益于框架为我们做了很多事情，让我们只需要做一些简单的配置和逻辑即可把网站的功能开发出来。但是，在使用Django的过程中，有一个地方一直是比较难受的，那就是使用Django自带的模版，这种通常需要自己利用HTML+CSS+Jquery的方式总感觉是上一个时代的做法，前后端分离无论对于开发效率、多端支持等等都是很有好处的。所以，本文希望通过一个简单的demo，讲一讲基于Django+Vue的前后端分离开发，将Django作为一个纯后端的服务，为前端Vue页面提供数据支持。

本文采用的django版本号2.2.5，Vue版本2.9.6。

## 项目准备

对于django和Vue的安装这里就略过了~
创建前后端项目：创建一个文件夹，然后命令行创建项目即可，如下图

![Image](https://pic4.zhimg.com/80/v2-e800f1c26829608dddc5731f9c8bf5d5.png)

1. 测试：

命令行进入后端文件夹book_demo，输入下面命令，浏览器登陆127.0.0.1:8000看见欢迎页即成功。

    python manage.py runserver

再进入前端文件夹appfront，输入下面命令，浏览器登陆127.0.0.1:8080看见欢迎页即成功。

    npm run dev

上面两个命令也是对应前后端项目的启动命令，后面就直接将过程说成启动前/后端项目。

## 后端实现

为了方便后端的实现，作为django做后端api服务的一种常用插件，django-rest-framework(DRF)提供了许多好用的特性，所以本文demo中也应用一下，命令行输入命令安装：

    pip install django-rest-framework

进入book_demo目录，创建一个新的名为books的应用，并在新应用中添加urls.py文件，方便后面的路由配置，命令行输入：

    python manage.py startapp books 
    cd books
    touch urls.py
现在的目录结构如下：

![Image](https://pic4.zhimg.com/80/v2-663a90e660d2607c671bcfbfa3c7e18d.png)

下面开始做一些简单的配置：

将DRF和books配置到django项目中，打开项目中的settings.py文件，添加：

```python

# book_demo/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # demo add
    'rest_framework',
    'books',
]
```

对整个项目的路由进行配置，让访问api/路径时候转到books应用中的urls.py文件配置进行处理。

```python

# book_demo/settings.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('books.urls')), # demo add
] 
```

下面在books应用中写简单的逻辑，demo只最简单涉及对书本的增删改查。因为这一部分不是本文重点，所以这里只介绍写代码流程和贴代码，对代码不做详细解释：

在models.py文件中写简单数据类Books：

```python
# books/models.py
from django.db import models


class Books(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_books'
        verbose_name = '书籍'
        verbose_name_plural = '书籍'
```

在books文件夹中创建serializer.py文件，并写对应序列化器BooksSerializer：

```python
# books/serializer.py
from rest_framework import serializers

from books.models import Books


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

```

在views.py文件中写对应的视图集BooksViewSet来处理请求：

```python
# books/views.py
from rest_framework import viewsets

from books.models import Books
from books.serializer import BooksSerializer


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

```

在urls.py文件中写对应的路由映射：

```python
# books/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books import views


router = DefaultRouter()
router.register('books', views.BooksViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

对于books应用中的内容，如果对DRF和Django流程熟悉的同学肯定知道都干了些什么，篇幅关系这里只能简单解释，DRF通过视图集ViewSet的方式让我们对某一个数据类Model可以进行增删改查，而且不同的操作对应于不同的请求方式，比如查看所有books用get方法，添加一本book用post方法等，让整个后端服务是restful的。如果实在看不懂代码含义，只需知道这样做之后就可以通过不同的网络请求对后端数据库的Books数据进行操作即可，后续可以结合Django和DRF官方文档对代码进行学习。

到这里，可以运行一下后端项目看看效果，命令行运行：

    python manage.py makemigrations
    python manage.py migrate

    python manage.py createsuperuser #创建超级管理员账号，登录后台添加数据

    python manage.py runserver

得益于DRF提供的api可视化界面，浏览器访问127.0.0.1:8000/api/books/，如果出现了以下界面并添加数据正常，则说明后端的基本逻辑已经ok了~下图为添加了一条数据之后的效果。

![Image](https://pic4.zhimg.com/80/v2-465d3c12312047bb2adb40d0d9afb8d8.png)

## 前端实现

接下来的工作以appfront项目目录为根目录进行，开始写一点前端的展示和表单，希望达到两个目标，一是能从后端请求到所有的books列表，二是能往后端添加一条book数据。说白了就是希望把上面的页面用Vue简单实现一下，然后能达到相同的功能。对于Vue项目中各个文件的功能这里也不多解释，可以参考其文档系统学习。这里只需要知道欢迎页面中的样式是写在App.vue和components/HelloWorld.vue中即可。

这里直接用HelloWorld.vue进行修改，只求功能不追求页面了~

```vue

// appfront/src/components/HelloWorld.vue
<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <!-- show books list -->
    <ul>
      <li v-for="(book, index) in books" :key="index" style="display:block">
        {{index}}-{{book.name}}-{{book.author}}
      </li>
    </ul>
    <!-- form to add a book -->
    <form action="">
      输入书名：<input type="text" placeholder="book name" v-model="inputBook.name"><br>
      输入作者：<input type="text" placeholder="book author" v-model="inputBook.author"><br>
    </form>
    <button type="submit" @click="bookSubmit()">submit</button>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      // books list data
      books: [
        {name: 'test', author: 't'},
        {name: 'test2', author: 't2'}
      ],
      // book data in the form
      inputBook: {
        "name": "",
        "author": "",
      }
    }
  },
  methods: {
    loadBooks () {...}, // load books list when visit the page
    bookSubmit () {...} // add a book to backend when click the button
  },
  created: function () {
    this.loadBooks()
  }
}
</script>
...
```

启动前端项目，浏览器访问127.0.0.1:8080，可以看到刚写的页面已经更新上去了，丑是丑了点，意思到了就行~如下图：

![Image](https://pic4.zhimg.com/80/v2-3cc5e7eb8e6e479b0fd5d5afa32f1028.png)

## 前后端联调

敲黑板，重点来了！！上面的页面中数据其实是写死在前端页面的模拟数据，这一节希望通过从后端拿数据并展示在前端页面的方式来完成前后端联调。前后端联调，涉及最多的就是跨域的问题，为了保证安全，通常需要遵循同源策略，即“协议、域名、端口”三者都相同，具体可以看看相关的博客，这里只需知道上述三者相同才算同源即可。

后端部分，对于django的跨域问题，网上比较常用的做法就是利用django-cors-headers模块来解决，这里也不能免俗，操作如下。

先在命令行中进行对应模块的安装：

    pip install django-cors-headers

然后在项目中添加该模块：

```python

# books_demo/settings.py
INSTALLED_APPS = [
    ...
    # demo
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # 需注意与其他中间件顺序，这里放在最前面即可
    ...
]

# 支持跨域配置开始
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True 
```

后端部分告于段落，接下来需要补充一下前端的逻辑，Vue框架现在一般都用axios模块进行网络请求，这里沿用这种方式，下面是在前端项目中操作：

首先命令行安装axios模块，如果没有安装cnpm就还是用npm安装：

    cnpm install axios
为了方便管理api请求的各种逻辑，在前端项目的src目录下创建api目录，然后创建api.js和index.js文件。index.js文件是对axios做配置：

```js
// appfront/src/api/index.js
import Vue from 'vue'
import Axios from 'axios'

const axiosInstance = Axios.create({
    withCredentials: true
})

// 通过拦截器处理csrf问题，这里的正则和匹配下标可能需要根据实际情况小改动
axiosInstance.interceptors.request.use((config) => {
    config.headers['X-Requested-With'] = 'XMLHttpRequest'
    const regex = /.*csrftoken=([^;.]*).*$/
    config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1]
    return config
})

axiosInstance.interceptors.response.use(
    response => {
        return response
    },
    error => {
        return Promise.reject(error)
    }
)

Vue.prototype.axios = axiosInstance

export default axiosInstance

```
api.js文件是对后端进行请求，可以看到，获取books列表和添加一本book各对应于一个请求：

```js
// appfront/src/api/api.js
import axiosInstance from './index'

const axios = axiosInstance

export const getBooks = () => {return axios.get(`http://localhost:8000/api/books/`)}

export const postBooks = (bookName, bookAuthor) => {return axios.post(`http://localhost:8000/api/books/`, {'name': bookName, 'author': bookAuthor})}
```

然后更新HelloWorld.vue中的处理逻辑：

```vue
// appfront/src/components/HelloWorld.vue
<script>
import {getBooks, postBooks} from '../api/api.js'
export default {
  ...
  methods: {
    loadBooks () {
      getBooks().then(response => {
        this.books = response.data
      })
    }, // load books list when visit the page
    bookSubmit () {
      postBooks(this.inputBook.name, this.inputBook.author).then(response => {
        console.log(response)
        this.loadBooks()
      })
    } // add a book to backend when click the button
  },
  ...
}
</script>
```

至此，一个极其简陋的查询和添加书籍的功能算是完成了~如下图：

![Image](https://pic4.zhimg.com/80/v2-464cdcce3d069502d6b92382fc31e573.png)

![Image](https://pic4.zhimg.com/80/v2-dd97f2d83e2a0acc6f35e6dce831ab47.png)

可以看到，列表里面的数据是从后端读取到的，同时前端的提交数据库也能有对应的操作，所以前后端至此是打通了。

打包

现阶段是前后端分开开发，但是当最后要用的时候，还需要把代码合在一起。

首先对前端项目进行打包，这里用Vue的自动打包：

    npm run build

可以看到前端项目中多出了一个dist文件夹，这个就是前端文件的打包结果。需要把dist文件夹复制到books_demo项目文件夹中。

然后对settings.py文件进行相应的修改，其实就是帮django指定模版文件和静态文件的搜索地址：

```python
# books_demo/books_demo/settings.py
...
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'dist')], # demo add
        ...
    },
]
...
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'dist/static'),
]
..

```

最后在根urls.py文件中配置一下入口html文件的对应路由：

```python
# books_demo/books_demo/urls.py
...
from django.views.generic.base import TemplateView

urlpatterns = [
    ...
    path('', TemplateView.as_view(template_name='index.html'))
]
````

重新启动项目，这次用浏览器访问127.0.0.1:8000，即django服务的对应端口即可。

可以看到，项目的交互是正常的，符合我们的预期。

总结

本文以一个非常简单的demo为例，介绍了利用django+drf+vue的前后端分离开发模式，基本可以算是手把手入门。有了这个小demo之后，不管是前端页面还是后端功能，都可以做相应的扩展，从而开发出更加复杂使用的网站。

[原文链接 ](https://zhuanlan.zhihu.com/p/128976272)
