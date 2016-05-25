abc = 'abcdefghijklmnopqrstuvwxyz'

msg = 'g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr\'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.'
newmsg = ''
for i in range(len(msg)):
    pos = abc.find(msg[i])
    if pos >= 0:
        res = pos + 2
        res = res % len(abc)
        newmsg += abc[res]
    else:
        newmsg += msg[i]
print(newmsg)
