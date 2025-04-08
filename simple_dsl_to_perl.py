#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

def transpile_dsl_to_perl(dsl_file, perl_file):
    # DSL ファイルを読み込む
    with open(dsl_file, 'r') as f:
        dsl_code = f.read()
    
    # Perl のヘッダーを作成
    perl_header = """#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
binmode(STDOUT, ':utf8');

# Scene Graph Scenario DSL から変換された Perl コード

# クラスとメソッドの定義
package SceneGraph;

sub new {
    my $class = shift;
    return bless {}, $class;
}

sub Text {
    my ($text) = @_;
    print "テキスト: $text\\n";
    return $text;
}

sub Statement {
    my ($statement) = @_;
    return $statement;
}

sub Character {
    my ($name) = @_;
    my $character = {
        name => $name,
        position => [0, 0, 0],
        motion => undef,
    };
    print "キャラクター '$name' を作成しました\\n";
    return $character;
}

sub Model {
    my ($name, %options) = @_;
    my $model = {
        name => $name,
        %options,
    };
    print "モデル '$name' を作成しました\\n";
    return $model;
}

sub Scene {
    my ($name) = @_;
    my $scene = {
        name => $name,
        elements => [],
        add => sub {
            my ($self, $type, $name) = @_;
            my $element = {
                type => $type,
                name => $name,
                add => sub {
                    my ($self, $item) = @_;
                    push @{$self->{items}}, $item;
                    return $self;
                },
                items => [],
            };
            print "シーン '$self->{name}' に $type '$name' を追加しました\\n";
            return $element;
        },
        play => sub {
            my ($self) = @_;
            print "シーン '$self->{name}' を再生します\\n";
        },
    };
    return $scene;
}

sub Cut {
    my ($name) = @_;
    my $cut = {
        name => $name,
        items => [],
        add => sub {
            my ($self, $item) = @_;
            push @{$self->{items}}, $item;
            print "カット '$self->{name}' に要素を追加しました\\n";
            return $self;
        },
    };
    return $cut;
}

sub Transition {
    my ($type) = @_;
    print "トランジション: $type\\n";
}

package main;
use SceneGraph;

# メイン処理
"""
    
    # DSL コードを行ごとに処理
    lines = dsl_code.split('\n')
    perl_lines = []
    
    for line in lines:
        # コメント行を変換
        if line.strip().startswith('---'):
            perl_line = '# ' + line.strip()[3:].strip()
        
        # Transition を変換
        elif re.match(r'\s*Transition\s*\(\s*(.+?)\s*\)\s*;', line):
            match = re.match(r'\s*Transition\s*\(\s*(.+?)\s*\)\s*;', line)
            transition_type = match.group(1)
            perl_line = f"Transition('{transition_type}');"
        
        # let 変数宣言を変換
        elif re.match(r'\s*let\s+(\w+)\s*=\s*(.+?)\s*;', line):
            match = re.match(r'\s*let\s+(\w+)\s*=\s*(.+?)\s*;', line)
            var_name = match.group(1)
            var_value = match.group(2)
            perl_line = f"my ${var_name} = {var_value};"
        
        # local 変数宣言を変換
        elif re.match(r'\s*local\s+(\w+)\s*=\s*(.+?)\s*;', line):
            match = re.match(r'\s*local\s+(\w+)\s*=\s*(.+?)\s*;', line)
            var_name = match.group(1)
            var_value = match.group(2)
            
            # メソッド呼び出しの形式 (obj.method()) を変換
            method_call_match = re.match(r'(\w+)\.(\w+)\s*\(\s*(.*?)\s*\)', var_value)
            if method_call_match:
                obj_name = method_call_match.group(1)
                method_name = method_call_match.group(2)
                args = method_call_match.group(3)
                
                # 引数内の変数名に $ を付ける
                processed_args = []
                for arg in args.split(','):
                    arg = arg.strip()
                    # 引用符で囲まれていない単語は変数とみなす
                    if arg and not (arg.startswith('"') or arg.startswith("'") or arg.startswith('[') or arg.isdigit()):
                        arg = f"${arg}"
                    processed_args.append(arg)
                
                processed_args_str = ', '.join(processed_args)
                var_value = f"${obj_name}->{method_name}({processed_args_str})"
            
            perl_line = f"my ${var_name} = {var_value};"
        
        # プロパティ設定を変換 (通常の変数)
        elif re.match(r'\s*(\w+)\.(\w+)\s*=\s*(.+?)\s*;', line):
            match = re.match(r'\s*(\w+)\.(\w+)\s*=\s*(.+?)\s*;', line)
            obj_name = match.group(1)
            prop_name = match.group(2)
            prop_value = match.group(3)
            perl_line = f"${obj_name}->{{{prop_name}}} = {prop_value};"
        
        # プロパティ設定を変換 (関数呼び出し結果)
        elif re.match(r'\s*(\w+\([^)]*\))\.(\w+)\s*=\s*(.+?)\s*;', line):
            match = re.match(r'\s*(\w+\([^)]*\))\.(\w+)\s*=\s*(.+?)\s*;', line)
            func_call = match.group(1)
            prop_name = match.group(2)
            prop_value = match.group(3)
            
            # 関数名が小文字で始まる場合は、Perl の関数として扱う
            if func_call[0].islower():
                # character("haduki") のような関数呼び出しを Character("haduki") に変換
                if func_call.startswith("character("):
                    func_call = "Character" + func_call[9:]
                perl_line = f"{func_call}->{{{prop_name}}} = {prop_value};"
            else:
                # 大文字で始まる場合は、クラスメソッドとして扱う
                perl_line = f"{func_call}->{{{prop_name}}} = {prop_value};"
        
        # 名前付き引数を持つ関数呼び出しを変換
        elif re.match(r'\s*(\w+)\s*\(\s*([^,]+)\s*,\s*(\w+)\s*:\s*(.+?)\s*\)\s*;', line):
            match = re.match(r'\s*(\w+)\s*\(\s*([^,]+)\s*,\s*(\w+)\s*:\s*(.+?)\s*\)\s*;', line)
            func_name = match.group(1)
            arg1 = match.group(2)
            named_arg_name = match.group(3)
            named_arg_value = match.group(4)
            perl_line = f"{func_name}({arg1}, '{named_arg_name}' => {named_arg_value});"
        
        # 通常の関数呼び出しを変換
        elif re.match(r'\s*(\w+)\s*\(\s*(.*?)\s*\)\s*;', line):
            match = re.match(r'\s*(\w+)\s*\(\s*(.*?)\s*\)\s*;', line)
            func_name = match.group(1)
            args = match.group(2)
            perl_line = f"{func_name}({args});"
        
        # メソッド呼び出しを変換
        elif re.match(r'\s*(\w+)\.(\w+)\s*\(\s*(.*?)\s*\)\s*;', line):
            match = re.match(r'\s*(\w+)\.(\w+)\s*\(\s*(.*?)\s*\)\s*;', line)
            obj_name = match.group(1)
            method_name = match.group(2)
            args = match.group(3)
            
            # 引数内の変数名に $ を付ける
            processed_args = []
            for arg in args.split(','):
                arg = arg.strip()
                # 引用符で囲まれていない単語は変数とみなす
                if arg and not (arg.startswith('"') or arg.startswith("'") or arg.startswith('[') or arg.isdigit()):
                    arg = f"${arg}"
                processed_args.append(arg)
            
            processed_args_str = ', '.join(processed_args)
            perl_line = f"${obj_name}->{method_name}({processed_args_str});"
        
        # その他の行はそのまま
        else:
            perl_line = line
        
        perl_lines.append(perl_line)
    
    # Perl コードを生成
    perl_code = perl_header + '\n'.join(perl_lines)
    
    # Perl ファイルに書き込む
    with open(perl_file, 'w') as f:
        f.write(perl_code)
    
    print(f"DSL を Perl コードに変換しました: {perl_file}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使用方法: python simple_dsl_to_perl.py <dsl_file> <perl_file>")
        sys.exit(1)
    
    dsl_file = sys.argv[1]
    perl_file = sys.argv[2]
    
    success = transpile_dsl_to_perl(dsl_file, perl_file)
    sys.exit(0 if success else 1)