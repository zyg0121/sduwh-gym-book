<h2 align="center">SDUWH-GYM-BOOK</h2>

山东大学（威海） · 体育馆预约脚本 
有任何问题可以发送邮件到zyg21@vip.qq.com,欢迎提交issues和pr！

## 使用前须知

**项目仅供学习交流使用，请不要将其用于商业用途，更不要有偿出位置！**

### CHANGE LOG
- [x] 2022/05/18 针对新增加的验证码部分进行识别处理
- [x] 2022/05/10 测试版本发布
---

## 使用方法

### 下载和安装

注意：建议使用**Python版本大于等于3.8**

```shell
# 获取源码
git clone https://github.com/zyg0121/sduwh-gym-book.git
# 打开仓库目录
cd sduwh-gym-book
# 新建log文件夹来保存日志文件,新建img文件夹来保存验证码图片相关文件
mkdir log
mkdir img
# 安装python依赖
pip install -r requirements.txt
# 若由于网络问题无法获取依赖，请执行
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 运行

```shell
python main.py --userid [学号] --passwd [密码] --area [区域] --retry [重试次数] --starttime [场馆开始时间] --endtime [场馆结束时间]
```

### 参数说明

| 参数名 |   类型    | 必需  |               说明                |
| :----: | :-------: | :---: |:-------------------------------:|
| userid |    str    | True  |             山东大学学工号             |
| passwd |    str    | True  |          山东大学统一身份认证密码           |
|  area  |    str    | True  |          区域编号,具体见表格下方           |
| retry  |    int    | False | 如果预约失败（网络原因等）重试的次数，默认重试30次，间隔1s |
| starttime  |    str    | False |         具体请到体育场馆预约系统查看          |
| endtime  |    str    | False |         具体请到体育场馆预约系统查看          |

| 区域编号 | 区域名称 |
|:----:|:----:|
| 1001 | 健身房  |
| 1002 | 乒乓球馆 |
| 1003 | 风雨操场羽毛球  |
| 1004 | 篮球馆  |
| 1005 | 排球馆  |

附：开始和结束时间
周一至周五：16:30-18:30 19:30-21:30
周六周日：8:00-10:00 10:00-12:00 14:00-16:00 16:30-18:30 19:30-21:30

### Example

```shell
python main.py --userid 201900639999 --passwd abc123 --area 1001 --retry 10 --starttime 19:30 --endtime 21:30
```
