import datetime
import hashlib
import inspect
import shutil
import math
import sys
import os

######################
## Folder Functions ##
######################

def join_paths(*args): # it joins a list of string in a proper file path; if the first argument is ~ it is turnded into the used home folder path 
    args = list(args)
    args[0] = os.path.expanduser("~") if args[0] == "~" else args[0]
    return os.path.abspath(os.path.join(*args))

def is_folder(folder, log = False):
    res = os.path.isdir(folder)
    if not res and log:
        print("not a folder:", folder)
    return res

def script_folder(): # the folder of the script executed
    return parent_folder(inspect.getfile(sys._getframe(1)))

def parent_folder(folder, level = 1): # it return the parent folder of the path or file given; if level is higher then 1 the process is iterated
    is_folder(folder)
    if level <= 0:
        return path
    elif level == 1:
        return os.path.abspath(os.path.join(folder, os.pardir))
    else:
        return parent_folder(parent_folder(folder, level - 1))

def folders(folder):
    is_folder(folder)
    files_and_folders = os.listdir(folder)
    folders = []
    for f in files_and_folders:
      file_path = os.path.join(folder, f)
      if is_folder(file_path):
          folders.append(file_path)
    folders.sort()
    return folders

def all_folders(folder):
    allfolders = folders(folder)
    for fol in folders(folder):
        allfolders += all_folders(fol)
    return allfolders

def create_folder(folder, log = False):
    if not is_folder(folder, log):
        os.makedirs(folder)
        if log:
            print("folder created:", folder)
    elif log:
        print("no folder to create:", folder)
        
def delete_folder(folder, log = False):
    if is_folder(folder):
        shutil.rmtree(folder, ignore_errors = True)
        if log:
            print('folder removed:', folder)
    elif log:
        print("no folder to remove:", folder)

####################
## File Functions ##
####################

def is_file(path, log = False): # returns True if path exists
    res = os.path.isfile(path)
    if not res and log:
        print("not a folder:", folder)
    return res

def files(path): # it returns files in a path (excluding subfolders)
    is_folder(path)
    files_and_folders = os.listdir(path)
    files = []
    for f in files_and_folders:
      file_path = os.path.join(path, f)
      if is_file(file_path):
          files.append(file_path)
    files.sort()
    return files

def all_files(path): # it returns all files in a folder and its subfolders
    allfiles = files(path)
    dirs = [fol for fol in folders(path)]
    for fol in dirs:
        allfiles += all_files(fol)
    return allfiles

def file_basename(path): # file base_name
    return os.path.basename(path)

def file_extension(path): 
    names = file_name(path).split('.')
    if len(names) >= 2:
        return '.'.join(names[1:])
    else:
        return ""

def delete_file(path, log = False):
    if is_file(path, log):
        os.remove(path)
        if log:
            print("file removed: ", path)
    elif log:
        print("no file to remove: ", path)

def file_copy(source, destination, log = False):
    if is_file(source, log):
        create_folder(parent_folder(destination))
        shutil.copyfile(source, destination)
        if log:
            print("file copied in", destination)
    elif log:
        print("no file to copy:", source)

def delete_empty_folders(folder, log = False):
    deleted = False
    for fol in folders(folder):
        if len(all_files(fol)) + len(all_folders(fol)) == 0:
            delete_folder(fol)
            print('empty folder removed:', folder)
            deleted = True
        else:
            deleted += delete_empty_folders(fol, log)
    if deleted:
        delete_empty_folders(folder, log)
    if deleted and log:
        print("all empty folders removed from:", folder)
    return deleted


#####################
#### Files Info #####
#####################

def file_size(path):
    return os.path.getsize(path)

def show_size(size): # properly shows the size of a file
    order = 0
    num = size
    if size != 0:
        order = int(math.log(size, 1000))
        num = size / 1000 ** order
    unit = "B"
    if order == 1:
        unit = "K" + unit
    if order == 2:
        unit = "M" + unit
    if order == 3:
        unit = "G" + unit
    if order >= 4:
        unit = "T" + unit
        num = size / 1000 ** 4
    if order == 0:
        num = int(num)
    else:
        num = round(num, 1)
    return str(num) + " " + unit

def files_size(file_list):
    return [file_size(f) for f in file_list]

def file_modification_time(path):
    time = os.path.getmtime(path)
    time = datetime.datetime.fromtimestamp(time)
    return time

