from struct import unpack
from io import BytesIO
from math import sin, cos

import lz4.block  # pip install lz4


def exit(*a, **kw):
    print("Error:", *a, **kw)
    # input("Enter...")
    __builtins__.exit(*a, **kw)

# структура rbxm (Roblox Binary Model Format): https://dom.rojo.space/binary.html#byte-interleaving
# чей-то уже существующий python-вариант парсера rbxm: https://github.com/tapple/pyrxbm/blob/main/pyrxbm/binary.py
# основа LZ4-декомпрессора: https://github.com/python-lz4/python-lz4/blob/master/lz4libs/lz4.c#L1937
# процесс обращения с robloxAssetDelivery (взял только ссылку rbxassetidReadURL): https://github.com/Anaminus/rbxmk/blob/imperative/library/rbxassetid.go
# структура сеток (Roblox Mesh Format): https://devforum.roblox.com/t/roblox-mesh-format/326114
# структура CSGPHS (встречается в Shared String): https://devforum.roblox.com/t/some-info-on-sharedstrings-for-custom-collision-data-meshparts-unions-etc/294588

# пример цепочки ссылок:
#     rbxassetid://17481576983
#     https://assetdelivery.roblox.com/v1/assetId/17481576983
#     https://c7.rbxcdn.com/c9cf425d469ebf995547557fdb3d8f07
# уже ранее известно, что семёрка после 'c' - номер CDN-сервера, что просто модуль 8 суммы ascii/unicode-кодов hex-символов хеша





def String(content): # 0x01
    L = unpack("<I", content.read(4))[0]
    str = content.read(L)
    if len(str) < L: exit("Неудачная попытка считывания строки длины %s: %r" % (L, str))
    return str if any(i < 32 for i in str) else str.decode("utf-8")

def Bool(content, count): # 0x02
    arr = content.read(count)
    for byte in arr:
        if byte not in range(2): exit("Недопустимое Bool-значение: %s" % byte)
    return map(bool, arr)

def Int32(content, count): # 0x03
    data = b"".join(map(bytes, zip(*(content.read(count) for i in range(4)))))
    referents = tuple((x >> 1) ^ -(x & 1) for x in unpack(">%sI" % count, data))
    return referents

def Float(bytes):
    # Standard	seeeeeee emmmmmmm mmmmmmmm mmmmmmmm
    # Roblox	eeeeeeee mmmmmmmm mmmmmmmm mmmmmmms
    #exp, b, c, d = content.read(4)
    #mant, sign = b << 15 | c << 7 | d >> 1, d & 1
    #data = sign << 31 | exp << 23 | mant
    #print(data.to_bytes(4, "big").hex())
    #return unpack(">f", data.to_bytes(4, "big"))[0]
    x = int.from_bytes(bytes, "big", signed = False) # signed и так по умолчанию = False... просто пометил
    return unpack(">f", ((x & 1) << 31 | x >> 1).to_bytes(4, "big"))[0]
#print(Float(bytes.fromhex("7c400001"))) # -0.15625 ok!
#exit()
def Float32(content, count): # 0x04
    return (Float(bytes(i)) for i in zip(*(content.read(count) for i in range(4))))

def Float64(content, count): # 0x05
    return unpack("<%sd" % count, content.read(count * 8))

def UDim(content, count): # 0x06
    scale = Float32(content, count)
    offset = Int32(content, count)
    return zip(scale, offset)

def UDim2(content, count): # 0x07
    scale = Float32(content, count)
    scale2 = Float32(content, count)
    offset = Int32(content, count)
    offset2 = Int32(content, count)
    return zip(zip(scale, offset), zip(scale2, offset2))

def Color3(content, count): # 0x0c
    R = Float32(content, count)
    G = Float32(content, count)
    B = Float32(content, count)
    return zip(R, G, B)

def Vector2(content, count): # 0x0d
    X = Float32(content, count)
    Y = Float32(content, count)
    return zip(X, Y)

def Vector3(content, count): # 0x0e
    X = Float32(content, count)
    Y = Float32(content, count)
    Z = Float32(content, count)
    return zip(X, Y, Z)

