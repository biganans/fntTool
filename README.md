
# fntTool
因为项目里策划、产品、美术都认为默认字体丑的出天际，每次都出一堆的自已喜欢的漂亮的字，啧啧，最后发现fnt的格式是一样的，于是写了一个py脚本

# windows版本下载    
方便美术等没有安装py的人使用，并支持名字配置，更加强大： [下载](https://github.com/biganans/fntTool/tree/master/EXE/fntTool.exe ) 
    
# 脚本使用环境
python 3.x    
python PIL库    

# 目录结构
把py脚本放于美术字平行目录，目前只处理了第一层目录的美术字，美术字生成的名字为目录名字    

# 使用方法
windows 直接点击bat文件即可    
生成的fnt和png图片位于每个文件夹的output目录下方    

# 关于报错
环境请自行百度    
代码请自行观察黑框打印信息    

# 增加修改
2018-5-21     
处理了【..png】直接过滤的bug    
2018-10-24    
增加单独的dict来处理电脑上无法命名或者冲突的文件名fnt_change_words
