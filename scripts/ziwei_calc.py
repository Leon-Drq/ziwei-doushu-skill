#!/usr/bin/env python3
"""紫微斗数基础排盘器；输出命宫、主星、辅煞星、四化和大限骨架。"""

import argparse
import json
from datetime import date
from typing import Dict, List, Tuple

TIANGAN = list("甲乙丙丁戊己庚辛壬癸")
DIZHI = list("子丑寅卯辰巳午未申酉戌亥")
GONG_NAMES = ["命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫", "迁移宫", "交友宫", "事业宫", "田宅宫", "福德宫", "父母宫"]
HOUR_INDEX = {23: 0, 0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5, 10: 5, 11: 6, 12: 6, 13: 7, 14: 7, 15: 8, 16: 8, 17: 9, 18: 9, 19: 10, 20: 10, 21: 11, 22: 11}
LUNAR_INFO = [0x04bd8,0x04ae0,0x0a570,0x054d5,0x0d260,0x0d950,0x16554,0x056a0,0x09ad0,0x055d2,0x04ae0,0x0a5b6,0x0a4d0,0x0d250,0x1d255,0x0b540,0x0d6a0,0x0ada2,0x095b0,0x14977,0x04970,0x0a4b0,0x0b4b5,0x06a50,0x06d40,0x1ab54,0x02b60,0x09570,0x052f2,0x04970,0x06566,0x0d4a0,0x0ea50,0x06e95,0x05ad0,0x02b60,0x186e3,0x092e0,0x1c8d7,0x0c950,0x0d4a0,0x1d8a6,0x0b550,0x056a0,0x1a5b4,0x025d0,0x092d0,0x0d2b2,0x0a950,0x0b557,0x06ca0,0x0b550,0x15355,0x04da0,0x0a5d0,0x14573,0x052d0,0x0a9a8,0x0e950,0x06aa0,0x0aea6,0x0ab50,0x04b60,0x0aae4,0x0a570,0x05260,0x0f263,0x0d950,0x05b57,0x056a0,0x096d0,0x04dd5,0x04ad0,0x0a4d0,0x0d4d4,0x0d250,0x0d558,0x0b540,0x0b5a0,0x195a6,0x095b0,0x049b0,0x0a974,0x0a4b0,0x0b27a,0x06a50,0x06d40,0x0af46,0x0ab60,0x09570,0x052f2,0x04af5,0x04970,0x064b0,0x074a3,0x0ea50,0x06b58,0x05ac0,0x0ab60,0x096d5,0x092e0,0x0c960,0x0d954,0x0d4a0,0x0da50,0x07552,0x056a0,0x0abb7,0x025d0,0x092d0,0x0cab5,0x0a950,0x0b4a0,0x0baa4,0x0ad50,0x055d9,0x04ba0,0x0a5b0,0x15176,0x052b0,0x0a930,0x07954,0x06aa0,0x0ad50,0x05b52,0x04b60,0x0a6e6,0x0a4e0,0x0d260,0x0ea65,0x0d530,0x05aa0,0x076a3,0x096d0,0x04afb,0x04ad0,0x0a4d0,0x1d0b6,0x0d250,0x0d520,0x0dd45,0x0b5a0,0x056d0,0x055b2,0x049b0,0x0a577,0x0a4b0,0x0aa50,0x1b255,0x06d20,0x0ada0,0x14b63,0x09370,0x049f8,0x04970,0x064b0,0x168a6,0x0ea50,0x06aa0,0x1a6c4,0x0aae0,0x092e0,0x0d2e3,0x0c960,0x0d557,0x0d4a0,0x0da50,0x05d55,0x056a0,0x0a6d0,0x055d4,0x052d0,0x0a9b8,0x0a950,0x0b4a0,0x0b6a6,0x0ad50,0x055a0,0x0aba4,0x0a5b0,0x052b0,0x0b273,0x06930,0x07337,0x06aa0,0x0ad50,0x14b55,0x04b60,0x0a570,0x054e4,0x0d160,0x0e968,0x0d520,0x0daa0,0x16aa6,0x056d0,0x04ae0,0x0a9d4,0x0a2d0,0x0d150,0x0f252]
WUXING_JU = {0:[6,2,4,4,3,3,2,2,4,2,6,3],1:[6,3,4,5,5,5,3,4,5,2,2,5],2:[2,3,3,3,2,6,3,6,4,3,3,6],3:[3,4,4,2,4,5,5,5,4,2,5,2],4:[4,5,3,6,2,2,6,6,3,4,2,6],5:[6,2,4,4,3,3,2,2,4,2,6,3],6:[6,3,4,5,5,5,3,4,5,2,2,5],7:[2,3,3,3,2,6,3,6,4,3,3,6],8:[3,4,4,2,4,5,5,5,4,2,5,2],9:[4,5,3,6,2,2,6,6,3,4,2,6]}
ZIWEI_POS = {2:[1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,0,0,1,1,2,2,3,3,4],3:[4,1,2,5,2,3,6,3,4,7,4,5,8,5,6,9,6,7,10,7,8,11,8,9,0,9,10,1,10,11],4:[11,4,1,2,0,5,2,3,1,6,3,4,2,7,4,5,3,8,5,6,4,9,6,7,5,10,7,8,6,11],5:[6,11,4,1,2,7,0,5,2,3,8,1,6,3,4,9,2,7,4,5,10,3,8,5,6,11,4,9,6,7],6:[9,6,11,4,1,2,10,7,0,5,2,3,11,8,1,6,3,4,0,9,2,7,4,5,1,10,3,8,5,6]}
SIHUA = {"甲": {"禄":"廉贞","权":"破军","科":"武曲","忌":"太阳"},"乙":{"禄":"天机","权":"天梁","科":"紫微","忌":"太阴"},"丙":{"禄":"天同","权":"天机","科":"文昌","忌":"廉贞"},"丁":{"禄":"太阴","权":"天同","科":"天机","忌":"巨门"},"戊":{"禄":"贪狼","权":"太阴","科":"右弼","忌":"天机"},"己":{"禄":"武曲","权":"贪狼","科":"天梁","忌":"文曲"},"庚":{"禄":"太阳","权":"武曲","科":"太阴","忌":"天同"},"辛":{"禄":"巨门","权":"太阳","科":"文曲","忌":"文昌"},"壬":{"禄":"天梁","权":"紫微","科":"左辅","忌":"武曲"},"癸":{"禄":"破军","权":"巨门","科":"太阴","忌":"贪狼"}}

