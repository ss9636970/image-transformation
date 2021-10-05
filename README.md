# HW1-image transformation

# 1.  檔案說明
這次作業使用python只做，檔案列有兩個資料夾source_code、HW1_exe，source_code為原始碼裡面包含兩個py檔UI.py、utils.py，utils.py中包含作業要求的所有轉換方法，UI.py中包含將所有轉換方法執行的使用者介面，HW1_exe中有一個資料夾為dist，裡面有個檔案連結到google雲端，連結中有個UI.exe為這次作業的執行檔，這個執行檔是用python的pyinstaller將原始碼UI.py包成exe執行檔，開啟UI.exe即可執行這次作業的程式碼，底下為執行UI.py後的使用者介面使用方式說明。



# 2. 使用方式

開啟UI.exe後會出現一個標題為image transfers的視窗，視窗上方會有六個按鈕，最左邊的按鈕為開啟圖片檔按鈕，按下去之後可以選擇要開啟的圖片，HW1_exe資料夾中包含一個data資料夾，裡面有作業要用到的六張圖片分別為三個bmp檔和三個raw檔，另外兩個圖片檔graph128.jpg和graph32.jpg為網路上找的圖片，圖片大小分別為128 * 128、32 * 32，這兩張圖為在網路上找的圖片用PIL package轉為灰階後改變圖片大小成32 * 32、128 * 128。

除了最左邊的按鈕外，其他按鈕皆為作業二和三用到的圖片轉換方法，由左而右分別為，log-transform、gamma-transform、image negative、bilinear interpolation、nearest-neighbor interpolation，共五個方法，最右邊有一個文字框是用來選擇參數的，所有方法共用這個輸入參數的文字框，根據使用不同的方法，這個文字框代表的參數會有所不同。

log-transform: 請輸入一個大於0的數，可以為小數，代表log transformation的係數 c

gamma-transform: 請輸入介於0到1之間的數代表gamma transform的指數項 gamma

image negative: 不用輸入

bilinear interpolation、nearest-neighbor interpolation: 請輸入兩個正整數中間用逗號分割，ex: 512, 512，代表要轉成大小為 512 * 512的圖片

作業第一題寫在UI.py的open_img方法中，第二題跟第三題的方法寫在urils.py的類別Pic_Transformations的方法中，各個方法的細節會寫在pdf報告中。