def time_to_string(time):
    return time.strftime("%y/%m/%d-%H:%M:%S")

def md5(path, log = False):
     try:
        return hashlib.md5(open(path,"rb").read()).hexdigest()
     except:
         if log:
             print("no md5 found for ", file_basename(path))
         return path

######################
#### Folder Info #####
######################

def free_space(folder, log = False):
    if is_folder(folder, log):
        return shutil.disk_usage(folder)[2]
    else:
        return 0

def folder_size(path):
    return sum([file_size(f) for f in all_files(path)])

############################
#### Path Manipulation #####
############################

def first_subfolder(path, sub_path):
    common = os.path.commonprefix([sub_path, path])
    return sub_path[len(common) + 1:].split('/')[0]
# first_subfolder("/home/user", "/home/user/subfolder/file.est") = "subfolder"


##############################
#### String Manipulation #####
##############################

def pad_string(string, length = 20, alignment = 0): # it cuts a string if longer then 'length'
    if len(string) > length:
        string = string[0 : length - 5] + " ... "
        spaces = ""
    else:
        spaces = " " * (length - len(string))
    if alignment == 0:
        string += spaces
    else:
        string = spaces + string
    return string

############################
##### Backup Helper ########
############################

def clear_terminal():
    sys.stdout.write('\033c')

def loop_input(message):
    ans = ""
    while ans != "y" and ans != "n":
        ans = input(message)
    return 1 if ans == "y" else 0

class progress_indicator():
    def __init__(self, tot):
        self.counter = 0
        self.tot = tot
        
    def update(self, new_val):
        self.counter += new_val
        
    def show(self, message = ""):
        print('\r', end = "")
        print(str(round(100 * self.counter / self.tot, 1)) + " % " + message, end = "")
        
    def close(self):
        print('')

def flat(array):
    return [item for sublist in array for item in sublist]

def terminal_size():
    y , x = map(int, os.popen('stty size', 'r').read().split())
    return [x, y]

#########################
#### Backup Manager #####
#########################