def getRotators():
    def rotX(s, c): return 1, 0, 0, 0, c, -s, 0, s, c
    def rotY(s, c): return c, 0, s, 0, 1, 0, -s, 0, c
    def rotZ(s, c): return c, -s, 0, s, c, 0, 0, 0, 1
    def mul(a, b):
        a00, a01, a02, a10, a11, a12, a20, a21, a22 = a
        b00, b01, b02, b10, b11, b12, b20, b21, b22 = b
        return (
            a00 * b00 + a01 * b10 + a02 * b20, a00 * b01 + a01 * b11 + a02 * b21, a00 * b02 + a01 * b12 + a02 * b22,
            a10 * b00 + a11 * b10 + a12 * b20, a10 * b01 + a11 * b11 + a12 * b21, a10 * b02 + a11 * b12 + a12 * b22,
            a20 * b00 + a21 * b10 + a22 * b20, a20 * b01 + a21 * b11 + a22 * b21, a20 * b02 + a21 * b12 + a22 * b22)
    pi180 = 0.017453292519943295
    def fromEulerAngles(x, y, z): # проверено в Roblox Studio на print(CFrame.fromEulerAngles(math.rad(10), math.rad(20), math.rad(30)))
        x, y, z = x * pi180, y * pi180, z * pi180
        sx, cx, sy, cy, sz, cz = sin(x), cos(x), sin(y), cos(y), sin(z), cos(z)
        return mul(mul(rotX(sx, cx), rotY(sy, cy)), rotZ(sz, cz))
    def fromEulerAnglesYXZ(x, y, z): # проверено в Roblox Studio на print(CFrame.fromEulerAnglesYXZ(math.rad(10), math.rad(20), math.rad(30)))
        x, y, z = x * pi180, y * pi180, z * pi180
        sx, cx, sy, cy, sz, cz = sin(x), cos(x), sin(y), cos(y), sin(z), cos(z)
        return mul(mul(rotY(sy, cy), rotX(sx, cx)), rotZ(sz, cz))
    rotators = (
        None, None, (0, 0, 0), (90, 0, 0), None, (0, 180, 180), (-90, 0, 0), (0, 180, 90), None, (0, 90, 90),
        (0, 0, 90), None, (0, -90, 90), (-90, -90, 0), (0, -90, 0), None, (90, -90, 0), (0, 90, 180),
        None, None, (0, 180, 0), (-90, -180, 0), None, (0, 0, 180), (90, 180, 0), (0, 0, -90), None, (0, -90, -90),
        (0, -180, -90), None, (0, 90, -90), (90, 90, 0), (0, 90, 0), None, (-90, 90, 0), (0, -90, 180))
    #for i, j in enumerate(rotators):
    #    if j: print(hex(i), j) всё сошлось
    return tuple((fromEulerAnglesYXZ(rotator[0], rotator[1], rotator[2]) if rotator else None) for rotator in rotators)
    # также, properties explorer в Roblox Studio преобразует поворот именно по fromEulerAnglesYXZ, а не fromEulerAngles!
CFrameRotators = getRotators()

def CFrame(content, count): # 0x10
    rotators = []
    for i in range(count):
        ID = content.read(1)[0]
        if ID:
            try: rotator = CFrameRotators[ID]
            except KeyError: rotator = None
            if rotator is None: exit("Недопустимое значение вращателя CFrame: %s" % ID)
            rotators.append(rotator)
        else: rotators.append(unpack("<9f", content.read(36)))
    return (vec + rot for rot, vec in zip(rotators, Vector3(content, count)))

def Enum(content, count): # 0x12
    data = b"".join(map(bytes, zip(*(content.read(count) for i in range(4)))))
    return unpack(">%sI" % count, data)

def Referent(content, count): # 0x13
    data = b"".join(map(bytes, zip(*(content.read(count) for i in range(4)))))
    referents = [(x >> 1) ^ -(x & 1) for x in unpack(">%sI" % count, data)]
    for i in range(1, count): referents[i] += referents[i - 1]
    return referents

def Rect(content, count): # 0x18 не до конца протестировано
    MinX = Float32(content, count)
    MinY = Float32(content, count)
    MaxX = Float32(content, count)
    MaxY = Float32(content, count)
    return zip(zip(MinX, MaxX), zip(MinY, MaxY))

def PhysicalProperties(content, count): # 0x19
    #content = BytesIO(bytes.fromhex("00 01 33 33 33 3f 9a 99 99 3e 00 00 00 3f 00 00 80 3f 00 00 80 3f".replace(" ", "")) + b"\0" * (count - 2))
    return tuple(unpack("<5f", content.read(20)) if content.read(1)[0] else None for i in range(count))

def Color3uint8(content, count): # 0x1a
    R = content.read(count)
    G = content.read(count)
    B = content.read(count)
    return zip(R, G, B)

def Int64(content, count): # 0x1b
    data = b"".join(map(bytes, zip(*(content.read(count) for i in range(8)))))
    return ((x >> 1) ^ -(x & 1) for x in unpack(">%sQ" % count, data))

def SharedString(content, count): # 0x1c
    data = b"".join(map(bytes, zip(*(content.read(count) for i in range(4)))))
    return (SStrings[i] for i in unpack(">%sI" % count, data))

