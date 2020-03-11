# 强智教务系统课表转换ICS
目前已知绝大部分强智教务系统留有API可供抓取课程数据，所以编写此小站以方便优雅的将课表导入手机日历中

## 本项目使用Flask开发，并以包括未完成的脚本部分：
- 教务网站爬虫
- 强智教务系统提供的Excel文件的读入转换json

## 计划完成
- 支持更多学校

## 食用方法

- 如果迁移本项目，请将QZ_API.py文件中URL改为自己学校教务处网站并以app.do结尾
- 感谢对本项目有帮助的开源项目
    * TLingC的文档[强智教务系统API文档](https://qzapi.github.tlingc.com)
    * wylapp的项目[强智API python封装](https://github.com/wylapp/QZapi_py)