class backup():
    def __init__(self, source, destin):
        self.source = source
        self.destin = destin
        
        self.source_acquired = False
        self.destin_acquired = False
        self.backup_acquired = False

        self.main()

    def main(self):
        clear_terminal()
        print("Backup Script" + "\n")
        is_folder(self.source)
        is_folder(self.destin)
        p = 12
        
        print(pad_string("source",      11), self.source)
        print(pad_string("destination", 11), self.destin)

        print()
        self.get_source()
        self.get_destin()

        if self.source_len == 0:
            print("nothing to backup")
            return 0
        
        print()
        p = 24
        print(pad_string("number of files to copy", p), self.source_len)
        print(pad_string("total size to copy", p), show_size(self.source_size))
        print()
        
        if self.source_size < free_space(self.destin):
            space = True
            print("there is enough space in destination")
        else:
            space = False
            print("not enough space to copy: wait ...")
            self.get_delatable()
            print("you could delete these folders in destination: ")
            for n in range(len(self.delatable)):
                print("•",file_basename(self.delatable[n]))
            if loop_input("delete? "):
                for fol in self.delatable:
                    delete_folder(fol, True)
                space = True
                self.destin_acquired = False

        if space and loop_input("proceed coping? "):
            self.get_backup()
            delete_folder(self.backup_folder, True)
            self.do_backup()

        print()
        if loop_input("search for duplicate files in destination? "):
            self.get_destin()
            self.get_destin_md5()
            self.get_duplicates()
            self.get_duplicates_to_delete()

            if self.duplicates_len == 0:
                print("no duplicates to delete")
            else:
                if loop_input(str(self.duplicates_len) + " duplicates found: do you want to view them? "):
                    self.view_duplicates()
                if loop_input("removed the red colored files permanently? "):
                    self.delete_duplicates()

        print()
        if loop_input("remove empty folders in destination? "):
            deleted = delete_empty_folders(self.destin, True)
            if not deleted:
                print("no empty folders to remove")
        
    def get_source(self):
        if self.source_acquired == False:
            self.source_files = all_files(self.source)
            self.source_len = len(self.source_files)
            self.source_sizes = files_size(self.source_files)
            self.source_size = sum(self.source_sizes)
            self.source_acquired = True
            print("source files acquired")
        else:
            print("source files already acquired")

    def get_destin(self):
        if self.destin_acquired == False:
            self.destin_files = all_files(self.destin)
            self.destin_len = len(self.destin_files)
            self.destin_sizes = files_size(self.destin_files)
            self.destin_size = sum(self.destin_sizes)
            self.destin_free = free_space(self.destin)
            self.destin_folders = folders(self.destin)
            self.destin_folders_sizes = [folder_size(fol) for fol in self.destin_folders]
            self.destin_acquired = True
            print("destination files acquired")
        else:
            print("destination files already acquired")

    def get_delatable(self):
        to_delete = []
        for n in range(len(self.destin_folders)):
            to_delete = self.destin_folders[0 : n + 1]
            partial_size = self.destin_folders_sizes[0 : n + 1]
            if sum(partial_size) + self.destin_free > self.source_size:
                break
        self.delatable = to_delete

    def get_backup(self):
        if self.backup_acquired == False:
            self.today = datetime.date.today().strftime("%y-%m-%d")
            self.backup_folder = self.destin + '/' + self.today
            self.backup_files = [self.backup_folder + f[len(self.source):] for f in self.source_files]
            self.backup_len = len(self.backup_files)
            self.backup_acquired = True
            print("backup files acquired")
        else:
            print("backup files already acquired")

    def do_backup(self):
        print("copying ...")
        progress = progress_indicator(self.source_size)
        for s in range(len(self.source_sizes)):
            file_copy(self.source_files[s], self.backup_files[s])
            progress.update(self.source_sizes[s])
            progress.show()
        progress.close()
        print("copied")

    def get_destin_md5(self):
        print("acquiring destination md5 info ...")
        self.destin_md5 = []
        progress = progress_indicator(self.destin_size)
        for s in range(len(self.destin_sizes)):
            progress.update(self.destin_sizes[s])
            progress.show()
            self.destin_md5.append(md5(self.destin_files[s], True))
        progress.close()
        
    def get_duplicates(self):
        print("searching for duplicates ...")
        self.duplicates = []
        progress = progress_indicator(self.destin_size)
        for s in range(len(self.destin_files)):
            progress.update(self.destin_sizes[s])
            progress.show()
            previous_duplicates = flat(self.duplicates)
            if self.destin_files[s] in previous_duplicates:
                continue
            current_duplicates = [self.destin_files[a] for a in range(self.destin_len) if a != s and self.destin_md5[a] == self.destin_md5[s]]
            if len(current_duplicates) > 1:
                self.duplicates.append(current_duplicates)
        progress.close()
        self.duplicates_len = len(self.duplicates)

    def get_duplicates_to_delete(self):
        self.duplicates_to_delete = []
        for s in range(self.duplicates_len):
            time = [file_modification_time(f) for f in self.duplicates[s]]
            to_delete = [False if el == max(time) else True for el in time]
            self.duplicates_to_delete.append(to_delete)

    def view_duplicates(self):
        length = int(terminal_size()[0] / 4)
        res = []
        for d in range(self.duplicates_len):
            line = ''
            for s in range(len(self.duplicates[d])):
                path = self.duplicates[d][s]
                delete_flag = self.duplicates_to_delete[d][s]
                color_code = '\x1b[31m' if delete_flag else '\x1b[32m'
                file_name = file_basename(path)
                file_name = pad_string(file_name, length)
                file_name = color_code + file_name + '\x1b[0m'
                size = show_size(file_size(path))
                size = pad_string(size, length)
                fol = first_subfolder(self.destin, path)
                fol = pad_string(fol, length)
                time = time_to_string(file_modification_time(path))
                time = pad_string(time, length, 1)
                line += file_name + size + fol + time + '\n'
            res.append(line)
            
        print("[press enter to continue or q to exit]")
        title = pad_string("file", length) + pad_string("size", length) + pad_string("folder", length) + pad_string("modification time", length, 1)
        print()
        print(title)
        for i in range(len(res)):
            print(res[i], end = "")
            if input() == "q":
                break

    def delete_duplicates(self):
        progress = progress_indicator(self.duplicates_len)
        for d in range(self.duplicates_len):
            for s in range(len(self.duplicates_to_delete[d])):
                if self.duplicates_to_delete[d][s]:
                    delete_file(self.duplicates[d][s])
            progress.update(1)
            progress.show()
        progress.close()
        print(str(self.duplicates_len) + " duplicates removed")

if __name__== "__main__":
    args = sys.argv
    source = os.path.abspath(args[1])
    destin = os.path.abspath(args[2])

    man = backup(source, destin)
