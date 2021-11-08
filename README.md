## 说明

>这是一个旨在让 [JA2-Stracciatella](https://github.com/ja2-stracciatella/ja2-stracciatella) 支持中文的配套项目。

## 准备环境

* 安装 [python](https://www.python.org/downloads/) 3.6 或以上版本 
    

* 安装 [Pillow](https://python-pillow.org/)
    ```
    pip install pillow
    ```

* 安装 [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
    ```
    pip install openpyxl
    ```

* 安装 [pandas](https://pandas.pydata.org/)
    ```
    pip install pandas
    ```

* 下载字体
 
    https://github.com/andot/zfull-for-yosemite
    
    把 `Zfull-GB.ttf` 放在项目根目录下

## 脚本说明
* 从 edt 文件中导出文本到 execl 文件
    
    ```export_txt.py```

* 从 excel 文件中读取翻译，生成 edt 文件

    ```import_txt.py```

* 生成字库

    ```gen_font.py```