def year_days(info: int) -> int:
    leap = info & 15; total = 348 + sum(1 for i in range(12) if info & (0x8000 >> i))
    if leap: total += 29 + (1 if info & 0x10000 else 0)
    return total

def month_days(info: int, month: int, leap: bool = False) -> int:
    if leap: return 29 + (1 if info & 0x10000 else 0)
    return 30 if info & (0x10000 >> month) else 29

def gregorian_to_lunar(year: int, month: int, day: int) -> Tuple[int, int, int, bool]:
    if year < 1900 or year > 2099: raise ValueError("仅支持 1900–2099")
    offset = (date(year, month, day) - date(1900, 1, 31)).days; lunar_year = 1900
    for info in LUNAR_INFO:
        span = year_days(info)
        if offset < span: break
        offset -= span; lunar_year += 1
    else: raise ValueError("日期超出内置农历范围")
    leap = LUNAR_INFO[lunar_year - 1900] & 15
    for lunar_month in range(1, 13):
        span = month_days(info, lunar_month)
        if offset < span: return lunar_year, lunar_month, offset + 1, False
        offset -= span
        if lunar_month == leap:
            span = month_days(info, lunar_month, True)
            if offset < span: return lunar_year, lunar_month, offset + 1, True
            offset -= span
    raise ValueError("农历转换失败")

def year_ganzhi(lunar_year: int) -> Tuple[int, int]:
    offset = lunar_year - 1984
    return offset % 10, offset % 12

def ming_gong(lunar_month: int, hour_index: int) -> int: return (13 + lunar_month - hour_index) % 12
def shen_gong(lunar_month: int, hour_index: int) -> int: return (1 + lunar_month + hour_index) % 12
def ziwei_position(lunar_day: int, ju: int) -> int: return ZIWEI_POS[ju][max(0, min(29, lunar_day - 1))]

def add_star(stars: Dict[int, List[str]], pos: int, name: str, group: str) -> None:
    stars.setdefault(pos % 12, []).append(name + (f"/{group}" if group else ""))

