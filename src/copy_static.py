import os, shutil

def list_static_contents(destination = "static") -> list:
    # list contents of static dir with recursive call, replacing dir with (dir, contents) tuple
    # returns a list

    # escape
    if not os.path.exists(destination):
        raise OSError(f"Destination {destination} does not exist.")

    # build contents list
    contents = [os.path.join(destination, item) for item in os.listdir(destination)]
    for (i, c) in enumerate(contents):
        if os.path.isdir(c):
            contents[i] = (c, list_static_contents(c)) # recursive call if directory found

    return contents

def strip_leading_destination(destination: str) -> str:
    # strip the leading destination from the destinations provided by list_static_contents()
    # called individually depending on dir or file in copy_static_contents()
    # usually removes "static/" but fundamentally agnostic
    path_list = destination.split("/") # this is not platform agnostic I think
    return "/".join(path_list[1:])
    

def copy_static_contents(contents: list, destination = "../public") -> None:
    # copy static dir in src dir to public dir in root dir

    # escapes
    if len(contents) == 0: # in case contents are empty
        return
    if os.path.exists(destination): # idempotency (this is sus) 
        shutil.rmtree(destination)
    os.mkdir(destination)


    # iterate over contents, copying per item, checking if  dir or file
    for c in contents:
        
        if type(c) == tuple: # this means it's a dir
            new_path = os.path.join(destination, strip_leading_destination(c[0])) # this is the dir path, e.g. os.path.join("../public", "images") -> "../public/images"
            #os.mkdir(new_path)
            copy_static_contents(c[1], new_path) # recursive call for populating a dir
        
        else: #in case it is NOT a dir
            new_path = os.path.join(destination, os.path.basename(c)) # this is the dir path, e.g. os.path.join("../public", "images") -> "../public/images"
            shutil.copy(c, new_path)
            
    return

def main():
    contents = list_static_contents()
    copy_static_contents(contents)


if __name__ == "__main__":
    main()
