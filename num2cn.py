#!/usr/bin/env python3
"""num2cn —— 把金额数字转成中文大写。

用法:
    python num2cn.py 1234.56
    python num2cn.py 0.07 100 100000001     (可一次传多个)
    python num2cn.py --test                 (跑内置用例)

零依赖，只用标准库。
"""

import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# Windows 控制台默认 GBK，输出中文大写时容易乱码；能改就改成 UTF-8
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

DIGITS = "零壹贰叁肆伍陆柒捌玖"
UNITS = ("", "拾", "佰", "仟")
SECTIONS = ("", "万", "亿", "万亿")


def _four(chunk):
    """把 4 位数字串（如 '0102'）转成 '零壹佰零贰'。"""
    out = ""
    zero = False
    for i, ch in enumerate(chunk):
        digit = int(ch)
        if digit == 0:
            if out:
                zero = True
            continue
        if zero:
            out += DIGITS[0]
            zero = False
        out += DIGITS[digit] + UNITS[3 - i]
    return out


def integer_to_cn(n):
    """非负整数 -> 中文大写（不含单位'元'）。"""
    if n == 0:
        return DIGITS[0]
    groups = []
    s = str(n)
    while s:
        groups.append(s[-4:])
        s = s[:-4]

    out = ""
    pending_zero = False
    for idx in range(len(groups) - 1, -1, -1):
        value = int(groups[idx])
        if value == 0:
            if out:
                pending_zero = True
            continue
        if out and (pending_zero or value < 1000):
            out += DIGITS[0]
        out += _four(groups[idx].zfill(4)) + SECTIONS[idx]
        pending_zero = False
    return out


def amount_to_cn(text):
    """金额字符串 -> 中文大写金额。"""
    try:
        amount = Decimal(str(text)).quantize(Decimal("0.01"), ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise ValueError("不是合法数字: %r" % (text,))
    if amount < 0:
        raise ValueError("暂不支持负数: %s" % text)

    yuan = int(amount)
    jiao, fen = divmod(int((amount - yuan) * 100), 10)

    parts = []
    if yuan:
        parts.append(integer_to_cn(yuan) + "元")
    if jiao:
        parts.append(DIGITS[jiao] + "角")
    if fen:
        if yuan and not jiao:
            parts.append(DIGITS[0] + DIGITS[fen] + "分")
        else:
            parts.append(DIGITS[fen] + "分")
    if not parts:
        return "零元整"
    # 没有「分」就要跟「整」，例如 壹元整 / 伍角整
    if not fen:
        parts.append("整")
    return "".join(parts)


CASES = [
    ("0", "零元整"),
    ("0.07", "柒分"),
    ("0.5", "伍角整"),
    ("1", "壹元整"),
    ("10", "壹拾元整"),
    ("1001.05", "壹仟零壹元零伍分"),
    ("10001", "壹万零壹元整"),
    ("100000", "壹拾万元整"),
    ("100000001", "壹亿零壹元整"),
    ("1234.56", "壹仟贰佰叁拾肆元伍角陆分"),
    ("999999999.99", "玖亿玖仟玖佰玖拾玖万玖仟玖佰玖拾玖元玖角玖分"),
]


def _run_tests():
    failed = 0
    for raw, expect in CASES:
        got = amount_to_cn(raw)
        flag = "ok " if got == expect else "FAIL"
        if got != expect:
            failed += 1
        print("%s %-12s -> %-28s %s" % (flag, raw, got, "" if got == expect else "期望: " + expect))
    print("\n%d 通过 / %d 总计" % (len(CASES) - failed, len(CASES)))
    return 1 if failed else 0


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 0
    if argv[0] in ("--test", "-t"):
        return _run_tests()
    code = 0
    for raw in argv:
        try:
            print(amount_to_cn(raw))
        except ValueError as exc:
            print("错误: %s" % exc, file=sys.stderr)
            code = 2
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
