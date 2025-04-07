#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lark import Lark
import sys

def test_grammar():
    # 文法ファイルを読み込む
    with open('scene_graph_grammar.lark', 'r') as f:
        grammar = f.read()
    
    # サンプルDSLコードを読み込む
    with open('sample_dsl.txt', 'r') as f:
        sample_code = f.read()
    
    # Larkパーサーを作成
    parser = Lark(grammar, start='start', parser='lalr')
    
    try:
        # サンプルコードを解析
        tree = parser.parse(sample_code)
        print("パース成功！")
        print("構文木:")
        print(tree.pretty())
        return True
    except Exception as e:
        print(f"パースエラー: {e}")
        return False

if __name__ == "__main__":
    success = test_grammar()
    sys.exit(0 if success else 1)