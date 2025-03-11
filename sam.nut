// クラスの定義だわ
class Character {
    // コンストラクタ
    constructor(name, hp, atk) {
        this.name = name;
        this.hp = hp;
        this.atk = atk;
    }

    // メソッド
    attack(target) {
        print(this.name + "が" + target.name + "に攻撃したわ。\n");
        target.takeDamage(this.atk);
    }

    takeDamage(amount) {
        this.hp -= amount;
        print(this.name + "のHPは" + this.hp + "になったわ。\n");
        if (this.hp <= 0) {
            print(this.name + "は倒れてしまったわ…。\n");
        }
    }

    // 状態を表示するメソッド
    status() {
        print(this.name + ": HP=" + this.hp + ", ATK=" + this.atk + "\n");
    }
}

// 配列とテーブルを使ったアイテム管理だわ
local inventory = [
    { name = "ポーション", effect = function(character) {
        character.hp += 30;
        print(character.name + "はポーションを使って、HPが30回復したわ。\n");
    }},
    { name = "パワーアップ", effect = function(character) {
        character.atk += 5;
        print(character.name + "の攻撃力が5上がったわ。\n");
    }},
];

// アイテムを使う関数だわ
function useItem(character, itemIndex) {
    if (itemIndex >= 0 && itemIndex < inventory.len()) {
        inventory[itemIndex].effect(character);
        // 使ったアイテムを削除するわ
        inventory.remove(itemIndex);
    } else {
        print("アイテムが存在しないわ。\n");
    }
}

// バトルの処理（関数）
function battle(player, enemy) {
    print("戦闘開始だわ！\n");
    local turn = 1;
    while (player.hp > 0 && enemy.hp > 0) {
        print("\n【ターン" + turn + "】\n");

        // プレイヤーのターン
        if (turn % 2 == 1) {
            player.attack(enemy);
        }
        // 敵のターン
        else {
            enemy.attack(player);
        }
        turn += 1;
    }

    // 戦闘結果の表示
    if (player.hp > 0) {
        print("\n" + player.name + "の勝利よ！\n");
    } else {
        print("\n" + enemy.name + "の勝利ね…\n");
    }
}

// メイン処理
function main() {
    local hero = Character("ひたぎ", 100, 20);
    local enemy = Character("怪異", 80, 15);

    print("初期ステータス：\n");
    hero.status();
    enemy.status();

    // アイテムを使う
    print("\n戦闘前にアイテムを使うわ。\n");
    useItem(hero, 0);  // ポーション使用
    useItem(hero, 0);  // パワーアップ使用（インデックスがずれるため0番目を再指定）

    print("\n戦闘前ステータス：\n");
    hero.status();
    enemy.status();

    // 戦闘開始
    battle(hero, enemy);
}

// メイン処理を呼び出すわ
main();