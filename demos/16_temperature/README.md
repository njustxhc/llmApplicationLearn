# 15 Temperature 与采样参数

同一问题用不同 **temperature** 调用模型，对比输出：低 temperature 更稳定、重复性高；高 temperature 更多样、随机性强。部分 API 支持该参数。

## 运行

```bash
python -m demos.16_temperature.run
```

若当前 API 不支持 temperature 参数，可能报错，可查阅所用接口文档。
