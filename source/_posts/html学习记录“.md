---
title: html学习记录
date: 2023-03-03 16:36:36
tags:
---
<>已经省略
## 单标签总结

1. hr width=' ' color=' ' align=' ' size=' ' 分割线
2. br 换行

## 格式总结
1. &nbsp 空格
2. &copy+; 版权信息（+表示使不被执行）

## 双标签总结

1. 六级标题
	h# align='right|center|left' 标题文字
	#代表1-6
2. 字体设置
	font face='' size=' ' color=' '
	face新版浏览器不在支持。
	b 粗体
	i 斜体
	u 下划线
	strike 删除线
3. 上标及下标
	sup 上标
	sub 下标
4. 文字滚动
	marquee 文字从左向右移动

4. 文字标注
	ruby被说明的文字
		rt文字的标注/rt
	/ruby

5. 链接
	a 超链接
	EMBED 音乐链接

5. address用来标记html文档的特定信息：E-mail,地址,签名,作者,文档,信息等
	
## Table表格

1. table表示一个表格的开始
2. tr表示一行
3. td表示一列
1)共有属性
 属性|值|作用
 --|:--:|--:
 border|数字|边界大小|
 bordercolor|颜色|边界颜色|
 bgcolor|颜色|背景颜色|
 background|图片：.jpg,.gtf,.png|自选背景图片|
 cellpadding|边框间距|文本与边框间距|
 cellspacing|边框间距|边框与边框间距|
 colspan|数字|横向合并单元格，放在td标签中，从当前设置属性标签开始向后计数|
 rowspan|数字|纵向合并单元格，放在td标签中，从当前设置属性标签开始向下计数|
 align|left/right/center|对齐方式|






## 注释方式
<!--注释内容 -->
实例： <center><!--<font size=6 color='blue'>苏州旅游数据分析</font>--></center>注释内容将不会被执行
网站首页文件名一般是index.html或default.html.





\<html>