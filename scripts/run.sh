#!/bin/sh

echo '##############################################################'
echo "#                ______      _____                           #"
echo "#               / _  (_)_ __/ _  / ___  _ __                 #"
echo "#               \// /| | '_ \// / / _ \| '_ \                #"
echo "#                / //\ | |_) / //\ (_) | |_) |               #"
echo "#               /____/_| .__/____/\___/| .__/                #"
echo "#                      |_|             |_|                   #"
echo '##############################################################'
echo ""

VER=$(python -c "import sys;sys.path.append('/app/lbz_ma_tw/');import libs.cons as cons;print(cons.s_VER)")

echo "Starting zipzop/lbz_ma_tw:$VER"
echo "=============================================================="

# Copying cron template with proper value
sed -e "s|%H%|$MSG_HOUR|" /app/config/lbz_ma_tw.tpl > /app/config/lbz_ma_tw.cron

# Finally we launch the cron
export PYTHONUNBUFFERED=1
supercronic -quiet -passthrough-logs /app/config/lbz_ma_tw.cron