def OptionalCoordinateFrame(content, count): # 0x1e
    # content = BytesIO(bytes.fromhex("10 0a 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7f 00 00 00 00 00 00 00 02 01 00".replace(" ", "")))
    # count = 2
    if content.read(1)[0] != 0x10: exit("Ожидался CFrame внутри OptionalCoordinateFrame")
    cframes = CFrame(content, count)
    if content.read(1)[0] != 0x02: exit("Ожидался Bool внутри OptionalCoordinateFrame")
    have_a_value = Bool(content, count)
    return zip(have_a_value, cframes)

def Font(content, count): # 0x20
    fonts = []
    for i in range(count):
        family = String(content)
        weight, style = unpack("<HB", content.read(3))
        cachedFaceId = String(content)
        fonts.append((family, weight, style, cachedFaceId))
    return fonts

def Capabilities(content, count): # 0x21
    print(content.read().hex())
    return "?" * count
    exit()

#dbgType = 0x13
dbgType = None

PROP_types = {
    # 0x00: не существует
    0x01: lambda content, count: (String(content) for i in range(count)),
    0x02: Bool,
    0x03: Int32,
    0x04: Float32,
    0x05: Float64,
    0x06: UDim,
    0x07: UDim2,
    # 0x08: Ray,
    # 0x09: Faces,
    # 0x0a: Axes,
    # 0x0b: BrickColor,
    0x0c: Color3,
    0x0d: Vector2,
    0x0e: Vector3,
    # 0x0f: не существует
    0x10: CFrame,
    # 0x11: не существует
    0x12: Enum,
    0x13: Referent,
    # 0x14: Vector3int16
    # 0x15: NumberSequence
    # 0x16: ColorSequence,
    # 0x17: NumberRange,
    0x18: Rect,
    0x19: PhysicalProperties,
    0x1a: Color3uint8,
    0x1b: Int64,
    0x1c: SharedString,
    # 0x1d: Bytecode,
    0x1e: OptionalCoordinateFrame,
    # 0x1f: UniqueId,
    0x20: Font,
    # 0x21: Capabilities, неизвестное содержание. Везде нулевые байты :/
    # всё, что после 0x21: не существует
}





def META(content):
    entries = unpack("<I", content.read(4))[0]
    meta = {}
    for i in range(entries):
        key, value = String(content), String(content)
        try:
            conflict = meta[key]
            exit("Конфликтный ключ %r: %r <-> %r" % (key, conflict, value))
        except KeyError: meta[key] = value
    what = content.read()
    if what: exit("Не до конца считанный META-чанк: %s" % what)
    return meta

def SSTR(content): # Shared STRings
    version, count = unpack("<II", content.read(8))
    SStrings = []
    if version != 0: exit("Странная версия SSTR-чанка: %s" % version)
    for i in range(count):
        hash, str = content.read(16), String(content)[:256] # заглушка по длине строки
        print("%s %r" % (hash.hex(), str))
        SStrings.append(str)
    what = content.read()
    if what: exit("Не до конца считанный SSTR-чанк: %s" % what)
    return SStrings

def INST(content):
    classID = unpack("<I", content.read(4))[0]
    className = String(content)
    objectFormat, count = unpack("<BI", content.read(5))
    if objectFormat not in range(2): exit("Неизвестный формат INST-чанка: %s" % objectFormat)
    referents = Referent(content, count)
    markers = unpack("<%sB" % count, content.read(count)) if objectFormat else None
    what = content.read()
    if what: exit("Не до конца считанный INST-чанк: %s" % what)
    return classID, className, objectFormat, referents, markers

typesAll = set()
def PROP(content):
    classID = unpack("<I", content.read(4))[0]
    propertyName = String(content)
    typeID = content.read(1)[0]
    typesAll.add(typeID)

    try: inst = classes[classID]
    except KeyError: exit("Несуществующий classID в PROP-чанке: %s" % classID)
    className, objectFormat, referents, markers = inst
    count = len(referents)

    try:
        Type = PROP_types[typeID]
        if dbgType is None or typeID == dbgType:
            # print()
            print(propertyName, hex(typeID), "| class:", classID, className, count, referents, "---> ", end = "")
    except KeyError: Type = None

    if Type is None:
        print("Неизвестный typeID: %s" % typeID)
        values = ()
    else: values = Type(content, count)

    values2 = [] # только для печати
    for id, value in zip(referents, values):
        values2.append(value)
        try: node = instances[id]
        except KeyError: exit("Нет экземпляра с таким id: %s" % id)
        try:
            conflict = node[propertyName]
            exit("Повторяющийся параметр %r: %r <-> %r" % (propertyName, conflict, value))
        except KeyError:
            #if dbgType is None or typeID == dbgType or propertyName == "Name":
            node[propertyName] = typeID, value

    if dbgType is None:
        if Type is not None:
            what = content.read()
            if what: exit("Не до конца считанный PROP-чанк: %s" % what)
            print(tuple(values2))
            # print()
    elif typeID == dbgType:
        what = content.read()
        print(count, len(what), what.hex(), tuple(values2))
        print()

