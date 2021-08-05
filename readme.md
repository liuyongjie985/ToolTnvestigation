墨迹识别器（微软）

输入方式：轨迹 

响应时间 15.15s 

限制 10次/分钟

microsoftOnlineRequest.py 

里面deal_fanti_file和deal_single_file方法分别为加载繁体字.json文件和精品课英文测试数据.json文件


===================================

myscript（微软） 

输入方式：轨迹 

响应时间 9.2 

限制 无

myscriptOnline.py 里面loadYunbiPointerEvents和loadPointerEvent分别为加载繁体字.json文件和精品课英文测试数据.json文件

===================================

Google document_text_detect 

输入方式：图片 

响应时间 2.31 

限制 无

googleOfflineRequest.py 中Text为False代表整页识别 

Google text_detect 

输入方式：图片 

响应时间 2.98 

限制 无

googleOfflineRequest.py 中Text为True代表单行识别

####如果有指定语言的需求，需要用Google REST方式请求

==================================

Google document_text_detect REST 

输入方式：图片 

响应时间 3.34 

限制 无

googleOfflineREST.py 中Text 为False代表整页识别

Google text_detect REST 

输入方式：图片 

响应时间 未测 

限制 无

googleOfflineREST.py 中Text 为True代表单行识别

=================================

mathpix 不在此次调研范围
