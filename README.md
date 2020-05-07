# simple_assembler

[計算機科学実験及演習3(HW)](http://www.lab3.kuis.kyoto-u.ac.jp/~takase/le3a/)の仕様に準拠するアセンブラです．  
Pythonで記述されています．(Java版は[simple_simulator](https://github.com/kuis-isle3hw/simple_simulator)にオプション機能として同梱)  

アセンブリ命令のテキストファイルを入力として読み込み，QuartusのRAMに対応する.mif形式の情報を出力します．


## ツール・バージョン
- Python 3.7.6

## 使用方法
```
$ python3 assembler.py input-file [output-file]
```

- output-fileを省略した場合は標準出力に出力されます

## 注意点など

- [MIT License](LICENSE) です．この条項下で自由にご利用ください．また，本ツールの使用にあたって何か問題が起きても，スタッフは一切の責任を負いません．
- [SIMPLEアーキテクチャの基本命令セット](http://www.lab3.kuis.kyoto-u.ac.jp/~takase/le3a/#SIMPLE)のみに対応しています．
  - この範囲内でbugなどあればぜひ [Issue](../../issues) で教えてください．
  - この範囲内で機能追加や改善があれば [Pull request](../../pulls) も歓迎します．
  - 課題でもある独自の改良や拡張については，対応しません．


