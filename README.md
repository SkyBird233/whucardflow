本项目用于抓取 校园卡消费记录，可以顺便导出到钱迹。

由于在校内通过统一身份认证登录校园卡查询页面（202.114.64.162，只能校内访问）不需要任何验证，故采用这种方式登录并抓取数据。因为没有提供 api，最初使用 Selenium，之后尝试分析了下请求过程，改用 requests。

因为提前放假，无法在校内测试，而此项目又严重依赖校内网络环境，故暂时无法保证项目的可用性。假前只完成了最基本功能（见 [commit 881bb98](https://github.com/SkyBird233/whucardflow/tree/881bb98506ec1aa27678d1568812619dfc5b5ccc)），会在返校后继续完善（~~毕竟我自己要用（）~~）。

# 安装
> 假设您已安装 Python

1. 克隆本项目或下载源代码并解压
2. 创建虚拟环境
    ```bash
    python -m venv venv
    ```
3. 激活虚拟环境
    Linux：
    ```bash
    source venv/bin/activate
    ```
    Windows PowerShell:
    ```PowerShell
    .\venv\Scripts\activate.ps1
    ```
4. 安装依赖
    ```bash
    pip install -r requirements.txt
    ```


# 配置
配置生效顺序：命令行参数 > 环境变量 > 配置文件
## 配置文件
- whulogin
    与登录官网时的相同，建议使用环境变量传入
    - username: 你的学号
    - password: 你的密码
- date
    抓取内容的日期范围
    - start_date
    - end_date
- others
    - output_csv: 是否输出到 csv 文件，填入文件名路径。为空则不输出到 csv 文件
    - standard_output: 是否输出到标准输出
    - qianji: 是否输出到钱迹

## 环境变量
- WHUCF_USERNAME：学号
- WHUCF_PASSWORD：密码

## 参数
与配置文件对应，可以使用 `python main.py -h` 查看帮助


# 使用示例
> 注意：Windows PowerShell 下需使用 `$env:WHUCF_USERNAME=202200000000` 设置环境变量
- 导出当日记录至钱迹
    ```bash
    WHUCF_USERNAME=202200000000 WHUCF_PASSWORD=123456 python main.py --qianji
    ```
- 查看特定日期范围内的记录
    ```bash
    export WHUCF_USERNAME=202200000000, WHUCF_PASSWORD=123456
    python main.py -s 2020-01-01 -e 2020-01-31 -o
    python main.py -s 2020-02-01 -e 2020-02-31 -o
    ```
- 设定过帐号的情况下导出当日记录至 csv 文件
    ```bash
    WHUCF_PASSWORD=123456 python main.py -c output.csv
    ```