def arrange_stars(ziwei: int, year_gan: int, year_zhi: int, hour: int) -> Dict[int, Dict[str, List[str]]]:
    result = {i: {"主星": [], "辅星": [], "煞星": []} for i in range(12)}
    for name, offset in {"紫微":0,"天机":11,"太阳":9,"武曲":8,"天同":7,"廉贞":4}.items(): result[(ziwei + offset) % 12]["主星"].append(name)
    tianfu = {0:4,1:3,2:2,3:1,4:0,5:11,6:10,7:9,8:8,9:7,10:6,11:5}[ziwei]
    for name, offset in {"天府":0,"太阴":1,"贪狼":2,"巨门":3,"天相":4,"天梁":5,"七杀":6,"破军":10}.items(): result[(tianfu + offset) % 12]["主星"].append(name)
    h = HOUR_INDEX[hour]
    for pos, name in [((h + 4) % 12, "左辅"), ((10 - h) % 12, "右弼"), ((10 - h) % 12, "文昌"), ((4 + h) % 12, "文曲"), ((year_gan + 6) % 12, "天魁"), ((year_gan + 2) % 12, "天钺")]: result[pos]["辅星"].append(name)
    for pos, name in [((year_zhi + 1) % 12, "擎羊"), ((year_zhi - 1) % 12, "陀罗"), ((year_zhi + h) % 12, "火星"), ((year_zhi - h) % 12, "铃星"), ((11 - h) % 12, "地空"), ((h + 11) % 12, "地劫")]: result[pos]["煞星"].append(name)
    return result

def daxian(ming: int, ju: int, gender: str, year_gan: int) -> List[Dict]:
    forward = (year_gan % 2 == 0 and gender == "男") or (year_gan % 2 == 1 and gender == "女")
    direction = 1 if forward else -1; result = []
    for i in range(8): result.append({"序": i + 1, "年龄范围": f"{ju + i * 10}-{ju + i * 10 + 9}岁", "宫位地支": DIZHI[(ming + i * direction) % 12]})
    return result

def paipan_from_lunar(lunar_year: int, lunar_month: int, lunar_day: int, hour: int, gender: str = "男", leap: bool = False) -> Dict:
    yg, yz = year_ganzhi(lunar_year); hi = HOUR_INDEX[hour]; ming = ming_gong(lunar_month, hi); shen = shen_gong(lunar_month, hi); ju = WUXING_JU[yg][ming]; ju_name = {2:"水二局",3:"木三局",4:"金四局",5:"土五局",6:"火六局"}[ju]; ziwei = ziwei_position(lunar_day, ju); stars = arrange_stars(ziwei, yg, yz, hour)
    houses = []
    for index, name in enumerate(GONG_NAMES):
        pos = (ming - index) % 12
        houses.append({"宫位": name, "地支": DIZHI[pos], "主星": stars[pos]["主星"], "辅星": stars[pos]["辅星"], "煞星": stars[pos]["煞星"], "是否命宫": pos == ming, "是否身宫": pos == shen})
    return {"基本信息": {"农历": f"{lunar_year}年{'闰' if leap else ''}{lunar_month}月{lunar_day}日", "性别": gender, "年干支": TIANGAN[yg] + DIZHI[yz], "时支": DIZHI[hi]}, "命盘结构": {"命宫": DIZHI[ming], "身宫": DIZHI[shen], "五行局": ju_name, "紫微位置": DIZHI[ziwei]}, "年干四化": SIHUA[TIANGAN[yg]], "十二宫": houses, "大限": daxian(ming, ju, gender, yg), "计算说明": "主星为基础安星；辅煞星、大限和边界时刻需按流派核验"}

def paipan(year: int, month: int, day: int, hour: int, gender: str = "男") -> Dict:
    ly, lm, ld, leap = gregorian_to_lunar(year, month, day)
    result = paipan_from_lunar(ly, lm, ld, hour, gender, leap)
    result["基本信息"]["公历"] = f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:00"
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description="紫微斗数基础排盘")
    parser.add_argument("year", type=int); parser.add_argument("month", type=int); parser.add_argument("day", type=int); parser.add_argument("hour", type=int); parser.add_argument("gender", nargs="?", default="男")
    args = parser.parse_args(); print(json.dumps(paipan(args.year, args.month, args.day, args.hour, args.gender), ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
