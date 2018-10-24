# -*- coding: utf-8 -*-
# 到了 生成美术字的图片集fnt
import os
#import PIL
from PIL import Image
import sys, os, glob, math,codecs

colCount = 1 #列数
rowCount = 1 #行数
max_height = 0
max_width = 0

#默认文本fnt字体
face = "Arial"

#无法命名或者冲突的字体转换(特别是windows大小写居然不敏感f**k)
fnt_change_words = dict([("gang","/"),("mao",":"),("space"," "),("star","*"),("wh","?"),("fu","-"),("aa","A"),("bb","B"),("cc","C"),("dd","D"),("ee","E"),("ff","F"),("gg","G"),("hh","H"),("ii","I"),("jj","J"),("kk","K"),("ll","L"),("mm","M"),("nn","N"),("oo","O"),("pp","P"),("qq","Q"),("rr","R"),("ss","S"),("tt","T"),("uu","U"),("vv","V"),("ww","W"),("xx","X"),("yy","Y"),("zz","Z")])

def create_fnt_file(fnt_name, fnt_define):
    global face
    write_file=open(fnt_name,"w")
    write_file = codecs.open(fnt_name,"w","utf-8")
    #face="Arial”,字体为”Arial”
    # size=32:大小为32像素
    # bold=0 :不加粗
    # italic=0:不使用斜体
    # charset="": charset是编码字符集，这里没有填写值即使用默认，
    # unicode=0:不使用Unicode
    # stretchH=100:纵向缩放百分比
    # smooth=1 :开启平滑
    # aa=1:开启抗锯齿
    # padding=0,0,0,0:内边距，文字与边框的空隙。
    # spacing=1,1 :外边距，就是相临边缘的距离。
    head_msg1="""info face="%s" size=%s bold=0 italic=0 charset="" unicode=0 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing=2,2 outline=0\n""" % (face,fnt_define["size"])
    write_file.write(head_msg1)
    # lineHeight=37：行高，如果遇到换行符时，绘制字的位置坐标的Y值在换行后增加的像素值。
    # base=28 :字的基本大小
    # scaleW=512 :图片大小
    # scaleH=512:图片大小
    # pages=1 :此种字体共用到几张图。
    # packed=0:图片不压缩
    head_msg2 ="""common lineHeight=%s base=%s scaleW=%s scaleH=%s pages=1 packed=0 alphaChnl=0 redChnl=0 greenChnl=0 blueChnl=0\n""" % (fnt_define["lineHeight"],fnt_define["base"],fnt_define["scaleW"],fnt_define["scaleH"])
    write_file.write(head_msg2)
    # //第一页，文件名称是”bitmapFontChinese.png”
    # page id=0 file="bitmapFontChinese.png"
    head_msg3 = """page id=0 file="%s"\n""" % (fnt_define["file"])
    write_file.write(head_msg3)
    # 第四行是当前贴图中所容纳的文字数量
    head_msg4 = """chars count=%s\n""" % (fnt_define["count"])
    write_file.write(head_msg4)

    for i in range(0,int(fnt_define["count"])):
        data=fnt_define["data"][i]
        line="char id=%s x=%s y=%s width=%s height=%s xoffset=%s yoffset=%s xadvance=%s page=%s chnl=%s letter=\"%s\"\n" %(data["id"],data["x"],data["y"],data["width"],data["height"],data["xoffset"],data["yoffset"],data["xadvance"],data["page"],data["chnl"],data["letter"])
        write_file.write(line)


def joint_image(image_name,convert_list):
    # 引用全局变量
    outW=max_width*colCount
    outH=max_height*rowCount

    print("out image size %dx%d" %(outW,outH))

    toImage = Image.new('RGBA', (outW, outH))

    x=0
    index = 0
    for key in convert_list.keys():
        fromImage=Image.open(key)
        offsetX = (index%colCount)*max_width
        offsetY = int(int(index/colCount)*max_height)
        toImage.paste(fromImage,( offsetX, offsetY))
        # print("\t %s offset %d %d" %(key,offsetX, offsetY))
        x+=fromImage.size[0]
        index += 1

    toImage.save(image_name)


