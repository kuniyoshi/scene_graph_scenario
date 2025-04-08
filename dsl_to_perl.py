#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lark import Lark, Transformer, v_args
import sys

# Lark 文法を読み込む
with open('scene_graph_grammar.lark', 'r') as f:
    grammar = f.read()

# DSL を Perl に変換するトランスフォーマー
class DSLToPerlTransformer(Transformer):
    def start(self, items):
        # Perl のヘッダーを追加
        header = [
            "#!/usr/bin/env perl",
            "use strict;",
            "use warnings;",
            "use utf8;",
            "binmode(STDOUT, ':utf8');",
            "",
            "# Scene Graph Scenario DSL から変換された Perl コード",
            "",
            "# クラスとメソッドの定義",
            "package SceneGraph;",
            "",
            "sub new {",
            "    my $class = shift;",
            "    return bless {}, $class;",
            "}",
            "",
            "sub Text {",
            "    my ($text) = @_;",
            "    print \"テキスト: $text\\n\";",
            "    return $text;",
            "}",
            "",
            "sub Statement {",
            "    my ($statement) = @_;",
            "    return $statement;",
            "}",
            "",
            "sub Character {",
            "    my ($name) = @_;",
            "    my $character = {",
            "        name => $name,",
            "        position => [0, 0, 0],",
            "        motion => undef,",
            "    };",
            "    print \"キャラクター '$name' を作成しました\\n\";",
            "    return $character;",
            "}",
            "",
            "sub Model {",
            "    my ($name, %options) = @_;",
            "    my $model = {",
            "        name => $name,",
            "        %options,",
            "    };",
            "    print \"モデル '$name' を作成しました\\n\";",
            "    return $model;",
            "}",
            "",
            "sub Scene {",
            "    my ($name) = @_;",
            "    my $scene = {",
            "        name => $name,",
            "        elements => [],",
            "        add => sub {",
            "            my ($self, $type, $name) = @_;",
            "            my $element = {",
            "                type => $type,",
            "                name => $name,",
            "                add => sub {",
            "                    my ($self, $item) = @_;",
            "                    push @{$self->{items}}, $item;",
            "                    return $self;",
            "                },",
            "                items => [],",
            "            };",
            "            print \"シーン '$self->{name}' に $type '$name' を追加しました\\n\";",
            "            return $element;",
            "        },",
            "        play => sub {",
            "            my ($self) = @_;",
            "            print \"シーン '$self->{name}' を再生します\\n\";",
            "        },",
            "    };",
            "    return $scene;",
            "}",
            "",
            "sub Cut {",
            "    my ($name) = @_;",
            "    my $cut = {",
            "        name => $name,",
            "        items => [],",
            "        add => sub {",
            "            my ($self, $item) = @_;",
            "            push @{$self->{items}}, $item;",
            "            print \"カット '$self->{name}' に要素を追加しました\\n\";",
            "            return $self;",
            "        },",
            "    };",
            "    return $cut;",
            "}",
            "",
            "sub Transition {",
            "    my ($type) = @_;",
            "    print \"トランジション: $type\\n\";",
            "}",
            "",
            "package main;",
            "use SceneGraph;",
            "",
            "# メイン処理",
            ""
        ]
        
        # 各行を処理して Perl コードに変換
        perl_code = []
        for item in items:
            if item is not None:
                perl_code.append(item)
        
        return "\n".join(header + perl_code)
    
    def line(self, items):
        for item in items:
            if item is not None:
                return item
        return None
    
    def block_start(self, _):
        return "{"
    
    def block_end(self, _):
        return "}"
    
    def comment(self, items):
        # コメントを Perl のコメントに変換
        comment_text = items[0].value.strip()
        return f"# {comment_text[3:].strip()}"
    
    def transition(self, items):
        print(f"transition items: {items}, type: {type(items)}, length: {len(items)}")
        if len(items) > 0:
            transition_type = items[0]
            return f"Transition('{transition_type}');"
        return "Transition('unknown');"
    
    def transition_type(self, items):
        print(f"transition_type items: {items}, type: {type(items)}, length: {len(items)}")
        if len(items) > 0:
            item = items[0]
            print(f"  item[0]: {item}, type: {type(item)}")
            if hasattr(item, 'value'):
                return item.value
            return str(item)
        return "unknown"
    
    def declaration(self, items):
        print(f"declaration items: {items}, type: {type(items)}, length: {len(items)}")
        if len(items) >= 2:
            # items[0] が "let" または "local" を含むかチェック
            if "let" in items[0] or "local" in items[0]:
                keyword = "let" if "let" in items[0] else "local"
                identifier = items[0].replace(keyword, "").strip()
                value = items[1]
            else:
                identifier, value = items[0], items[1]
            # let と local を my に変換
                return f"my ${identifier} = {value};"
        return None
    
    def assignment(self, items):
        print(f"assignment items: {items}, type: {type(items)}, length: {len(items)}")
        if len(items) >= 3:
            # 最初の要素が関数呼び出しかどうかを確認
            if isinstance(items[0], str) and "(" in items[0] and ")" in items[0]:
                # 関数呼び出し結果のプロパティ設定
                function_call, property_name, value = items[0], items[1], items[2]
                return f"{function_call}->{{{property_name}}} = {value};"
            else:
                # 通常の変数のプロパティ設定
                identifier, property_name, value = items[0], items[1], items[2]
                return f"${identifier}->{{{property_name}}} = {value};"
        return None
    
    def function_call(self, items):
        function_name = items[0]
        if len(items) > 1 and items[1] is not None:
            arguments = items[1]
            return f"{function_name}({arguments})"
        return f"{function_name}()"
    
    def method_call(self, items):
        object_name, method_name = items[0], items[1]
        if len(items) > 2 and items[2] is not None:
            arguments = items[2]
            return f"${object_name}->{method_name}({arguments})"
        return f"${object_name}->{method_name}()"
    
    def arguments(self, items):
        # 引数リストを構築
        args = []
        named_args = {}
        
        for item in items:
            if isinstance(item, tuple) and len(item) == 2:
                # 名前付き引数
                name, value = item
                named_args[name] = value
            else:
                # 位置引数
                args.append(item)
        
        # 位置引数と名前付き引数を結合
        result = ", ".join(args)
        if named_args:
            named_args_str = ", ".join([f"{k} => {v}" for k, v in named_args.items()])
            if result:
                result += ", " + named_args_str
            else:
                result = named_args_str
        
        return result
    
    def value(self, items):
        return items[0]
    
    def array(self, items):
        if not items:
            return "[]"
        elements = ", ".join(items)
        return f"[{elements}]"
    
    def STRING(self, token):
        return token.value
    
    def NUMBER(self, token):
        return token.value
    
    def IDENTIFIER(self, token):
        return token.value

# メイン処理
def transpile_dsl_to_perl(dsl_file, perl_file):
    # DSL ファイルを読み込む
    with open(dsl_file, 'r') as f:
        dsl_code = f.read()
    
    # Lark パーサーを作成
    parser = Lark(grammar, start='start', parser='lalr')
    
    try:
        # DSL コードを解析
        tree = parser.parse(dsl_code)
        
        # Perl コードに変換
        transformer = DSLToPerlTransformer()
        perl_code = transformer.transform(tree)
        
        # Perl ファイルに書き込む
        with open(perl_file, 'w') as f:
            f.write(perl_code)
        
        print(f"DSL を Perl コードに変換しました: {perl_file}")
        return True
    except Exception as e:
        print(f"変換エラー: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使用方法: python dsl_to_perl.py <dsl_file> <perl_file>")
        sys.exit(1)
    
    dsl_file = sys.argv[1]
    perl_file = sys.argv[2]
    
    success = transpile_dsl_to_perl(dsl_file, perl_file)
    sys.exit(0 if success else 1)