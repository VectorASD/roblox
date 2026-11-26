from rbxmReader import rbxmReader

import os


if __name__ == "__main__":
    instances = rbxmReader("Iris.rbxm")
    for instance in instances.values():
        if instance._class == "ModuleScript":
            path = instance.path()
            path += "/init.lua" if path in ("Iris", "Iris/widgets") else ".lua"
            os.makedirs(path.rsplit('/', 1)[0], exist_ok=True)

            source = instance.data["Source"][1]
            if b'\r\n' not in source:
                source = source.replace(b'\n', b'\r\n')  # Unix (LF) -> Windows (CR LF)

            with open(path, "wb") as file:
                file.write(source)
