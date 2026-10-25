# num2cn

把金额数字转成中文大写。单文件、零依赖、只用 Python 标准库。

## 用法

```bash
python num2cn.py 1234.56
# 壹仟贰佰叁拾肆元伍角陆分

python num2cn.py 0.07 100000001 3.5
# 柒分
# 壹亿零壹元整
# 叁元伍角整

python num2cn.py --test
# 跑内置的 11 条用例
```

也可以当模块用：

```python
from num2cn import amount_to_cn
amount_to_cn("1001.05")   # '壹仟零壹元零伍分'
```

## 规则

- 支持整数与两位小数，四舍五入到分。
- 无角无分补「整」（`壹元整`、`伍角整`）；
- 有分无角补「零」（`壹元零伍分`）；
- `0` → `零元整`；
- 暂不支持负数（会报错退出，退出码 2）。

## 许可

MIT，见 [LICENSE](LICENSE)。
