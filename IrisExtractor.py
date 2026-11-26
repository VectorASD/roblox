from rbxmReader import rbxmReader


if __name__ == "__main__":
    instances = rbxmReader("Iris.rbxm")
    for instance in instances.values():
        if instance._class == "ModuleScript":
            print(instance)
