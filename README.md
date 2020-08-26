# 一、项目介绍

## 1、框架结构

以下为当前框架的目录结构：

```
┌─audio
├─config
├─operate
├─page_object
├─public
├─report
└─test_case
```

### audio

用来存放测试用到的音频文件。

### config目录

用来存放config.ini配置文件，配置文件中包含浏览器驱动路径、鉴定系统exe程序路径。  

同时，config.ini文件当前也用作存放测试数据，通过api.py中封装好的get_config方法可以读取配置文件。

### operate

操作层。用来封装对page_object页面元素的操作。

### page_object目录

该目录用来存放页面元素定位文件，文件命名遵循“module_page.py”的格式。例如：案件页面元素统一放在“case_page.py”文件中。

### public目录

该目录下包含api.py和backend_api.py两个文件，提供一些封装好的公共方法。其中backend_api.py仅提供后台接口请求的接口，这些接口当前被用作测试环境数据的还原。

### report目录

用来存放执行测试后生成的html测试报告文件，测试报告名称遵循：report_YYYYmmddHHMMSS.html。

### test_case目录

用来存放测试用例。每一个模块最好都单独新建一个以“test”开头的测试文件，例如：test_case.py。

### test_case.xlsx文件

里面用来存放测试用例及每条用例的驱动数据。

## 2、说明

- 通过run_by_pytest.py文件可以运行所有test_xxx.py文件中的测试用例，而test_xxx.py仅用作单个模块测试用例的执行。
- 运行测试前，请将`‪\\192.168.0.8\test\06_测试工具\谷歌驱动\chromedriver.exe`放到谷歌浏览器安装目录下，一般谷歌安装目录是`C:\Program Files (x86)\Google\Chrome\Application`。
- 运行时请在电脑D盘新建一个`UI_AUTO_TEST`目录，目录可以直接从`\\192.168.0.8\test\06_测试工具\UI_AUTO_TEST\`拷贝

# 二、常见问题

## 1. 谷歌浏览器启动失败

把Pycharm设置为以管理员方式运行。



