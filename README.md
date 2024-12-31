# kong-buffer-check
## これは何？
Kong GatewayのRouteで設定できるRequest/ResponseのBufferingを確認するためのツールです。


## Bufferingの確認方法
### Request Buffering:
1. サーバを起動する
```sh
python3 ./server.py
```

2. ServiceとRouteを作成する
例）
- Service:
  - host: http://192.168.64.9
- Route:
  - paths: /server

3. テストデータを生成する
```sh
python3 -c 'import json; print(json.dumps({"key": "value" * 100000}))' > large_file.json
```

4. アクセスする
```sh
curl -sX POST http://localhost:8000/server/request-buffer -H "Content-Type: application/json" -H "Transfer-Encoding: chunked" --data-binary @large_file.json --no-buffer
```

Request Bufferingがfalseの場合：
```sh
2024-12-27 17:26:40,769 - Handling request buffering
2024-12-27 17:26:40,772 - Request is using chunked transfer encoding.
2024-12-27 17:26:40,778 - Received chunk of size: 9052 bytes
2024-12-27 17:26:40,785 - Received chunk of size: 8192 bytes
...
2024-12-27 17:26:41,103 - Received chunk of size: 8192 bytes
2024-12-27 17:26:41,110 - Received chunk of size: 7695 bytes
2024-12-27 17:26:41,112 - Total request data received: 500012 bytes
```
バッファリングされないのでチャンクで受け取る

Request Bufferingがtrueの場合：
```sh
2024-12-27 17:29:35,161 - Handling request buffering
2024-12-27 17:29:35,176 - Total request data received: 500012 bytes
```
バッファリングされてまとめて受け取る
Kongのログにも以下が表示される。（Request Bufferingがfalseだと出ない）
```sh
2024/12/27 08:32:28 [warn] 2550#0: *26854 a client request body is buffered to a temporary file /usr/local/kong/client_body_temp/0000000022, client: 172.18.0.1, server: kong, request: "POST /server/request-buffer HTTP/1.1", host: "localhost:8000", request_id: "2bbaa3780d067a234331253a24615f45"
```

### Response Buffering
1. サーバを起動する
```sh
python3 ./server.py
```

2. ServiceとRouteを作成する
例）
- Service:
  - host: http://192.168.64.9
- Route:
  - paths: /server

3. Response Bufferingの有無でそれぞれtest_response.shを実行する。
```
bash ./test_response.sh
```
スクリプトでは10回試行してTTFBの平均値を取得する。
Response Buffering有りの出力例：
```
Averages:
Connect: 0.000262 TTFB: 0.039415 Total time: 1.543241
```
Response Buffering無しの出力例：
```
Averages:
Connect: 0.000254 TTFB: 0.018649 Total time: 1.689541
```
Response Bufferingがある場合はすぐにClientにレスポンスが返らないのでTTFBが遅くなる。