def PRNT(content): # parents
    version, count = unpack("<BI", content.read(5))
    if version != 0: exit("Странная версия PRNT-чанка: %s" % version)
    childs = Referent(content, count)
    parents = Referent(content, count)
    for child, parent in zip(childs, parents):
        try: L = instances[child]
        except KeyError: exit("Нет потомка с таким id: %s" % child)
        try: R = instances[parent]
        except KeyError: exit("Нет родителя с таким id: %s" % parent)
        if L["_parent"] is not None: exit("Повторное присвоение родителя: %s %s %s %s" % (child, parent, L, R))
        L["_parent"] = R
        R["_childs"].append(L)
        # print(child, parent, L, R)
    for node in instances.values():
        if node["_parent"] is None: exit("Существует узел без родителя: %s" % node)
    what = content.read()
    if what: exit("Не до конца считанный PRNT-чанк: %s" % what)
    return childs, parents





SStrings = None
classes = {}
root = {"_id": -1, "_parent": "x", "_childs": [], "_class": "root", "Name": (1, "root")}
instances = {-1: root}

def printTree(node = root, lvl = "", check = False):
    id, parent, childs, className, name = node["_id"], node["_parent"], node["_childs"], node["_class"], node["Name"][1]
    data = {k: v for k, v in node.items() if k not in {"_id", "_parent", "_childs", "_class", "Name"}}
    data = {k: v for k, (t, v) in data.items() if dbgType is None or t == dbgType}

    checked = dbgType is None or any(printTree(child, "", True) for child in childs)
    if check: return bool(data) or checked

    if data or checked: print("%s%s %s (%s) %s" % (lvl, id, name, className, data))
    lvl += "| "
    for child in childs: printTree(child, lvl)

def Chunk(file):
    global SStrings

    name, compressL, uncompressL, reserved = unpack("<4sII4s", file.read(16))
    while name[-1] == 0: name = name[:-1]
    print("Чанк %r длины %s -> %s" % (name, compressL, uncompressL))
    if reserved != b"\0" * 4: exit("Странный reserved чанка: %s" % reserved.hex())

    compressed = compressL > 0
    dataL = compressL if compressed else uncompressL
    chunk = file.read(dataL)
    #print(chunk)
    data = lz4.block.decompress(chunk, uncompressL) if compressed else chunk
    # check = lz4.block.compress(data, store_size=False)
    content = BytesIO(data)
    if name == b"META":
        meta = META(content)
        print(meta)
    elif name == b"SSTR":
        SStrings = SSTR(content)
        print(SStrings)
    elif name == b"INST":
        classID, className, objectFormat, referents, markers = INST(content)
        print(classID, className, "service" if objectFormat else "regular", referents, markers)
        inst = className, objectFormat, referents, markers
        try:
            conflict = classes[classID]
            exit("Конфликтный classID %r: %r <-> %r" % (classID, conflict, inst))
        except KeyError: classes[classID] = inst

        for referent in referents:
            data = {"_id": referent, "_parent": None, "_childs": [], "_class": className}
            try:
                conflict = instances[referent]
                exit("Конфликтный referent %r: %r <-> %r" % (referent, conflict, data))
            except: instances[referent] = data
    elif name == b"PROP":
        PROP(content)
        #exit("OK")
    elif name == b"PRNT":
        PRNT(content)
    elif name == b"END":
        if data != b'</roblox>': print("Странное окончание: %r" % data)
        return True
    else: exit("UNKNOWN CHUNK (%r): %r" % (name, data))

def rbxmReader(name):
    with open(name, "rb") as file:
        if file.read(8) != b'<roblox!': exit("Это не rbxm!")
        sign = file.read(6).hex()
        if sign != "89ff0d0a1a0a": exit("Неверная подпись: %s" % sign)
        version, classes, instances, reserved = unpack("<Hii8s", file.read(18))
        print("Класов:", classes)
        print("Экземпляров:", instances)
        if version != 0: exit("Странная версия заголовка: %s" % version)
        if reserved != b"\0" * 8: exit("Странный reserved заголовка: %s" % reserved.hex())
        while True:
            end = Chunk(file)
            if end: break


if __name__ == "__main__":
    # rbxmReader("rbxm/avatar3.rbxm")
    # rbxmReader("rbxm/gui.rbxm")
    # rbxmReader("rbxm/headAsset.rbxm")
    # rbxmReader("rbxm/SolarSystem.rbxm")
    rbxmReader("rbxm/CageDeformerPlugin")

    print("=" * 77)
    printTree()
    # print(*map(hex, sorted(typesAll)))
    print("OK!")
