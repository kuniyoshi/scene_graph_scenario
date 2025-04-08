#!/usr/bin/env perl
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
    print "テキスト: $text\n";
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
    print "キャラクター '$name' を作成しました\n";
    return $character;
}

sub Model {
    my ($name, %options) = @_;
    my $model = {
        name => $name,
        %options,
    };
    print "モデル '$name' を作成しました\n";
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
            print "シーン '$self->{name}' に $type '$name' を追加しました\n";
            return $element;
        },
        play => sub {
            my ($self) = @_;
            print "シーン '$self->{name}' を再生します\n";
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
            print "カット '$self->{name}' に要素を追加しました\n";
            return $self;
        },
    };
    return $cut;
}

sub Transition {
    my ($type) = @_;
    print "トランジション: $type\n";
}

package main;
use SceneGraph;

# メイン処理
# Root blocks makes a cut cluster
{
# three hypens means a comment line
    Text(
        Statement("2023年10月某日……\n\n新たに《子やぎドレス》が発見された。")
    );
}

Transition('fadeout-fadein');

{
# access the character by `shiori` symbol
my $shiori = Character("shiori");

# access the character by character("haduki")
Character("haduki");

Model("Table", 'position' => [0, 0, 0]);

$shiori->{position} = [1, 0, 0];
Character("haduki")->{position} = [0, 1, 0];
}

my $scene = Scene("event");
my $tsubame = $scene->add("Character", "Tsubame");
my $cut = Cut("1");
$cut->add($tsubame);
$scene->add($cut);
$scene->play();