# 支持文件类型
# 用16进制字符串的目的是可以知道文件头是多少字节
# 各种文件头的长度不一样，少半2字符，长则8字符
def typeList():
    print('获取文件格式十六进制码表……')
    return {
        "d0cf11e0a1b11ae10000": 'xls',
        '38425053000100000000': 'psd',
        'd0cf11e0a1b11ae10000': 'doc',
        '255044462d312e350d0a': 'pdf',
        '504b0304140006000800': 'docx',
        'd0cf11e0a1b11ae10000': 'wps'
    }


# 字节码转16进制字符串
def bytes2hex(bytes):
    print('关键码转码……')
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
            hexstr += t
    return hexstr.upper()


# 获取文件类型
def filetype(filename):
    print('读文件二进制码中……')
    # binfile = open(filename, 'rb')  # 必需二制字读取
    print('提取关键码……')
    # bins = binfile.read(20)  # 提取20个字符
    # binfile.close()  # 关闭文件流
    bins = bytes2hex(filename)  # 转码
    bins = bins.lower()  # 小写
    print(bins)
    tl = typeList()
    ftype = 'unknown'
    print('关键码比对中……')
    for hcode in tl.keys():
        lens = len(hcode)  # 需要的长度
        if filename[0:lens] == hcode:
            ftype = tl[hcode]
            break
    if ftype == 'unknown':  # 全码未找到，优化处理，码表取5位验证
        filename = filename[0:5]
        for hcode in tl.keys():
            if len(hcode) > 5 and filename == hcode[0:5]:
                ftype = tl[hcode]
                break
    return ftype
