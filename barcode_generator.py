#TP04
import tkinter as tk
import tkinter.messagebox as tkmsg

def checksumdigit(code) :                              #fungsi untuk menghitung checkdigit
    checksum = 0                                       
    for i in code [::2] :
        num = int(i) 
        checksum += num
    for i in code [1::2] :
        xweight = int(i)*3
        checksum += xweight
    x = checksum % 10
    if x != 0 :
        checkdigit = 10 - x
    else :                                            #kemudian checkdigit yang diperoleh digunakan lagi
        checkdigit = x                                #untuk membuat pattern barcode
    return EAN_13(checkdigit, code)                     

def EAN_13 (checkdigit, code) :                          #fungsi untuk mencari pattern barcode
    codes = code + str (checkdigit)                      #yang sesuai dengan EAN-13
    firstgroup_6digit = {0:'LLLLLL', 1:'LLGLGG', 2:'LLGGLG', 3:'LLGGGL', 4:'LGLLGG',
                        5:'LGGLLG', 6:'LGGGLL', 7:'LGLGLG', 8:'LGLGGL', 9:'LGGLGL'}
    Lcode = {0:'0001101', 1:'0011001', 2:'0010011', 3:'0111101', 4:'0100011',
            5:'0110001', 6:'0101111', 7:'0111011', 8:'0110111', 9:'0001011'}
    EAN_structure = firstgroup_6digit[int(codes[0])] + 'RRRRRR'      #membuat EAN structure untuk membuat pattern barcode
    barcode_pattern = []                                             #berdasarkan huruf awal sebuah code
    barcode_pattern.append(('first', code[0]))
    barcode_pattern.append(('S', '101'))            #append ke list of tuple barcode_pattern sesuai urutan
    b = 0
    for i in range(1,7) :
        per_code = codes[i]                         
        if EAN_structure[b] == 'L' :                
            barcode_pattern.append((per_code, Lcode[int(per_code)]))
        elif EAN_structure[b] == 'G' :
            R_code = ''
            for num in Lcode[int(per_code)] :         #membaca percode dan mengubahnya menjadi 7 bit
                if num == '0' :                       #berdasarkan EAN structure nya, apakah L M atau R code
                    R_code += '1'
                else :
                    R_code += '0'
            G_code = R_code[::-1]
            barcode_pattern.append((per_code, G_code))
        b+=1
    barcode_pattern.append(('M', '01010'))            #menambahkan batas di middle ke pattern barcode
    for j in range (7,13) :
        percode = codes[j]
        R_code = ''
        for num in Lcode[int(percode)] :
            if num == '0' :                           #membaca percode dan mengubahnya menjadi 7 bit
                R_code += '1'                         #berdasarkan EAN structure nya, apakah L M atau R code
            else :
                R_code += '0'
        barcode_pattern.append((percode, R_code))
    barcode_pattern.append(('E', '101'))               #menambahkan batas akhir ke pattern barcode
    return barcode_pattern                             #return list of tuple barcode_pattern agar dapat digunakan kembali

class BarcodeApp (tk.Frame) :              
    def __init__(self, master = None):
        super().__init__ (master)                      #membuat frame di mainwindow
        self.pack()
        self.file_name = tk.StringVar()               #variable untuk menyimpan jawaban pada entry file name
        self.codes = tk.StringVar()                    #variable untuk menyimpan jawaban pada entry code
        self.create_widgets()

    def create_widgets(self) :                        #membuat widget sesuai dengan apa yang diinginkan
        self.label1 = tk.Label(self, text='Save barcode to PS file [eg: EAN13.eps]:').pack()    #menambahkan label untuk nama file
        self.ent_file = tk.Entry(self, textvariable = self.file_name)              #membuat kotak entry dan di bind focusout
        self.ent_file.bind('<FocusOut>', self.entryfile)                           #lalu menuju ke event self.entryfile
        self.ent_file.pack()                                                       #dan di pack ke frame tersebut
        self.label2 = tk.Label(self, text='Enter code (first 12 decimal digits):').pack()        #menambahkan label untuk code
        self.ent_code = tk.Entry(self, textvariable = self.codes)                  #membuat kotak entry dan di bind return
        self.ent_code.bind('<Return>', self.entrycode)                             #lalu menuju ke event self.entrycode
        self.ent_code.pack()
        self.canvas = tk.Canvas(self, width=400, height=250, bg='white')           #membuat canvas kosong dan di pack
        self.canvas.pack()

    def entryfile(self, event) :                       #event ini agar program notice jika nama file yang dimasukkan
        file_name = self.file_name.get()               #tidak valid sehingga harus diberi warning dan meminta kembali
        if file_name [:-5:-1] != 'spe.' : 
            tkmsg.showwarning ('WrongInput', 'Please enter correct input file name.')

    def entrycode (self, event) :                      #event ini agar program notice jika code yang dimasukkan
        code = self.codes.get()                        #tidak valid sehigga diberi warning dan meminta kembali
        if len(code) != 12 :
            tkmsg.showwarning ('WrongInput', 'Please enter correct input code.')
        else :                                         #jika code valid, jalankan fungsi menghitung checkdigit
            self.barcode_pattern = checksumdigit(code)
            self.create_canvas()                       #setelah masuk ke fungsi create_canvas

    def create_canvas(self) :                        #fungsi untuk membuat barcode pada canvas
        x = 100                                      #yang telah dipack sebelumnya
        a = 90
        self.canvas.delete('all')                    #delete objek yang ada di canvas agar tidak tertumpuk-tumpuk
        self.canvas.create_text(200, 50, text='EAN-13 Barcode:', fill='blue')
        for code, ean in self.barcode_pattern :
            if code == 'S' or code == 'M' or code == 'E' :
                for num in ean :                              #jika bit nya 1, membuat line dengan panjang 110 untuk batas awal
                    if num == '1':                            #batas tengah dan batas akhir
                        self.canvas.create_line (x,75,x,185, width=2, fill='green')
                    else :
                        pass                                  #jika bit 0, lewatkan 
                    x += 2                                    #x akan terus bertambah agar line terus bergeser ke kanan
            else :
                for num in ean :                    #jika bukan batas, gambar line dengan panjang hanya 100
                    if num == '1':
                        self.canvas.create_line (x,75,x,175, width=2, fill='purple')
                    else:                           #jika bit 0, lewatkan
                        pass
                    x += 2
        self.canvas.create_text (a, 190, text=self.barcode_pattern[0][1], fill='black')
        for i in range (1,16) :                     #membuat text dengan nomor kode-kode dibawah barcode
            a += 13                                 #berjarak 13 pixel ke kanan
            if self.barcode_pattern[i][0] == 'S' or self.barcode_pattern[i][0] == 'M' or self.barcode_pattern[i][0] == 'E' :
                pass                                #jika batas, lewatkan
            else :
                self.canvas.create_text (a, 190, text= self.barcode_pattern[i][0])
        self.canvas.create_text(200, 220, text=f'Check Digit: {self.barcode_pattern[14][0]}', 
                                fill='red', font='arial')                                   #menampilkan check digit
    
        self.canvas.postscript(file=self.file_name.get(), colormode='color', height = 250, width = 400)
        #membuat file yang berisi barcode dengan code yang dimasukkan dan bernama sesuai dengan yang dimasukkan

if __name__ == "__main__":
    myapp = BarcodeApp()                             #menjalankan main program
    myapp.master.title('EAN-13 [by Icha]')
    myapp.master.mainloop()