def make_fnt_file(pre_str,convert_list,output_path_name):
    # 引用全局变量
    global max_width
    global max_height
    global colCount
    global rowCount
    fnt_name=output_path_name+"/"+pre_str+".fnt"
    image_name=pre_str+".png"
    fnt_define=dict()
    index=0
    xOffset=0
    max_height=0
    max_width=0
    for key in convert_list.keys():
        image = Image.open(key)
        print("image %s   size: w{%d} h{%d}"%(key,image.size[0],image.size[1]))
        max_width=max(max_width,image.size[0])
        max_height=max(max_height,image.size[1])
    totalCount = len(convert_list)
    colCount =  int(math.ceil(math.sqrt(max_height*max_width*totalCount*1.0)/max_width))
    rowCount = int(math.ceil(len(convert_list)*1.0/colCount))
    print("--------------------colxrow---", colCount, rowCount, totalCount)

    fnt_define_item=list()
    for key in convert_list.keys():
        # print("\t+"+key+"\t"+"Key:"+chr(int(convert_list[key])))
        image = Image.open(key)
        image_size= image.size
        fnt_define_item_data=dict()
        fnt_define_item_data["id"]=convert_list[key]
        fnt_define_item_data["x"]=str((index%colCount)*max_width)
        fnt_define_item_data["y"]=str(int(index/colCount)*max_height)
        fnt_define_item_data["width"]=str(image_size[0])
        fnt_define_item_data["height"]=str(image_size[1])
        fnt_define_item_data["xoffset"]=str(0)
        fnt_define_item_data["yoffset"]=str(0)
        fnt_define_item_data["xadvance"]=str(image_size[0]) #???
        fnt_define_item_data["page"]=str(0)
        fnt_define_item_data["chnl"]=str(0)
        fnt_define_item_data["letter"]=chr(int(convert_list[key]))

        fnt_define_item.append(fnt_define_item_data)

        index+=1
        xOffset+=image_size[0]
        max_width=max(max_width,image_size[0])
        max_height=max(max_height,image_size[1])

    fnt_define["data"]=fnt_define_item
    fnt_define["size"]=str(max_width)
    fnt_define["lineHeight"]=str(max_height)
    fnt_define["base"]=str(max_width)
    fnt_define["scaleW"]=str(max_width*colCount)
    fnt_define["scaleH"]=str(max_height*rowCount)
    fnt_define["file"]=image_name
    fnt_define["count"]=len(convert_list)

    image_name=output_path_name+"/"+image_name

    create_fnt_file(fnt_name, fnt_define)
    print ("make:"+fnt_name+"done!")
    joint_image(image_name,convert_list)
    print("make {%s} fnt done! good!"%(image_name))


