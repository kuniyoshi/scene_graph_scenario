// Squirrelのサンプルコードだわ

// 変数の定義
local greeting = "こんにちは";
local name = "ひたぎ";
local count = 3;

// 関数の定義
function sayHello(greet, person, times) {
    for(local i = 0; i < times; i++) {
        print(greet + "、" + person + "！\n");
    }
}

// 関数の呼び出し
sayHello(greeting, name, count);