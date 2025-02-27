#!/usr/bin/env python3
"""
リマインダーウィンドウを表示するスクリプト

このスクリプトは単体で実行され、フルスクリーンのリマインダーウィンドウを表示します。
"""

import pygame
import sys
import os

# Pygameの初期化
pygame.init()

# 画面情報の取得
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# 全画面ウィンドウの作成
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("全画面アプリケーション")

# フォントの設定
font_path = "NotoSansJP-VariableFont_wght.ttf"  # フォントファイルのパス
font_size = 36
font = pygame.font.Font(font_path, font_size)

# タイトルを取得（コマンドライン引数から）
title = "予定の時間です"  # デフォルトメッセージ
if len(sys.argv) > 1:
    title = sys.argv[1]

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 画面を黒でクリア
    screen.fill((0, 0, 0))

    # テキストを描画
    text = font.render(title + " (ESCキーで終了)", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