def check_and_make(fnt_name,convert_list,output_path_name):
    if len(convert_list)>=1 :
        print("*************************************************************")
        print("fnt file: " +fnt_name+" ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
        make_fnt_file(fnt_name,convert_list,output_path_name)


def main():
    global fnt_change_words
    print("****************************************************************************")
    print("欢迎使用FNT打包工具：")
    print("1：工具需要放在资源目录同级，并且上级最好不要有中文文件夹出现。")
    print("2：美术资源文字需要单独命名，如：+.png；必须要png图片。")
    print("3：建立文件夹，且文件夹的名字为打包出来fnt的名字，并把需要打包的png丢在这个文件夹里。")
    print("4：JJFnt.exe、包含png文件夹、words.ini均在同一个目录下，并保持没有其他目录，提高打包FNT速度。")
    print("5：打包出来的资源在美术字文件夹下的子文件夹output里：xx.fnt xx.png")
    print("****************************************************************************")
    print("u can in dir use words.ini to do this (as=A) every line,make sure use utf-8 write ini.")
    print("你可以直接在工具所在当前目录使用words.ini来进行配置(utf-8格式)，每一行格式：(as=A).等号右边不能有空格.")
    print("****************************************************************************")
    print("已经有名字的对应表(key,value)")
    print("[(\"gang\",\"/\"),(\"mao\",\":\"),(\"space\",\" \"),(\"star\",\"*\"),(\"wh\",\"?\"),(\"fu\",\"-\"),(\"aa\",\"A\"),(\"bb\",\"B\"),(\"cc\",\"C\"),(\"dd\",\"D\"),(\"ee\",\"E\"),(\"ff\",\"F\"),(\"gg\",\"G\"),(\"hh\",\"H\"),(\"ii\",\"I\"),(\"jj\",\"J\"),(\"kk\",\"K\"),(\"ll\",\"L\"),(\"mm\",\"M\"),(\"nn\",\"N\"),(\"oo\",\"O\"),(\"pp\",\"P\"),(\"qq\",\"Q\"),(\"rr\",\"R\"),(\"ss\",\"S\"),(\"tt\",\"T\"),(\"uu\",\"U\"),(\"vv\",\"V\"),(\"ww\",\"W\"),(\"xx\",\"X\"),(\"yy\",\"Y\"),(\"zz\",\"Z\")]")
    print("****************************************************************************")

    # 遍历当前文件夹，直接使用目录作为fnt的名字
    #读取配置文件words.ini
    wordsIniPath = "./words.ini"
    if os.path.exists(wordsIniPath):
        words = open(wordsIniPath,'r',encoding='utf-8')
        try:
            change_words = words.readlines()
        finally:
            words.close()
        # print("change_words",change_words)
        if change_words:
            for i in range(0,len(change_words)):
                if change_words[i]:
                    r = change_words[i].split(',')
                    for j in range(0,len(r)):
                        #是否有等号
                        si = r[j].find('=')
                        if si == -1 :
                            #抛弃掉当前行
                            continue
                        # print("s",r)
                        s = r[j].split('=')
                        if len(s) == 2:
                            try:
                                k = s[0]
                                k = k.strip()
                                v = s[1]
                                v = v.rstrip('\r\n')
                                v = v.rstrip('\n')
                                if not v or len(v) > 1:
                                    print("ini key:(",k,") error plz check and run again!")
                                    return
                                fnt_change_words[k]=v
                                # print("k,v",k,v)
                            except TypeError as e:
                                print("ini error plz check and run again!")
                                return
    else:
        print("当前没有words.ini配置文件，生成文件.")
        f = open(wordsIniPath,'a',encoding='utf-8')
        s = '###配置文件###'
        f.write(s)
        f.close()
    #输出目录
    output_path_name="output"
    resourePath = "./"
    for parent,dirnames,filenames in os.walk(resourePath):
        # print(parent)
        # print(dirnames)
        # print(filenames)
        # 取第一层目录即可
        for dir_list in dirnames:
            srcpath = resourePath + dir_list
            print("start dir name:"+srcpath)
            output_path_name = srcpath+os.sep+"output"
            if not os.path.exists(output_path_name):
                os.makedirs(output_path_name)

            convert_list=dict()
            fnt_name = os.path.basename(srcpath)
            # 存对应的ascii码
            list = os.listdir(srcpath) #列出文件夹下所有的目录与文件
            for i in range(0,len(list)):
            # for filename in glob.glob(srcpath+os.sep+"*.png"):
                basename = list[i]
                # 判断是否是png
                isPng = basename[-4:]
                if isPng != ".png":
                    continue
                filename = srcpath+os.sep+basename
                # basename = os.path.basename(filename)
                font=basename[:basename.rfind(".")]
                # utf-8 下需要调用UTF-8编码
                # ascii_code = ascii_code.decode('UTF-8')
                # 手动处理不能命名的文件，囧。
                if str(font) in fnt_change_words :
                    print("font",font,fnt_change_words[str(font)])
                    font = fnt_change_words[str(font)]
                try:
                    ascii_code = ord(font)
                except TypeError as e:
                    print("font define name:" + font + " error !!")
                    return
                print("font " + font +  " ascii_code : %d" %(ascii_code))
                # print ascii_code
                convert_list[filename]=ascii_code
                continue
            check_and_make(fnt_name,convert_list,output_path_name)
        # 取第一层目录即可
        break


if __name__ == '__main__':
    main()

    os.system('pause')