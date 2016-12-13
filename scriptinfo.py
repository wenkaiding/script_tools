#!/usr/bin/python
# coding: utf-8

execmds_intranet = {
    "ABtest": "php /usr/local/webdata/php/{}/fun/batch/Betatest/cacheAppBetatest.php",
    "Slefsupporting": "",
    "Super": "php /usr/local/webdata/php/{}/super/Cron/Supercron.php method=readData",
    "Shop": "php /usr/local/webdata/php/{}/fun/batch/goshop/cacheTemplates.php",
    "Super_Special": "php /usr/local/webdata/php/{}/super/Cron/Cron.php method=cacheZcData",
    "Super_12": "php /usr/local/webdata/php/{}/super/Cron/Supercron.php method=cacheD12Data ",
    "Super_Tag": "php /usr/local/webdata/php/{}/super/Cron/Supercron.php method=cacheIcons ",
    "Super_New": "php /usr/local/webdata/php/{}/super/Cron/Supercron.php method=cacheNewbieItems",
    "Super_SECKILL": " php /usr/local/webdata/php/{}/super/Cron/Maincron.php method=cacheHotItemData",
    "Super_Class": "php /usr/local/webdata/php/{}/super/Cron/Supercron.php method=cacheFgcats",
    "Super_jump": "php /usr/local/webdata/php/{}/super/Cron/Supercron.php method=cacheAllowQcodeItemIds",
    "Super_21117": "php /usr/local/webdata/php/{}/super/Cron/Supercron.php method=cacheUsergroupRatios",
    "Super_YygData": "php /usr/local/webdata/php/{}/super/Cron/Yygcron.php method=cacheYygData",
    "Super_Brand": "php /usr/local/webdata/php/{}/super/Cron/Maincron.php method=cacheRelateBrands",
    "k9k9": "",
    "taoke": "php /usr/local/webdata/php/{}/union/Cron/Cron.php method=cacheTaobaoSecondTaokeItems",
    "gaea": "php /usr/local/webdata/php/{}/gaea/Cron/Cron.php method=readData"
}
execmds_outside = {
    "ABtest": "php /usr/local/webdata/fun/fun/batch/Betatest/cacheAppBetatest.php",
    "Slefsupporting": "",
    "Super": "php /usr/local/webdata/super/super/Cron/Supercron.php method=readData",
    "Shop": "php /usr/local/webdata/fun/fun/batch/goshop/cacheTemplates.php",
    "Super_Special": "php /usr/local/webdata/super/super/Cron/Cron.php method=cacheZcData",
    "Super_12": "php /usr/local/webdata/super/super/Cron/Supercron.php method=cacheD12Data ",
    "Super_Tag": "php /usr/local/webdata/super/super/Cron/Supercron.php method=cacheIcons ",
    "Super_New": "php /usr/local/webdata/super/super/Cron/Supercron.php method=cacheNewbieItems",
    "Super_SECKILL": " php /usr/local/webdata/super/super/Cron/Maincron.php method=cacheHotItemData",
    "Super_Class": "php /usr/local/webdata/super/super/Cron/Supercron.php method=cacheFgcats",
    "Super_jump": "php /usr/local/webdata/super/super/Cron/Supercron.php method=cacheAllowQcodeItemIds ",
    "Super_21117": "php /usr/local/webdata/super/super/Cron/Supercron.php method=cacheUsergroupRatios",
    "Super_YygData": "php /usr/local/webdata/super/super/Cron/Yygcron.php method=cacheYygData",
    "Super_Brand": "php /usr/local/webdata/super/super/Cron/Maincron.php method=cacheRelateBrands",
    "taoke": "php /usr/local/webdata/union/union/Cron/Cron.php method=cacheTaobaoSecondTaokeItems",
    "gaea": "php /usr/local/webdata/gaea/gaea/Cron/Cron.php method=readData"
}

script_data = {
    "ABtest": ["分流脚本", "cacheAppBetatest.php"],
    "Super": ["超级返所有数据脚本readData", "Supercron.php method=readData"],
    "Shop": ["商城脚本", "cacheTemplates.php"],
    "Super_Special": ["超级返专场数据脚本", "Cron.php method=cacheZcData"],
    "Super_12": ["超级返双12数据脚本", "Supercron.php method=cacheD12Data"],
    "Super_Tag": ["超级返标签数据脚本", "Supercron.php method=cacheIcons"],
    "Super_New": ["超级返新人专享数据脚本", "Supercron.php method=cacheNewbieItems"],
    "Super_SECKILL": ["超级返限时秒杀数据脚本", "Maincron.php method=cacheHotItemData"],
    "Super_Class": ["超级返缓存前台类目数据脚本", "Supercron.php method=cacheFgcats"],
    "Super_jump": ["超级返插队码脚本", "Supercron.php method=cacheAllowQcodeItemIds"],
    "Super_21117": ["缓存21117返利分组", "Supercron.php method=cacheUsergroupRatios"],
    "Super_YygData": ["一元购", "Yygcron.php method=cacheYygData"],
    "Super_Brand": ["品牌关联列表脚本", "Maincron.php method=cacheRelateBrands"],
    "taoke": ["第二淘客脚本", "Cron.php method=cacheTaobaoSecondTaokeItems"],
    "gaea": ["后台配置gaea数据后跑脚本", "Cron.php method=readData"],
}
