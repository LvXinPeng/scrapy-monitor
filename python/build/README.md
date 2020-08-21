### Setuptools 打包依赖
#### 修改setup.py的依赖
    from setuptools import setup, find_packages
    from os import path, environ
    
    from io import open
    
    here = path.abspath(path.dirname(__file__))
    
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
    
    setup(
        name='scrapy-monitor',
        version=0.1,
        description='scrapy monitor',
        author='Roc Lv',
        author_email='lvxinpeng1996@126.com',
        python_requires='<3',
        install_requires=[
            'arrow==0.15.7',
            'attrs==19.3.0',
            'Automat==20.2.0',
            'backports.functools-lru-cache==1.6.1',
            'cffi==1.14.0',
            'constantly==15.1.0',
            'cryptography==2.9.2',
            'cssselect==1.1.0',
            'hyperlink==19.0.0',
            'idna==2.9',
            'incremental==17.5.0',
            'lxml==4.5.0',
            'parsel==1.6.0',
            'pyasn1==0.4.8',
            'pyasn1-modules==0.2.8',
            'pycparser==2.20',
            'PyDispatcher==2.0.5',
            'PyHamcrest==1.9.0',
            'pymongo==3.10.1',
            'PyMySQL==0.9.3',
            'python-dateutil==2.8.1',
            'queuelib==1.5.0',
            'Scrapy==1.8.0',
            'service-identity==18.1.0',
            'six==1.15.0',
            'Twisted==20.3.0',
            'w3lib==1.21.0',
            'zope.interface==5.1.0'
        ],
    )
- name : 软件包的名称。该名称由字母，数字，_和-组成。并且不能与其他已经上传至pypi.org的项目相同
- version : 软件包的版本
- author : 作者
- author_email : 作者邮箱地址
- description ：软件包的描述信息
- install_requires ：指定了当前软件包所依赖的其他python类库。这些指定的python类库将会在本package被安装的时候一并被安装

#### 生成软件包
##### 安装setuptools和wheel
    python -m pip install --user --upgrade setuptools wheel

如果存在，进行第二步；

##### 打包程序
    python setup.py sdist bdist_wheel

结束后会在当前目录下生成dist目录，该目录包含相应的whl和tar.gz文件；

### 部署所需依赖
#### 上传依赖包
包括第一步打包的whl以及所需的离线依赖包
> 离线依赖包在site-packages下
> 具体可查看requirements.txt
#### 执行部署
##### 部署
    pip install --no-index --find-links=site-packages svw_scrapy_monitor-0.1-py2-none-any.whl
##### 检查
    pip list

### 部署Scrapy项目
#### 打包Scrapy项目
- 从顶级目录压缩scrapy项目

#### 上传项目包至服务器
- 上传Scrapy压缩包至服务器并解压
- 进入到项目文件夹下
- 执行指令

    export SCRAPY_PROJECT=your env; scrapy crawl xxx

### 注意事项
##### 某些机器在打包时，会遇到“Cannot uninstall 'pyOpenSSL'”异常
解决方法：

- 查看pyOpenssl所在路径
    pip show pyOpenSSl
- 进入该路径，修改该文件的名称
    ll | grep 'pyOpenSSL'
- 重试打包即可
