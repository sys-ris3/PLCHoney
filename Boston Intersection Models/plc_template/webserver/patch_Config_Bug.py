import os


def main():
    files = os.listdir("./")

    if "Config0.c" in files and "Config0.h" in files and "Res0.c" in files:
        exit(0)

    header = ''
    for _f in files:
        if _f.lower().startswith("conf"):
            if _f.endswith(".c"):
                cmd = "mv " + _f + " Config0.c"
                os.system(cmd)
            if _f.endswith(".h") and _f != "Config0.h" :
                header = _f
                print('header is ' + header)
                cmd = "mv " + _f + " Config0.h"
                os.system(cmd)
            
    for _f in files:
        if _f.lower().startswith("res"):
            if header != '':
                cmd = "sed -i 's/" + header + "/Config0.h/g' " + _f
                print(cmd)
                os.system(cmd)
            cmd = "mv " + _f + " Res0.c"
            os.system(cmd)


if __name__ == '__main__':
    main()
