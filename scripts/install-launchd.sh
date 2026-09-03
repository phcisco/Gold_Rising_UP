#!/usr/bin/env bash
# 安装/卸载/查看 每日 07:30（周二至周六）的 launchd 任务。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LABEL="com.goldrising.daily"
TARGET="$HOME/Library/LaunchAgents/$LABEL.plist"
case "${1:-status}" in
  install)
    mkdir -p "$HOME/Library/LaunchAgents" "$ROOT/logs"
    sed "s#__ROOT__#$ROOT#g" "$ROOT/scripts/$LABEL.plist.template" > "$TARGET"
    launchctl unload "$TARGET" 2>/dev/null || true
    launchctl load "$TARGET"
    echo "已安装：$TARGET（北京时间需与系统时区一致；当前系统时区 $(date +%Z)）"
    ;;
  uninstall)
    launchctl unload "$TARGET" 2>/dev/null || true
    rm -f "$TARGET"
    echo "已卸载 $LABEL"
    ;;
  status)
    launchctl list | grep "$LABEL" || echo "未加载 $LABEL"
    [ -f "$TARGET" ] && echo "plist: $TARGET"
    ;;
  run-now)
    launchctl start "$LABEL" && echo "已触发一次运行，日志见 $ROOT/logs/launchd.log"
    ;;
  *)
    echo "用法: $0 install|uninstall|status|run-now"; exit 1;;
esac
