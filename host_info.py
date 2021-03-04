import platform

def system_compatibility_check(delimiter=False):
    host_system = platform.system()
    if host_system == "Windows":
        delimiter_slash = "\\"
    elif host_system == "Linux" or host_system == "Darwin":
        delimiter_slash = "/"
    else:
        print(f"\n\nERROR:\t\"{host_system}\" is not supported operation system.\n\n"
              "\tFor further detail please visit project webpage: https://github.com/RajtoraM/DirCrawler\n"
              "\tPlease report this error at https://github.com/RajtoraM/DirCrawler/issues")
        quit()
    if delimiter:
        return delimiter_slash