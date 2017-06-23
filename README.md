一个基于命令行的网易云音乐下载器。


## 安装


### Git clone最新版

```bash
$ git clone https://github.com/ziwenxie/netease-dl
$ python3 setup.py install
```

### PyPi安装

```bash
$ pip3 install netease-dl
```

p.s: 仅支持Python3.x。


## 功能特性


通过`--help`可以查看到所有的功能特性，包括下载单首歌曲，下载一张唱片的所有歌曲，下载一个歌手的前50首热门歌曲，下载一张歌单的所有歌曲，下载一个用户的公开歌单以及登录后可下载个人的私人歌单。

```
$ netease-dl --help
Usage: netease-dl [OPTIONS] COMMAND [ARGS]...

  A command tool to download NetEase-Music's songs.

Options:
  -t, --timeout INTEGER  Time to wait before giving up, in seconds.
  -p, --proxy TEXT       Use the specified HTTP/HTTPS/SOCKS proxy.
  -o, --output PATH      Specify the storage path.
  -q, --quiet            Automatically select the best one.
  -l, --lyric            Download lyric.
  -a, --again            Login Again.
  --help                 Show this message and exit.

Commands:
  album     Download a album's songs by name or id.
  artist    Download a artist's hot songs by name or id.
  me        Download my playlists.
  playlist  Download a playlist's songs by id.
  song      Download a song by name or id.
  user      Download a user's playlists by id.
```


## 使用

### 下载单首歌曲

使用`song`命令，在后面通过`--name`或者`-n`选项来指定歌曲的名字：

```
$ netease-dl song --name 歌曲名
```

上面会返回10条搜索结果，可以在`song`命令前面加一个`--quiet`，`netease-dl`会自动匹配第一个返回的结果：
```
$ netease-dl --quiet song --name 歌曲名
```

如果知道歌曲id的话，也可以直接使用`--id`或者`-i`选项来指定：
```
$ netease-dl song --id 歌曲id
```

`netease-dl`的所有子命令所支持的特性都可以通过在子命令后面加一个`--help`选项来查看：
```
$ netease-dl song --help
Usage: netease-dl song [OPTIONS]

  Download a song by name or id.

Options:
  -n, --name TEXT   Song name.
  -i, --id INTEGER  Song id.
  --help            Show this message and exit.
```


### 下载一个歌手的50首热门歌曲

使用`artist`命令，并且在后面通过`--name`或者`-n`选项来指定歌手的姓名：

```
$ netease-dl artist --name 歌手名
```

和上面下载歌曲的时候一样，也可以使用`--quiet`和`--id`，下面也是一样的原理，接下来我就不重复了。


### 下载一张唱片的所有歌曲

使用`album`命令，后面接`--name`或者`-n`选项来指定唱片的名字：

```
$ netease-dl album --name 唱片名
```


### 下载一张歌单的所有歌曲

使用`playlist`命令，后面接`--name`或者`-n`选项来指定歌单的名字：
```
$ netease-dl playlist --name 歌单名
```

### 下载指定用户的公开歌单

使用`user`命令，后面接`--name`或者`-n`选项来指定用户的名字：
```
$ netease-dl user --name 用户名
```


### 下载个人收藏以及创建的歌单

使用`me`命令登录之后可以下载自己的所有歌单包括私人的歌单，以后一段之间之内如果没有修改过密码就不需要重新登录了：
```
$ netease-dl me
```

如果要换一个帐号或者登录密码修改了，使用`--again`或者`-a`选项重新登录：
```
$ netease-dl --again me
```

## 更多选项

除了上面提到的`--quiet`选项，正如使用`netease-dl --help`选项看到的，`netease-dl`还支持设置代理，设置超时时间，指定下载目录，是否下载歌词等选项，这些都可以通过在子命令前面加上相关的选项来指定。

### 将歌曲下载到指定路径

使用`--output`或者`-o`选项指定下载路径：
```
$ netease-dl -o 路径名 artist -n 歌手名
```

### 设置代理

海外用户可能要设置相关的代理，`netease-dl`同时支持http和socks协议代理，可以通过`--proxy`或者`-p`选项指定，注意要声明代理所使用的协议：
```
$ netease-dl -p 'http://127.0.0.1:8118' artist -n 歌手名
$ netease-dl -p 'socks5://127.0.0.1:1080' artist -n 歌手名
```

## 更新日志

2017-03-19 1.0.2 fix song may contains special character and won't download again if song exists(#2, #3)

2017-03-16 1.0.1 fix dependencies problem(#1)


## Contact

Email: ziwenxiecat@gmail.com
Blog: www.ziwenxie.site

## License

https://github.com/ziwenxie/netease-dl/blob/master/LICENSE
